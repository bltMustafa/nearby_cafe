from flask import Flask, request, render_template, jsonify
import overpy
from geopy.distance import geodesic
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OVERPASS_API_TIMEOUT = int(os.getenv('OVERPASS_API_TIMEOUT', 60))
SEARCH_RADIUS = int(os.getenv('SEARCH_RADIUS', 5000))
MAX_CAFES = int(os.getenv('MAX_CAFES', 10))

OVERPASS_URL = "http://overpass-api.de/api/interpreter"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_cafes', methods=['POST'])
def get_cafes():
    try:
        data = request.get_json()
        user_lat = data.get("latitude")
        user_lon = data.get("longitude")

        if user_lat is None or user_lon is None:
            logger.error("Latitude or Longitude not provided.")
            return jsonify({'error': 'Invalid input data'}), 400

        try:
            user_lat = float(user_lat)
            user_lon = float(user_lon)
        except ValueError:
            logger.error("Latitude or Longitude not provided.")
            return jsonify({'error': 'Invalid input data'}), 400

        logger.info(f"User Location: Latitude={user_lat}, Longitude={user_lon}")

        api = overpy.Overpass()
        query = f"""
               (
                 node["amenity"="cafe"](around:{SEARCH_RADIUS},{user_lat},{user_lon});
                 way["amenity"="cafe"](around:{SEARCH_RADIUS},{user_lat},{user_lon});
                 relation["amenity"="cafe"](around:{SEARCH_RADIUS},{user_lat},{user_lon});
               );
               out center;
               """
        result = api.query(query)

        cafe_list = []

        elements = result.nodes + result.ways + result.relations
        for element in elements:
            try:
                if isinstance(element, overpy.Node):
                    lat, lon = float(element.lat), float(element.lon)
                elif isinstance(element, (overpy.Way, overpy.Relation)):
                    if element.center_lat is None or element.center_lon is None:
                        logger.warning(f"Element has no center: {element}")
                        continue
                    lat, lon = float(element.center_lat), float(element.center_lon)
                else:
                    continue

                cafe_name = element.tags.get('name', 'Unnamed Cafe')
                distance = geodesic((user_lat, user_lon), (lat, lon)).meters

                cafe_list.append({
                    'name': cafe_name,
                    'latitude': lat,
                    'longitude': lon,
                    'distance': distance
                })
            except AttributeError as e:
                logger.error(f"Incomplete element data: {e}")

        if not cafe_list:
            logger.info("No cafes found within the specified radius.")
            return jsonify({'message': 'No cafes found nearby.'}), 200

        # Sort and limit the cafe list
        sorted_cafes = sorted(cafe_list, key=lambda x: x['distance'])
        nearest_cafes = sorted_cafes[:MAX_CAFES]

        logger.info(f"Found {len(nearest_cafes)} cafes.")
        return jsonify({'cafes': nearest_cafes})

    except overpy.exception.OverpassTooManyRequests:
        logger.error("Overpass API: Too many requests")
        return jsonify({'error': 'Overpass API is receiving too many requests. Please try again later.'}), 503
    except overpy.exception.OverpassGatewayTimeout:
        logger.error("Overpass API: Gateway timeout")
        return jsonify({'error': 'Overpass API gateway timeout. Please try again later.'}), 504
    except overpy.exception.OverpassBadRequest as e:
        logger.error(f"Overpass API bad request: {e}")
        return jsonify({'error': 'Overpass API received a bad request.'}), 400
    except Exception as e:
        logger.exception("An unexpected error occurred.")
        return jsonify({'error': 'An error occurred. Please try again later.'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=bool(os.getenv('FLASK_DEBUG', 'False')))

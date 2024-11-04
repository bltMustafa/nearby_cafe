# Flask Cafe Finder Application

## Overview

This is a Flask-based web application designed to help users locate nearby cafes using the Overpass API and display them
on an interactive map powered by Leaflet.js. Users can see their current location and nearby cafes within a specified
radius on the map.

## Features

- Interactive map display using Leaflet.js
- Geolocation to capture the user's current position
- Fetches data from Overpass API to find nearby cafes
- Displays cafe information, including name and distance, on the map

## Requirements

- Python 3.x
- Flask
- Overpy
- Geopy

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/flask-cafe-finder.git
   cd flask-cafe-finder
   ```

2. **Set up a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** (optional)
   Set the environment variables for custom configurations:
   ```
   OVERPASS_API_TIMEOUT=60
   SEARCH_RADIUS=5000
   MAX_CAFES=10
   FLASK_DEBUG=True
   ```

## Running the Application

1. **Start the Flask app**
   ```bash
   flask run --host=0.0.0.0 --port=7777
   ```

2. **Access the application**
   Open your web browser and go to `http://127.0.0.1:7777`.

## File Structure

- `app.py`: Main Flask application script.
- `templates/index.html`: HTML template for rendering the frontend.
- `static/styles.css`: Custom CSS for styling (optional).

## How It Works

1. **User Interface**: The user clicks a button to get their current location.
2. **Geolocation**: The browser captures the user's latitude and longitude.
3. **Backend Request**: The frontend sends this location data to the `/get_cafes` endpoint.
4. **Overpass API Query**: The server queries the Overpass API to find cafes within the specified radius.
5. **Response**: The results are processed and returned as JSON to the frontend.
6. **Map Display**: The frontend displays the user's location and nearby cafes on the map.

## Dependencies

- **Flask**: For building the web application
- **Overpy**: For querying the Overpass API
- **Geopy**: For calculating distances
- **Leaflet.js**: For rendering the map

## Example Query

The Overpass API query used in the app:

```python
query = f"""
(
  node["amenity"="cafe"](around:{SEARCH_RADIUS},{user_lat},{user_lon});
  way["amenity"="cafe"](around:{SEARCH_RADIUS},{user_lat},{user_lon});
  relation["amenity"="cafe"](around:{SEARCH_RADIUS},{user_lat},{user_lon});
);
out center;
"""
```

## Error Handling

The application includes error handling for common issues:

- **Invalid input data**: Returns a 400 status code with an appropriate message.
- **Overpass API issues**: Handles `OverpassTooManyRequests`, `OverpassGatewayTimeout`, and `OverpassBadRequest` errors.
- **Unexpected errors**: Logs detailed error messages and returns a 500 status code.




import overpy
import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """ Test the index route returns status 200."""
    response = client.get('/')
    assert response.status_code == 200


def test_get_cafes_with_valid_input(client):
    """ Test the index route return status 200"""
    response = client.post('/get_cafes', json={
        'latitude': 40.748816,
        'longitude': -73.96908,
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'cafes' in data
    assert isinstance(data['cafes'], list)


def test_get_cafes_no_results(client, mocker):
    """Test the /get_cafes route with valid latitude and longitude."""
    mocker.patch('overpy.Overpass.query', return_value=overpy.Result())
    response = client.post('/get_cafes', json={
        'latitude': 40.748816,
        'longitude': -73.96908,
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'No cafes found nearby.'


def test_get_cafes_api_error(client, mocker):
    """Test handling of Overpass API errors."""
    mocker.patch('overpy.Overpass.query', side_effect=overpy.exception.OverpassTooManyRequests)
    response = client.post('/get_cafes', json={
        'latitude': 40.748816,
        'longitude': -73.96908,
    })
    assert response.status_code == 503
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Overpass API is receiving too many requests. Please try again later.'


if __name__ == "__main__":
    pytest.main()
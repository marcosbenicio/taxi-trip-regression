import numpy as np
from geopy import distance


def geodesic(start_lat, start_long, end_lat, end_long):
    """
    Calculate geodesic distances between pickup and dropoff locations.

    Args:
    - start_lat, start_long, end_lat, end_long: Lists or arrays of coordinates 
    for the start point and end point.

    Returns:
    List of distances in meters for each pair of start and end points.
    """
    coordinates = zip(start_lat, start_long, end_lat, end_long)
    distances = [distance.distance((lat1, lon1), (lat2, lon2)).meters for lat1, lon1, lat2, lon2 in coordinates]
    return distances

def bearing(start_lat, start_lon, end_lat, end_lon):
    """
    Calculate the initial bearing (azimuth) between two sets of latitude and longitude coordinates.

    Args:
    - start_lat (float): Latitude of the starting point in degrees.
    - start_lon (float): Longitude of the starting point in degrees.
    - end_lat (float): Latitude of the ending point in degrees.
    - end_lon (float): Longitude of the ending point in degrees.

    Returns:
    float: The initial bearing in degrees, normalized to the range [0, 360).
    """
    
    # Convert latitude and longitude from degrees to radians
    start_lat, start_lon, end_lat, end_lon = map(np.radians, [start_lat, start_lon, end_lat, end_lon])

    # Calculate the change in coordinates
    dlon = end_lon - start_lon

    # Calculate bearing
    x = np.sin(dlon) * np.cos(end_lat)
    y = np.cos(start_lat) * np.sin(end_lat) - np.sin(start_lat) * np.cos(end_lat) * np.cos(dlon)
    initial_bearing = np.arctan2(x, y)

    # Convert from radians to degrees and normalize (0-360)
    initial_bearing = np.degrees(initial_bearing)
    bearing = (initial_bearing + 360) % 360

    return bearing
import math
import geopy.distance


def distance_between_two_coords(ll1, ll2):
    coords_1 = ll1
    coords_2 = ll2

    km = geopy.distance.distance(coords_1, coords_2).km
    mi = km * 0.621371
    meters = km * 1000
    yards = mi * 1760
    return {
        "miles": round(mi, 2),
        "km": round(km, 2),
        "meters": round(meters, 2),
        "yards": round(yards, 2),
    }


def radius_around_coords(latitude, longitude, radius, radial_step=10):
    R = 6373.0

    lat = math.radians(latitude)
    lon = math.radians(longitude)

    d = radius / 1000

    coords = []

    for brng in range(0, 360, radial_step):
        brng = math.radians(brng)

        lat2 = math.asin(
            math.sin(lat) * math.cos(d / R)
            + math.cos(lat) * math.sin(d / R) * math.cos(brng)
        )
        lon2 = lon + math.atan2(
            math.sin(brng) * math.sin(d / R) * math.cos(lat),
            math.cos(d / R) - math.sin(lat) * math.sin(lat2),
        )

        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)
        coords.append({"latitude": lat2, "longitude": lon2, "bearing": brng})

    return coords


def is_out_of_radius(pointA, pointB, radius):
    if type(pointA) == dict:
        pointA = (pointA["latitude"], pointA["longitude"])
    if type(pointB) == dict:
        pointB = (pointB["latitude"], pointB["longitude"])

    distance = distance_between_two_coords(pointA, pointB)

    res = {
        "distance": distance,
    }

    if radius > distance["miles"]:
        res["out_of_radius"] = True
    else:
        res["out_of_radius"] = False

    return res

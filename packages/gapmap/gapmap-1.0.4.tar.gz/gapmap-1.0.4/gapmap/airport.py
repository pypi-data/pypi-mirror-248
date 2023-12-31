import airportsdata
import geopy


async def details_for_iata(iata):
    airports = airportsdata.load("IATA")
    return airports[iata]


def find_airports_near_position(lat, lon, radius=50):
    airports = airportsdata.load()

    airports_near = []

    for aps in list(airports.keys()):
        ap = airports[aps]

        coords_test = (ap["lat"], ap["lon"])
        dist = geopy.distance.geodesic((lat, lon), coords_test).miles
        if dist <= radius:
            iata = ap["iata"]
            if len(iata) > 0:
                airports_near.append(
                    {
                        "id": aps,
                        "iata": iata,
                        "icao": ap["icao"],
                        "name": ap["name"],
                        "elevation": ap["elevation"],
                        "timezone": ap.get("tz", None),
                        "distance_from_point": round(dist),
                        "coords": {"latitude": ap["lat"], "longitude": ap["lon"]},
                        "country": ap["country"],
                        "city": ap["city"],
                        "subdomain": ap["subd"],
                    }
                )

    return airports_near

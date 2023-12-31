import geonamescache
import json
import math
import geopy.distance

from gapmap.distance import (
    distance_between_two_coords,
    radius_around_coords,
    is_out_of_radius,
)


def pretty_print(dta):
    json_object = json.dumps(dta, indent=4)
    json_formatted_str = json.dumps(json_object, indent=2)
    print(json_formatted_str)


def cities():
    gc = geonamescache.GeonamesCache()
    cities = gc.get_cities()
    return cities


def countries():
    gc = geonamescache.GeonamesCache()
    countries = gc.get_countries()
    return countries


def continents():
    gc = geonamescache.GeonamesCache()
    continents = gc.get_continents()
    return continents


def remap_country_output(countries, expanded=False):
    dta = []
    return_single = False

    if type(countries) == dict:
        return_single = True
        countries = [countries]

    for c in countries:
        d = {}
        d["id"] = c["geonameid"]
        d["name"] = c["name"]
        d["iso"] = c["iso"]
        d["iso3"] = c["iso3"]
        d["isonumeric"] = c["isonumeric"]
        d["fips"] = c["fips"]
        d["continentcode"] = c["continentcode"]
        d["capital"] = c["capital"]

        dta.append(d)

    if return_single:
        return dta[0]
    return dta


def remap_continent_output(continents, expanded=False):
    dta = []
    return_single = False

    if type(continents) == dict:
        return_single = True
        continents = [continents]

    for c in continents:
        d = {}
        d["id"] = c["geonameId"]
        d["name"] = c["name"]
        d["bounding"] = {
            "north": c["bbox"]["north"],
            "south": c["bbox"]["south"],
            "east": c["bbox"]["east"],
            "west": c["bbox"]["west"],
        }

        dta.append(d)

    if return_single:
        return dta[0]
    return dta


def remap_city_output(cities, expanded=False):
    dta = []
    return_single = False

    if type(cities) == dict:
        return_single = True
        cities = [cities]

    for c in cities:
        d = {}
        d["id"] = c["geonameid"]
        d["name"] = c["name"]
        d["countrycode"] = c["countrycode"]
        d["latitude"] = c["latitude"]
        d["longitude"] = c["longitude"]
        d["population"] = c["population"]
        d["timezone"] = c["timezone"]
        d["population"] = c["population"]

        if expanded:
            d["country"] = remap_country_output(
                countries()[c["countrycode"]], expanded=expanded
            )
            d["continent"] = remap_continent_output(
                continents()[d["country"]["continentcode"]], expanded=expanded
            )

        dta.append(d)

    if return_single:
        return dta[0]
    return dta


def get_city_by_name(name, radius=0, expanded=False):
    gc = geonamescache.GeonamesCache()
    c = gc.search_cities(name, case_sensitive=False)

    if len(c) == 0:
        return None

    if radius > 0:
        lat = c[0]["latitude"]
        lon = c[0]["longitude"]
        c = radius_around_coords(lat, lon, radius)

        remap = remap_city_output(c, expanded=expanded)

        return {
            "radius": radius,
            "cities": remap[0],
        }

    if len(c) == 1:
        return remap_city_output(c, expanded=expanded)[0]

    return {
        "cities": remap_city_output(c, expanded=expanded)[0],
    }


def radius_around_city(cityName, radius):
    c = get_city_by_name(cityName)
    return radius_around_coords((c["latitude"], c["longitude"]), radius)


def cities_near_lat_lon(lat, lon):
    gc = geonamescache.GeonamesCache()
    cities = gc.get_cities()

    cities_near = []

    for c in list(cities.keys()):
        city = cities[c]
        lata = city["latitude"]
        lona = city["longitude"]

        is_out = is_out_of_radius((lat, lon), (lata, lona), 50)

        if is_out["distance"]["miles"] <= 50:
            cities_near.append(remap_city_output(city))

    return cities_near


def distance_between_cities(fromCityName, toCityName):
    c1 = get_city_by_name(fromCityName)
    c2 = get_city_by_name(toCityName)

    cities1 = c1.get("cities", None)
    cities2 = c2.get("cities", None)

    if cities1 is not None:
        if type(cities1) == dict:
            c1 = cities1
        else:
            c1 = cities1[0]
    if cities2 is not None:
        if type(cities2) == dict:
            c2 = cities2
        else:
            c2 = cities2[0]

    coords_1 = (c1["latitude"], c1["longitude"])
    coords_2 = (c2["latitude"], c2["longitude"])

    distance = distance_between_two_coords(coords_1, coords_2)

    return {
        "distances": distance,
        "from": c1,
        "to": c2,
    }

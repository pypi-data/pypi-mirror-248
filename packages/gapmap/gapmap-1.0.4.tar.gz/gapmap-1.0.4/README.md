[![Release](https://github.com/mooncitizen/gapmap/actions/workflows/pypi.yaml/badge.svg)](https://github.com/mooncitizen/gapmap/actions/workflows/pypi.yaml)


![alt text](https://github.com/mooncitizen/gapmap/blob/main/images/logo150.png?raw=true)

## GAPMAP

A helper library that makes pathing simple in the real world. Point to Point distance finding and even Placename finding.

Roadmap

- [x] Placename finder (City, Country)
- [x] Airport finder
- [x] Euclidean Distances
- [] GIS based Pathing
- [] GIS Based timing
- [] Map Generation
- [] Hotswapping hosted maps

# Installation
```pip install gapmap``` or download the latest binary from the releases tab

# Usage
1. [Get City by name](#get-city-by-name)
2. [Distance between cities](#distance-between-cities)
3. [Radius around coords](#radius-around-coords)
4. [Is out of radius](#is-out-of-radius)
5. [Airport Finder](#airport-finder)

### Get City by name
```python
from gapmap import get_city_by_name

# this is not case sensitive
# Expanded returns continent and country information also
city = get_city_by_name("edinburgh", expanded=True)

# The returning object could be one of just the city information itself or an array of cities
cities = city.get('cities', None)

if cities is None:
    print(city)
else:
    print(cities)

```

This will return 

```json
{
  "id": 2650225,
  "name": "Edinburgh",
  "countrycode": "GB",
  "latitude": 55.95206,
  "longitude": -3.19648,
  "population": 506520,
  "timezone": "Europe/London",
  "country": {
    "id": 2635167,
    "name": "United Kingdom",
    "iso": "GB",
    "iso3": "GBR",
    "isonumeric": 826,
    "fips": "UK",
    "continentcode": "EU",
    "capital": "London"
  },
  "continent": {
    "id": 6255148,
    "name": "Europe",
    "bounding": {
      "north": 80.76416015625,
      "south": 27.6377894797159,
      "east": 41.73303985595703,
      "west": -24.532675386662543
    }
  }
}
```

### Distance between cities

```python

from gapmap import distance_between_cities

distance = distance_between_cities("edinburgh", "glasgow")

```

This will return 

```json
{
  "distances": {
    "miles": 41.67,
    "km": 67.07,
    "meters": 67065.32,
    "yards": 73343.5
  },
  "from": {
    "id": 2650225,
    "name": "Edinburgh",
    "countrycode": "GB",
    "latitude": 55.95206,
    "longitude": -3.19648,
    "population": 506520,
    "timezone": "Europe/London"
  },
  "to": {
    "id": 2648579,
    "name": "Glasgow",
    "countrycode": "GB",
    "latitude": 55.86515,
    "longitude": -4.25763,
    "population": 626410,
    "timezone": "Europe/London"
  }
}
```

### Radius around coords

This will provide a circular radius around the given latitude and longitude the radius from point to circle is in miles. There is an optional radial step that you can draw at each degree around the circle or you can step it up to whatever you want ```1-359``` the default step is every 10 degrees

```python
from gapmap import radius_around_coords

radius = radius_around_coords(55.95206, -3.19648, radial_step=10)

```

This will return 

```json
{
  "id": 2650225,
  "name": "Edinburgh",
  "countrycode": "GB",
  "latitude": 55.95206,
  "longitude": -3.19648,
  "population": 506520,
  "timezone": "Europe/London",
  "range": 15,
  "radius": [
    {
      "latitude": 55.95219485590659,
      "longitude": -3.19648,
      "bearing": 0
    },
    {
      "latitude": 55.952192807135276,
      "longitude": -3.1964381744369734,
      "bearing": 0.17453292519943295
    },
    {
      "latitude": 55.95218672307282,
      "longitude": -3.196397619735461,
      "bearing": 0.3490658503988659
    },
    {
      "latitude": 55.95217678858224,
      "longitude": -3.196359568140929,
      "bearing": 0.5235987755982988
    },
    {
      "latitude": 55.95216330552083,
      "longitude": -3.1963251758402738,
      "bearing": 0.6981317007977318
    },
    {
      "latitude": 55.95214668356804,
      "longitude": -3.196295487830642,
      "bearing": 0.8726646259971648
    },
    {
      "latitude": 55.95212742777716,
      "longitude": -3.1962714061671837,
      "bearing": 1.0471975511965976
    },
    {
      "latitude": 55.95210612322911,
      "longitude": -3.1962536625545614,
      "bearing": 1.2217304763960306
    },
    {
      "latitude": 55.95208341725465,
      "longitude": -3.1962427961150164,
      "bearing": 1.3962634015954636
    },
    {
      "latitude": 55.95205999976514,
      "longitude": -3.196239137008431,
      "bearing": 1.5707963267948966
    },
    {
      "latitude": 55.95203658228979,
      "longitude": -3.196242796401961,
      "bearing": 1.7453292519943295
    },
    {
      "latitude": 55.95201387635612,
      "longitude": -3.196253663093841,
      "bearing": 1.9198621771937625
    },
    {
      "latitude": 55.951992571870555,
      "longitude": -3.196271406893753,
      "bearing": 2.0943951023931953
    },
    {
      "latitude": 55.95197331615633,
      "longitude": -3.196295488656866,
      "bearing": 2.2689280275926285
    },
    {
      "latitude": 55.95195669428511,
      "longitude": -3.1963251766664977,
      "bearing": 2.443460952792061
    },
    {
      "latitude": 55.95194321130033,
      "longitude": -3.1963595688674986,
      "bearing": 2.6179938779914944
    },
    {
      "latitude": 55.951933276872246,
      "longitude": -3.19639762027474,
      "bearing": 2.792526803190927
    },
    {
      "latitude": 55.95192719285057,
      "longitude": -3.1964381747239186,
      "bearing": 2.9670597283903604
    },
    {
      "latitude": 55.951925144093416,
      "longitude": -3.19648,
      "bearing": 3.141592653589793
    },
    {
      "latitude": 55.95192719285057,
      "longitude": -3.196521825276082,
      "bearing": 3.3161255787892263
    },
    {
      "latitude": 55.951933276872246,
      "longitude": -3.1965623797252603,
      "bearing": 3.490658503988659
    },
    {
      "latitude": 55.95194321130033,
      "longitude": -3.196600431132502,
      "bearing": 3.6651914291880923
    },
    {
      "latitude": 55.95195669428511,
      "longitude": -3.1966348233335022,
      "bearing": 3.839724354387525
    },
    {
      "latitude": 55.95197331615633,
      "longitude": -3.1966645113431342,
      "bearing": 4.014257279586958
    },
    {
      "latitude": 55.951992571870555,
      "longitude": -3.1966885931062468,
      "bearing": 4.1887902047863905
    },
    {
      "latitude": 55.95201387635612,
      "longitude": -3.196706336906159,
      "bearing": 4.363323129985824
    },
    {
      "latitude": 55.95203658228979,
      "longitude": -3.1967172035980393,
      "bearing": 4.537856055185257
    },
    {
      "latitude": 55.95205999976514,
      "longitude": -3.1967208629915693,
      "bearing": 4.71238898038469
    },
    {
      "latitude": 55.95208341725465,
      "longitude": -3.1967172038849836,
      "bearing": 4.886921905584122
    },
    {
      "latitude": 55.95210612322911,
      "longitude": -3.1967063374454385,
      "bearing": 5.061454830783556
    },
    {
      "latitude": 55.95212742777716,
      "longitude": -3.1966885938328167,
      "bearing": 5.235987755982989
    },
    {
      "latitude": 55.95214668356804,
      "longitude": -3.196664512169358,
      "bearing": 5.410520681182422
    },
    {
      "latitude": 55.95216330552083,
      "longitude": -3.1966348241597267,
      "bearing": 5.585053606381854
    },
    {
      "latitude": 55.95217678858224,
      "longitude": -3.1966004318590713,
      "bearing": 5.759586531581287
    },
    {
      "latitude": 55.95218672307282,
      "longitude": -3.1965623802645395,
      "bearing": 5.934119456780721
    },
    {
      "latitude": 55.952192807135276,
      "longitude": -3.196521825563027,
      "bearing": 6.1086523819801535
    }
  ]
}
```

### Is out of radius

A helper function to determine if something is out of radius. This is currently straight line.

```python

from gapmap import is_out_of_radius

## Input tuple or dict (55.95206, -3.19648) or object with latitude and longitude in the root { "latitude: ..., "longitude": ....}
## is_out_of_radius(pointA, pointB, radius) - Radius is in miles
radius = is_out_of_radius((55.95206, -3.19648), (55.86515, -4.25763), 40)

```

This will return

```json
{
  "distance": {
    "miles": 41.67,
    "km": 67.07,
    "meters": 67065.32,
    "yards": 73343.5
  },
  "out_of_radius": false
}
```

## Airport finder
A helper function to find airports in a given area
```python
from gapmap import find_airports_near_position

airports = find_airports_near_position(55.95206, -3.19648, radius=70)

```

This will return

```json
[
  {
    "id": "EGPF",
    "iata": "GLA",
    "icao": "EGPF",
    "name": "Glasgow International Airport",
    "elevation": 26,
    "timezone": "Europe/London",
    "distance_from_point": 48,
    "coords": {
      "latitude": 55.8718986511,
      "longitude": -4.4330601692
    },
    "country": "GB",
    "city": "Glasgow",
    "subdomain": "Scotland"
  },
  {
    "id": "EGPH",
    "iata": "EDI",
    "icao": "EGPH",
    "name": "Edinburgh Airport",
    "elevation": 135,
    "timezone": "Europe/London",
    "distance_from_point": 7,
    "coords": {
      "latitude": 55.9500007629,
      "longitude": -3.3724999428
    },
    "country": "GB",
    "city": "Edinburgh",
    "subdomain": "Scotland"
  },
  {
    "id": "EGPN",
    "iata": "DND",
    "icao": "EGPN",
    "name": "Dundee Airport",
    "elevation": 17,
    "timezone": "Europe/London",
    "distance_from_point": 35,
    "coords": {
      "latitude": 56.4524993896,
      "longitude": -3.0258300304
    },
    "country": "GB",
    "city": "Dundee",
    "subdomain": "Scotland"
  },
  {
    "id": "EGPT",
    "iata": "PSL",
    "icao": "EGPT",
    "name": "Perth/Scone Airport",
    "elevation": 397,
    "timezone": "Europe/London",
    "distance_from_point": 34,
    "coords": {
      "latitude": 56.439201355,
      "longitude": -3.3722200394
    },
    "country": "GB",
    "city": "Perth",
    "subdomain": "Scotland"
  },
  {
    "id": "EGQL",
    "iata": "ADX",
    "icao": "EGQL",
    "name": "RAF Leuchars",
    "elevation": 38,
    "timezone": "Europe/London",
    "distance_from_point": 32,
    "coords": {
      "latitude": 56.3728981018,
      "longitude": -2.8684399128
    },
    "country": "GB",
    "city": "St. Andrews",
    "subdomain": "Scotland"
  }
]
```

# Euclidean Distance
This can simply be described as stright line distance or as the crow flys. This will not be accurate in terms of finding ranges where there is a route to be adhered to. Its more of an indication rather than guidance. But can help build a picture between points. For example you could levy a percentage of overage to be applied that could guestimate that an area is out of range. However this is exponentially bad when the direct line distance is great. It might be good for something within 20 miles but not at 100 miles. A great starting resource would be to read [Euclidean Distance Formula - CUEMATH](https://www.cuemath.com/euclidean-distance-formula/)

# Purpose

The purpose of this library is to grow it into a trusted framework of getting real world distance finding for land, sea and air using real world restrictions. The ability to create pathing in a unified form to work with the likes of <b>Google Maps</b> and <b>Mapbox</b>

# End Goal
To create a machine/ai learned process that predict routing, pathing and distance. But got to start somewhere


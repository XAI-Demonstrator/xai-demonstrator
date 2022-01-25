import random
from shapely.geometry import Point

def generate_random(polygon):
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < 1:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(pnt):
            points.append(pnt)
    return list(points[0].coords)

def get_locstring(coordinates):
    lng = coordinates[0][0]
    lat = coordinates[0][1]
    locstring = str(lat) + "," + str(lng)
    return locstring
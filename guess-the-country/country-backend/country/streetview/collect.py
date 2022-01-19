from shapely.geometry import Point, Polygon
import random
from urllib.request import urlopen
from urllib.error import URLError
import requests
from pydantic import BaseModel
import base64
from xaidemo.tracing import traced

class Streetview(BaseModel):
    image: bytes
    class_label: str

GOOGLE_URL = (
    "http://maps.googleapis.com/maps/api/streetview?size=448x448&sensor=false&"
    "size=640x640&source=outdoor&key="
)

API_URL = "https://maps.googleapis.com/maps/api/streetview/metadata"  # Not billed    

def generate_random(polygon):
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < 1:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(pnt):
            points.append(pnt)
    return list(points[0].coords)


@traced
def get_streetview(country_array, API_KEY):
    nominated_country = random.randint(0, 3)
    coordinaten = country_array[nominated_country]['polygon']
    poly = Polygon(coordinaten)
    imagery_hits = 0
    status = False
    while imagery_hits < 1:
        while status != "OK":
            coord = generate_random(poly)
            lng = coord[0][0]
            lat = coord[0][1]
            locstring = str(lat) + "," + str(lng)
            r = requests.get(API_URL + "?key=" + API_KEY +
                             "&location=" + locstring + "&source=outdoor")
            status = r.json()["status"]
            print(status)
        print("    ========== Got one! ==========")
        url = GOOGLE_URL + API_KEY + "&location=" + locstring
        try:
            contents = urlopen(url).read()
            #urlretrieve(url, outfile)
        except URLError:
            #print("    No imagery")
            break

        imagery_hits += 1
        status = False
        encoded_image_string = base64.b64encode(contents)
        encoded_bytes = bytes("data:image/png;base64,",
                              encoding="utf-8") + encoded_image_string
    return Streetview(
        image=encoded_bytes,
        class_label=country_array[nominated_country]['city']
    )
import pytest
from country.streetview import collect, polygon
from shapely.geometry import Polygon

def test_that_image_is_encoded(generate_image):
    result = collect.encode_image(generate_image(448,448))
    assert result[:22] == bytes("data:image/png;base64,", encoding='utf-8')

def test_if_polygon_is_returned():
    polygon, city = collect.get_city()
    assert type(polygon) is Polygon
    assert type(city) is str


def test_if_locstring_is_returned():
    coord = polygon.generate_random( Polygon([(35.1817982, 31.7716133), (35.1801823, 31.7690279), (35.176277, 31.7691009), (35.1740883, 31.7681887), (35.1743458, 31.765963), (35.1731012, 31.7635914), (35.1723288, 31.7619859), (35.1747749, 31.7612196), (35.1763003, 31.7617966), (35.1840876, 31.7554542), (35.1887653, 31.7542865), (35.1934002, 31.7565125), (35.197472, 31.7574317), (35.1997517, 31.754177), 
                    (35.2008246, 31.7520605), (35.2047728, 31.7507103), (35.205674, 31.7489951), (35.2083347, 31.7512212), (35.2149008, 31.7506373), (35.2190636, 31.7497615), (35.225458, 31.7623873), (35.226445, 31.7686265), (35.2255867, 31.7705603), (35.2266167, 31.7714724), (35.2273033, 31.7763247), (35.2255009, 31.7784407), (35.2250413, 31.7789474), (35.2278523, 31.7806164), (35.2280025, 31.7817382), (35.2271656, 31.7834528), (35.2272407, 31.7861522), (35.2265112, 31.7925176), (35.2265594, 31.7933976), (35.2232764, 31.7942183), (35.2216242, 31.7936347), 
                    (35.2198646, 31.7956043), (35.2152225, 31.7936072), (35.2118609, 31.7921391), (35.2089856, 31.792431), (35.2044278, 31.7923225), (35.2030115, 31.7910093), (35.2009731, 31.7907722), (35.1996133, 31.7893066), (35.1999968, 31.7878228), (35.1954584, 31.7833671), (35.1901155, 31.7826922), (35.1869949, 31.7788226), (35.1844951, 31.7763532), (35.1817982, 31.7716133)]))
    location = polygon.get_locstring(coord) 
    assert type(location) is str

@pytest.mark.integration
def test_if_streetview_image_is_obtained():
    result = collect.get_streetview()
    assert type(result) is collect.Streetview
    assert type(result.class_label) is str
    assert result[:22] == bytes("data:image/png;base64,", encoding='utf-8')


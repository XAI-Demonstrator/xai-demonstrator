from xaidemo import routers


def test_that_vue_frontend_has_three_routes():
    f = routers.vue_frontend(__file__)

    assert len(f.routes) == 3


def test_main_page():
    f = routers.vue_frontend(__file__)

    for route in f.routes:
        if route.name == "get_frontend":
            r = route.endpoint()
            assert r.path.name == "index.html"
            assert r.path.parent.name == "static"
            break
    else:
        raise Exception("Missing route 'get_frontend'")


def test_favicon():
    f = routers.vue_frontend(__file__)

    for route in f.routes:
        if route.name == "get_favicon":
            r = route.endpoint()
            assert r.path.name == "favicon.ico"
            assert r.path.parent.name == "static"
            break
    else:
        raise Exception("Missing route 'get_favicon'")


def test_static():
    f = routers.vue_frontend(__file__)

    for route in f.routes:
        if route.name == "get_static":
            r = route.endpoint("folder", "file")
            assert r.path.name == "file"
            assert r.path.parent.name == "folder"
            assert r.path.parent.parent.name == "static"
            break
    else:
        raise Exception("Missing route 'get_static'")

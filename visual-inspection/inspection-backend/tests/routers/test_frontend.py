from inspection.routers import frontend


def test_main_page():
    r = frontend.frontend()

    assert r.path.name == "index.html"
    assert r.path.parent.name == "static"


def test_favicon():
    r = frontend.favicon()

    assert r.path.name == "favicon.ico"
    assert r.path.parent.name == "static"


def test_static():
    r = frontend.static("folder", "file")

    assert r.path.name == "file"
    assert r.path.parent.name == "folder"
    assert r.path.parent.parent.name == "static"

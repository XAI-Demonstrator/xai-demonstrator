import fastapi
from fastapi.testclient import TestClient

from xaidemo import routers

import pytest


@pytest.fixture
def client_with_static_files(tmp_path):
    app = fastapi.FastAPI()
    app.include_router(routers.vue_frontend(str(tmp_path / "main.py")))

    client = TestClient(app)

    static_dir = tmp_path / "static"
    static_dir.mkdir()

    index_html = static_dir / "index.html"
    index_html.write_text("INDEX PAGE")

    favicon_ico = static_dir / "favicon.ico"
    favicon_ico.write_text("FAVICON")

    js_dir = static_dir / "js"
    js_dir.mkdir()

    app_js = js_dir / "app.js"
    app_js.write_text("JS FOR TEST")

    unreachable_file = tmp_path / "unreachable.txt"
    unreachable_file.write_text("none of your business")

    return client


def test_that_vue_frontend_has_three_routes():
    f = routers.vue_frontend(__file__)
    assert len(f.routes) == 3


def test_that_main_page_is_returned(client_with_static_files):
    r = client_with_static_files.get("/")
    assert r.status_code == 200


def test_that_favicon_is_returned(client_with_static_files):
    r = client_with_static_files.get("/favicon.ico")
    assert r.status_code == 200


def test_that_static_files_are_returned(client_with_static_files):
    r = client_with_static_files.get("/js/app.js")
    assert r.status_code == 200


def test_that_missing_static_files_yield_404(client_with_static_files):
    r = client_with_static_files.get("/js/missing.js")
    assert r.status_code == 404


def test_that_users_can_only_access_static_files(client_with_static_files):
    r = client_with_static_files.get("/%2E%2E/unreachable.txt")
    assert r.status_code == 404


def test_that_users_cannot_reach_above_static_folder(client_with_static_files):
    r = client_with_static_files.get("/%2E%2E/static/favicon.ico")
    assert r.status_code == 404

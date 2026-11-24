from tools import find_breed_info

def test_siamese_origin(monkeypatch):
    class FakeResponse:
        status_code = 200
        def raise_for_status(self):
          pass
        def json(self):
          return [{"name": "Siamese", "origin": "Thailand"}]
    monkeypatch.setattr("tools.requests.get", lambda *a, **k: FakeResponse())
    monkeypatch.setenv("CAT_API_KEY", "test")
    assert find_breed_info("Siamese")["origin"] == "Thailand"


def test_api_error(monkeypatch):
    class FakeErrorResponse:
        status_code = 500
        text = "Server error"
        def raise_for_status(self):
          pass
        def json(self):
          return {}

    monkeypatch.setattr("tools.requests.get", lambda *a, **k: FakeErrorResponse())
    monkeypatch.setenv("CAT_API_KEY", "test")
    result = find_breed_info("Siamese")
    assert find_breed_info("Siamese")["error"] == "Breed not found"
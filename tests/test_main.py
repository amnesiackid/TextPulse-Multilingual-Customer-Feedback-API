from fastapi.testclient import TestClient
from main import app
import pytest
from dependencies import get_settings, get_db
from types import SimpleNamespace
from uuid import UUID
from datetime import datetime

client = TestClient(app)
settings = get_settings()


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "version": f"{settings['app_version']}"}

@pytest.mark.parametrize(
    "text",
    [
        "123 !!!",
        "456!!!",
        "...",
        "   ",
        "€$%",
    ],
)
def test_analyze_rejects_text_without_letters(text):
    with TestClient(app) as client:
        response = client.post(
            "/analyze",
            json={
                "text": text,
                "product_id": "00000000-0000-0000-0000-000000000001",
                "product_name": "Sample Product",
                "commenter_id": "00000000-0000-0000-0000-000000000002",
            },
        )

    assert response.status_code == 422
    assert response.json() == {
        "detail": "Text must contain at least one alphabetic character"
    }



@pytest.mark.parametrize(
    "text",
    [   "good!",
        "product",
        "bad:(",
    ],
)
def test_analyze_rejects_too_few_words(text):
    with TestClient(app) as client:
        response = client.post(
            "/analyze",
            json={
                "text": text,
                "product_id": "00000000-0000-0000-0000-000000000001",
                "product_name": "Sample Product",
                "commenter_id": "00000000-0000-0000-0000-000000000002",
            },
        )

    assert response.status_code == 422
    assert response.json() == {
        "detail": f"Text must contain at least {settings['min_word_count']} words"
    }

@pytest.mark.parametrize("word_count", [2001, 3000, 4000, 5000])
def test_analyze_rejects_too_many_words(word_count):
    with TestClient(app) as client:
        text = "word " * word_count

        response = client.post(
            "/analyze",
            json={
                "text": text,
                "product_id": "00000000-0000-0000-0000-000000000001",
                "product_name": "Sample Product",
                "commenter_id": "00000000-0000-0000-0000-000000000002",
            },
        )

    assert response.status_code == 422
    assert response.json() == {
        "detail": f"Text must not exceed {settings['max_word_count']} words"
    }

class FakeQuery:
    def __init__(self, records):
        self.records = records

    def filter(self, condition):
        return self

    def order_by(self, condition):
        return self

    def limit(self, limit):
        self.records = self.records[:limit]
        return self

    def all(self):
        return self.records
    
class FakeSession:
    def __init__(self, records=None):
        self.records = records or []
        self.added_record = None
        self.committed = False
        self.refreshed_record = None

    def query(self, model):
        return FakeQuery(self.records)

    def add(self, record):
        self.added_record = record

    def commit(self):
        self.committed = True

    def refresh(self, record):
        self.refreshed_record = record

def override_get_db():
    yield FakeSession()

@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.mark.parametrize(
    "text, expected_aspect, expected_positive",
    [
        ("The delivery was very good.", "delivery", True),
        ("The packaging was bad.", "packaging", False),
        ("I love the camera.", "camera", True),
        ("The screen was broken.", "screen", False),
    ],
)
def test_analyze_returns_successful_response(
    client,
    text,
    expected_aspect,
    expected_positive,
):
    response = client.post(
        "/analyze",
        json={
            "text": text,
            "product_id": "00000000-0000-0000-0000-000000000001",
            "product_name": "Sample Product",
            "commenter_id": "00000000-0000-0000-0000-000000000002",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["detected_language"] == "en"
    assert len(data["aspects"]) == 1
    assert data["aspects"][0]["aspect"] == expected_aspect

    polarity = data["aspects"][0]["polarity"]

    if expected_positive:
        assert polarity > 0
    else:
        assert polarity < 0


@pytest.fixture
def client_and_db():
    fake_db = FakeSession()

    def override_get_db():
        yield fake_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client, fake_db

    app.dependency_overrides.clear()
def test_analyze_adds_record_and_commits(client_and_db):
    client, fake_db = client_and_db

    response = client.post(
        "/analyze",
        json={
            "text": "The delivery was very good.",
            "product_id": "00000000-0000-0000-0000-000000000001",
            "product_name": "Sample Product",
            "commenter_id": "00000000-0000-0000-0000-000000000002",
        },
    )

    assert response.status_code == 200
    assert fake_db.added_record is not None
    assert fake_db.committed is True
    assert fake_db.refreshed_record is fake_db.added_record

dummy_record_1 = SimpleNamespace(
    id=UUID("00000000-0000-0000-0000-000000000010"),
    product_id=UUID("00000000-0000-0000-0000-000000000001"),
    product_name="Sample Product",
    commenter_id=UUID("00000000-0000-0000-0000-000000000002"),
    text="The delivery was good.",
    detected_language="en",
    processed_at=datetime(2026, 8, 2, 12, 0, 0),
    aspects=[
        {
            "aspect": "delivery",
            "polarity": 0.5,
            "excerpt": "delivery was good",
        }
    ],
    keywords=["delivery", "good"],
    entities=[],
    lexical_density=0.5,
    negation_detected=False,
)

dummy_record_2 = SimpleNamespace(
    id=UUID("00000000-0000-0000-0000-000000000011"),
    product_id=UUID("00000000-0000-0000-0000-000000000001"),
    product_name="Another Product",
    commenter_id=UUID("00000000-0000-0000-0000-000000000002"),
    text="The camera is broken.",
    detected_language="en",
    processed_at=datetime(2026, 8, 2, 12, 0, 0),
    aspects=[
        {
            "aspect": "camera",
            "polarity": -0.8,
            "excerpt": "camera is broken",
        }
    ],
    keywords=["camera", "broken"],
    entities=[],
    lexical_density=0.8,
    negation_detected=False,
)

@pytest.fixture
def history_client():
    fake_db = FakeSession(
        records=[
            dummy_record_1,
            dummy_record_2,
        ]
    )

    def override_get_db():
        yield fake_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

def test_history_returns_records(history_client):
    response = history_client.get("/history")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["product_name"] == "Sample Product"
    assert data[0]["text"] == "The delivery was good."
    assert data[0]["metrics"]["lexical_density"] == 0.5

def test_history_applies_limit(history_client):
    response = history_client.get("/history?limit=1")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["text"] == "The delivery was good."

@pytest.mark.parametrize("limit", [0, 101])
def test_history_rejects_invalid_limit(history_client, limit):
    response = history_client.get(f"/history?limit={limit}")

    assert response.status_code == 422
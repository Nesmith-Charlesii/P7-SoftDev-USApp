from flask import request

from server import app


def test_homepage():
    """Test the homepage works (HTTP status 200 OK)"""
    with app.test_client() as c:
        resp = c.get("/")
        assert resp.status_code == 200


def test_login():
    """Tests a login action"""
    with app.test_client() as c:
        resp = c.post(
            "/login", data={"email": "john@simplylift.co"}, follow_redirects=True
        )
        # We should be redirected to the summary page
        assert request.path == "/summary"
        # The status code should be 200 OK
        assert resp.status_code == 200
        # The email of the user logged in is displayed on the page
        assert "john@simplylift.co" in resp.data.decode()


def test_booking_past_competition_returns_403():
    with app.test_client() as client:
        client.post("/login", data={"email": "john@simplylift.co"})

        response = client.get("/book/Fall Classic")
        page = response.data.decode()

        assert response.status_code == 403
        assert "You cannot book spots for past competitions." in page


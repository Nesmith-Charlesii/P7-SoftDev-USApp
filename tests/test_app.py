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


def test_clubs_page():
    """
    Test that the /clubs page loads correctly
    and displays all club names and their points
    """
    with app.test_client() as client:
        resp = client.get("/clubs")
        
        assert resp.status_code == 200

        html = resp.data.decode()

        assert "Simply Lift" in html
        assert "13" in html
        assert "Iron Temple" in html
        assert "4" in html
        assert "She Lifts" in html
        assert "12" in html

        
def test_booking_deducts_club_points():
    """
    Booking spots should deduct the same number of points
    from the club balance (1 spot = 1 point)
    """
    with app.test_client() as client:
        client.post(
            "/login",
            data={"email": "john@simplylift.co"},
            follow_redirects=True,
        )

        response = client.post(
            "/book",
            data={
                "competition": "Spring Festival",
                "spots": "2",
            },
            follow_redirects=True,
        )

        page = response.data.decode()

        assert "Great-booking complete!" in page

        assert "Points available: <strong>11</strong>" in page


def test_booking_past_competition_returns_403():
    with app.test_client() as client:
        client.post("/login", data={"email": "john@simplylift.co"})

        response = client.get("/book/Fall Classic")
        page = response.data.decode()

        assert response.status_code == 403
        assert "You cannot book spots for past competitions." in page


def test_cannot_book_more_than_12_spots_returns_403():
    with app.test_client() as client:
        client.post(
            "/login",
            data={"email": "john@simplylift.co"},
            follow_redirects=True,
        )

        response = client.post(
            "/book",
            data={
                "competition": "Spring Festival",
                "spots": "13",
            },
        )

        page = response.data.decode()
       
        assert response.status_code == 403
        assert "You cannot book more than 12 spots for a competition." in page


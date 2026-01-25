from flask import Flask, flash, redirect, render_template, request, session, url_for
from datetime import datetime


from provider import get_clubs, get_competitions, save_competitions, save_clubs


app = Flask(__name__)
# You should change the secret key in production!
app.secret_key = "something_special"


@app.route("/")
def index():
    """Homepage"""
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    """Use the session object to store the club information across requests"""

    clubs = get_clubs()
    email = request.form["email"]

    if email not in [club["email"] for club in clubs]:
        return render_template(
            "error.html", message="Sorry, but we couldn't find an account with that email.",
            status_code=401
        ), 401

    club = [item for item in clubs if item["email"] == email][0]
    session["club"] = club

    return redirect(url_for("summary"))


@app.route("/summary")
def summary():
    """Custom "homepage" for logged in users"""

    club = session["club"]
    competitions = get_competitions()

    return render_template(
        "welcome.html",
        club=club,
        competitions=competitions)


@app.route("/book/<competition>")
def book(competition):
    """Book spots in a competition page"""
    club = session["club"]

    competitions = get_competitions()
    matching_comps = [
        comp for comp in competitions if comp["name"] == competition]

    found_competition = matching_comps[0]
    competition_date = datetime.strptime(
        found_competition["date"], "%Y-%m-%d %H:%M:%S")

    if competition_date < datetime.now():
        return render_template(
            "error.html",
            message="You cannot book spots for past competitions.",
            status_code=403
        ), 403

    if found_competition:
        return render_template(
            "booking.html",
            club=club,
            competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return redirect(url_for("summary"))


@app.route("/book", methods=["POST"])
def book_spots():
    """This page is only accessible through a POST request (form validation)"""
    club = session["club"]
    competitions = get_competitions()

    matching_comps = [
        comp for comp in competitions if comp["name"] == request.form["competition"]]

    competition = matching_comps[0]
    spots_required = int(request.form["spots"])

    if spots_required > int(club["points"]):
        return (
            render_template(
                "error.html",
                message="Not enough points available",
                status_code=403
            ),
            403,
        )

    if spots_required > 12:
        return (
            render_template(
                "error.html",
                message="You cannot book more than 12 spots for a competition.",
                status_code=403),
            403,
        )

    if spots_required > int(competition["spotsAvailable"]):
        flash("Not enough spots available!")
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions)

    competition["spotsAvailable"] = int(competition["spotsAvailable"]) - spots_required
    club["points"] = int(club["points"]) - spots_required

    clubs = get_clubs()
    for c in clubs:
        if c["email"] == club["email"]:
            c["points"] = club["points"]

    save_clubs(clubs)
    save_competitions(competitions)

    flash("Great-booking complete!")

    return render_template(
        "welcome.html",
        club=club,
        competitions=competitions)


@app.route("/clubs")
def clubs():
    clubs = get_clubs()
    return render_template("clubs.html", clubs=clubs)


@app.route("/logout")
def logout():
    """We delete session data in order to log the user out"""
    del session["club"]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

# gudlift-registration

This is a proof of concept (POC) project to demonstrate a lightweight competition booking platform. The goal is to keep things simple while allowing iterative improvements based on user feedback. This project uses Python v3.x+, Flask, virtual environments, pytest, and coverage.

1. **Clone the repository and navigate into it:**

   git clone <repo-url>  
   cd <root folder>

2. **Create a virtual environment:**

   python -m venv venv

3. **Activate the virtual environment:**

   - Windows (PowerShell): .\venv\Scripts\Activate.ps1  
   - Windows (cmd): venv\Scripts\activate  
   - macOS/Linux: source venv/bin/activate

4. **Install dependencies:**

   pip install -r requirements.txt

5. **Run the application:**

   python server.py

   The app will start and display a local link in the terminal (e.g., http://127.0.0.1:5000/) where you can access it in your browser.

6. **Understand the data:**

   The app uses JSON files in the `data/` folder:  

   - `competitions.json` – list of competitions with date, available spots, etc.  
   - `clubs.json` – list of clubs with name, email, and points. Use these emails to log in.

7. **Run Tests:**

   Tests, coverage, and reports can be generated with a single command:

   pytest --cov=. --cov-report=term --cov-report=html --junitxml=report.xml

   This will:
   - Display a coverage summary in the terminal  
   - Generate an HTML coverage report in `htmlcov/`  
   - Generate a JUnit-compatible test report as `report.xml`  

   Mock fixtures in `conftest.py` provide static data during tests, so modifying the JSON files will not affect tests unless the mocks are updated.

8. **Follow Naming Conventions:**

   Routes are lowercase with underscores, e.g., /book/<competition>. Templates match endpoints logically, e.g., index.html, booking.html, error.html. Static assets go in static/ (CSS, JS, images, gifs). JSON files live in data/ and use snake_case, e.g., clubs.json, competitions.json.

9. **External Resources:**

   - [Flask Documentation](https://flask.palletsprojects.com/)  
   - [pytest](https://docs.pytest.org/)  
   - [coverage.py](https://coverage.readthedocs.io/)  
   - [JSON Guide](https://www.tutorialspoint.com/json/json_quick_guide.htm)  

10. **Common Questions:**

   - How do I log in? Use an email listed in clubs.json.  
   - How are competitions ordered? By the order in competitions.json.  
   - Why is data static? This is a POC; data is mocked via JSON for simplicity.  
   - Can I book more spots than allowed? No, the system prevents booking more than 12 spots or more than your available points.  
   - What happens if I try to book a past competition? You will see an error page with HTTP status code 403.  
   - Why do some tests fail if I change JSON files? Tests use mocked data from conftest.py. Editing data/ alone won't affect them.  
   - How do I add a new club or competition? Update the JSON files in data/ and restart the server.

11. **Demo / Error Flows:**

   - Invalid Login: entering an email not in clubs.json shows an error page with HTTP 401.  
   - Booking More Points Than Available: attempting to book more spots than your club has shows an error page with HTTP 403.  
   - Booking More Than 12 Spots: the system enforces a 12-spot maximum, returning HTTP 403.

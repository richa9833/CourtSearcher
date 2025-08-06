# 🏛️ CourtSearcher - Delhi High Court Case Search App

CourtSearcher is a Flask-based web application that allows users to search Delhi High Court case details by entering the case type, year, and number. It scrapes publicly available court data, displays metadata, and provides direct PDF links if available. The app also maintains a searchable history using SQLite.

---

## Features

-  **Case Search Form**: Search cases using type, year, and number.
-  **PDF Access**: If available, download the full case judgment.
-  **Recent Searches**: View recent cases accessed.
-  **Responsive UI**: Clean and mobile-friendly layout using Bootstrap 5.
-  **Local Database**: Stores recent case data using SQLite.
-  **Client-Side Validation**: Prevents incorrect or empty submissions.
-  **Smart Loader**: Loading indicators enhance user experience.

---

##  Tech Stack

| Layer        | Technology                |
|--------------|---------------------------|
| Backend      | Python, Flask             |
| Frontend     | HTML5, Bootstrap 5, JavaScript |
| Styling      | CSS                       |
| Database     | SQLite                    |
| Web Scraping | `requests`, `BeautifulSoup` |
| Forms        | Flask-WTF                 |

---

## 📂 Project Structure

```plaintext
CourtSearcher/
│
├── app.py                  # Main Flask backend
├── court_cases.db          # SQLite database (optional)
├── requirements.txt        # Dependencies list
├── README.md               # Project documentation
│
├── templates/
│   ├── index.html          # Main search form UI
│   ├── results.html        # Display case results
│   └── recent_searches.html # Table of recent searches
│
└── static/
    ├── style.css           # Custom styles
    └── main.js             # JavaScript for interactivity

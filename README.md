Based on the repository structure and code visible in your screenshots, I've put together a professional `README.md` for your **ATS-Ranker** project. It follows the clean, structured style of your previous sneaker project but is tailored to this Django-based backend and its specific features.

---

# ATS-Ranker – AI-Powered Resume Screening Tool

**ATS-Ranker** is a web application designed to streamline the recruitment process. It uses natural language processing (NLP) to analyze resumes against job descriptions, providing a compatibility score to help recruiters identify the best candidates quickly.

## Features

* **Resume Upload:** Support for PDF resume uploads via a clean interface.
* **Job Description Matching:** Input specific job requirements to compare against candidate profiles.
* **AI Analysis:** Utilizes custom analyzer logic to calculate similarity scores between the resume text and job descriptions.
* **RESTful API:** Built with Django Rest Framework (DRF) for seamless frontend-backend communication.
* **Real-time Results:** Instant feedback on candidate suitability based on extracted keywords and technical skills.

## Tech Stack

* **Backend:** Python 3.11, Django 5.2.5
* **API Framework:** Django Rest Framework (DRF)
* **Frontend:** Django Templates (HTML/CSS), JavaScript
* **Database:** SQLite (Development)
* **Environment:** Virtualenv, Pip

## Project Structure

```text
ATS-Ranker/
├── backend/
│   ├── core/                  # Project configuration (settings, urls, wsgi)
│   │   ├── settings.py
│   │   └── urls.py
│   ├── resumechecker/         # Main application logic
│   │   ├── migrations/        # Database migrations
│   │   ├── templates/         # Frontend HTML templates
│   │   ├── analyzer.py        # NLP logic (text extraction & similarity)
│   │   ├── models.py          # JobDescription and ResumeScore models
│   │   ├── serializers.py     # DRF Serializers for data validation
│   │   └── views.py           # API views and request handling
│   ├── staticfiles/           # Collected static assets
│   ├── db.sqlite3             # Local database
│   └── manage.py              # Django management script
├── scripts.py                 # Utility scripts for environment setup
├── runtime.txt                # Specifies Python version (3.11.6)
├── Procfile                   # Deployment configuration
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation

```

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/inflictt/ATS-Ranker.git
cd ATS-Ranker

```

### 2. Set up a Virtual Environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Run Migrations

```bash
python backend/manage.py migrate

```

### 5. Start the Development Server

```bash
python backend/manage.py runserver

```

The application will be available at: **[http://127.0.0.1:8000](https://www.google.com/search?q=http://127.0.0.1:8000)**

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| **POST** | `/api/upload/` | Upload a resume and job ID to get a similarity score |
| **GET** | `/` | Home page / Dashboard |
| **GET** | `/api/results/` | Fetch previous ranking results |

## Contributors

* **Saksham Lodha**

---

Would you like me to add a specific section for the **NLP algorithms** you're using in `analyzer.py`, or perhaps a **Screenshots** section once you have the UI finalized?

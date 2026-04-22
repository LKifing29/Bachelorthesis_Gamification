# 🎮 Gamified Job Application Platform (Bachelor Thesis)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey.svg)
![HTML/CSS/JS](https://img.shields.io/badge/Frontend-HTML%2Fcss%2Fjs-orange.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)

## 📌 About The Project
This repository contains the practical implementation of my Bachelor Thesis: **"Optimizing the Application Process with Gamification"**. 

Traditional job applications can be tedious and static. This project reimagines the process as an engaging, RPG-like experience. Applicants create a "character profile" and allocate experience points in an interactive **Skill Tree**, turning self-assessment into a playful and motivating journey. The final output is an automatically generated, professional PDF resume.

## ✨ Key Features
* **👤 Character Creation:** Users enter their personal details and upload a profile picture via a secure, session-based form.
* **🌳 Interactive Skill Tree:** A dynamic, visually engaging node-system. Users can unlock categories, upvote/downvote skills (experience levels 1-3), and even add custom skills dynamically.
* **📄 Automated PDF Generation:** Compiles the user's "Character Stats" (CV, Skills, Hobbies, Tools) into a clean, recruiter-ready PDF using `reportlab`.
* **🔒 Secure Session Handling:** Each user session is isolated. Temporary files (like image uploads) are handled via UUIDs and automatically cleaned up after PDF generation.

## 🛠️ Tech Stack & Architecture
This project is built with a focus on clean code principles, separating business logic from routing (MVC pattern).

* **Backend:** Python, Flask
* **Frontend:** HTML5, CSS3 (Custom Properties/Variables), Vanilla JavaScript
* **PDF Engine:** ReportLab
* **Architecture Highlights:** * Object-Oriented Programming (OOP) via Python `@dataclass`.
  * Strict separation of concerns (`app.py` as a pure controller, logic handled in `models.py`, `pdf_service.py`, and `utils.py`).
  * Stateless routing & secure file handling.

## 📸 Screenshots
*(Note: Add screenshots of your application here to give recruiters a quick visual impression!)*

| Character Creation | Interactive Skill Tree |
| :---: | :---: |
| <img src="link_to_your_character_image.png" width="400"/> | <img src="link_to_your_skilltree_image.png" width="400"/> |

## 🚀 How to Run Locally

To get a local copy up and running, follow these simple steps:

1. **Clone the repository**
   ```bash
   git clone [https://github.com/LKifing29/Bachelorthesis_Gamification.git](https://github.com/LKifing29/Bachelorthesis_Gamification.git)
   ```

2. **Navigate into the directory**
   ```bash
   cd Bachelorthesis_Gamification
   ```

3. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in Browser**
   Navigate to `http://localhost:5000`

## 🎓 Learning Outcomes
This project bridged the gap between theoretical process optimization (Business Informatics) and practical software engineering. It heavily improved my understanding of DOM manipulation, backend-frontend communication via Fetch API, and refactoring a monolithic script into a scalable, enterprise-ready structure.
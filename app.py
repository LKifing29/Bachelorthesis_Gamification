import os
import json
from flask import Flask, render_template, request, session, redirect, url_for

from skills_data import create_skill_tree
from pdf_service import PDFGenerator
from utils import handle_image_upload

app = Flask(__name__)
app.secret_key = 'test'  # In production, use environment variables

base_dir = os.path.abspath(os.path.dirname(__file__))


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/character', methods=['GET'])
def character():
    """Renders the character creation form with existing session data if available."""
    return render_template('character.html',
                           first_name=session.get('first_name', ''),
                           last_name=session.get('last_name', ''),
                           birth_date=session.get('birth_date', ''),
                           country_of_birth=session.get('country_of_birth', ''),
                           phone=session.get('phone', ''),
                           address=session.get('address', ''),
                           email=session.get('email', ''),
                           gender=session.get('gender', ''),
                           image_name=session.get('image_name', ''))


@app.route('/perkmenu', methods=['GET', 'POST'])
def perkmenu():
    return render_template('perkmenu.html',
                           tool_data=session.get('tool_data', ''),
                           hobbys=session.get('hobbys', ''))


@app.route('/cv', methods=['GET', 'POST'])
def cv():
    return render_template('cv.html', resume_entries=session.get('resume', ''))


@app.route('/save_image_data', methods=['POST'])
def save_image_data():
    """Handles async image uploads and stores the reference in the session."""
    if 'image' not in request.files:
        return 'No file part', 400

    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400

    try:
        user_folder, filename = handle_image_upload(file, base_dir)
        session['user_folder'] = user_folder
        session['image_name'] = filename
        return 'Image uploaded successfully.', 200
    except Exception as e:
        print(f"Upload error: {e}")
        return 'Internal Server Error during upload', 500


@app.route('/process_cv', methods=['POST'])
def process_cv():
    """Processes and formats the submitted CV entries."""
    from_dates = request.form.getlist('from_date[]')
    to_dates = request.form.getlist('to_date[]')
    locations = request.form.getlist('location[]')
    descriptions = request.form.getlist('description[]')

    resume_entries = [
        {'from_date': f, 'to_date': t, 'location': l, 'description': d}
        for f, t, l, d in zip(from_dates, to_dates, locations, descriptions)
    ]

    session['resume'] = resume_entries
    return redirect(url_for('skilltree'))


@app.route('/process_character', methods=['POST'])
def process_character():
    """Stores character information in the current session."""
    session_keys = ['first_name', 'last_name', 'birth_date', 'country_of_birth',
                    'phone', 'address', 'email', 'gender']

    # Store form data dynamically
    for key in session_keys:
        # Mapping form names (e.g., firstName) to session keys (e.g., first_name)
        form_key = key.replace('_', '') if '_' in key and key != 'country_of_birth' else key
        if form_key == 'firstname': form_key = 'firstName'
        if form_key == 'lastname': form_key = 'lastName'
        if form_key == 'birthdate': form_key = 'birthDate'

        session[key] = request.form.get(form_key)

    return redirect(url_for('cv'))


@app.route('/process_skilltree', methods=['POST'])
def process_skilltree():
    """Parses and stores the selected skills."""
    skill_data = request.form.get('skill_data')
    session['skills'] = json.loads(skill_data) if skill_data else []
    return redirect(url_for('perkmenu'))


@app.route('/endscreen', methods=['GET', 'POST'])
def endscreen():
    return render_template('endscreen.html')


@app.route('/submit_perkmenu', methods=['POST'])
def submit_perkmenu():
    session['tool_data'] = request.form.get('learned_programs')
    session['hobbys'] = request.form.get('hobbys')
    return redirect(url_for('endscreen'))


@app.route('/create_pdf')
def create_pdf():
    """Generates the final PDF based on session data and clears the session."""
    pdf_gen = PDFGenerator(dict(session), base_dir)
    response = pdf_gen.generate()

    session.clear()
    return response


@app.route('/skilltree', methods=['GET', 'POST'])
def skilltree():
    """Renders the interactive skill tree."""
    skill_tree = create_skill_tree()

    if session.get('skills'):
        stored_skills = session.get('skills')
        new_skill_tree_data = skill_tree.get_actual_skill_tree_data(stored_skills)
        new_connections_data = skill_tree.draw_new_connections(stored_skills)
        return render_template('skilltree.html',
                               skill_tree_data=new_skill_tree_data,
                               connections_data=new_connections_data)

    skill_tree_data = skill_tree.get_skill_tree_data()
    connections_data = skill_tree.draw_connections()
    activated_skills = [skill.name for skill in skill_tree.skills if skill.is_active]

    return render_template('skilltree.html',
                           skill_tree_data=skill_tree_data,
                           connections_data=connections_data,
                           activated_skills=activated_skills)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

import os
import math

app = Flask(__name__)
app.secret_key = 'test'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Skill:
    def __init__(self, name, id=None, category=None, parent_id=None, position=(0, 0), is_start_node=False, is_custom_skill=False, is_category = False ):
        self.name = name
        self.id = id
        self.category = category
        self.parent_id = parent_id
        self.position = (0, 0)
        self.is_active = False
        self.children = []
        self.position = position
        self.is_start_node = is_start_node
        self.is_custom_skill = is_custom_skill
        self.experience_level = 0
        self.is_category = is_category

        if category:
            category.add_child(self)

    def add_child(self, child):
        self.children.append(child)

    def activate(self):
        if not self.is_start_node and (not self.category or self.category.is_active):
            self.is_active = True

    def deactivate(self):
        if not self.is_start_node:
            self.is_active = False
            for child in self.children:
                child.deactivate()

    def toggle_state(self):
        print("Befinden uns in toggle_state")
        if not self.is_active:
            self.is_active = True
            self.activate()
        else:
            self.is_active = False
            self.deactivate()


class SkillTree:
    def __init__(self):
        self.skills = []
        self.active_skills = []

    def add_skill(self, skill):
        self.skills.append(skill)

    def get_skill_tree_data(self):
        data = []
        for skill in self.skills:
            category_name = skill.category.name if skill.category else None
            parent_id = skill.category.id if skill.category else None
            data.append({
                'name': skill.name,
                'position': skill.position,
                'id': skill.id,
                'parent_id': parent_id,
                'category': category_name,
                'is_start_node': skill.is_start_node,
                'is_custom_skill': skill.is_custom_skill,
                'is_active': skill.is_active,
                'experience_level': skill.experience_level,
                'is_category': skill.is_category
            })
        return data

    def get_skill_by_id(self, skill_id):
        for skill in self.skills:
            if skill.id == skill_id:
                return skill
        return None

    def calculate_angle(self, x1, y1, x2, y2):
        angle = math.atan2(y2 - y1, x2 - x1)
        return angle - math.pi / 2

    def draw_connections(self):
        connections = []
        for skill in self.skills:
            if skill.category:
                x1 = skill.category.position[0]
                y1 = skill.category.position[1]
                x2 = skill.position[0]
                y2 = skill.position[1]

                angle = self.calculate_angle(x1, y1, x2, y2)
                angle += math.pi
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                category_name = skill.category.name if skill.category else None
                connections.append({
                    'x1': 45,
                    'y1': 45,
                    'length': distance,
                    'angle': angle,
                    'category': category_name,
                    'skill_name': skill.name
                })

        return connections

    @app.route('/toggle_skill/<skill_name>', methods=['POST'])
    def toggle_skill(skill_id):
        skill = skill_tree.get_skill_by_id(skill_id)

        if skill:
            skill.toggle_state()
            return jsonify({'success': True, 'message': f'Skill {skill_id} toggled successfully'})
        else:
            return jsonify({'success': False, 'message': f'Skill {skill_id} not found'})

def create_skill_tree():
    skill_tree = SkillTree()

    # Create skills
    # <editor-fold desc="Create skills">
    central_skill = Skill('Skills', 1, position=(750, 500), is_start_node=True)
    leadership_skill = Skill('Leadership', 2, central_skill, 1, position=(200, 200),
                             is_category=True)
    design_skill = Skill('Design', 3, central_skill,  1, position=(200, 950),
                         is_category=True)
    programming_skill = Skill('Programming', 4, central_skill, 1, position=(1200, 200),
                              is_category=True)
    methodological_skill = Skill('Methodological competence', 5, central_skill, 1, position=(200, 1300),
                                 is_category=True)
    social_skill = Skill('Social skills', 6, central_skill, 1, position=(1200, 1800),
                                       is_category=True)
    others_skill = Skill('Others', 7, central_skill, 1, position=(1200, 950), is_category=True)
    communication_skill = Skill('Communication competence', 8, central_skill, 1, position=(750, 175),
                                is_category=True)
    project_management_skill = Skill('Project management', 9, central_skill, 1, position=(200, 575),
                                is_category=True)
    personal_skill = Skill('Personal skills', 10, central_skill, 1, position=(1200, 575),
                                is_category=True)

    photoshop_skill = Skill('Photoshop', 31, design_skill, 3, position=(425, 300))
    graphics_skill = Skill('Graphics', 32, design_skill, 3, position=(575, 300))
    java_skill = Skill('Java', 33, programming_skill, 4, position=(1300, 75))
    python_skill = Skill('Python', 34, programming_skill, 4, position=(1425, 200))
    csharp_skill = Skill('C#', 35, programming_skill, 4, position=(1300, 325))
    javascript_skill = Skill('JavaScript', 36, programming_skill, 4, position=(1400, 100))
    php_skill = Skill('PHP', 37, programming_skill, 4, position=(1400, 300))
    c_cplusplus_skill = Skill('C/C++', 38, programming_skill, 4, position=(1200, 300))
    kotlin_skill = Skill('Kotlin', 39, programming_skill, 4, position=(1200, 100))
    delegation_skill = Skill('Delegation', 40, leadership_skill, 2, position=(300, 100))
    listening_skill = Skill('Active listening', 41, communication_skill, 8)
    integrity_skill = Skill('Integrity', 42, leadership_skill, 2, position=(100, 100))
    flexibility_skill = Skill('Flexibility', 43, leadership_skill, 2, position=(300, 300))
    criticism_skill = Skill('Express criticism', 44, leadership_skill, 2, position=(100, 300))
    time_management_skill = Skill('Time management', 45, project_management_skill, 9)
    prioritization_skill = Skill('Prioritization', 46, methodological_skill, 5)
    negotiation_technique_skill = Skill('Negotiation technique', 47, methodological_skill, 5)
    organization_skill = Skill('Organization', 48, methodological_skill, 5)
    teamwork_skill = Skill('Teamwork', 49, social_skill, 6)
    empathy_skill = Skill('Empathy', 50, social_skill, 6)
    service_skill = Skill('Service orientation', 51, social_skill, 6)
    conflict_management_skill = Skill('Conflict management', 52, social_skill, 6)
    help_skill = Skill('Willingness to help', 53, social_skill, 6)
    communication_with_others_skill = Skill('Communication', 54, communication_skill, 8)
    inspire_skill = Skill('Inspire others', 55, communication_skill, 8)
    change_willingness_skill = Skill('Willingness to change', 57, leadership_skill, 2)
    trust_skill = Skill('Trust', 58, leadership_skill, 2)
    trust_skill = Skill('Trust', 59, leadership_skill, 2)
    trust_skill = Skill('Trust', 60, leadership_skill, 2)

    problem_solving_skill = Skill('Problem solving', 61, project_management_skill, 9)
    analytic_thinking_skill = Skill('Analytic thinking', 62, project_management_skill, 9)
    building_teams_skill = Skill('Building teams', 63, project_management_skill, 9)
    lateral_leading_skill = Skill('Lateral leading', 64, project_management_skill, 9)







    # </editor-fold>

    # Add skills
    # <editor-fold desc="Add skills to the tree">
    skill_tree.add_skill(change_willingness_skill)
    skill_tree.add_skill(trust_skill)
    skill_tree.add_skill(problem_solving_skill)
    skill_tree.add_skill(analytic_thinking_skill)
    skill_tree.add_skill(building_teams_skill)
    skill_tree.add_skill(lateral_leading_skill)
    skill_tree.add_skill(listening_skill)
    skill_tree.add_skill(communication_with_others_skill)
    skill_tree.add_skill(inspire_skill)
    skill_tree.add_skill(personal_skill)
    skill_tree.add_skill(project_management_skill)
    skill_tree.add_skill(criticism_skill)
    skill_tree.add_skill(prioritization_skill)
    skill_tree.add_skill(negotiation_technique_skill)
    skill_tree.add_skill(organization_skill)
    skill_tree.add_skill(teamwork_skill)
    skill_tree.add_skill(service_skill)
    skill_tree.add_skill(help_skill)
    skill_tree.add_skill(central_skill)
    skill_tree.add_skill(leadership_skill)
    skill_tree.add_skill(design_skill)
    skill_tree.add_skill(programming_skill)
    skill_tree.add_skill(communication_skill)
    skill_tree.add_skill(photoshop_skill)
    skill_tree.add_skill(graphics_skill)
    skill_tree.add_skill(java_skill)
    skill_tree.add_skill(python_skill)
    skill_tree.add_skill(csharp_skill)
    skill_tree.add_skill(javascript_skill)
    skill_tree.add_skill(php_skill)
    skill_tree.add_skill(c_cplusplus_skill)
    skill_tree.add_skill(kotlin_skill)
    skill_tree.add_skill(methodological_skill)
    skill_tree.add_skill(social_skill)
    skill_tree.add_skill(delegation_skill)
    skill_tree.add_skill(empathy_skill)
    skill_tree.add_skill(integrity_skill)
    skill_tree.add_skill(flexibility_skill)
    skill_tree.add_skill(conflict_management_skill)
    skill_tree.add_skill(time_management_skill)
    skill_tree.add_skill(others_skill)
    # </editor-fold>


    return skill_tree


@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template('index.html')


@app.route('/data/character', methods=['GET'])
def character():
    # Überprüfe, ob die Session-Variablen vorhanden sind
    first_name = session.get('first_name')
    last_name = session.get('last_name')
    age = session.get('age')
    origin = session.get('origin')
    knowledge = session.get('knowledge')
    phone_number = session.get('phoneNumber')
    address = session.get('address')
    email = session.get('email')
    gender = session.get('gender')
    image_data = session.get('image_data')

    # Gehe sicher, dass "None" nicht in das Template eingesetzt wird
    return render_template('character.html', first_name=first_name or '',
                           last_name=last_name or '', age=age or '', origin=origin or '',
                           knowledge=knowledge or '', phone_number=phone_number or '',
                           address=address or '', email=email or '', gender=gender or '',
                           image_data=image_data or '')

@app.route('/data/perkmenu', methods=['GET', 'POST'])
def perkmenu():
    return render_template('perkmenu.html')

@app.route('/save_image_data', methods=['POST'])
def save_image_data():
    image_data = request.json.get('image_data')
    session['image_data'] = image_data
    return 'Bild erfolgreich gespeichert.', 200

@app.route('/process_character', methods=['POST'])
def process_character():
    print("test")
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    age = request.form.get('age')
    origin = request.form.get('origin')
    knowledge = request.form.get('knowledge')
    phone_number = request.form.get('phoneNumber')
    address = request.form.get('address')
    email = request.form.get('email')
    gender = request.form.get('gender')
    # Speichere die Daten in Session-Variablen
    session['first_name'] = first_name
    session['last_name'] = last_name
    session['age'] = age
    session['origin'] = origin
    session['knowledge'] = knowledge
    session['phone_number'] = phone_number
    session['address'] = address
    session['email'] = email
    session['gender'] = gender
    return redirect(url_for('skilltree'))

@app.route('/data/skilltree', methods=['GET', 'POST'])
def skilltree():
    global skill_tree
    skill_tree = create_skill_tree()
    skill_tree_data = skill_tree.get_skill_tree_data()
    connections_data = skill_tree.draw_connections()

    activated_skills = [skill.name for skill in skill_tree.skills if skill.is_active]
    return render_template('skilltree.html', skill_tree_data=skill_tree_data, connections_data=connections_data,
                           activated_skills=activated_skills)

@app.before_request
def clear_session():
    if not request.path.startswith('/data') | request.path.startswith('/static'):
        session.clear()

if __name__ == '__main__':
    app.run(debug=True)

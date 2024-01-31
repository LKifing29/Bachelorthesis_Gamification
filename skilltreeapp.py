from flask import Flask, render_template, request, jsonify
import pygame
import math

import Skill

app = Flask(__name__)

class Skill:
    def __init__(self, name, id=None, category=None, parent_id=None, position=(0, 0), is_start_node=False, is_custom_skill=False, is_category = False ):
        self.name = name
        self.id = id
        self.category = category
        self.parent_id = parent_id
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
    central_skill = Skill('Skills', 1, position=(750, 400), is_start_node=True)
    leadership_skill = Skill('Leadership', 2, central_skill, 1, position=(200, 200), is_category=True)
    design_skill = Skill('Design', 3, central_skill,  1, position=(375, 550), is_category=True)
    programming_skill = Skill('Programming', 4, central_skill, 1, position=(1300, 200), is_category=True)
    communication_skill = Skill('Communication', 5, leadership_skill, 2,  position=(200, 325))
    photoshop_skill = Skill('Photoshop', 6, design_skill, 3, position=(425, 300))
    graphics_skill = Skill('Graphics', 7, design_skill, 3, position=(575, 300))
    java_skill = Skill('Java', 8, programming_skill, 4, position=(1300, 75))
    python_skill = Skill('Python', 9, programming_skill, 4, position=(1425, 200))
    python2_skill = Skill('Python2', 9, programming_skill, 4, position=(1175, 200))
    python3_skill = Skill('Python3', 9, programming_skill, 4, position=(1300, 325))
    csharp_skill = Skill('C#', 10, programming_skill, 4, position=(1300, 325))
    javascript_skill = Skill('JavaScript', 11, programming_skill, 4, position=(1400, 100))
    php_skill = Skill('PHP', 12, programming_skill, 4, position=(1400, 300))
    c_cplusplus_skill = Skill('C/C++', 13, programming_skill, 4, position=(1200, 300))
    kotlin_skill = Skill('Kotlin', 14, programming_skill, 4, position=(1200, 100))
    knowledge_management_skill = Skill('Knowledge management', 15, central_skill, 1, position=(750, 150), is_category=True)
    delegation_skill = Skill('Delegation', 19, leadership_skill, 2, position=(300, 100))
    empathy_skill = Skill('Empathy', 20, leadership_skill, 2, position=(200, 75))
    integrity_skill = Skill('Integrity', 21, leadership_skill, 2, position=(100, 100))
    creativity_skill = Skill('Creativity', 22, leadership_skill, 2, position=(325, 200))
    flexibility_skill = Skill('Flexibility', 23, leadership_skill, 2, position=(300, 300))
    conflict_management_skill = Skill('Conflict management', 24, leadership_skill, 2, position=(100, 300))
    time_management_skill = Skill('Time management', 25, leadership_skill, 2, position=(75, 200))
    others_skill = Skill('Others', 26, central_skill, 1, position=(1125, 550), is_category=True)



    #custom_skill1 = Skill('Enter own skill', 16, central_skill, 1, position=(1100, 450), is_custom_skill=True)
    #custom_skill2 = Skill('Enter own skill', 17, custom_skill1, 16, position=(1100, 575), is_custom_skill=True)
    #custom_skill3 = Skill('Enter own skill', 18, leadership_skill, 2, position=(50, 350), is_custom_skill=True)
    #custom_skill4 = Skill('Enter own skill', 27, custom_skill3, 18, position=(50, 475), is_custom_skill=True)
    #custom_skill5 = Skill('Enter own skill', 28, custom_skill4, 27, position=(50, 600), is_custom_skill=True)
    #custom_skill6 = Skill('Enter own skill', 29, custom_skill5, 28, position=(50, 725), is_custom_skill=True)

    # </editor-fold>

    # Add skills
    # <editor-fold desc="Add skills to the tree">
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
    skill_tree.add_skill(knowledge_management_skill)
    #skill_tree.add_skill(custom_skill1)
    #skill_tree.add_skill(custom_skill2)
    skill_tree.add_skill(delegation_skill)
    skill_tree.add_skill(empathy_skill)
    skill_tree.add_skill(integrity_skill)
    skill_tree.add_skill(flexibility_skill)
    skill_tree.add_skill(conflict_management_skill)
    skill_tree.add_skill(time_management_skill)
    skill_tree.add_skill(others_skill)
    #skill_tree.add_skill(custom_skill3)
    #skill_tree.add_skill(custom_skill4)
    #skill_tree.add_skill(custom_skill5)
    #skill_tree.add_skill(custom_skill6)
    skill_tree.add_skill(python2_skill)
    skill_tree.add_skill(python3_skill)
    # </editor-fold>


    return skill_tree


@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template('startingpage.html')


@app.route('/character')
def character():
    return render_template('character.html')

@app.route('/skilltree.html')
def skilltree():
    global skill_tree
    skill_tree = create_skill_tree()
    skill_tree_data = skill_tree.get_skill_tree_data()
    connections_data = skill_tree.draw_connections()

    activated_skills = [skill.name for skill in skill_tree.skills if skill.is_active]
    return render_template('skilltree.html', skill_tree_data=skill_tree_data, connections_data=connections_data,
                           activated_skills=activated_skills)



if __name__ == '__main__':
    app.run(debug=True)

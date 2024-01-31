from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

skills = [
    {"id": 1, "name": "Skill 1", "disabled": False},
    {"id": 2, "name": "Skill 2", "parent_id": 1, "disabled": False},
    {"id": 3, "name": "Skill 2.1", "parent_id": 2, "disabled": False},
    {"id": 4, "name": "Skill 2.2", "parent_id": 2, "disabled": False},
    {"id": 5, "name": "Skill 3", "parent_id": None, "disabled": False},
]

@app.route('/')
def index():
    return render_template('index_ajax.html', skills=skills)

@app.route('/toggle_skill/<int:skill_id>', methods=['POST'])
def toggle_skill(skill_id):
    skill = next((s for s in skills if s['id'] == skill_id), None)
    if skill:
        skill['disabled'] = not skill.get('disabled', False)
        return jsonify({'success': True, 'disabled': skill['disabled']})
    return jsonify({'success': False, 'error': 'Skill not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

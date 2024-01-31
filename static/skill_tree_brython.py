# static/skill_tree_brython.py
skill_data = [
    {"id": 1, "name": "Skill 1", "dependencies": []},
    {"id": 2, "name": "Skill 2", "dependencies": [1]},
    {"id": 3, "name": "Skill 3", "dependencies": [2]},
    # Weitere Skills hier hinzufügen...
]

def render_skill_tree(skill_data):
    for skill in skill_data:
        print(skill['name'])
        if skill['dependencies']:
            for dependency_id in skill['dependencies']:
                dependency = next(s for s in skill_data if s['id'] == dependency_id)
                print(f" - {dependency['name']}")

print("Hello world!")
render_skill_tree(skill_data)

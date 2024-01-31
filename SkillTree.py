

class SkillTree(object):

    def __init__(self):
        self.hard_skills = []
        self.soft_skills = []

    def add_skill(self, skill):
        if skill.category == 1:
            self.hard_skills.append(skill)
        elif skill.category == 2:
            self.soft_skills.append(skill)

    def delete_skill(self, skill):
        if skill.category == 1:
            self.hard_skills.remove(skill)
        elif skill.category == 2:
            self.soft_skills.remove(skill)

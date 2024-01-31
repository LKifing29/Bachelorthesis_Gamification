import SkillCategory


class Skill(object):

    def __init__(self, category, name):
        self.category = category
        self.skill_name = name


    def get_skill_name(self):
        return self.skill_name

    def set_skill_name(self, skill_name):
        skill_name = skill_name
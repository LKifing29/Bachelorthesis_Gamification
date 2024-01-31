from SkillTree import SkillTree


class Controller:

    def __init__(self):
        self.skill_tree = SkillTree()
        self.predefined_hard_skills = []
        self.predefined_soft_skills = []

    def create_hard_skill_list(self):
        self.hard_skills = []

    def create_soft_skills_list(self):
        self.soft_skills = []
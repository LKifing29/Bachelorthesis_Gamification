import pygame
import sys
import math



class Skill:
    def __init__(self, name, parent=None, position=(0, 0), is_start_node=False, is_custom_skill=False):
        self.name = name
        self.parent = parent
        self.is_active = is_start_node
        self.children = []
        self.position = position
        self.is_start_node = is_start_node
        self.is_custom_skill = is_custom_skill

        if parent:
            parent.add_child(self)

    def add_child(self, child):
        self.children.append(child)

    def activate(self):
        if not self.is_start_node and (not self.parent or self.parent.is_active):
            self.is_active = True

    def deactivate(self):
        if not self.is_start_node:
            self.is_active = False
            for child in self.children:
                child.deactivate()


class SkillTree:
    def __init__(self):
        self.skills = []
        self.active_skills = []

    def add_skill(self, skill):

        self.skills.append(skill)

    def draw(self, screen):
        font = pygame.font.Font(None, 16)

        for skill in self.skills:
            x, y = skill.position
            radius = 45
            color = (0, 255, 0) if skill.is_start_node else (173, 216, 230) if skill.is_active else (169, 169, 169)

            pygame.draw.circle(screen, color, (x, y), radius)

            # Draw text with line breaks
            lines = skill.name.splitlines()
            total_lines = len(lines)
            for i, line in enumerate(lines):
                text = font.render(line, True, (0, 0, 0))
                text_rect = text.get_rect(
                    center=(x, y - (total_lines - 1) * 10 + i * 20))  # Vertically center each line
                screen.blit(text, text_rect)

            # Draw line from the edge of the circle
            if skill.parent and not skill.is_start_node:
                parent_x, parent_y = skill.parent.position

                delta_x = x - parent_x
                delta_y = y - parent_y

                distance = math.hypot(delta_x, delta_y)
                unit_x = delta_x / distance
                unit_y = delta_y / distance

                line_start = (parent_x + int(radius * unit_x), parent_y + int(radius * unit_y))
                line_end = (x - int(radius * unit_x), y - int(radius * unit_y))

                pygame.draw.line(screen, (0, 0, 0), line_start, line_end, 2)


def create_skill_tree():
    skill_tree = SkillTree()

    # Central skill (start node)
    central_skill = Skill('Skills', is_start_node=True, position=(600, 50))

    # Child skills
    hr_skill = Skill('Human\nResources', central_skill, position=(100, 200))
    design_skill = Skill('Design', central_skill, position=(300, 200))
    programming_skill = Skill('Programming', central_skill, position=(1000, 200))
    communication_skill = Skill('Communication', hr_skill, position=(100, 300))
    photoshop_skill = Skill('Photoshop', design_skill, position=(225, 300))
    graphics_skill = Skill('Graphics', design_skill, position=(375, 300))
    java_skill = Skill('Java', programming_skill, position=(1000, 75))
    python_skill = Skill('Python', programming_skill, position=(1125, 200))
    csharp_skill = Skill('C#', programming_skill, position=(1000, 325))
    javascript_skill = Skill('JavaScript', programming_skill, position=(1100, 100))
    php_skill = Skill('PHP', programming_skill, position=(1100, 300))
    c_cplusplus_skill = Skill('C/C++', programming_skill, position=(900, 300))
    kotlin_skill = Skill('Kotlin', programming_skill, position=(900, 100))
    #neuer_skill = Skill('Neues', programming_skill, position=(875, 200))
    knowledge_management_skill = Skill('Knowledge \nmanagement', central_skill, position=(550, 200))
    custom_skill1 = Skill('Enter own skill', central_skill, position=(900, 450), is_custom_skill=True)
    custom_skill2 = Skill('Enter own skill', custom_skill1, position=(900, 575), is_custom_skill=True)

    skill_tree.add_skill(central_skill)
    skill_tree.add_skill(hr_skill)
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
    #skill_tree.add_skill(neuer_skill)
    skill_tree.add_skill(knowledge_management_skill)
    skill_tree.add_skill(custom_skill1)
    skill_tree.add_skill(custom_skill2)

    return skill_tree


def main():
    pygame.init()

    width, height = 1200, 900
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Skill Tree')

    skill_tree = create_skill_tree()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for skill in skill_tree.skills:
                    if pygame.math.Vector2(mouse_x - skill.position[0], mouse_y - skill.position[1]).length() <= 50:
                        if skill.is_active:
                            if not skill.is_start_node:
                                for child in skill.children:
                                    if child.is_active:
                                        skill_tree.active_skills.remove(child)
                                skill.deactivate()
                                skill_tree.active_skills.remove(skill)
                        else:
                            skill.activate()
                            if skill.is_active:
                                skill_tree.active_skills.append(skill)
                        print("This are all your selected skills:")
                        for skill in skill_tree.active_skills:
                            print("-" + skill.name)

        screen.fill((255, 255, 255))
        skill_tree.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()

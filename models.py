import math
from dataclasses import dataclass, field
from typing import Tuple, List, Optional, Dict, Any


@dataclass
class Skill:
    """Represents a single node in the skill tree."""
    name: str
    id: Optional[int] = None
    category: Optional['Skill'] = None
    parent_id: Optional[int] = None
    position: Tuple[int, int] = (0, 0)
    is_start_node: bool = False
    is_custom_skill: bool = False
    is_category: bool = False
    is_active: bool = False
    experience_level: int = 0
    children: List['Skill'] = field(default_factory=list)


class SkillTree:
    """Manages the logic and data representation of the entire skill tree."""

    def __init__(self):
        self.skills: List[Skill] = []
        self.active_skills: List[Skill] = []

    def add_skill(self, skill: Skill):
        self.skills.append(skill)

    def get_skill_tree_data(self) -> List[Dict[str, Any]]:
        """Provides all necessary data to render the skill tree in the frontend."""
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

    def get_actual_skill_tree_data(self, stored_skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Restores the actual skill tree state based on current session data."""
        for skill in self.skills:
            category_name = skill.category.name if skill.category else None
            parent_id = skill.category.id if skill.category else None

            if skill.is_start_node or skill.is_category:
                stored_skills.append({
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
        return stored_skills

    def calculate_angle(self, x1: int, y1: int, x2: int, y2: int) -> float:
        """Calculates the angle for the connecting line between two nodes."""
        angle = math.atan2(y2 - y1, x2 - x1)
        return angle - math.pi / 2

    def draw_connections(self) -> List[Dict[str, Any]]:
        """Generates the connection lines between nodes for the initial state."""
        connections = []
        for skill in self.skills:
            if skill.category:
                x1, y1 = skill.category.position
                x2, y2 = skill.position

                angle = self.calculate_angle(x1, y1, x2, y2) + math.pi
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

    def draw_new_connections(self, stored_skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generates the connection lines between nodes based on session data."""
        connections = []
        for skill in stored_skills:
            if skill.get('category'):
                current_category = next((s for s in self.skills if s.name == skill['category']), None)

                if current_category:
                    x1, y1 = current_category.position
                    position_0 = int(str(skill['position'][0]).replace("px", ""))
                    position_1 = int(str(skill['position'][1]).replace("px", ""))
                    x2, y2 = position_0, position_1

                    angle = self.calculate_angle(x1, y1, x2, y2) + math.pi
                    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

                    connections.append({
                        'x1': 45,
                        'y1': 45,
                        'length': distance,
                        'angle': angle,
                        'category': current_category.name,
                        'skill_name': skill['name']
                    })
        return connections
import io
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from flask import make_response


class PDFGenerator:
    """Handles the generation of the final application PDF document."""

    def __init__(self, session_data: Dict[str, Any], base_dir: str):
        self.session = session_data
        self.base_dir = Path(base_dir)
        self.buffer = io.BytesIO()
        self.c = canvas.Canvas(self.buffer, pagesize=letter)
        self.x = 100
        self.y = 750
        self.line_height = 14

    def check_page_break(self, margin_bottom: int = 50):
        """Checks if a page break is required and executes it."""
        if self.y < margin_bottom:
            self.c.showPage()
            self.y = 750

    def wrap_text(self, text: str, max_width: int) -> list:
        """Wraps text to fit within the specified PDF width constraints."""
        lines = []
        line = ''
        words = text.split()
        for word in words:
            if self.c.stringWidth(line + word, 'Helvetica', 12) < max_width:
                line += (', ' + word) if line else word
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines

    def draw_personal_info(self):
        self.c.setFont('Helvetica-Bold', 16)
        self.c.drawString(self.x, self.y, "Applicant Information")
        self.y -= 20

        info_fields = [
            ("Name:", f"{self.session.get('first_name', '')} {self.session.get('last_name', '')}"),
            ("Date and location of birth:",
             f"{self.session.get('birth_date', '')} {self.session.get('country_of_birth', '')}"),
            ("Phone:", self.session.get('phone', '')),
            ("Address:", self.session.get('address', '')),
            ("Email:", self.session.get('email', '')),
            ("Gender:", self.session.get('gender', ''))
        ]

        for label, value in info_fields:
            self.c.setFont("Helvetica-Bold", 12)
            self.c.drawString(self.x, self.y, label)
            self.c.setFont('Helvetica', 12)
            if value:
                self.c.drawString(self.x + 170, self.y, value)
            self.y -= 20

        self.y -= 20

    def draw_profile_image(self):
        filename = self.session.get('image_name')
        user_folder = self.session.get('user_folder')

        if filename and user_folder:
            image_path = self.base_dir / "static" / "temp_uploads" / user_folder / filename
            if image_path.exists():
                self.c.drawImage(str(image_path), 450, 600, width=1.7 * inch, height=2.25 * inch)

    def draw_cv(self):
        self.c.setFont('Helvetica-Bold', 16)
        self.c.drawString(self.x, self.y, "Curriculum vitae")
        self.y -= 20

        table_headers = ["From", "To", "Location", "Description"]
        col_width = 80

        self.c.setFont('Helvetica-Bold', 12)
        for i, header in enumerate(table_headers):
            self.c.drawString(self.x + i * col_width, self.y, header)

        self.c.setFont('Helvetica', 12)
        resume_entries = self.session.get('resume', [])

        for entry in resume_entries:
            if entry.get('description'):
                self.y -= 20
                self.c.drawString(self.x, self.y, entry.get('from_date', ''))
                self.c.drawString(self.x + col_width, self.y, entry.get('to_date', ''))
                self.c.drawString(self.x + 2 * col_width, self.y, entry.get('location', ''))
                self.c.drawString(self.x + 3 * col_width, self.y, entry.get('description', ''))
                self.check_page_break()
        self.y -= 40

    def draw_skills(self):
        self.c.setFont('Helvetica-Bold', 16)
        self.c.drawString(self.x, self.y, "Skilltree Information")
        self.y -= 20
        self.c.setFont('Helvetica', 12)

        skills = self.session.get('skills', [])
        for skill in skills:
            if skill.get('is_active'):
                self.c.drawString(self.x, self.y, f"Skillname: {skill.get('name')}")
                self.c.drawString(self.x + 300, self.y, f"Experience Level: {skill.get('experience_level')}/3")
                self.y -= self.line_height
                self.check_page_break()

    def draw_additional_info(self, title: str, session_key: str):
        self.y -= 16
        self.check_page_break()
        self.c.setFont('Helvetica-Bold', 16)
        self.c.drawString(self.x, self.y, title)
        self.c.setFont('Helvetica', 12)
        self.y -= self.line_height

        data = self.session.get(session_key, "")
        if data:
            for line in self.wrap_text(data, max_width=400):
                self.c.drawString(self.x + 20, self.y, line)
                self.y -= self.line_height
                self.check_page_break()

    def cleanup_temp_files(self):
        """Removes the user's temporary upload directory to free up space."""
        user_folder = self.session.get('user_folder')
        if user_folder:
            folder_path = self.base_dir / "static" / "temp_uploads" / user_folder
            try:
                if folder_path.exists() and folder_path.is_dir():
                    shutil.rmtree(folder_path)
            except Exception as e:
                print(f"Error deleting folder {folder_path}: {e}")

    def generate(self):
        """Executes all drawing steps and returns the formatted Flask response."""
        self.draw_personal_info()
        self.draw_profile_image()
        self.draw_cv()
        self.draw_skills()
        self.draw_additional_info("Learned Tools", "tool_data")
        self.draw_additional_info("Hobbys", "hobbys")

        self.c.save()
        self.cleanup_temp_files()

        self.buffer.seek(0)
        response = make_response(self.buffer.read())

        first_name_l = self.session.get("first_name", "unknown").lower()
        last_name_l = self.session.get("last_name", "applicant").lower()
        current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'application_{first_name_l}_{last_name_l}_{current_datetime}.pdf'

        response.mimetype = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename={filename}'

        return response
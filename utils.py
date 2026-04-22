import uuid
from pathlib import Path
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


def handle_image_upload(file: FileStorage, base_dir: str) -> tuple[str, str]:
    """
    Saves an uploaded image to a unique, temporary directory.
    Returns the unique folder name and the secure filename.
    """
    filename = secure_filename(file.filename)
    user_folder_name = str(uuid.uuid4())

    upload_dir = Path(base_dir) / 'static' / 'temp_uploads' / user_folder_name
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / filename
    file.save(str(file_path))

    return user_folder_name, filename
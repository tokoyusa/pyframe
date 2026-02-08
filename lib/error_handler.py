import os


class FileError(Exception):
    pass


class ProcessingError(Exception):
    pass


def validate_file_exists(path):
    if not os.path.exists(path):
        raise FileError(f"File not found: {path}")
    return True


def validate_file_extension(path, allowed_extensions):
    ext = os.path.splitext(path)[1].lower()
    if ext not in allowed_extensions:
        raise FileError(f"Unsupported file type: {ext}. Allowed: {', '.join(allowed_extensions)}")
    return ext


def validate_folder(path, create=False):
    if not os.path.exists(path):
        if create:
            os.makedirs(path, exist_ok=True)
        else:
            raise FileError(f"Folder not found: {path}")
    return True


def safe_read_image(path):
    validate_file_exists(path)
    try:
        with open(path, 'rb') as f:
            return f.read()
    except Exception as e:
        raise ProcessingError(f"Failed to read {path}: {str(e)}")


def safe_cleanup(path):
    try:
        if os.path.exists(path):
            if os.path.isdir(path):
                import shutil
                shutil.rmtree(path)
            else:
                os.remove(path)
    except Exception:
        pass

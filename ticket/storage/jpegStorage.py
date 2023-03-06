
import os
from pathlib import Path
from datetime import datetime

from django.conf import settings
from django.core.files import File
from django.core.files import locks
from django.utils.timezone import utc
from django.core.files.storage import FileSystemStorage


def iso_date_prefix(_, file_name_ext: str) -> str:
    
    """Get current date in ISO8601 format [year-month-day] as string"""
    now = datetime.utcnow().replace(tzinfo=utc)
    iso_date = f"{now.year}-{now.month}-{now.day}"

    """
    ## copied from django-minio-backend github
    Get filename prepended with current date in ISO8601 format [year-month-day] as string
    The date prefix will be the folder's name storing the object e.g.: 2020-12-31/cat.png
    """
    return f"{iso_date}/{file_name_ext}"

class JpegStorage(FileSystemStorage):
    
    def __init__(self, bucket_name=None):
        FileSystemStorage.__init__(self, location=Path("D:\\minio\\ticket"), base_url="http://localhost:9001")
        self.bucket_name = bucket_name
    
    def _open(self, name: str, mode="rb") -> File :
        filepath = Path(self.location) / self.bucket_name / name
        print(f"open({name=} -> {filepath=})")
        return File(open(name, mode))
    
    def _save(self, name: str, content : File):
        filepath = Path(self.location) / self.bucket_name / name
        print(f"_save({name=} -> {filepath.parent} -> {filepath=})")
        
        os.makedirs(filepath.parent, 777, exist_ok=True)
        fd = os.open(filepath, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o666)
        _file = None
        try:
            locks.lock(fd, locks.LOCK_EX)
            for chunk in content.chunks():
                if _file is None:
                    mode = "wb" if isinstance(chunk, bytes) else "wt"
                    _file = os.fdopen(fd, mode)
                _file.write(chunk)
        finally:
            locks.unlock(fd)
            if _file is not None:
                _file.close()
            else:
                os.close(fd)
            
        return str(name).replace("\\", "/")
    
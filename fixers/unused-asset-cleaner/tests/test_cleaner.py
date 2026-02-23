import pytest
import shutil
from pathlib import Path
from tools.cleaner import Cleaner

def test_cleaner_delete(tmp_path):
    f1 = tmp_path / "f1.txt"
    f2 = tmp_path / "f2.txt"
    f1.write_text("content1")
    f2.write_text("content2")

    cleaner = Cleaner(str(tmp_path))

    # Delete without backup
    cleaner.delete([f1], backup=False)
    assert not f1.exists()
    assert f2.exists()

def test_cleaner_backup(tmp_path):
    f1 = tmp_path / "f1.txt"
    f1.write_text("content1")

    cleaner = Cleaner(str(tmp_path))

    # Delete with backup
    cleaner.delete([f1], backup=True)
    assert not f1.exists()

    backup_path = tmp_path / ".unused_assets_backup" / "f1.txt"
    assert backup_path.exists()
    assert backup_path.read_text() == "content1"

def test_cleaner_restore(tmp_path):
    f1 = tmp_path / "f1.txt"
    f1.write_text("content1")

    cleaner = Cleaner(str(tmp_path))
    cleaner.delete([f1], backup=True)
    assert not f1.exists()

    cleaner.restore()
    assert f1.exists()
    assert not (tmp_path / ".unused_assets_backup").exists()

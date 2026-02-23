"""Tests for File Organizer."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.organizer import categorize_file, get_extension, organize_file_list, suggest_structure, format_result_markdown, CATEGORIES

FILES = [{"name": "photo.jpg", "size": 1024}, {"name": "doc.pdf", "size": 2048}, {"name": "app.py", "size": 512}, {"name": "styles.css", "size": 256}, {"name": "data.json", "size": 128}, {"name": "video.mp4", "size": 4096}, {"name": "archive.zip", "size": 8192}, {"name": "readme.txt", "size": 64}]

def test_cat_image(): assert categorize_file("photo.jpg") == "images"
def test_cat_doc(): assert categorize_file("doc.pdf") == "documents"
def test_cat_code(): assert categorize_file("app.py") == "code"
def test_cat_data(): assert categorize_file("data.json") == "data"
def test_cat_media(): assert categorize_file("video.mp4") == "media"
def test_cat_archive(): assert categorize_file("archive.zip") == "archives"
def test_cat_web(): assert categorize_file("styles.css") == "web"
def test_cat_other(): assert categorize_file("mystery.xyz") == "other"
def test_ext(): assert get_extension("photo.JPG") == ".jpg"
def test_count(): r = organize_file_list(FILES); assert r.total_files == 8
def test_categories(): r = organize_file_list(FILES); assert len(r.categories) >= 5
def test_size(): r = organize_file_list(FILES); assert r.total_size == sum(f["size"] for f in FILES)
def test_largest(): r = organize_file_list(FILES); assert r.largest_files[0].size == 8192
def test_extensions(): r = organize_file_list(FILES); assert ".jpg" in r.extensions
def test_suggest(): s = suggest_structure(organize_file_list(FILES * 3)); assert len(s) >= 1
def test_format(): md = format_result_markdown(organize_file_list(FILES)); assert "File Organization" in md
def test_cats_count(): assert len(CATEGORIES) >= 7

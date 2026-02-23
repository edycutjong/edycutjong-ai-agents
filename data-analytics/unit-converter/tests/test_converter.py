"""Tests for Unit Converter."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.converter import convert, find_category, list_units, convert_temperature, format_result_markdown, CONVERSIONS

def test_m_to_km(): r = convert(1000, "m", "km"); assert abs(r.result - 1) < 0.01
def test_km_to_mi(): r = convert(1, "km", "mi"); assert abs(r.result - 0.621) < 0.01
def test_kg_to_lb(): r = convert(1, "kg", "lb"); assert abs(r.result - 2.205) < 0.01
def test_g_to_kg(): r = convert(1000, "g", "kg"); assert abs(r.result - 1) < 0.01
def test_c_to_f(): r = convert(100, "c", "f"); assert abs(r.result - 212) < 0.1
def test_f_to_c(): r = convert(32, "f", "c"); assert abs(r.result - 0) < 0.1
def test_c_to_k(): r = convert(0, "c", "k"); assert abs(r.result - 273.15) < 0.1
def test_l_to_gal(): r = convert(1, "l", "gal"); assert abs(r.result - 0.264) < 0.01
def test_s_to_min(): r = convert(120, "s", "min"); assert abs(r.result - 2) < 0.01
def test_h_to_s(): r = convert(1, "h", "s"); assert abs(r.result - 3600) < 0.1
def test_gb_to_mb(): r = convert(1, "gb", "mb"); assert abs(r.result - 1024) < 0.1
def test_invalid_from(): r = convert(1, "xyz", "m"); assert not r.is_valid
def test_invalid_to(): r = convert(1, "m", "xyz"); assert not r.is_valid
def test_category(): assert find_category("m") == "length"
def test_category_temp(): assert find_category("c") == "temperature"
def test_list(): u = list_units(); assert "length" in u
def test_list_cat(): u = list_units("weight"); assert "kg" in u["weight"]
def test_format(): md = format_result_markdown(convert(1, "km", "m")); assert "Unit Converter" in md
def test_to_dict(): d = convert(1, "m", "km").to_dict(); assert "result" in d

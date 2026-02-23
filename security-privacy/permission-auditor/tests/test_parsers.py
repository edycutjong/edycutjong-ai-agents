import pytest
import sys
import os

# Add parent dir to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.parsers import (
    parse_android_manifest,
    parse_ios_plist,
    parse_chrome_manifest,
    parse_web_package,
    identify_file_type
)

ANDROID_MANIFEST = """
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.app">
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
</manifest>
"""

IOS_PLIST = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSCameraUsageDescription</key>
    <string>We need camera access to take photos.</string>
    <key>NSLocationWhenInUseUsageDescription</key>
    <string>We need location for maps.</string>
</dict>
</plist>
"""

CHROME_MANIFEST = """
{
    "manifest_version": 3,
    "name": "Test Extension",
    "permissions": ["storage", "activeTab"],
    "host_permissions": ["https://google.com/"]
}
"""

WEB_PACKAGE = """
{
    "name": "web-app",
    "dependencies": {
        "react": "^18.0.0",
        "axios": "^1.0.0"
    }
}
"""

def test_parse_android_manifest():
    permissions = parse_android_manifest(ANDROID_MANIFEST)
    assert "android.permission.CAMERA" in permissions
    assert "android.permission.ACCESS_FINE_LOCATION" in permissions
    assert len(permissions) == 2

def test_parse_ios_plist():
    permissions = parse_ios_plist(IOS_PLIST)
    assert "NSCameraUsageDescription" in permissions
    assert "NSLocationWhenInUseUsageDescription" in permissions
    assert len(permissions) == 2

def test_parse_chrome_manifest():
    permissions = parse_chrome_manifest(CHROME_MANIFEST)
    assert "storage" in permissions
    assert "activeTab" in permissions
    assert "https://google.com/" in permissions
    assert len(permissions) == 3

def test_parse_web_package():
    deps = parse_web_package(WEB_PACKAGE)
    assert "react" in deps
    assert "axios" in deps
    assert len(deps) == 2

def test_identify_file_type():
    assert identify_file_type(ANDROID_MANIFEST, "AndroidManifest.xml") == "android"
    assert identify_file_type(IOS_PLIST, "Info.plist") == "ios"
    assert identify_file_type(CHROME_MANIFEST, "manifest.json") == "chrome"
    assert identify_file_type(WEB_PACKAGE, "package.json") == "web"

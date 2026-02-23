import json
import plistlib
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Union

def parse_android_manifest(content: Union[str, bytes]) -> List[str]:
    """
    Parses AndroidManifest.xml content to extract uses-permission tags.
    Handles both standard Android namespace and potential missing namespaces.
    """
    try:
        if isinstance(content, str):
            content_bytes = content.encode('utf-8')
        else:
            content_bytes = content

        root = ET.fromstring(content_bytes)
        permissions = []

        # Define namespace map
        namespaces = {'android': 'http://schemas.android.com/apk/res/android'}

        # Find all uses-permission tags
        # Note: ET.findall with namespaces requires the namespace to be passed
        for elem in root.findall(".//uses-permission", namespaces):
            name = elem.get(f"{{{namespaces['android']}}}name")
            if name:
                permissions.append(name)

        # Also try finding without namespace if the above fails or XML is malformed/different
        if not permissions:
            for elem in root.findall(".//uses-permission"):
                name = elem.get("android:name") or elem.get("name")
                if name:
                    permissions.append(name)

        return list(set(permissions))
    except Exception as e:
        print(f"Error parsing Android Manifest: {e}")
        return []

def parse_ios_plist(content: Union[str, bytes]) -> List[str]:
    """
    Parses Info.plist content to extract UsageDescription keys.
    These keys usually end with 'UsageDescription' (e.g., NSCameraUsageDescription).
    """
    try:
        if isinstance(content, str):
            # plistlib.loads expects bytes for XML plists
            content_bytes = content.encode('utf-8')
        else:
            content_bytes = content

        try:
            plist_data = plistlib.loads(content_bytes)
        except plistlib.InvalidFileException:
             # Fallback: maybe it's a JSON plist or just weird text?
             # But for now assume standard XML/Binary plist.
             return []

        permissions = []
        if isinstance(plist_data, dict):
            for key in plist_data.keys():
                if isinstance(key, str) and key.endswith("UsageDescription"):
                    permissions.append(key)
        return permissions
    except Exception as e:
        print(f"Error parsing iOS Plist: {e}")
        return []

def parse_chrome_manifest(content: Union[str, bytes]) -> List[str]:
    """
    Parses Chrome Extension manifest.json to extract permissions and host_permissions.
    """
    try:
        if isinstance(content, bytes):
            content = content.decode('utf-8')

        data = json.loads(content)
        permissions = data.get("permissions", [])
        host_permissions = data.get("host_permissions", [])
        optional_permissions = data.get("optional_permissions", [])

        # Combine all relevant permission fields
        all_perms = []
        if isinstance(permissions, list):
            all_perms.extend(permissions)
        if isinstance(host_permissions, list):
            all_perms.extend(host_permissions)
        if isinstance(optional_permissions, list):
            all_perms.extend(optional_permissions)

        # Remove duplicates
        return list(set(all_perms))
    except Exception as e:
        print(f"Error parsing Chrome Manifest: {e}")
        return []

def parse_web_package(content: Union[str, bytes]) -> List[str]:
    """
    Parses package.json to find dependencies that might imply permissions or capabilities.
    For now, returns a list of dependencies.
    """
    try:
        if isinstance(content, bytes):
            content = content.decode('utf-8')

        data = json.loads(content)
        dependencies = data.get("dependencies", {})
        devDependencies = data.get("devDependencies", {})

        all_deps = []
        if isinstance(dependencies, dict):
            all_deps.extend(dependencies.keys())
        if isinstance(devDependencies, dict):
            all_deps.extend(devDependencies.keys())

        return list(set(all_deps))
    except Exception as e:
        print(f"Error parsing package.json: {e}")
        return []

def identify_file_type(content: Union[str, bytes], filename: str) -> str:
    """
    Helper to identify file type based on content or filename.
    """
    filename = filename.lower()

    if isinstance(content, bytes):
        try:
            content_str = content.decode('utf-8')
        except:
            content_str = ""
    else:
        content_str = content

    if filename.endswith(".xml") or ("<manifest" in content_str and "android" in content_str):
        return "android"
    elif filename.endswith(".plist") or ("plist" in content_str and "<plist" in content_str):
        return "ios"
    elif filename.endswith("manifest.json"):
        return "chrome"
    elif filename.endswith("package.json"):
        return "web"
    else:
        return "unknown"

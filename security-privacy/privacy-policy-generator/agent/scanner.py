import os
import re
from pathlib import Path
from typing import Dict, List, Set, Any

class CodeScanner:
    """
    Scans a directory for code patterns indicating data collection and third-party usage.
    """

    # Patterns to identify Personal Identifiable Information (PII)
    PII_PATTERNS = {
        "email": [r"email",r"e-mail", r"mail_address", r"contact_email"],
        "phone": [r"phone", r"mobile", r"telephone", r"cell", r"contact_number"],
        "name": [r"first_name", r"last_name", r"full_name", r"username", r"user_name"],
        "address": [r"address", r"street", r"city", r"zip_code", r"postal_code", r"country"],
        "ip_address": [r"ip_address", r"remote_addr", r"client_ip"],
        "location": [r"location", r"latitude", r"longitude", r"gps", r"geo"],
        "device_id": [r"device_id", r"android_id", r"idfa", r"uuid", r"imei"],
        "cookies": [r"cookie", r"local_storage", r"session_storage"],
        "password": [r"password", r"passwd", r"pwd", r"secret"],
        "financial": [r"credit_card", r"card_number", r"cvv", r"billing", r"payment"],
        "biometric": [r"face_id", r"fingerprint", r"voice_print"],
        "health": [r"health", r"medical", r"patient", r"diagnosis"],
    }

    # Patterns to identify Third-Party Services
    THIRD_PARTY_PATTERNS = {
        "Google Analytics": [r"google-analytics", r"ga\(", r"gtag"],
        "Firebase": [r"firebase", r"firestore"],
        "Stripe": [r"stripe"],
        "PayPal": [r"paypal"],
        "AWS": [r"aws", r"amazon"],
        "Facebook/Meta": [r"facebook", r"fb_"],
        "Twitter/X": [r"twitter"],
        "Sentry": [r"sentry"],
        "Mixpanel": [r"mixpanel"],
        "Segment": [r"segment"],
        "Intercom": [r"intercom"],
        "AdMob": [r"admob"],
    }

    SKIP_DIRS = {".git", "node_modules", "venv", "__pycache__", "build", "dist", "target", "vendor"}
    SKIP_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".woff", ".woff2", ".ttf", ".eot", ".mp3", ".mp4", ".zip", ".tar", ".gz", ".pyc", ".class", ".o", ".obj", ".dll", ".so", ".exe", ".pdf", ".lock"}

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)

    def scan(self) -> Dict[str, Any]:
        """
        Scans the directory and returns a summary of findings.
        """
        if not self.root_dir.exists():
             raise FileNotFoundError(f"Directory not found: {self.root_dir}")

        pii_found: Set[str] = set()
        third_parties_found: Set[str] = set()
        files_scanned = 0

        findings_detail: Dict[str, List[str]] = {} # Map category -> list of file:line

        for file_path in self._iterate_files():
            files_scanned += 1
            try:
                content = file_path.read_text(errors='ignore')

                # Check PII
                for category, patterns in self.PII_PATTERNS.items():
                    for pattern in patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            pii_found.add(category)
                            if category not in findings_detail:
                                findings_detail[category] = []
                            findings_detail[category].append(str(file_path.relative_to(self.root_dir)))
                            break # Found one pattern for this category in this file, move to next category

                # Check Third Parties
                for service, patterns in self.THIRD_PARTY_PATTERNS.items():
                     for pattern in patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            third_parties_found.add(service)
                            if service not in findings_detail:
                                findings_detail[service] = []
                            findings_detail[service].append(str(file_path.relative_to(self.root_dir)))
                            break

            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

        return {
            "pii": list(pii_found),
            "third_parties": list(third_parties_found),
            "files_scanned": files_scanned,
            "details": findings_detail
        }

    def _iterate_files(self):
        """Recursively yields file paths, skipping ignored directories."""
        for root, dirs, files in os.walk(self.root_dir):
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.SKIP_DIRS]

            for file in files:
                path = Path(root) / file
                if path.suffix.lower() not in self.SKIP_EXTENSIONS:
                    yield path

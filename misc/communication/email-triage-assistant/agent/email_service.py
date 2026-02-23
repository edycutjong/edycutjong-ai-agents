from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime, timedelta
import random
from imap_tools import MailBox, AND
from bs4 import BeautifulSoup
from .models import Email
from config import Config

class EmailProvider(ABC):
    @abstractmethod
    def fetch_emails(self, limit: int = 10, folder: str = "INBOX") -> List[Email]:
        pass

    @abstractmethod
    def get_email(self, email_id: str) -> Optional[Email]:
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

class MockEmailProvider(EmailProvider):
    def __init__(self):
        self.emails = self._generate_mock_emails()

    def connect(self):
        print("Connected to Mock Email Server")

    def disconnect(self):
        print("Disconnected from Mock Email Server")

    def fetch_emails(self, limit: int = 10, folder: str = "INBOX") -> List[Email]:
        return self.emails[:limit]

    def get_email(self, email_id: str) -> Optional[Email]:
        for email in self.emails:
            if email.id == email_id:
                return email
        return None

    def _generate_mock_emails(self) -> List[Email]:
        mock_data = [
            {
                "id": "1",
                "subject": "URGENT: Project Deadline Update",
                "sender": "boss@company.com",
                "recipient": "me@company.com",
                "body": "Hi,\n\nWe need to move the deadline for the Alpha project to this Friday. Please update the team and ensure all deliverables are ready.\n\nThanks,\nBoss",
                "date_offset": 0
            },
            {
                "id": "2",
                "subject": "Weekly Newsletter: Tech Trends",
                "sender": "news@techtrends.com",
                "recipient": "me@company.com",
                "body": "Here are the top stories in tech this week:\n1. AI takes over coding.\n2. New frameworks released.\n3. Hardware updates.\n\nClick here to read more.",
                "date_offset": 1
            },
            {
                "id": "3",
                "subject": "Invoice #12345 Due",
                "sender": "billing@service.com",
                "recipient": "me@company.com",
                "body": "Dear Customer,\n\nYour invoice #12345 for $50.00 is due tomorrow. Please pay via the portal.\n\nRegards,\nBilling Team",
                "date_offset": 2
            },
            {
                "id": "4",
                "subject": "Team Lunch on Friday?",
                "sender": "colleague@company.com",
                "recipient": "me@company.com",
                "body": "Hey,\n\nAre you free for lunch this Friday? We were thinking of trying that new burger place.\n\nLet me know!",
                "date_offset": 3
            },
            {
                "id": "5",
                "subject": "Limited Time Offer: 50% Off",
                "sender": "promo@store.com",
                "recipient": "me@company.com",
                "body": "Don't miss out on our biggest sale of the year! 50% off everything. Shop now!",
                "date_offset": 4
            }
        ]

        emails = []
        for data in mock_data:
            emails.append(Email(
                id=data["id"],
                subject=data["subject"],
                sender=data["sender"],
                recipient=data["recipient"],
                date=datetime.now() - timedelta(hours=data["date_offset"] * 5),
                body=data["body"],
                snippet=data["body"][:50] + "..."
            ))
        return emails

class ImapEmailProvider(EmailProvider):
    def __init__(self, server=None, username=None, password=None):
        self.server = server or Config.IMAP_SERVER
        self.username = username or Config.EMAIL_ACCOUNT
        self.password = password or Config.EMAIL_PASSWORD
        self.mailbox = None

    def connect(self):
        if not self.server or not self.username or not self.password:
            raise ValueError("Missing IMAP configuration")
        self.mailbox = MailBox(self.server).login(self.username, self.password)

    def disconnect(self):
        if self.mailbox:
            self.mailbox.logout()

    def fetch_emails(self, limit: int = 10, folder: str = "INBOX") -> List[Email]:
        if not self.mailbox:
            self.connect()

        try:
            # Select folder
            self.mailbox.folder.set(folder)

            emails = []
            for msg in self.mailbox.fetch(limit=limit, reverse=True):
                body = msg.text or ""
                if not body and msg.html:
                    soup = BeautifulSoup(msg.html, "html.parser")
                    body = soup.get_text(separator="\n").strip()

                emails.append(Email(
                    id=str(msg.uid),
                    subject=msg.subject,
                    sender=msg.from_,
                    recipient=msg.to[0] if msg.to else "",
                    date=msg.date,
                    body=body,
                    snippet=body[:100] + "..."
                ))
            return emails
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []

    def get_email(self, email_id: str) -> Optional[Email]:
        if not self.mailbox:
            self.connect()

        try:
            for msg in self.mailbox.fetch(AND(uid=email_id), limit=1):
                body = msg.text or ""
                if not body and msg.html:
                    soup = BeautifulSoup(msg.html, "html.parser")
                    body = soup.get_text(separator="\n").strip()

                return Email(
                    id=str(msg.uid),
                    subject=msg.subject,
                    sender=msg.from_,
                    recipient=msg.to[0] if msg.to else "",
                    date=msg.date,
                    body=body,
                    snippet=body[:100] + "..."
                )
            return None
        except Exception as e:
            print(f"Error fetching email {email_id}: {e}")
            return None

def get_email_provider(use_mock: bool = True) -> EmailProvider:
    if use_mock:
        return MockEmailProvider()
    else:
        return ImapEmailProvider()

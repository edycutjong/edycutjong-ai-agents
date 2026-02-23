import json
import os
from datetime import datetime
from .ui import console

STATS_FILE = ".style_enforcer_stats.json"

class Gamification:
    def __init__(self):
        self.stats = self._load_stats()

    def _load_stats(self):
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                return self._default_stats()
        return self._default_stats()

    def _default_stats(self):
        return {
            "clean_commits": 0,
            "total_fixes": 0,
            "streak": 0,
            "last_clean_run": None,
            "level": 1,
            "xp": 0
        }

    def _save_stats(self):
        with open(STATS_FILE, "w") as f:
            json.dump(self.stats, f, indent=4)

    def record_clean_run(self):
        today = datetime.now().strftime("%Y-%m-%d")
        if self.stats["last_clean_run"] == today:
            # Already recorded today
            return

        self.stats["clean_commits"] += 1

        # Check streak
        last_date_str = self.stats["last_clean_run"]
        if last_date_str:
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
            delta = (datetime.now() - last_date).days
            if delta == 1:
                self.stats["streak"] += 1
            elif delta > 1:
                self.stats["streak"] = 1
        else:
            self.stats["streak"] = 1

        self.stats["last_clean_run"] = today
        self.add_xp(10 + (self.stats["streak"] * 2))
        self._save_stats()

    def record_fix(self, count=1):
        self.stats["total_fixes"] += count
        self.add_xp(5 * count)
        self._save_stats()

    def add_xp(self, amount):
        self.stats["xp"] += amount
        # Simple level up logic: level * 100 XP
        while self.stats["xp"] >= self.stats["level"] * 100:
            self.stats["xp"] -= self.stats["level"] * 100
            self.stats["level"] += 1
            console.print(f"[bold magenta]🎉 Level Up! You are now Level {self.stats['level']}! 🎉[/bold magenta]")

    def get_stats_summary(self):
        return (
            f"Level: {self.stats['level']} | XP: {self.stats['xp']}/{self.stats['level']*100}\n"
            f"Clean Commits: {self.stats['clean_commits']} | Streak: {self.stats['streak']} days\n"
            f"Total Fixes: {self.stats['total_fixes']}"
        )

gamification = Gamification()

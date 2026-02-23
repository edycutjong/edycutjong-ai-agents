import os
import pytest
from unittest.mock import patch
from utils.config import config
from utils.gamification import gamification

def test_config_load():
    # It should have defaults
    assert config.tone == "friendly"
    assert config.max_line_length == 88

def test_gamification_record_clean():
    # Patch STATS_FILE
    with patch("utils.gamification.STATS_FILE", "test_stats.json"):
        # Reset stats to default so we start fresh
        gamification.stats = gamification._default_stats()

        gamification.record_clean_run()

        assert gamification.stats["clean_commits"] == 1
        assert gamification.stats["streak"] == 1

        # Verify file creation
        assert os.path.exists("test_stats.json")

        # Clean up
        if os.path.exists("test_stats.json"):
            os.remove("test_stats.json")

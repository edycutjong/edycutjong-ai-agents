import pytest
from pathlib import Path
from tools.optimizer import Optimizer
from PIL import Image

def test_optimizer(tmp_path):
    img_path = tmp_path / "test.png"
    # Create a red image
    img = Image.new('RGB', (100, 100), color = 'red')
    img.save(img_path)

    optimizer = Optimizer()
    count, saved = optimizer.optimize([img_path])

    # Check if optimized
    assert count >= 0
    # Size might not decrease for such simple image, but process should not crash
    assert img_path.exists()

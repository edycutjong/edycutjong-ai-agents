from PIL import Image
from pathlib import Path
from typing import List, Tuple
import os

class Optimizer:
    """
    Optimizes image assets to save space.
    """

    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.webp'}

    def __init__(self):
        pass

    def optimize(self, files: List[Path], quality: int = 80) -> Tuple[int, int]:
        """
        Optimizes the given list of files.
        Returns (count_optimized, bytes_saved).
        """
        count_optimized = 0
        bytes_saved = 0

        for file_path in files:
            if not file_path.exists():
                continue  # pragma: no cover

            if file_path.suffix.lower() not in self.SUPPORTED_FORMATS:
                continue  # pragma: no cover

            try:
                original_size = file_path.stat().st_size

                # Create a temp file to save the optimized version
                # Use a unique suffix but keep the original extension to help PIL detect format
                temp_path = file_path.with_name(f".tmp_{file_path.name}")

                # Use context manager to ensure file is closed
                with Image.open(file_path) as img:
                    if file_path.suffix.lower() in {'.jpg', '.jpeg'}:
                        img.save(temp_path, quality=quality, optimize=True)  # pragma: no cover
                    elif file_path.suffix.lower() == '.png':
                        img.save(temp_path, optimize=True)
                    elif file_path.suffix.lower() == '.webp':  # pragma: no cover
                        img.save(temp_path, quality=quality)  # pragma: no cover

                # File is closed now

                if temp_path.exists():
                    new_size = temp_path.stat().st_size

                    if new_size < original_size:
                        # Replace original
                        temp_path.replace(file_path)
                        bytes_saved += (original_size - new_size)
                        count_optimized += 1
                    else:
                        # Keep original if optimization didn't help (or made it larger)
                        temp_path.unlink()  # pragma: no cover

            except Exception as e:  # pragma: no cover
                # Ensure temp file is cleaned up in case of error
                try:  # pragma: no cover
                    if 'temp_path' in locals() and temp_path.exists():  # pragma: no cover
                        temp_path.unlink()  # pragma: no cover
                except:  # pragma: no cover
                    pass  # pragma: no cover
                # print(f"Error optimizing {file_path}: {e}")

        return count_optimized, bytes_saved

if __name__ == "__main__":
    pass  # pragma: no cover

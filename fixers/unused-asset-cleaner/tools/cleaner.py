import shutil
import os
from pathlib import Path
from typing import List, Tuple

class Cleaner:
    """
    Handles deletion and backup of unused assets.
    """

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)

    def delete(self, files: List[Path], backup: bool = True, backup_dir_name: str = '.unused_assets_backup') -> Tuple[int, int]:
        """
        Deletes the specified files. Returns (count_deleted, bytes_freed).
        If backup is True, files are moved to backup_dir instead of permanent deletion.
        """
        deleted_count = 0
        freed_bytes = 0

        backup_path = self.root_dir / backup_dir_name
        if backup and not backup_path.exists():
            backup_path.mkdir(parents=True, exist_ok=True)

        for file_path in files:
            if not file_path.exists():
                continue

            try:
                file_size = file_path.stat().st_size

                if backup:
                    # Maintain relative structure in backup
                    # e.g. assets/img/logo.png -> .backup/assets/img/logo.png
                    rel_path = file_path.relative_to(self.root_dir)
                    dest_path = backup_path / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)

                    shutil.move(str(file_path), str(dest_path))
                else:
                    os.remove(file_path)

                deleted_count += 1
                freed_bytes += file_size
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

        return deleted_count, freed_bytes

    def restore(self, backup_dir_name: str = '.unused_assets_backup') -> int:
        """
        Restores all files from the backup directory.
        Returns the number of files restored.
        """
        backup_path = self.root_dir / backup_dir_name
        if not backup_path.exists():
            return 0

        restored_count = 0
        for root, dirs, files in os.walk(backup_path):
            for file in files:
                src_path = Path(root) / file
                rel_path = src_path.relative_to(backup_path)
                dest_path = self.root_dir / rel_path

                try:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src_path), str(dest_path))
                    restored_count += 1
                except Exception as e:
                    print(f"Error restoring {src_path}: {e}")

        # Clean up empty backup dir
        shutil.rmtree(backup_path)
        return restored_count

if __name__ == "__main__":
    pass

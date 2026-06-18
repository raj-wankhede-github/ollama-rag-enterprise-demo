"""
Initialize empty directories with placeholder files for git tracking.
"""

import os

directories = [
    "data/uploads",
    "data/chroma_db",
    "tests",
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    gitkeep_path = os.path.join(directory, ".gitkeep")
    if not os.path.exists(gitkeep_path):
        with open(gitkeep_path, "w") as f:
            f.write("")
        print(f"Created {gitkeep_path}")

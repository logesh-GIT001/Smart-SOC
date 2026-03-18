import os

folders = [
    "data/raw",
    "data/processed",
    "data/samples",
    "notebooks",
    "models/saved",
    "models/experiments",
    "api/routes",
    "api/schemas",
    "dashboard/components",
    "dashboard/pages",
    "tests",
    "scripts",
    "docs",
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    with open(f"{folder}/.gitkeep", "w") as f:
        pass

print("✅ All folders created!")

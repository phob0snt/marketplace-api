import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.db.session import create_tables

def init_database():
    create_tables()

if __name__ == "__main__":
    init_database()

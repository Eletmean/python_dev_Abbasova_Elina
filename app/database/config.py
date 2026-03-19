from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB1_PATH = DATA_DIR / "db1.sqlite"
DB2_PATH = DATA_DIR / "db2.sqlite"

DATABASE_URL_DB1 = f"sqlite+aiosqlite:///{DB1_PATH}"
DATABASE_URL_DB2 = f"sqlite+aiosqlite:///{DB2_PATH}"
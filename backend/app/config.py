import tempfile
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_dir = os.path.join(PROJECT_ROOT, "database")

if os.environ.get("VERCEL") or not os.access(db_dir, os.W_OK):
    DB_PATH = os.path.join(tempfile.gettempdir(), "lpu_examprep.db")
else:
    DB_PATH = os.path.join(db_dir, "lpu_examprep.db")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

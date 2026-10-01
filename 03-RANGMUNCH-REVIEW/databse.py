from sqlmodel import SQLModel, Session, create_engine

DATEABASE_URL = "sqlite:///./rangmunch_reviews.db"

engine = create_engine(DATEABASE_URL, echo=True)

def create_tables():
    """Create the database tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get a new database session."""
    with Session(engine) as session:
        yield session
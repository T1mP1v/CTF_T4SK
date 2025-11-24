from sqlmodel import SQLModel, create_engine, select, Session
from database.model import Users_db

sqlite_file_name = "database/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        sql = select(Users_db).where(Users_db.name == "admin")
        admin_user = session.exec(sql).first()

        if not admin_user:
            new_admin = Users_db(
                name="admin",
                email="admin@admin.com",
                password="H655,w6H6&7T"
            )
            session.add(new_admin)
            session.commit()
            session.refresh(new_admin)

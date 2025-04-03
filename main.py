from fastapi import FastAPI
from config import engine
import tables.users as user_table
import routes.users as user_routes
user_table.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(user_routes.router)
# @app.get("/")
# def read_root():
#     return "Serevr is runing"
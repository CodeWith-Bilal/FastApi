from fastapi import FastAPI
from config import engine
import tables.users as user_table
import tables.products as product_table
import routes.users as user_routes
import routes.products as product_routes

user_table.Base.metadata.create_all(bind=engine)
product_table.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(product_routes.router)

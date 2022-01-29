from fastapi import FastAPI, Request, HTTPException, status 
from tortoise import models
from tortoise.contrib.fastapi import register_tortoise
from models import *
from authentication import (get_hashed_password, very_token)

# signals 
from tortoise.signals import post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient
from emails import *  

#response classes
from fastapi.responses import HTMLResponse    

#templates
from fastapi.templating import Jinja2Templates 

app = FastAPI()

@post_save(User)
async def create_business(
    sender: "Type[User]",
    instance: User,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str]
) -> None:
    if created:
        await send_email([instance.email], instance)



@app.post("/registeration")
async def user_registertions(user: user_pydanticIn):
    user_info = user.dict(exclude_unset=True)
    user_info["password"] = get_hashed_password(user_info["password"])
    user_obj = await User.create(**user_info)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)
    return{
        "status": "ok",
        "data": f"hello {new_user.username}, thanks for choosing our services. please cheack your email inbox and click on the link to confirm your registration."
    }


@app.get("/")
def index():
    return{"Message": "hello...."}

register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas = True,
    add_exception_handlers = True
)
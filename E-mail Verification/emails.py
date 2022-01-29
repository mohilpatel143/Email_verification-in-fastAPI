from fastapi import (BackgroundTasks, UploadFile, File, Form, Depends, HTTPException, status) 
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig  
from dotenv import dotenv_values  
from pydantic import BaseModel, EmailStr  
from typing import List 
from models import User 
import jwt 

config_credentials = dotenv_values(".env") 

conf = ConnectionConfig(    
    MAIL_USERNAME = config_credentials["EMAIL"], 
    MAIL_PASSWORD = config_credentials["PASS"], 
    MAIL_FROM = config_credentials["EMAIL"], 
    MAIL_PORT = 587, 
    MAIL_SERVER = "smtp.gmail.com", 
    MAIL_TLS = True, 
    MAIL_SSL = False, 
    USE_CREDENTIALS = True 
)

class EmailSchema(BaseModel): 
    email: List[EmailStr] 


async def send_email(email:EmailSchema, instance: User): 
    token_data = { 
        "id" : instance.id, 
        "username": instance.username 
    }    
    token = jwt.encode(token_data, config_credentials["SECRET"], algorithm='HS256')

    template = """
        <html>
        <body>

           <p>Hi !!!
           <br>Thanks for using fastapi mail, keep using it..!!!</p>
 
        </body>
        </html>
    """

    message = MessageSchema(
        subject = "Account Verification Email",
        recipients = email,
        body = template,
        subtype = "html"
    )

    fm = FastMail(conf)
    await fm.send_message(message=message)
from fastapi import FastAPI,Form,HTTPException,status,Depends
from sqlalchemy.orm import Session

from .database.session import engine,Base,get_db
from .routes import users
from .models import models
from .routes.users import pwd_context



Base.metadata.create_all(bind=engine)
app=FastAPI(title="Nepal Shop E-commerce App")

app.include_router(users.router)

@app.get("/")
def root():
    return {"message":"FastApi backedn is running"}



def verify_password(plained_password,hashed_password):
    return pwd_context.verify(plained_password,hashed_password)


@app.post("/login")
def login(email:str=Form(...),password:str=Form(...),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==email).first()
    if not user and verify_password(password,user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )
    return {"message":"Login Successful"}


@app.post("/logout")
def logout():
    return {"message":"Logout Successful"}


    
    
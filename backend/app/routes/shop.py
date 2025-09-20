from fastapi import APIRouter,Depends,HTTPException,Form,Form,UploadFile,File
from sqlalchemy.orm import Session
import os
import shutil

from ..models import models
from ..schemas import schemas
from  ..database.session import get_db

router=APIRouter(prefix="/shops")
upload_folder="shops"

@router.get("/")
def get_all_shops(db: Session=Depends(get_db)):
    shops=db.query(models.Shop).all()
    return {"shops":shops}

@router.get("/{shop_id}")
def get_shop(shop_id:int,db: Session=Depends(get_db)):
    shop=db.query(models.Shop).filter(models.Shop.id == shop_id).first()
    return {"id":shop.id,"shop_name":shop.shop_name,"phone":shop.phone,"lat":shop.location_lat,"lon":shop.location_lon,"address":shop.address}


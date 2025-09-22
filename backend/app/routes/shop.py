from fastapi import APIRouter,Depends,HTTPException,Form,UploadFile,status,Body
from sqlalchemy.orm import Session


from ..models import models

from  ..database.session import get_db

router=APIRouter(prefix="/shops",tags=["Shop"])
upload_folder="shops"

@router.get("/")
def get_all_shops(db: Session=Depends(get_db)):
    shops=db.query(models.Shop).all()
    return {"shops":shops}

@router.get("/{shop_id}")
def get_shop(shop_id:int,db: Session=Depends(get_db)):
    shop=db.query(models.Shop).filter(models.Shop.id == shop_id).first()
    return {"id":shop.id,"shop_name":shop.shop_name,"phone":shop.phone,"lat":shop.location_lat,"lon":shop.location_lon,"address":shop.address}


@router.post("/")
def create_shop(user_id:int=Body(...),
                shop_name:str=Body(...),
                phone:int=Body(...),
                location_lat: float=Body(...),
                location_lon: float=Body(...),
                address:str=Body(...),
                db:Session=Depends(get_db)):
    shop=db.query(models.Shop).filter(models.Shop.phone == phone).first()
    if shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Phone number already exists")
    new_shop=models.Shop(user_id=user_id,shop_name=shop_name,phone=phone,location_lat=location_lat,location_lon=location_lon,address=address)
    db.add(new_shop)
    db.commit()
    return {"message":"Shop added successfully"}

@router.put("/{shop_id}")
def update_shop(shop_id:int,user_id:int=Body(...),
                shop_name:str=Body(...),
                phone:int=Body(...),
                location_lat:float=Body(...),
                location_lon:float=Body(...),
                address:str=Body(...),
                db:Session=Depends(get_db)):
    shop=db.query(models.Shop).filter(models.Shop.id == shop_id).first()
    shop.shop_name=shop_name
    shop.phone=phone
    shop.address=address
    shop.location_lat=location_lat,
    shop.location_lon=location_lon
    db.commit()
    return {"message":"Shop updated successfully"}

@router.delete("/{shop_id}")
def delete_shop(shop_id:int,db: Session=Depends(get_db)):
    shop=db.query(models.Shop).filter(models.Shop.id==shop_id).first()
    db.delete(shop)
    db.commit()
    return {"message":"Shop deleted successfully"}



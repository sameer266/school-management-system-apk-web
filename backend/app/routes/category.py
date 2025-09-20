from fastapi import APIRouter,Depends,HTTPException,Body
from sqlalchemy.orm import Session
from ..models import models
from ..schemas import schemas
from  ..database.session import get_db


router=APIRouter(prefix="/categories")

@router.get("/")
def get_all_category(db: Session=Depends(get_db)):
    categories=db.query(models.Category).all()
    return {categories:categories}

@router.post("/")
def create_category(name: str =Body(...),db: Session=Depends(get_db)):
    new_category=models.Category(name=name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return {"message":"Category added successfully"}

@router.patch("/{category_id}")
def update_category(category_id:int,name:str=Body(...),description: str=Body(...),db: Session=Depends(get_db)):
    category=db.query(models.Category).filter(models.Category.id == category_id).first()
    category.name=name
    category.description=description
    db.commit()
    return {"message":f"Catgory {category_id} updated Successfully"}

@router.delete("/{category_id}")
def delete_category(category_id:int,db: Session=Depends(get_db)):
    category=db.query(models.Category).filter(models.Category.id==category_id).first()
    db.delete(category)
    db.commit()
    return {"message":f"Category {category.name} deleted successfully"}


@router.get("/{category_name}")
def filter_category_products(category_name:str,db: Session=Depends(get_db)):
    category=db.query(models.Category).filter(models.Category.name.ilike(category_name)).first()
    products=[]
    for p in category.products:
        products.append({ "id":p.id,"name":p.name,"price":p.price,"sales_price":p.sales_price,"quantity":p.quantity,"image_url":p.image_url})
        
    return {"category_id":category.id,"category_name":category.name,"products":products}


    
    
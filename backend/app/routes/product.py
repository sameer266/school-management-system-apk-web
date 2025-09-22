from fastapi import APIRouter,Depends,HTTPException,Form,Form,UploadFile,File
from sqlalchemy.orm import Session
import os
import shutil

from ..models import models
from ..schemas import schemas
from  ..database.session import get_db

router=APIRouter(prefix="/products",tags=["Products"])
upload_folder="products"
# Get all products from the database
@router.get("/")
def get_all_products(db:Session=Depends(get_db)):
    products=db.query(models.Product).all()
    return {"products":products}

# Get a specific product by ID
@router.get("/{product_id}")
def get_product(product_id:int,db: Session=Depends(get_db)):
    product=db.query(models.Product).filter(models.Product.id == product_id).first()
    return {"id":product.id,"name":product.name,"category_name":product.category.name,"description":product.description,"sales_price":product.sales_price,"price":product.price,"image":product.image_url,"attributes":product.attributes}

# Filter products by name
@router.get("/{product_name}")
def filter_product(product_name:str,db: Session=Depends(get_db)):
    product_obj=db.query(models.Product).filter(models.Product.name.ilike(f"%{product_name}%")).all()
    products=[]
    for p in product_obj:
        products.append({"id":p.id,"category_name":p.category.name,"name":p.name,"price":p.price,"sales_price":p.sales_price,"description":p.description,"image_url":p.image_url,"attributes":{"id":p.attributes.id,"name":p.attributes.name,"value":p.attributes.value},})
    return {"products":products}

# Create a new product
@router.post("/")
def create_products(category_id:int=Form(...),
                    shop_id:int=Form(...),
                    name:str=Form(...),
                    description:str=Form(...),
                    price:float=Form(...),
                    sales_price:float=Form(...),
                    quantity:int=Form(...),
                    image:UploadFile=File(...),
                    db:Session=Depends(get_db)):
    
    os.makedirs(upload_folder,exist_ok=True)
    image_path=os.path.join(upload_folder,image.filename)
    with open(image_path,"wb") as buffer:
        shutil.copyfileobj(image.file,buffer)
    new_product=models.Product(
        category_id=category_id,
        shop_id=shop_id,
        name=name,
        description=description,
        price=price,
        sales_price=sales_price,
        quantity=quantity,
        image_url=image_path
    )
    db.add(new_product)
    db.commit()
    return {"message":"Produts added successfully"}

# Update an existing product by ID
@router.put("/{product_id}")
def update_product(product_id:int,
                   category_id:int=Form(...),
                   shop_id:int=Form(...),
                   name:str=Form(...),
                   description:str=Form(...),
                   price: float=Form(...),
                   sales_price:float=Form(...),
                   quantity:int=Form(...),
                   image:UploadFile=File(...),
                   db:Session=Depends(get_db)):
    
    os.makedirs(upload_folder,exist_ok=True)
    image_path=os.path.join(update_product,image.filename)
    with open(image_path,'wb') as buffer:
        shutil.copyfileobj(image.file,buffer)
        
    product=db.query(models.Product).filter(models.Product.id == product_id).first()
    product.category_id=category_id
    product.shop_id=shop_id
    product.name=name
    product.description=description
    product.price=price
    product.sales_price=sales_price
    product.quantity=quantity
    product.image_url=image_path
    db.commit()
    return {"message":"Product updated successfully"}

# Delete a product by ID
@router.delete("/{product_id}")
def delete_product(product_id:int,db: Session=Depends(get_db)):
    product=db.query(models.Product).filter(models.Product.id==product_id).first()
    db.delete(product)
    db.commit()
    return {"message":f"Product {product_id} deleted successfully"}

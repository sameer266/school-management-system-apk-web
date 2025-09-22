from fastapi import APIRouter,Depends,HTTPException,Form,UploadFile,status,Body
from sqlalchemy.orm import Session


from ..models import models
from  ..database.session import get_db

router=APIRouter(prefix="/attributes",tags=["Attributes"])

@router.get("/")
def get_all_attributes(db:Session=Depends(get_db)):
    attributues_obj=db.query(models.Attribute).filter(models.Attribute).all()
    attributes=[]
    for attr in attributues_obj:
        attributes.append({"id":attr.id,"name":attr.name,"value":attr.value})
    return {"attributes":attributes}

@router.post("/")
def create_attributes(name:str=Body(...),value:str=Body(...),db: Session=Depends(get_db)):
    new_attributes=models.Attribute(name=name,value=value)
    db.add(new_attributes)
    db.commit()
    return {"message":"Attributes added succesfully"}

@router.put("/{attr_id}")
def  update_attributes(attr_id:int,value:str=Body(...),name:str=Body(...),db: Session=Depends(get_db)):
    attr=db.query(models.Attribute).filter(models.Attribute.id==attr_id).first()
    attr.name=name
    attr.value=value
    db.commit()
    return {"message":"Atributes updated successfully"}

@router.delete("/{attr_id}")
def delete_attributes(attr_id: int,db: Session=Depends(get_db)):
    attr=db.query(models.Attribute).filter(models.Attribute.id == attr_id).first()
    db.delete(attr)
    db.commit()
    return {"message":"Attributes deleted successfully"}

    


    


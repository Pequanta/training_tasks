from fastapi import APIRouter, Request, HTTPException
from fastapi import Body, Path
from typing import Dict, List
from models import ProductDataModel, PyObjectId
from pymongo.errors import DuplicateKeyError 
import logging 
router = APIRouter()


@router.get("/{product_id}")
async def get_product(request: Request, product_id: PyObjectId=Path(...)):
    try:
        if (product := await request.app.mongodb["products"].find_one({"_id": product_id})) != None:
            product["_id"] = str(product["_id"])
            return product
        else:
            return HTTPException(status_code=404 , detail="product not found")
    except:
        return HTTPException(status_code=409, detail="Error with the CRUD operations")
    

@router.post("/")
async def create_product(request: Request, product: ProductDataModel=Body(...)):
    product_ = product.model_dump()
    product_["_id"] = product_.pop("id")
    try:
        if (await request.app.mongodb["products"].find_one({"_id": product_["_id"]})) == None:
            await request.app.mongodb["products"].insert_one(product_)
            logging.info("The product is inserted suffessfully")
        else:
            logging.error("The product already exists")
            return HTTPException(status_code=409, detail="The product already exists")
    except DuplicateKeyError:
        logging.error("The product name must be unique")
    except:
        logging.error("Something went wrong with the server!!!!!")
        return HTTPException(status_code=409, detail="Error with the CRUD operations")
    

@router.put("/{product_id}")
async def update_product(request: Request, new_product: ProductDataModel, product_id: PyObjectId=Path(...)):
    new_product = new_product.model_dump()
    new_product.pop("id")
    try:
        if (await request.app.mongodb["products"].find_one({"_id": product_id})) != None:
            new_product["_id"] = product_id
            await request.app.mongodb["products"].replace_one({"_id": product_id}, new_product)
        else:
            return HTTPException(status_code=404, detail="The product with the given id doesn't exist")
    except:
        return HTTPException(status_code=409, detail="Error with the CRUD operations")
    
    
@router.patch("/{product_id}")
async def update_product_data(request: Request, product_id: PyObjectId=Path(...) ,updated_data: Dict[str, str | float]=Body(...)):
    try:
        if (await request.app.mongodb["products"].find_one({"_id": product_id})) != None:
            for field in updated_data:
                await request.app.mongodb["products"].update_one({"_id": product_id}, {
                    "$set": {field: updated_data[field]}
                    })
        else:
            return HTTPException(status_code=404)
    except:
        return {"Message": "Error with the CRUD operations"}
    pass
@router.delete("/{product_id}")
async def remove_product(request: Request , product_id: PyObjectId=Path(...)):
    try:
        if (await request.app.mongodb["products"].find_one({"_id": product_id})) != None:
            await request.app.mongodb["products"].delete_one({"_id": product_id})
        else:
            return HTTPException(status_code=404)
    except:
        return {"Message": "Error with the CRUD operations"}
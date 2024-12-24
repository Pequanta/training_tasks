from fastapi import APIRouter, Request, HTTPException
from fastapi import Body, Path
from typing import Dict, List
from models import UserDataModel, PyObjectId
from pymongo.errors import DuplicateKeyError 
import logging 
router = APIRouter()


@router.get("/{user_id}")
async def get_user(request: Request, user_id: PyObjectId=Path(...)):
    try:
        if (user := await request.app.mongodb["users"].find_one({"_id": user_id})) != None:
            user["_id"] = str(user["_id"])
            return user
        else:
            return HTTPException(status_code=404 , detail="user not found")
    except:
        return HTTPException(status_code=409, detail="Error with the CRUD operations")
    

@router.post("/")
async def create_user(request: Request, user: UserDataModel=Body(...)):
    user_ = user.model_dump()
    user_["_id"] = user_.pop("id")
    try:
        if (await request.app.mongodb["users"].find_one({"_id": user_["_id"]})) == None:
            await request.app.mongodb["users"].insert_one(user_)
            logging.info("The user is inserted suffessfully")
        else:
            logging.error("The user already exists")
            return HTTPException(status_code=409, detail="The user already exists")
    except DuplicateKeyError:
        logging.error("The user name must be unique")
    except:
        logging.error("Something went wrong with the server!!!!!")
        return HTTPException(status_code=409, detail="Error with the CRUD operations")
    

@router.put("/{user_id}")
async def update_user(request: Request, new_user: UserDataModel, user_id: PyObjectId=Path(...)):
    new_user = new_user.model_dump()
    new_user.pop("id")
    try:
        if (await request.app.mongodb["users"].find_one({"_id": user_id})) != None:
            new_user["_id"] = user_id
            await request.app.mongodb["users"].replace_one({"_id": user_id}, new_user)
        else:
            return HTTPException(status_code=404, detail="The user with the given id doesn't exist")
    except:
        return HTTPException(status_code=409, detail="Error with the CRUD operations")
    
    
@router.patch("/{user_id}")
async def update_user_data(request: Request, user_id: PyObjectId=Path(...) ,updated_data: Dict[str, str | float]=Body(...)):
    try:
        if (await request.app.mongodb["users"].find_one({"_id": user_id})) != None:
            for field in updated_data:
                await request.app.mongodb["users"].update_one({"_id": user_id}, {
                    "$set": {field: updated_data[field]}
                    })
        else:
            return HTTPException(status_code=404)
    except:
        return {"Message": "Error with the CRUD operations"}
    pass    
@router.delete("/{user_id}")
async def remove_user(request: Request , user_id: PyObjectId=Path(...)):
    try:
        if (await request.app.mongodb["users"].find_one({"_id": user_id})) != None:
            await request.app.mongodb["users"].delete_one({"_id": user_id})
        else:
            return HTTPException(status_code=404)
    except:
        return {"Message": "Error with the CRUD operations"}
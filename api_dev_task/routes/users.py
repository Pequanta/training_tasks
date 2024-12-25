from fastapi import APIRouter, Request, HTTPException
from fastapi import Body, Path
from fastapi.encoders import jsonable_encoder
from typing import Dict, List
from models import UserDataModel, PyObjectId
from pymongo.errors import DuplicateKeyError , PyMongoError
import redis.asyncio as redis_here
import logging 
router = APIRouter()


@router.get("/{user_id}")
async def get_user(request: Request, user_id: PyObjectId=Path(...)):
    if (user_from_cache := await request.app.redis.get(str(user_id))) != None:
        return jsonable_encoder(user_from_cache)
    
    try:
        if (user := await request.app.mongodb["users"].find_one({"_id": user_id})) != None:
            user["_id"] = str(user["_id"])
            print(str(user_id))
            await request.app.redis.set(str(user_id), user)
            return user
        else:
            return HTTPException(status_code=404 , detail="user not found")
    except PyMongoError as e:
            logging.exception(f"MongoDB error: {str(e)}")
            raise HTTPException(status_code=500, detail="MongoDB operation failed") from e
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
            ##user lists conventionally persist
            id = user_.pop("_id")
            print(user_)
            await request.app.redis.set(str(id), jsonable_encoder(user_))
            print(user_)
            return user_
        else:
            logging.error("The user already exists")
            return HTTPException(status_code=409, detail="The user already exists")
    except DuplicateKeyError:
        logging.error("The user name must be unique")
    except PyMongoError as e:
            logging.exception(f"MongoDB error: {str(e)}")
            raise HTTPException(status_code=500, detail="MongoDB operation failed") from e
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
            ##the cache is updated with the new data:
            await request.app.redis.set(user_id, new_user)
            await request.app.mongodb["users"].replace_one({"_id": user_id}, new_user)
        else:
            return HTTPException(status_code=404, detail="The user with the given id doesn't exist")
    except PyMongoError as e:
        logging.exception(f"MongoDB error: {str(e)}")
        raise HTTPException(status_code=500, detail="MongoDB operation failed") from e
    except:
        return HTTPException(status_code=409, detail="Error with the CRUD operations")
    
    
@router.patch("/{user_id}")
async def update_user_data(request: Request, user_id: PyObjectId=Path(...) ,updated_data: Dict[str, str | float]=Body(...)):
    try:
        updated_data = {}
        if (user:= await request.app.mongodb["users"].find_one({"_id": user_id})) != None:
            for field in updated_data:
                await request.app.mongodb["users"].update_one({"_id": user_id}, {
                    "$set": {field: updated_data[field]}
                    })
                updated_data[field] = updated_data
            for field in user:
                if field in updated_data:
                    user[field] = updated_data[field]
            await request.app.redis.set(user["_id"], user)
        else:
            return HTTPException(status_code=404)
    except PyMongoError as e:
        logging.exception(f"MongoDB error: {str(e)}")
        raise HTTPException(status_code=500, detail="MongoDB operation failed") from e
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
    except PyMongoError as e:
        logging.exception(f"MongoDB error: {str(e)}")
        raise HTTPException(status_code=500, detail="MongoDB operation failed") from e
    except:
        return {"Message": "Error with the CRUD operations"}
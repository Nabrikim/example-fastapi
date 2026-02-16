from fastapi import status,Depends,HTTPException,APIRouter,Request
from .. import schemas
from ..utils import hashed_password
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db



router = APIRouter(
    prefix = "/users",
    tags=["USERS"]
)


#Create User
@router.post("/", status_code = status.HTTP_201_CREATED,response_model = schemas.UserOut)
def create_user(user:schemas.UserCreate,request:Request,db:Session = Depends(get_db)):

    #hash the password
    new_hash = hashed_password(user.password)
    user.password = new_hash
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    #1.The request line details
    print(f"Method;{request.method}")
    print(f"URL:{request.url}")

    #2.The Headers
    #Browsers send these automatically
    headers = request.headers
    print(f"Browser Info: {headers.get('user-agent')}")
    print(f"Content:Type:{headers.get("content-type")}")


    #3.Client details
    #This tells you the ip address and port of the user
    print(f"Client Ip:{request.client.host}")

    #4.The Body(The JSON data)
    body = request.json()
    print(f"Data received:{body}")

    #5. Extract the Authorization Header
    auth_header = request.headers.get("authorization")
    print(f"The authorization header :{auth_header}")



    return new_user

@router.get("/{id}",response_model = schemas.UserOut)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"user with id:{id} does not exist")
    return user
    
    


    

 
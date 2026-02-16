from fastapi import APIRouter,HTTPException,status,Depends,Response,Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database,schemas,models,utils,oath_2
 
router = APIRouter(
    tags =["Authentication"]
)

@router.post("/login",response_model=schemas.Token)
def login(request:Request,user_credentials:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()



    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail =f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail= f"Invalid credentials")
    
    #create token
    access_token = oath_2.create_access_token(data = {"user_id":str(user.id)})
    auth_header = request.headers.get("authorization")
    # parts = auth_header.split()
    # prefix = parts[0]
    # token = parts[1]
    

    #return token

    return{"access_token":access_token,"token_type":"bearer"}
    


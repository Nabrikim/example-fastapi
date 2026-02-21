from fastapi import status,Depends,HTTPException,APIRouter,Request
from typing import List,Optional
from .. import schemas
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import oath_2
from sqlalchemy import func

router = APIRouter(
    prefix = "/posts",
    tags= ["POSTS"]
)
#get all posts










@router.get("/",response_model = List[schemas.PostOut])
def get_posts(db:Session  = Depends(get_db),current_user:int = Depends(oath_2.get_current_user),limit:int = 10,skip:int = 0,search:Optional[str] = ""):
    posts = db.query(models.Post).all()
    #referred_posts = [post for post in posts if post.owner_id == current_user.id]

    results = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id ==  models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)



    return results
    


#Create post
@router.post('/',status_code = status.HTTP_201_CREATED,response_model = schemas.Post)
def create_posts(request:Request,post:schemas.PostCreate,db:Session = Depends(get_db),current_user:int = Depends(oath_2.get_current_user)):

    new_post = models.Post(**post.dict(),owner_id = current_user.id)
    print(current_user)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    print(new_post)

    return new_post



#get latest post
@router.get("/latest")
def get_latest_post(db:Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()

    return latest_post

#get one post
@router.get("/{id}",response_model= schemas.PostOut)
def get_post(id:int,db:Session= Depends(get_db),current_user :int = Depends(oath_2.get_current_user)):
    post = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id ==  models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code = status.HTTP_400_NOT_FOUND, detail=f"post with id{id} was not found")
    
    if post[0].owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f"Authorization Forbidden")
    
    
    return post
    

#delete content
@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),current_user :int = Depends(oath_2.get_current_user)):


    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist")
    
    if deleted_post.first().id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform specific action")
    
        
    
    deleted_post.delete(synchronize_session=False)
    db.commit()

    
    return{"Deleted_post":deleted_post}




@router.put("/{id}", response_model = schemas.Post)
def update_posts(post:schemas.PostCreate,id:int,db:Session = Depends(get_db),current_user :int = Depends(oath_2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"Post with id:{id} does not exist")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform requested action")
    
    
    post_query.update(post.dict(),synchronize_session =False)
    db.commit()

    return post_query.first()


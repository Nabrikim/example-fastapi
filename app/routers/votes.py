from fastapi import FastAPI, Response, status,HTTPException,Depends, APIRouter
from .. import database,schemas,models,oath_2
from sqlalchemy.orm import Session
router = APIRouter(
    prefix = "/vote",
    tags=['Vote']
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(votes:schemas.Vote,current_user: int = Depends(oath_2.get_current_user),db:Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == votes.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {votes.post_id} does not exist")
    
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == votes.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if (votes.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User {current_user.id} has already voted on post {votes.post_id}")
        
        elif not found_vote:
            new_vote = models.Votes(post_id = votes.post_id,user_id = current_user.id)
            db.add(new_vote)
            db.commit()

            return{"message":"successfully added vote"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post_id:{votes.post_id} does not exist")
        
    
    

        
    else:
        if not found_vote:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Vote does not exist")
        
        vote_query.delete(synchronize_session=False)

        return{"message":"Successfully deleted the message"}







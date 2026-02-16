from fastapi.params import Body
from fastapi import FastAPI,Response,status,HTTPException,APIRouter,Request
from pydantic import BaseModel,EmailStr
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from app import models,schemas
import time 
from app.utils import hashed_password,verify
from app.routers import posts,user
from app import oath_2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm,OAuth2PasswordBearer


app = FastAPI
oath_2 = OAuth2PasswordBearer()

#When we want the user interface to give us specific data we use a schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating:Optional[int] = None

while True:
    try:
    #connect to an exisitng database
        #conn = psycopg2.connect(host, database, user, password)
        conn = psycopg2.connect(host = 'localhost',database= 'fastapi', user='postgres', password = '0722jkdkeLL',cursor_factory = RealDictCursor)# Im the pipe connecting the two points
        cursor = conn.cursor() # im the fetcher and delivery guy
        print("Database connection was succesful")
        break

    except Exception as error:
        print("Failed to connect to the database")
        print(f"Error:{error}")
        time.sleep(1)

#get all posts using psycopg2
@app.get("/")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return{"message": my_posts} 
 
#Create post using psycopg2
@app.post('/posts',status_code = status.HTTP_201_CREATED)
def create_posts(post:Post): 
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING *""",(post.title,post.content,post.Published))
    new_post = cursor.fetchone()
    conn.commit()

    return{"New post":new_post}

#get latest post using psycopg2
@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("""SELECT * FROM posts ORDER BY "ID" DESC LIMIT 1""") # im using quotes in "ID" so that it remains in capital letters
    latest_post = cursor.fetchone()
    return{"detail":latest_post}

#get one post using psycopg2
@app.get("/posts/{id}")
def get_post(id:str):
    cursor.execute("""SELECT * FROM posts WHERE "ID" = (%s)""",(id))
    my_post = cursor.fetchone()
    if not my_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return {"message":my_post}

#delete content using psycopg2
@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE "ID" = (%s) RETURNING *""",(str(id)))
    deleted_post = cursor.fetchone()  
    conn.commit()
    return{"Deleted_post":deleted_post}

@app.put("/posts/{id}")
def update_posts(id:int,post:Post):
    cursor.execute("""UPDATE posts SET title = %s,content = %s, published = %s WHERE "ID" = %s RETURNING *""",(post.title,post.content,post.Published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"Post with id:{id} does not exist")
    
    return {"data":updated_post}

my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},{"title":"Favourite foods","content":"I like pizza","id":2}]




#get post
@app.get("/")
def get_posts():
    return{"message": my_posts}  #json.dumps()   ---- convert python objects into json 
    

#create posts
@app.post('/createposts')
def create_posts(payload:dict = Body()): #json.loads()
    # storage.update(payload)
    # print(storage)
    return{"message":f"{payload['title']} for me {payload['content']}" }


#create posts
@app.post('/createposts')
def create_posts(new_post:Post): #json.loads()
    # storage.update(payload)
    # print(storage)
    print(new_post)
    print(new_post.dict())
    return {"data":new_post}
    return {"data":"Succefully returned"}

"""
Create------ POST   @app.post("/posts)
Read------- GET     @app.get("/posts/id") or  @app.get("/posts")
Update----- PUT/PATCH @app.put("/posts/{id}")
Delete----- DELETE @app.delete("/posts/{id}")
"""

#create posts
@app.post('/createposts')
def create_posts(post:Post): 
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    if not any(item['id'] == post_dict['id'] for item in my_posts) :
        my_posts.append(post_dict)

    print(my_posts)


    return {"data":post_dict}


#get latest post
@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[len(my_posts) - 1]
    return{"detail":latest_post}

#get one post
@app.get("/posts/{id}")
def get_post(id:int):
    print(id)
    my_post = [post for post in my_posts if int(post['id']) == id]
    return {"message":my_post}


#get one post
@app.get("/posts/{id}")
def get_post(id:int,response:Response):
    print(id)
    my_post = [post for post in my_posts if int(post['id']) == id]
    if not my_post:
        response.status_code = 404
        my_post = None
    return {"message":my_post}

#get one post
@app.get("/posts/{id}")
def get_post(id:int,response:Response):
    print(id)
    my_post = [post for post in my_posts if int(post['id']) == id]
    if not my_post:
        response.status_code = status.HTTP_404_NOT_FOUND
        my_post = None
        return{'message':f"post with id {id} was not found"}
    return {"message":my_post}

#Create post
@app.post('/posts',status_code = status.HTTP_201_CREATED)
def create_posts(post:Post): 
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    if not any(item['id'] == post_dict['id'] for item in my_posts) :
        my_posts.append(post_dict)
    print(my_posts)
    return {"data":post_dict}


#delete content
@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    #delete post
    my_post_index = [index for index,post in enumerate(my_posts) if int(post['id']) == id][0]
    my_posts.pop(my_post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#delete content
@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    #delete post
    my_post_index = next((index for index,post in enumerate(my_posts) if int(post['id']) == id),None)

    if my_post_index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
    

    my_posts.pop(my_post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

#delete content
@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    #delete post
    indices = [index for index,post in enumerate(my_posts) if int(post['id']) == id]

    if not indices:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
    
    my_post_index = indices[0]
    my_posts.pop(my_post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)  

@app.put("/posts/{id}")
def update_posts(id:int,post:Post):

    
    index = next((index for index,post in enumerate(my_posts) if int(post['id']) == id),None)



    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
    
    post_dict = post.dict()
    post_dict['id'] = id

    my_posts[index] = post_dict
    print(my_posts)

    return{"data": post_dict}

#SELECT * FROM products WHERE id = 3;
#SELECT id AS products_id FROM products;
#SELECT * products WHERE inventory = 0;
#SELECT * products WHERE name = 'TV';
#SELECT * products WHERE price >= 50;
#SELECT * FROM products WHERE inventory != 0; also SELECT * FROM products WHERE inventory <> 0;
#SELECT * FROM products WHERE inventory > 0 AND price > 0;
#SELECT * FROM products WHERE inventory > 0 OR price > 0;
#SELECT * FROM products WHERE id = 1 OR id = 2 OR id = 3;
#SELECT * FROM products WHERE id IN(1,2,3);
#SELECT * FROM products WHERE name LIKE 'TV %';
#SELECT * FROM products WHERE name LIKE '%e';
#SELECT * FROM products WHERE name LIKE '%en%';
# SELECT * FROM products ORDER BY price ASC;
# SELECT * FROM products ORDER BY price DEC;
# SELECT * FROM products ORDER BY inventory DESC;
# SELECT * FROM products ORDER BY inventory DESC, price ASC;
# SELECT * FROM products ORDER BY created_at ASC;
# SELECT * FROM products ORDER BY created_at DESC;
# SELECT * FROM products WHERE inventory > 0 ORDER BY created_at DESC;
# SELECT * FROM products WHERE price > 10 LIMIT 2;
# SELECT * FROM products WHERE price > 10 ORDER BY id LIMIT 5;
# SELECT * FROM products WHERE price > 10 ORDER BY id LIMIT 5 OFFSET 2;
#INSERT INTO products (name,price,inventory) VALUES('Rolex',2000,12);
#INSERT INTO products (name,price,inventory) VALUES('Rolls Royce',200000,3) RETURNING *;
#DELETE FROM products WHERE id = 10;
#DELETE FROM products WHERE id = 10;
#DELETE FROM products WHERE name = 'laptop' RETURNING * ;
#UPDATE products SET is_sale = true WHERE name = 'Flask' RETURNING *;
#UPDATE products SET is_sale = false WHERE name = 'car' RETURNING *;
#UPDATE products SET is_sale = true WHERE id > 15 returning *;

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session

from fastapi import FastAPI,Response,status,HTTPException,Depends


SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionlocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base() # Used to define the Schema for the database

#models.Base.metadata.create_all(bind=engine)
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/sqlalchemy")
def get_post(db:Session  = Depends(get_db)):
    return{"success"}

@app.get("/sqlalchemy")
def get_post(db:Session  = Depends(get_db)):
    posts = db.query(models.Post).all()
    return{"Data": posts}

#Create post using sqlalchemy
@app.post('/posts',status_code = status.HTTP_201_CREATED)
def create_posts(post:Post,db:Session = Depends(get_db)): 

    print(post.dict())
    new_post = models.Post(title = post.title,content = post.content,published = post.Published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return{"data":new_post}

#get one post
@app.get("/posts/{id}")
def get_post(id:int,db:Session= Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first() 
    print(post)

    if not post:
        raise HTTPException(status_code = status.HTTP_400_NOT_FOUND, detail=f"post with id{id} was not found")
    
    return {"post_detail":post}


#delete content
@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db)):

    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()

    
    return{"Deleted_post":deleted_post}

@app.put("/posts/{id}")
def update_posts(post:Post,id:int,db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"Post with id:{id} does not exist")
    
    post_query.update(post.dict(),synchronize_session =False)
    db.commit()

    return{"data":post_query.first()}


from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(BaseModel):
    id:int
    created_at: datetime

    class Config:
        from_attributes = True

models.Base.metadata.create_all(bind = engine)

class Post(BaseModel):
    title:str
    content:str
    published: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        from_attributes = True    

#Create User
@app.post("/user", status_code = status.HTTP_201_CREATED,response_model = schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#Create User
@app.post("/user", status_code = status.HTTP_201_CREATED,response_model = schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):

    #hash the password
    new_hash = hashed_password(user.password)
    user.password = new_hash
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


router = APIRouter()

router = APIRouter(
    prefix = "/users",
    tags=["USERS"])

app.include_router(user)


# POST /posts/create HTTP/1.1
# Host: 127.0.0.1:8000
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0
# Content-Type: application/json
# Accept: application/json
# Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
# Content-Length: 55

# {
#     "title": "My Post",
#     "content": "This is the body"

from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/posts/create")
async def monitor_request(request: Request):
    # 1. The Request Line details
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")

    # 2. The Headers (Metadata)
    # Browsers send these automatically
    headers = request.headers
    print(f"Browser Info: {headers.get('user-agent')}")
    print(f"Content Type: {headers.get('content-type')}")
    
    # 3. Client Details
    # This tells you the IP address and Port of the user
    print(f"Client IP: {request.client.host}")

    # 4. The Body (The JSON data)
    body = await request.json()
    print(f"Data received: {body}")

    return {"status": "I saw everything you sent!"}

"""
The header :algorithm and the type of token(JWT)
The payload: Subject,Expiratin time in minutes,Custom_data
The secret key : an encoded hash

Signature: The header, The payload and the secret key
Token: The header, The payload and the signature
"""

from jose import JWTError,jwt
from datetime import datetime,timedelta


#------- HEADER--------
#SECERET KEY
#ALGORITHM
#EXPIRATION TIME

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES) 
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt


from fastapi import APIRouter,HTTPException,status,Depends,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database,schemas,models,utils,oath_2
 
router = APIRouter(
    tags =["Authentication"]
)

@router.post("/login")
def login(user_credentials:OAuth2PasswordRequestForm,db:Session = Depends(database.get_db)):
        #OAuth2PasswordRequestForm... will return username and password not this user_credentials.email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()



    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail =f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"Invalid credentials")
    
    #create token
    access_token = oath_2.create_access_token(data = {"user_id":user.id})

    #return token

    return{"access_token":access_token,"token_type":"bearer"}
    

@app.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Invalid credentials")\
        
    if not(verify(user_credentials.password)):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Invalid credentials")\
        
    token = oath_2.create_access_token(data = {"user":user.id})

    return{"access_token":token,"token_type":"bearer"}


def access_token(data):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update(expire) #---Payload
    #Algorithm ----- Header
    #SECRET KEY ----- secret key

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm = ALGORITHM)
    return encoded_jwt



def verify_access_token(token:str, credentials_exception):
    payload = jwt.decode(token,SECRET_KEY,algorithm = ALGORITHM) #YOU WILL GET THE PAYLOAD


    def verify_access_token(token:str, credentials_exception):
        try:
            payload = jwt.decode(token,SECRET_KEY,algorithm = [ALGORITHM]) #YOU WILL GET THE PAYLOAD

            id : str = payload.get("user_id")

            if id is None :
                raise credentials_exception
            token_data = schemas.TokenData(id = id)
            
        except JWTError:
            raise credentials_exception
        

        return token_data

def get_current_user(token:str = Depends(oath_2)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials")

    return verify_access_token(token,credentials_exception)





def access_create_token(data):
    to_encode = data.copy()
    expire = datetime.utcnow() + datetime.deltatime(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update(expire)

    token = jwt.encode(to_encode,SECRET_KEY,algorithm = [ALGORITHM])
    return token

def verify_access_token(token:str,credentials):
    payload = jwt.decode(token,SECRET_KEY,algorithm = [ALGORITHM])

    id = payload.get("user_id")

    if not id:
        raise credentials
    token_data = schemas.TokenData(id = id)

    return token_data


def get_current_user(token:str,credentials):
    credentials = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details = f"No token available")
    return verify_access_token(token,credentials)


from fastapi import status,Depends,HTTPException,APIRouter,Request
from typing import List
from .. import schemas
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import oath_2

router = APIRouter(
    prefix = "/posts",
    tags= ["POSTS"]
)
#get all posts










@router.get("/", response_model=List[schemas.Post])
def get_posts(db:Session  = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
    


#Create post
@router.post('/',status_code = status.HTTP_201_CREATED,response_model = schemas.Post)
def create_posts(request:Request,post:schemas.PostCreate,db:Session = Depends(get_db),user_id:int = Depends(oath_2.get_current_user)):

    new_post = models.Post(**post.dict())
    print(user_id)
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
@router.get("/{id}",response_model= schemas.Post)
def get_post(id:int,db:Session= Depends(get_db),user_id :int = Depends(oath_2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first() 
    print(post)

    if not post:
        raise HTTPException(status_code = status.HTTP_400_NOT_FOUND, detail=f"post with id{id} was not found")
    
    return post
    

#delete content
@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),user_id :int = Depends(oath_2.get_current_user)):

    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()

    
    return{"Deleted_post":deleted_post}




@router.put("/{id}", response_model = schemas.Post)
def update_posts(post:schemas.PostCreate,id:int,db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"Post with id:{id} does not exist")
    
    post_query.update(post.dict(),synchronize_session =False)
    db.commit()

    return{"data":post_query.first()}

#SELECT * FROM posts LEFT JOIN users ON posts.owner_id = users.id;
#SELECT title,content,email FROM posts LEFT JOIN users ON posts.owner_id = users.id;
#SELECT posts.id, email FROM posts LEFT JOIN users ON posts.owner_id = users.id;
#SELECT posts.* FROM posts LEFT JOIN users ON posts.owner_id = users.id;
#SELECT users.id,COUNT(*) FROM posts LEFT JOIN users ON posts.owner_id = users.id group by users.id ;
#SELECT users.id,COUNT(*) FROM posts RIGHT JOIN users ON posts.owner_id = users.id group by users.id ;.... IT shows the number of posts shown
#select posts.id, COUNT(post_id) from posts left join votes on posts.id = votes.post_id group by posts.id;
#select posts.id , COUNT(post_id) as likes from posts left join votes on posts.id = votes.post_id where posts.id = 10 group by posts.id ;
#select posts.* , COUNT(post_id) as likes from posts left join votes on posts.id = votes.post_id  group by posts.id ;


#DATABASE MIGRATIONS
"""
Developers can track changes to code and rollback code easily 
with GIT. Why can't we do the same for database models/tables

Database migrations allow us to incrementally track changes to database
schema and rollback changes to any point in time

We will use a tool called Alembic to make changes to our 
database

Alembic can also automatically pull database models from sqlalchemy 
and generate the proper tables

alembic --help
alembic init alembic

sqlalchemy.url = postgresql://postgres:0722jkdkeLL@localhost:5432/fastapi
config = context.config
config.set_main_option("sqlalchemy.url",'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}')
alembic revision --help
alembic revision -m "create posts table"

1. from alembic import op
The op (Operations) object is the most important part of a migration file. It is a set of "directives" that tell the database exactly what to change.

Instead of writing raw SQL, you use op methods. When you run the migration, Alembic translates these methods into the specific SQL dialect for your database (like PostgreSQL).

-------------------------------------------------
op.create_table(): Creates a new table.

op.add_column(): Adds a column to an existing table.

op.drop_table(): Deletes a table (used in the downgrade function).

op.alter_column(): Changes a column's type or nullability.
----------------------------------------------------------

2. import sqlalchemy as sa
While op provides the actions (the verbs), sa (SQLAlchemy) 
provides the definitions (the nouns). 
You use sa to define the data types and constraints
 of the columns you are creating or modifying.

--------------------------------------------------------------------------------------

. The upgrade() and downgrade() functions
In every migration file, you will see two functions that use these imports:

upgrade(): This runs when you type alembic 
upgrade head. It uses op to move your database 
forward (e.g., adding a table).
alembic upgrade 4b7228577b09
alembic upgrade heads



downgrade(): This runs when you type alembic 
downgrade -1. It should do the exact opposite 
of the upgrade (e.g., dropping the table you just 
added). This is your "Undo" button.
alembic downgrade 4b7228577b09... you downgrade to this exact revision you had created before 4b7228577b09.


alembic revision -m "add user table"

 op.drop_column('posts','content')

alembic history
alembic revision --autogenerate -m"auto-vote"


""""""
Cross Origin Resource Sharing(CORS) allows you to make
requests from a web browser on one domain to a server 
on a different domain

By default our API will only allow web browsers running on the same domain
as our server to make requests to it
fetch('http://localhost:8000/').then(res => res.json()).then(console.log)
"""
from fastapi.middleware.cors import CORSMiddleware

# origins = ["https://www.google.com","https://www.youtube.com"]
origins = ["*"]# for every domain
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials = True,
                   allow_methods=["*"],
                   allow_headers=["*"],)



#pip freeze > requirements.txt
#pip install -r requirements.txt

"""
-------
GIT
------
git init
git add --all
git commit -m "Initial Commit" # it will first bring an errror for you to provide your user account and password for your github
git config --global user.email brayosanta@gmail.com
git config --global user.name Nabrikim
git commit -m "Initial Commit"
git branch -M main
git remote add origin https://github.com/Nabrikim/example-fastapi.git
git push -u origin main
git remote


# to save changes in git
 git add learned_codes.py
  git status
  git commit -m "updated only the database connection logic"
  git push

"""


""""
==========
HEROKU
========
heroku --version
heroku login
heroku create name

render
uvicorn app.main:app --host 0.0.0.0 --port $PORT

"""
    



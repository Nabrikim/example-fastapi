# # def add_sprinkles(func):
# #     def wrapper():
# #         print("You add Sprinkles")
# #         func()
# #     return wrapper


# # @add_sprinkles
# # def get_ice_cream():
# #     print("This is an ice cream")

# # get_ice_cream()

# import json
# my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},{"title":"Favourite foods","content":"I like pizza","id":2}]

# my_posts = json.dumps(my_posts)
# print(json.loads(my_posts))

# def add_sprinkles(func):
#     def wrapper():
#         print("Add sprinkles on top")
#         func()
#     return wrapper

# @add_sprinkles
# def get_ice_cream():
#     print("whata wonderful Icecream")

# get_ice_cream()

# # import psycopg2
# # from psycopg2.extras import RealDictCursor
# # import time
# # while True:
# #     try:
# #         print("Attempting to connect to postgres")
# #         conn = psycopg2.connect(host = "localhost",database = "fastapi",user="postgres",password = "0722jkdkeLL",cursor_factory=RealDictCursor)
# #         cursor = conn.cursor()

# #         print("Succesful connection to the database")
# #         break

# #     except Exception as error:
# #         print("Failed connection to the database")
# #         print(f"error:{error}")
# #         time.sleep(2)

# import os
# path = os.getenv("MY_DB_URL")
# print(path)

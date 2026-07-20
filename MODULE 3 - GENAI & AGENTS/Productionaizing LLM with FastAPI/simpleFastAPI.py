#FastAPI: It is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. The key features are:
# Fast: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic). One of the fastest Python frameworks available.    
# It is a way to expose our builyn models and functions as REST APIs, so that anyone can use our functionality/model/project as an API.

# How FastAPI runs the API's? 
#It will use uvicorn as the ASGI(Asynchronous Server Gateway Interface) server to run the API's. Uvicorn is a lightning-fast ASGI server implementation, using uvloop and httptools.

#We installed FastAPI and uvicorn using pip install fastapi uvicorn

#http://127.0.0.1:8000/docs - This will give the swagger for the API's we have created. We can test the API's from this swagger page itself.


from fastapi import FastAPI

api = FastAPI()

@api.get("/")
def home():
    return {"message":"Hello, welcome to home endpoint"}

@api.get("/greet/{name}")    
def greet(name:str):
    return {"message":f"Hello {name}, welcome to greetendpoint"}

@api.get("/add")
def add(a: int,b: int):
    return {"result":a+b}





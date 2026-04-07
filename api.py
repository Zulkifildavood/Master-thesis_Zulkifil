from fastapi import FastAPI
from pydantic import BaseModel as BM

app = FastAPI()

class Task(BM):
    Title: str
    Description: str | None = none
    completed :bool = False 
    
@app.post("/tasks")
def create_task(task: Task):
    
    return {"Message: Task Created, Data":Task}

#FastAPI helps detects the error automatically that it saves time writing error handling 
#path varables denoted by parenthesis {}
#httpextensions helps to create the error handling mechanism easier

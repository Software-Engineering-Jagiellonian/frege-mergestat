from typing import Union
from fastapi import FastAPI
import subprocess
from pydantic import BaseModel
import json

class MergestatQuery(BaseModel):
    query: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/echo")
def mergestat(mergestat_query: MergestatQuery = None):
    if mergestat_query:
        #result = subprocess.run(["echo", mergestat_query.query], capture_output=True)
        result = subprocess.check_output(f"echo {mergestat_query.query}", shell=True, universal_newlines=True)
        return result
    else:
        return {"message": "Body not defined"}

@app.post("/mergestat")
def mergestat(mergestat_query: MergestatQuery = None):
    if mergestat_query:
        #result = subprocess.run(["/app/mergestat", mergestat_query.query], capture_output=True)
        result = subprocess.check_output(f"/app/mergestat {mergestat_query.query}", shell=True, universal_newlines=True)
        return json.loads(result)
    else:
        return {"message": "Body not defined"}

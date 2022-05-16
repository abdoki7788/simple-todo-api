from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

todos = []

origins = [
    "http://localhost",
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
	id: int
	text: str
	isDone: bool=False

@app.get('/')
def root():
	return todos

@app.post('/')
def create_todo(item: Item):
	todos.append(dict(item))
	return item

@app.get('/{id}')
def item(id: int):
	try:
		data = list(filter(lambda i: i["id"] == id, todos))[0]
	except IndexError:
		raise HTTPException(detail="todo not found", status_code=404)
	except:
		raise HTTPException(detail="todo not found", status_code=422)
	return data


@app.put('/{id}')
def item(id: int, item: Item):
	try:
		filtered = list(filter(lambda i: i["id"] == id, todos))[0]
		index = todos.index(filtered)
		todos[index] = dict(item)
	except IndexError:
		raise HTTPException(detail="todo not found", status_code=404)
	except:
		raise HTTPException(detail="something went wrong", status_code=422)
	return todos[index]




@app.delete('/{id}', status_code=204)
def item(id: int):
	try:
		filtered = list(filter(lambda i: i["id"] == id, todos))[0]
		index = todos.index(filtered)
		del todos[index]
		return HTTPException(detail="something went wrong", status_code=201)
	except IndexError:
		raise HTTPException(detail="todo not found", status_code=404)
	except:
		raise HTTPException(detail="something went wrong", status_code=422)

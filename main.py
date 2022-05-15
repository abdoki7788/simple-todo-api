from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

todos = []


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
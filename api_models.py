from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tags: list[str] = []
    tax: float | None = None


@app.get("/")
async def read_root():
    return {"message": "1-page"}


@app.get('/items')
async def read_items() -> list[Item]:
    return [
        # misol1
        Item(name='test name 1', description='test description', price=123, tags=['tag1']),
        # misol2
        Item(name='test name 2', description='test description', price=321, tags=['tag2']),
        # misol3
        Item(name='test name 3', description='test description', price=456, tags=['tag3']),
        # misol4
        Item(name='test name 4', description='test description', price=678, tags=['tag4']),
        # misol5
        Item(name='test name 5', description='test description', price=789, tags=['tag5']),
    ]


@app.post('/item_post')
async def create_item(item: Item) -> Item:
    return item


'''example for post  insomnia
{
    "name": "test",
    "description": "atest",
    "price": 100.25,
    "tags": [],
    "tax": null
}

{
    "name": "test2",
    "description": "testdeescription",
    "price": 34.25,
    "tags": [],
    "tax": null
}
{
    "name": "fast",
    "description": "apitest",
    "price": 10.10,
    "tags": [],
    "tax": null
}
{
    "name": "test4",
    "description": "fastapidescriptions",
    "price": 10.25,
    "tags": [],
    "tax": null
}
{
    "name": "finally",
    "description": "description5",
    "price": 20.20,
    "tags": [],
    "tax": null
}
'''
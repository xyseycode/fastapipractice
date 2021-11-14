from os import stat
from fastapi import FastAPI, status, HTTPException, Response
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


try:
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="pink5ive",
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()

    print("Database connection success!")
except Exception as e:
    print("Database Connection failed")
    print(e)


@app.get("/")
def index():
    return {"message": "Index page"}


@app.get("/posts")
def get_posts():
    cursor.execute("""Select * from posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"Post with id of {id} not found."
        )
    return {"data": post}


@app.post("/posts", status_code=HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()

    conn.commit()
    return {"new post": new_post}


@app.delete("/posts/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"Post with id of {id} not found."
        )
    return {"deleted post": deleted_post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"Post with id of {id} not found."
        )
    return {"updated post": updated_post}

from fastapi import FastAPI, Request, Response, HTTPException
from .comments import create_post

comments = []
app = FastAPI()


@app.get("/")
def root(request: Request):
    return Response(content="Welcome to Vox Pop", status_code=200)


@app.post("/new")
def add_post(content: str = "", category: str = ""):
    if content == "" and category == "":
        raise HTTPException(
            detail="Content and category are not defined", status_code=400
        )
    elif content == "":
        raise HTTPException(
            detail="Content is not defined", status_code=400
        )
    elif category == "":
        raise HTTPException(
            detail="Category is not defined", status_code=400
        )

    if category.lower() not in ["positive", "negative"]:
        raise HTTPException(
            detail=f"{category} is not valid category", status_code=400
        )

    category = category.lower()
    new_post = create_post(content, category)
    comments.append(new_post)
    print(comments)
    return {"message": "post succesfully posted"}


@app.get("/posts")
def get_posts(page: int = 1, limit: int = 5):
    print(comments)
    if page <= 0 or limit <= 0:
        raise HTTPException(
            status_code=400, detail="page and limit must be greater than 0"
        )

    index_of_first_post = limit * (page - 1)
    if index_of_first_post >= len(comments):
        raise HTTPException(
            status_code=400, detail="comments are out of range"
        )

    comments_to_show = []
    for i in range(limit):
        if index_of_first_post + i >= len(comments):
            break
        comments_to_show.append(comments[index_of_first_post + i])

    return {"comments": comments_to_show}
# Usage

To get started from the root directory run

```bash
cd backend && poetry shell && poetry install # activate virutal environment and install dependencies
export DATBASE_URL=... # exporting environment variables to establish the connection to our database on the startup of our backend
uvicorn app.main:app --reload
```

Now if you go to `http://127.0.0.1:8000`, you should see `{"Hello":"Adib!"}`, (bonus : FastAPI has built-in documentation for this project so by going to `http://127.0.0.1:8000/docs` you will see all routes, descriptions of it and can even interact with it since you can specifiy any variables or parameters )

Note your API key is simply your username plus password.

# To do

- Add an image
- Add an image privately
- Add in bulk

- Encrypt passwords and don't store them in plaintexts
- Test
- Document properly

# Questions

- How to run all tests in `pytest` instead of specifying the file. Also, why does `pytest *` run twice?

# Things I learned

- FastAPI offers two ways of handling file uploads by clients: `File` and `UploadFile` function. For this project I chose to work with `UploadFile` because for this challenge there's no specifcation for image file sizes. Therefore it would be best to work with `UploadFile` since it uses a "spooled" file meaning that the file will be stored in memory, but if it exceeds the limit then additional memory is stored in disk. `File` only stores files in memory.
- If your tests need to use the database, connect to it and then disconnect it so that you won't have any running processes which may interfere with other tests.
- Finally understood relative imports and how to gain access to variables in a file in Python from a different file

# Challenges

- Figuring out a file structure for FastAPI was challenging, especially configuring the database since this was my first time doing this. However I came across this [link](!https://testdriven.io/blog/fastapi-crud/) which is what my file structure is modeled after.
- Test coverage in asynchronous code (which is what most of my code is) doesn't get reported with the tool that I use called `coverage` and from my research this is what seems to be used. A solution to this is provided in this [gist](!https://gist.github.com/daviskirk/7e8495ca5b8150f9002c5bc80630fa5a#file-run-sh),

# Notes

full text search using postgresql
searching images with images https://github.com/postgrespro/imgsmlr
for testing https://changhsinlee.com/pytest-mock/
encrypt passwords
https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password

if possible using alembic
from fastapi doc
Oauth if we have time
https://fastapi.tiangolo.com/tutorial/security/

> In this case, we are creating the tables in the same Python file, but in production, you would probably want to create them with Alembic, integrated with migrations, etc.

> my two cents, approach your tests with the SLA in mind and validate response structure, edge cases and side effects Tests count as documentation for other devs. Dont over mock things. Dont make your test know too much about implementation (otherwise, it's going to be a pain to maintain). Use factories pattern for mock data. See factory-boy and pytest_factoryboy

# What I used

- FastAPI for backend framework, PostgreSQL for database, SQLAlchemy for ORM

# Usage

To get started from the root directory run

```bash
cd backend && poetry shell && poetry install # activate virutal environment and install dependencies
export DATBASE_URL=... # exporting environment variables to establish the connection to our database on the startup of our backend
uvicorn app.main:app --reload
```

Now if you go to `http://127.0.0.1:8000`, you should see `{"Hello":"Adib!"}`, (bonus : FastAPI has built-in documentation for this project so by going to `http://127.0.0.1:8000/docs` you will see all routes, descriptions of it and can even interact with it since you can specifiy any variables or parameters )

Note your API key is simply your username plus password after you hit `\create_user\` endpoint.

# To do

Delete

- Encrypt passwords and don't store them in plaintexts
- Test
- Document properly

- Maybe later create models directory and put the two models in separate files

# Questions

- How to run all tests in `pytest` instead of specifying the file. Also, why does `pytest *` run twice?
- How to test upload of multiple files with FastAPI?

# Things I learned

- FastAPI offers two ways of handling file uploads by clients: `File` and `UploadFile` function. For this project I chose to work with `UploadFile` because for this challenge there's no specifcation for image file sizes. Therefore it would be best to work with `UploadFile` since it uses a "spooled" file meaning that the file will be stored in memory, but if it exceeds the limit then additional memory is stored in disk. `File` only stores files in memory.
- If your tests need to use the database, connect to it and then disconnect it so that you won't have any running processes which may interfere with other tests.
- Finally understood relative imports and how to gain access to variables in a file in Python from a different file
- I learned the value of having migrations. I changed the columns of my tables multiple times and it wouldn't update for some reason so I had to destroy the entire database and work from scratch again.

# Challenges

- Figuring out a file structure for FastAPI was challenging, especially configuring the database since this was my first time doing this. However I came across this [link](!https://testdriven.io/blog/fastapi-crud/) which is what my file structure is modeled after.
- Test coverage in asynchronous code (which is what most of my code is) doesn't get reported with the tool that I use called `coverage` and from my research this is what seems to be used. A solution to this is provided in this [gist](!https://gist.github.com/daviskirk/7e8495ca5b8150f9002c5bc80630fa5a#file-run-sh) and I tried `coverage run --src=app --concurrency=gevent` but nothing happened. This is isn't urgent now I'll come back to it later.
- So I tried to use a ORM but for some reason one table wouldn't have any of my columns which was not good, so after a few hours and countless Stack Overflow posts I still couldn't get it to work. Eventually what I decided to do was create one models file and have all my models there. Also I can't use any queries from the ORM because it can't find where my model is even though people have told me that I imported it correctly. Raw SQL queries it is then. (My only usage of the ORM is the initial setup of the databases)
- Spent a lot of time figuring out a cryptic error message that said the data I was giving as an input was invalid. After posting a Github issue for help I found out that if I were to have form data, I can't have a request body since this is a limitation in the HTTP protocol. So this is why `add` route has a lot of parameters. Before I was passing down a schema, but a schema is considered a request body and therefore is not allowed.
- I struggled with my attempt of storing images in PostgreSQL database, so after spending two days and posting a Github [issue](!https://github.com/tiangolo/fastapi/issues/3156) and a Stack Overflow [post](!https://stackoverflow.com/questions/67350508/how-to-convert-binary-in-python-into-bytea-data-type-in-postgresql?noredirect=1#comment119047593_67350508) with no answers I decided to just store and retrieve images on AWS S3 and to just keep the filename and it's access control in the database.
- Testing multiple uploads is not possible according to a FastAPI expert but single files is doable. However that would require duplication of my current implementation and I don't know if this is something that's acceptable

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

On UUID to generate random filenames from this SO [post](!https://stackoverflow.com/questions/10501247/best-way-to-generate-random-file-names-in-python)

> This is a valid choice, given that an UUID generator is extremely unlikely to produce a duplicate identifier (a file name, in this case):

> Only after generating 1 billion UUIDs every second for the next 100 years, the probability of creating just one duplicate would be about 50%. The probability of one duplicate would be about 50% if every person on earth owns 600 million UUIDs.

# What I used

- FastAPI for backend framework, PostgreSQL for database, SQLAlchemy for ORM

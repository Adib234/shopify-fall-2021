# Usage

To get started from the root directory run

```bash
export USERNAME=... PASSWORD=... PORT=... # exporting environment variables to establish the connection to our database on the startup of our backend
uvicorn backend.main:app --reload
```

Now if you go to `http://127.0.0.1:8080`, you should see `{"Hello":"World"}`, (bonus : FastAPI has built-in documentation for this project so by going to `http://127.0.0.1:8080/docs` you will see all routes, descriptions of it and can even interact with it since you can specifiy any variables or parameters )

# To do

- Encrypt passwords and don't store them in plaintexts
- Test
- Document properly

# Things I learned

- FastAPI offers two ways of handling file uploads by clients: `File` and `UploadFile` function. For this project I chose to work with `UploadFile` because for this challenge there's no specifcation for image file sizes. Therefore it would be best to work with `UploadFile` since it uses a "spooled" file meaning that the file will be stored in memory, but if it exceeds the limit then additional memory is stored in disk. `File` only stores files in memory.

# Challenges

# Notes

full text search using postgresql
searching images with images https://github.com/postgrespro/imgsmlr
for testing https://changhsinlee.com/pytest-mock/
encrypt passwords
https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
later on when i clean up my directory https://fastapi.tiangolo.com/tutorial/bigger-applications/?h=projects#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies
if possible using alembic
from fastapi doc
Oauth if we have time
https://fastapi.tiangolo.com/tutorial/security/

> In this case, we are creating the tables in the same Python file, but in production, you would probably want to create them with Alembic, integrated with migrations, etc.

> my two cents, approach your tests with the SLA in mind and validate response structure, edge cases and side effects Tests count as documentation for other devs. Dont over mock things. Dont make your test know too much about implementation (otherwise, it's going to be a pain to maintain). Use factories pattern for mock data. See factory-boy and pytest_factoryboy

# What I used

- FastAPI for backend framework, PostgreSQL for database, SQLAlchemy for ORM, FastAPI's built in [HTTP BasicAuth](!https://fastapi.tiangolo.com/advanced/security/http-basic-auth/) to authenticate users

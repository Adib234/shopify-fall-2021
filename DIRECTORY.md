# The file structure explained

```bash
# Omitting all the files that end with .pyc and start with __init__
.
├── DIRECTORY.md # explains the file structure
├── README.md # for info about the project
└── backend
    ├── app
    │   ├── aws.py # aws config of env. variables
    │   ├── controllers
    │   │   ├── add.py
    │   │   ├── create_user.py
    │   │   ├── delete.py
    │   │   ├── my_images.py
    │   │   ├── my_info.py
    │   │   ├── root.py
    │   │   └── search.py
    │   ├── db.py # database config
    │   ├── main.py # where we register all our routes and startup and shutdown events like database connection happen
    │   ├── models.py # database tables
    │   ├── request.py # some initial information of user
    │   ├── schemas
    │   │   └── user.py
    │   ├── security.py # authenticating the user to determine access control to images
    │   ├── templates
    │   │   ├── images.html
    │   │   └── search_results.html
    |   ├── tests
    │       ├── add.py
    │       ├── create_user.py
    │       ├── delete.py
    │       ├── mock-data
    │       │   ├── test.jpg
    │       │   ├── test.pdf
    │       │   └── test1.jpg
    │       ├── my_images.py
    │       ├── my_info.py
    │       ├── root.py
    │       └── search.py
    ├── poetry.lock # dependencies
    ├── pyproject.toml # dependencies
    └── requirements.txt # dependencies

```

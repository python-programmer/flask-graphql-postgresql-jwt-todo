# A Todo Project(Flask, GraphQL, SQLAlchemy, JWT Auth)
This is a Todo project written by flask that uses GraphQL and also has user authentication that uses JWT to implement user authentication. Postgresql is used for the database

## Install Requirements
We’ll begin by creating a virtual environment for our project and install the dependencies we need inside of the virtual environment

> python3 -m venv venv

activate it and install the requirements

> source venv/bin/activate

> python -m pip install -r requirements.txt


## Create Database
create a database in postgresql and update the `connection_string` parameter in `.env` file

## Run the project
first of all, we need to create our tables

> python data.py

then run the app:

> python run.py

## Test it
We have two endpoints for the authenticated user and the anonymous user. "http://localhost:5000/graphq/" for user creation (unauthenticated), and "http://localhost:5000/graphql" for authenticated endpoints:
so

1. create a user from http://localhost:5000/graphq

        mutation {
            createUser(username: "user-1", password: "passw0rd") {
                ok
                user{
                    username
                }
            }
        }

2. get token from rest endpoint http://localhost:5000/login, use postman (POST method):

        {
            "username": "user-1",
            "password": "passw0rd"
        }

3. As such I added the token from the login request to headers from my browser via a browser plugin called ModHeader; you don’t have to test this from the browser, you can do it from Postman or any other API testing tool you prefer.

4. now is time to test our todo functionality, now use this url http://localhost:5000/graphql

### Create a todo

    mutation {
        addTodo(title: "a new todo", description: "about us", dueDate: "2021-12-03T10:15:30Z") {
            ok
            todo {
                id,
                title,
                description,
                dueDate,
                status
            }
        }
    }

### Get a todo by id

    {
        findTodo(id: 2) {
            id,
            title,
            description,
            dueDate,
            status,
            user {
                username
            }
        }
    }

### Get all user todo list

    {
        userTodoList {
            id,
            title,
            description,
            dueDate,
            status,
            user {
                id,
                username
            }
        }
    }

### Query by due date and status

    {
        findTodoByStatusOrDueDate(status: true, dueDate:"2021-12-03T10:15:30") {
            id,
            title,
            description,
            dueDate,
            status,
            user {
                id,
                username
            }
        }
    }

### Update status
True = Done
False = In progress

    mutation {
        updateTodo(status:true, todoId:1) {
            ok,
            todo {
                id,
                title,
                description,
                dueDate
                status
            }
        }
    }


### Update due date

    mutation {
        updateTodo(dueDate: "2021-12-03T10:15:30", todoId:1) {
            ok,
            todo {
                id,
                title,
                description,
                dueDate
                status
            }
        }
    }

### Delete a todo

    mutation {
        deleteTodo(id:2) {
            ok,
            todo {
                id,
                title,
                description,
                status,
                dueDate,
                user {
                    id,
                    username
                }
            }
        }
    }




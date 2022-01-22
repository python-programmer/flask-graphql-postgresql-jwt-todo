from datetime import datetime
from models import (
    User as UserModel, Todo as TodoModel,
    session
)
import graphene
from graphene_sqlalchemy import (
    SQLAlchemyConnectionField,
    SQLAlchemyObjectType
)
from extensions import bcrypt
from typing import Optional

# types
class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel


class Todo(SQLAlchemyObjectType):
    class Meta:
        model = TodoModel


class createUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()
    ok = graphene.Boolean()
    user = graphene.Field(User)

    def mutate(root, info, username, password):
        new_user = UserModel(
            username=username,
            password=str(
                bcrypt.generate_password_hash(password),
                'utf-8'
            )
        )
        session.add(new_user)
        session.commit()
        ok = True
        return createUser(ok=ok, user=new_user)


class addTodo(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()
        due_date = graphene.DateTime()

    ok = graphene.Boolean()
    todo = graphene.Field(Todo)

    def mutate(root, info, title, description, due_date):
        uid = info.context['uid']
        user = session.query(UserModel).filter_by(username=uid).first()
        new_todo = TodoModel(
            title=title,
            description=description,
            due_date=due_date,
            user=user
        )
        session.add(new_todo)
        session.commit()
        ok = True
        return addTodo(ok=ok, todo=new_todo)


class updateTodo(graphene.Mutation):
    class Arguments:
        todo_id = graphene.Int()
        status = graphene.Boolean()
        due_date = graphene.DateTime()
    ok = graphene.Boolean()
    todo = graphene.Field(Todo)

    def mutate(root, info, todo_id, status: Optional[bool]=None, due_date: Optional[datetime]=None):
        todo = session.query(TodoModel).filter_by(id=todo_id).first()
        if status is None:
            todo.due_date = due_date
        elif due_date is None:
            todo.status = status
        else:
            todo.status = status
            todo.due_date = due_date
        session.commit()
        ok = True
        todo = todo
        return updateTodo(ok=ok, todo=todo)


class deleteTodo(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
    ok = graphene.Boolean()
    todo = graphene.Field(Todo)

    def mutate(root, info, id):
        todo = session.query(TodoModel).filter_by(id=id).first()
        session.delete(todo)
        ok = True
        todo = todo
        session.commit()
        return deleteTodo(ok=ok, todo=todo)


class PostAuthMutation(graphene.ObjectType):
    addTodo = addTodo.Field()
    updateTodo = updateTodo.Field()
    deleteTodo = deleteTodo.Field()


class PreAuthMutation(graphene.ObjectType):
    create_user = createUser.Field()


class Query(graphene.ObjectType):
    find_todo = graphene.Field(Todo, id=graphene.Int())
    find_todo_by_status_or_due_date = graphene.List(Todo, status=graphene.Boolean(), due_date=graphene.DateTime())
    user_todo_list = graphene.List(Todo)

    def resolve_user_todo_list(root, info):
        uid = info.context['uid']
        user = session.query(UserModel).filter_by(username=uid).first()
        return user.todo_list

    def resolve_find_todo(root, info, id):
        return session.query(TodoModel).filter_by(id=id).first()

    def resolve_find_todo_by_status_or_due_date(root, info, status=None, due_date=None):
        print(status, due_date)
        if status is None:
            return session.query(TodoModel).filter_by(due_date=due_date)
        elif due_date is None:
            return session.query(TodoModel).filter_by(status=status)
        else:
            return session.query(TodoModel).filter_by(status=status, due_date=due_date)


auth_required_schema = graphene.Schema(query=Query, mutation=PostAuthMutation)
schema = graphene.Schema(mutation=PreAuthMutation)
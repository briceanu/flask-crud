from marshmallow import Schema, fields, validate
import uuid


class TodoSchemaIn(Schema):
    id = fields.UUID(load_default=uuid.uuid4)
    title = fields.Str(required=True, validate=validate.Length(max=10))
    age = fields.Int(required=True, validate=validate.Range(min=18, max=99))
    email = fields.Email(required=True)
    surname = fields.Str()


class TodoUpdateSchemaIn(TodoSchemaIn):
    # update all fields except id
    class Meta:
        exclude = ("id",)


class TodoUpdateTitleSchemaIn(TodoSchemaIn):
    # update only the title of the todo
    class Meta:
        exclude = ("id", "age", "email", "surname")


class TodoSchemaOut(Schema):
    # output schema for the todo, exclude email and age
    id = fields.UUID()
    title = fields.Str()
    age = fields.Int()
    email = fields.Email()
    surname = fields.Str()

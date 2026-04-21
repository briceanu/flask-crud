from marshmallow import Schema, fields, validate, ValidationError, validates_schema
import uuid
import re
from enum import Enum


class NameEnum(str, Enum):
    Gigi = "Gigi"
    Teo = "Teo"
    Ion = "Ion"


class Data(Schema):
    name = fields.Str(
        required=True,
        validate=validate.OneOf([e.value for e in NameEnum]),
    )
    age = fields.Int(validate=validate.Range(min=2, max=20))


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


def validate_password(n):
    if len(n) < 6:
        raise ValidationError("Passowrd must be at least 6 characters long.")
    if not re.search(r"[A-Z]", n):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r"[0-9]", n):
        raise ValidationError("Password must contain at least one number.")
    return n


class UserSignupSchemaIn(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=50))
    password = fields.Str(required=True, validate=validate_password)
    confirm_password = fields.Str(required=True, validate=validate_password)
    email = fields.Email(required=True)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data["password"] != data["confirm_password"]:
            raise ValidationError("Passwords do not match.")


class UserSchemaOut(Schema):
    name = fields.Str()
    password = fields.Str()
    email = fields.Email()
    scope = fields.Str()

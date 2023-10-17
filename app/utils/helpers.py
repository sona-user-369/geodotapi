import uuid
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.types import TypeDecorator
from passlib.context import CryptContext
import os
from app import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# utils for db


class UUID(TypeDecorator):
    impl = BINARY(16)

    def process_bind_param(self, value, dialect):
        try:
            return value.bytes
        except AttributeError:
            try:
                return uuid.UUID(value).bytes
            except TypeError:
                return value

    def process_result_value(self, value, dialect):
        return uuid.UUID(bytes=value)


# utils auth

def crypt_pass(password):
    return pwd_context.hash(password) if password is not None else Exception('error')


def check_pass(checker, password):
    return pwd_context.verify(password, checker)


def host_file(file, path):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, file.filename), 'wb') as f:
        file.file.seek(0)
        f.write(file.file.read())
    file_path = settings.URL_HOST + path + file.filename

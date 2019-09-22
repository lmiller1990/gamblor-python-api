from datetime import datetime
from peewee import *
import bcrypt

from .base import BaseModel


class User(BaseModel):
    id = PrimaryKeyField()
    email = TextField()
    encrypted_password = TextField()
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())
    admin = BooleanField(default=False)

    class Meta:
        table_name = 'users'

    @staticmethod
    def get_hashed_password(plaintext_password):
        return bcrypt.hashpw(plaintext_password, bcrypt.gensalt())
    
    def check_password(self, plaintext_password):
        return bcrypt.checkpw(plaintext_password, self.encrypted_password)

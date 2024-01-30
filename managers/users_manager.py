from bson.objectid import ObjectId
from six import string_types

import models
from app_core import db, logger


class UsersManager:
    __users = None

    def __init__(self):
        self.__users = db.users

    def get_users(self):
        try:
            db_users = self.__users.find()
            users_collection = []
            for db_user in db_users:
                if db_user is not None:
                    users_collection.append(models.User.deserializable(db_user))
            return users_collection
        except Exception as e:
            logger.info(e)

        return None

    def get_user(self, user_id):
        try:
            db_user = (
                self.__users.find_one({"_id": ObjectId(user_id)})
                if isinstance(user_id, string_types) or isinstance(user_id, str)
                else None
            )
            if db_user is not None:
                return models.User.deserializable(db_user)
        except Exception as e:
            logger.info(e)

        return None

    def get_user_by_email(self, user_email):
        try:
            db_users = (
                self.__users.find({"email": user_email})
                if isinstance(user_email, string_types) or isinstance(user_email, str)
                else None
            )
            if db_users is not None and db_users.count() == 1:
                return models.User.deserializable(db_users[0])
        except Exception as e:
            logger.info(e)

        return None

    def check_user_email(self, user_email):
        db_users = self.__users.find({"email": user_email})
        return db_users.count() == 0

    def add_user(self, user):
        try:
            self.__users.insert_one(user.serializable())
            return True
        except Exception as e:
            logger.info(e)

        return False

    def update_user(self, user):
        try:
            self.__users.update_one({"_id": ObjectId(user.id)}, {"$set": user.serializable()})
            return True
        except Exception as e:
            logger.info(e)

        return False

    def delete_user(self, user_id):
        try:
            if isinstance(user_id, string_types) or isinstance(user_id, str):
                self.__users.remove({"_id": ObjectId(user_id)})
                return True
            else:
                return False
        except Exception as e:
            logger.info(e)

        return False

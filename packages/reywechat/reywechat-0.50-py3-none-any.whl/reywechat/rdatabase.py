# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-23 20:55:58
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Database methods.
"""


from reytool.rdatabase import RDatabase as RRDatabase
from reytool.rtime import to_time, time_to

from .rreceive import RMessage
from .rwechat import RWeChat


__all__ = (
    "RDatabase",
)


class RDatabase(object):
    """
    Rey's `database` type.
    """


    def __init__(
        self,
        rwechat: RWeChat,
        rrdatabase: RRDatabase
    ) -> None:
        """
        Build `database` instance.

        Parameters
        ----------
        rwechat : `RClient` instance.
        rrdatabase : `RRDatabase` instance.
        """

        # Set attribute.
        self.rwechat = rwechat
        self.rrdatabase = rrdatabase

        # Build.
        self.build()


    def build(self) -> None:
        """
        Check and build all standard databases and tables.
        """

        # Set parameter.

        ## Database.
        databases = [
            {
                "database": "wechat"
            }
        ]

        ## Table.
        tables = [

            ### "message_receive".
            {
                "path": ("wechat", "message_receive"),
                "fields": [
                    {
                        "name": "create_time",
                        "type_": "datetime",
                        "constraint": "NOT NULL DEFAULT CURRENT_TIMESTAMP",
                        "comment": "Record create time."
                    },
                    {
                        "name": "receive_time",
                        "type_": "datetime",
                        "constraint": "NOT NULL",
                        "comment": "Message receive time."
                    },
                    {
                        "name": "message_id",
                        "type_": "bigint unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Message UUID."
                    },
                    {
                        "name": "room_id",
                        "type_": "char(20)",
                        "constraint": "DEFAULT NULL",
                        "comment": "Message chat room ID, null for private chat."
                    },
                    {
                        "name": "user_id",
                        "type_": "varchar(20)",
                        "constraint": "DEFAULT NULL",
                        "comment": "Message sender user ID, null for system message."
                    },
                    {
                        "name": "message_type",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Message type."
                    },
                    {
                        "name": "data",
                        "type_": "text",
                        "constraint": "CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL",
                        "comment": "Message data."
                    },
                    {
                        "name": "file_id",
                        "type_": "mediumint unsigned",
                        "constraint": "DEFAULT NULL",
                        "comment": "Message file ID, from the file database."
                    },
                    {
                        "name": "login_id",
                        "type_": "varchar(20)",
                        "constraint": "NOT NULL",
                        "comment": "Message receiver client login user ID."
                    }
                ],
                "primary": "message_id",
                "comment": "Message receive table."
            },

            ### "message_type".
            {
                "path": ("wechat", "message_type"),
                "fields": [
                    {
                        "name": "message_type",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Message type."
                    },
                    {
                        "name": "description",
                        "type_": "varchar(200)",
                        "constraint": "NOT NULL",
                        "comment": "Message type description."
                    }
                ],
                "primary": "message_type",
                "comment": "Message type table."
            },

            ### "contact_user".
            {
                "path": ("wechat", "contact_user"),
                "fields": [
                    {
                        "name": "create_time",
                        "type_": "datetime",
                        "constraint": "NOT NULL DEFAULT CURRENT_TIMESTAMP",
                        "comment": "Record create time."
                    },
                    {
                        "name": "update_time",
                        "type_": "datetime",
                        "constraint": "DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP",
                        "comment": "Record update time."
                    },
                    {
                        "name": "user_id",
                        "type_": "varchar(20)",
                        "constraint": "NOT NULL",
                        "comment": "User ID."
                    },
                    {
                        "name": "user_name",
                        "type_": "varchar(32)",
                        "constraint": "NOT NULL",
                        "comment": "User name."
                    },
                    {
                        "name": "is_valid",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Is the valid, invalid as 0, valid as 1."
                    }
                ],
                "primary": "user_id",
                "comment": "User contact table."
            },

            ### "contact_room".
            {
                "path": ("wechat", "contact_room"),
                "fields": [
                    {
                        "name": "create_time",
                        "type_": "datetime",
                        "constraint": "NOT NULL DEFAULT CURRENT_TIMESTAMP",
                        "comment": "Record create time."
                    },
                    {
                        "name": "update_time",
                        "type_": "datetime",
                        "constraint": "DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP",
                        "comment": "Record update time."
                    },
                    {
                        "name": "room_id",
                        "type_": "varchar(20)",
                        "constraint": "NOT NULL",
                        "comment": "Chat room ID."
                    },
                    {
                        "name": "room_name",
                        "type_": "varchar(32)",
                        "constraint": "NOT NULL",
                        "comment": "Chat room name."
                    },
                    {
                        "name": "is_valid",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Is the valid, invalid as 0, valid as 1."
                    }
                ],
                "primary": "room_id",
                "comment": "Chat room contact table."
            }
        ]

        # Build.
        self.rrdatabase.build(databases, tables)

        ## File.
        self.rrdatabase.file()

        # Insert and update.
        self.update_message_type()
        self.update_contact()


    def update_message_type(self) -> None:
        """
        Update table `message_type`.
        """

        # Generate data.
        data = [
            {"message_type": 1, "description": "text message"},
            {"message_type": 3, "description": "image message"},
            {"message_type": 34, "description": "voice message"},
            {"message_type": 37, "description": "new friend"},
            {"message_type": 42, "description": "business card"},
            {"message_type": 43, "description": "video message"},
            {"message_type": 47, "description": "expression message"},
            {"message_type": 48, "description": "position message"},
            {"message_type": 49, "description": "file or record quotes or record forward or share link or transfer money or real time location message"},
            {"message_type": 1000, "description": "system message"},
            {"message_type": 1002, "description": "recall message"}
        ]

        # Insert and update.
        self.rrdatabase.execute_insert(
            ("wechat", "message_type"),
            data,
            "update"
        )


    def update_contact(self) -> None:
        """
        Update table `contact_user` and `contact_room`.
        """

        # Get data.
        contact_table = self.rwechat.rclient.get_contact_table()
        user_data = []
        room_data = []
        user_ids = []
        room_ids = []
        for row in contact_table:
            if row["id"][-9:] == "@chatroom":
                item = {
                    "room_id": row["id"],
                    "room_name": row["name"],
                    "is_valid": 1
                }
                room_data.append(item)
                room_ids.append(row["id"])
            else:
                item = {
                    "user_id": row["id"],
                    "user_name": row["name"],
                    "is_valid": 1
                }
                user_data.append(item)
                user_ids.append(row["id"])

        # Insert and update.
        conn = self.rrdatabase.connect()

        ## "contact_user".

        ### Insert.
        conn.execute_insert(
            ("wechat", "contact_user"),
            user_data,
            "update"
        )

        ### Update.
        if user_ids != []:
            sql = (
                "UPDATE `wechat`.`contact_user`\n"
                "SET `is_valid` = 0\n"
                "WHERE `user_id` NOT IN :user_ids"
            )
            conn.execute(
                sql,
                user_ids=user_ids
            )

        ### Commit.
        conn.commit()

        ## "contact_room".

        ### Insert.
        conn.execute_insert(
            ("wechat", "contact_room"),
            room_data,
            "update"
        )

        ### Update.
        if room_ids != []:
            sql = (
                "UPDATE `wechat`.`contact_room`\n"
                "SET `is_valid` = 0\n"
                "WHERE `room_id` NOT IN :room_ids"
            )
            conn.execute(
                sql,
                room_ids=room_ids
            )

        ### Commit.
        conn.commit()

        ## Close.
        conn.close()


    def use_message_receive(self) -> None:
        """
        Add handler, write message parameters to table `message_receive`.
        """


        # Define.
        def handler_use_message_receive(message: RMessage) -> None:
            """
            Write message parameters to table `message_receive`.

            Parameters
            ----------
            message : `RMessage` instance.
            """

            # Upload file.
            if message.file is None:
                file_id = None
            else:
                file_id = self.rrdatabase.file.upload(
                    message.file["path"],
                    message.file["name"],
                    "WeChat"
                )

            # Generate data.
            receive_time_obj = to_time(message.time)
            receive_time_str = time_to(receive_time_obj)
            data = {
                "receive_time": receive_time_str,
                "message_id": message.id,
                "room_id": message.room,
                "user_id": message.user,
                "message_type": message.type,
                "data": message.data,
                "file_id": file_id,
                "login_id": self.rwechat.rclient.login_info["user_id"]
            }

            # Insert.
            self.rrdatabase.execute_insert(
                ("wechat", "message_receive"),
                data,
                "ignore"
            )


        # Add handler.
        self.rwechat.rreceiver.add_handler(handler_use_message_receive)


    def use_all(self) -> None:
        """
        Use all database tables.
        """

        # Use.
        self.use_message_receive()
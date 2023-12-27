# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-23 20:55:58
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Database methods.
"""


from reytool.rdatabase import RDatabase as RRDatabase

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
                        "name": "time",
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
                        "comment": "Message room ID."
                    },
                    {
                        "name": "sender",
                        "type_": "varchar(19)",
                        "constraint": "DEFAULT NULL",
                        "comment": "Message sender user ID."
                    },
                    {
                        "name": "receiver",
                        "type_": "varchar(19)",
                        "constraint": "NOT NULL",
                        "comment": "Message receiver user ID."
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
                        "comment": "Message file ID."
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
        ]

        # Build.
        self.rrdatabase.build(databases, tables)

        ## File.
        self.rrdatabase.file()

        # Insert.
        self.update_message_type()


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
            data = {
                "message_id": message.id,
                "room_id": message.room,
                "sender": message.sender,
                "receiver": message.receiver,
                "message_type": message.type,
                "data": message.data,
                "file_id": file_id
            }
            kwdata = {
                "time": ":NOW()"
            }

            self.rrdatabase.execute_insert(
                ("wechat", "message_receive"),
                data,
                "ignore",
                **kwdata
            )

        # Add handler.
        self.rwechat.rreceiver.add_handler(handler_use_message_receive)


    def use_all(self) -> None:
        """
        Use all database tables.
        """

        # Use.
        self.use_message_receive()
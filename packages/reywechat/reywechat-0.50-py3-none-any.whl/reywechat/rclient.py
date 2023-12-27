# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-17 20:27:16
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Client methods.
"""


from __future__ import annotations
from typing import Any, List, Tuple, Dict, Optional, Literal, Union
from os.path import abspath as os_abspath
from reytool.rcomm import request as reytool_request
from reytool.rdll import inject_dll
from reytool.rsystem import search_process
from reytool.ros import find_relpath

from .rwechat import RWeChat


__all__ = (
    "RClient",
)


class RClientAPIErorr(Exception):
    """
    Rey's `client API` exception type.
    """


class RClient(object):
    """
    Rey's `client` type.
    """


    def __init__(
        self,
        rwechat: RWeChat
    ) -> None:
        """
        Build `client` instance.

        Parameters
        ----------
        rwechat : `RWeChat` instance.
        """

        # Start.
        self.rwechat = rwechat
        self.start_api()

        # Set attribute.
        self.login_info = self.get_login_info()


    def start_api(self) -> None:
        """
        Start client control API.
        """

        # Check client.
        result = self.check_client()
        if not result:
            raise RClientAPIErorr("WeChat client not started")

        # Check start.
        result = self.check_api()
        if not result:

            # Inject DLL.
            self.inject_dll()

            # Check api.
            result = self.check_api()
            if not result:
                raise RClientAPIErorr("start WeChat client API failed")

        # Report.
        print("Start WeChat client API successfully, address is '127.0.0.1:19088'.")


    def check_client(self) -> bool:
        """
        Check if the client is started.

        Returns
        -------
        Check result.
        """

        # Search.
        processes = search_process(name="WeChat.exe")

        # Check.
        if processes == []:
            return False
        else:
            return True


    def check_api(self) -> bool:
        """
        Check if the client API is started.
        """

        # Search.
        processes = search_process(port=self.rwechat.client_api_port)

        # Check.
        if processes == []:
            return False
        process = processes[0]
        with process.oneshot():
            process_name = process.name()
        if process_name != "WeChat.exe":
            return False

        ## Check request.
        result = self.check_login()
        if not result:
            return False

        return True


    def inject_dll(self) -> None:
        """
        Inject DLL file of start API into the WeChat client process.
        """

        # Get parameter.
        dll_file_relpath = ".\\data\\client_api.dll"
        dll_file_path = find_relpath(__file__, dll_file_relpath)

        # Inject.
        processes = search_process(name="WeChat.exe")
        process = processes[0]
        inject_dll(
            process.pid,
            dll_file_path
        )


    def request(
        self,
        api: str,
        data: Optional[Dict] = None
    ) -> Dict[
        Literal["code", "message", "data"],
        Any
    ]:
        """
        Request client API.

        Parameters
        ----------
        api : API name.
        data : Request data.

        Returns
        -------
        Response content.
            - `code` : Response code.
            - `message` : Response message.
            - `data` : Response data.
        """

        # Get parameter.
        url = f"http://127.0.0.1:{self.rwechat.client_api_port}/api/{api}"
        if data is None:
            data = {}

        # Request.
        response = reytool_request(
            url,
            json=data,
            method="post",
            check=True
        )

        # Extract.
        response_data = response.json()
        data = {
            "code": response_data["code"],
            "message": response_data["msg"],
            "data": response_data["data"]
        }

        return response_data


    def check_login(self) -> bool:
        """
        Check if the client is logged in.

        Returns
        -------
        Check result.
        """

        # Get parameter.
        api = "checkLogin"

        # Request.
        response = self.request(api)

        # Check.
        if response["code"] == 1:
            return True
        elif response["code"] == 0:
            return False


    def get_login_info(
        self
    ) -> Dict[
        Literal[
            "user_id",
            "account",
            "name",
            "phone",
            "signature",
            "city",
            "province",
            "country",
            "head_image",
            "account_data_path",
            "wechat_data_path",
            "decrypt_key"
        ],
        Optional[str]
    ]:
        """
        Get login account information.

        Returns
        -------
        Login user account information.
            - `Key 'user_id'` : User ID, cannot change.
            - `Key 'account' : User account, can change.
            - `Key 'name' : User nickname.
            - `Key 'phone' : Phone number.
            - `Key 'signature' : Personal signature.
            - `Key 'city' : City.
            - `Key 'province' : Province.
            - `Key 'country' : Country.
            - `Key 'head_image' : Head image URL.
            - `Key 'account_data_path' : Current account data save path.
            - `Key 'wechat_data_path' : WeChat data save path.
            - `Key 'decrypt_key' : Database decrypt key.
        """

        # Get parameter.
        api = "userInfo"

        # Request.
        response = self.request(api)

        # Extract.
        data = response["data"]
        info = {
            "user_id": data["wxid"],
            "account": data["account"],
            "name": data["name"],
            "phone": data["mobile"],
            "signature": data["signature"],
            "city": data["city"],
            "province": data["province"],
            "country": data["country"],
            "head_image": data["headImage"],
            "account_data_path": data["currentDataPath"],
            "wechat_data_path": data["dataSavePath"],
            "decrypt_key": data["dbKey"]
        }
        info = {
            key: (
                None
                if value == ""
                else value
            )
            for key, value in info.items()
        }

        return info


    def hook_message(
        self,
        host: str,
        port: Union[str, int],
        timeout: float
    ) -> None:
        """
        Hook the message, and send the message to the TCP protocol request.

        Parameters
        ----------
        host : Request host.
        port : Request port.
        timeout : Request timeout seconds.
        """

        # Get parameter.
        api = "hookSyncMsg"
        port = str(port)
        timeout_ms_str = str(int(timeout * 1000))

        # Request.
        data = {
            "ip": host,
            "port": port,
            "timeout": timeout_ms_str,
            "enableHttp": "0"
        }
        response = self.request(api, data)

        # Check.
        if response["code"] == 2:
            self.unhook_message()
            self.hook_message(
                host,
                port,
                timeout
            )
        elif response["code"] != 0:
            raise RClientAPIErorr("hook message failed", response)

        # Report.
        print(
            "Hook message successfully, address is '%s:%s'." % (
                host,
                port
            )
        )


    def unhook_message(self) -> None:
        """
        Unhook the message.
        """

        # Get parameter.
        api = "unhookSyncMsg"

        # Request.
        response = self.request(api)

        # Check.
        if response["code"] != 0:
            raise RClientAPIErorr("unhook message failed", response)

        # Report.
        print("Unhook message successfully.")


    def download_file(
        self,
        id_: int
    ) -> None:
        """
        Download image or video or other file.

        Parameters
        ----------
        id_ : Message ID.
        """

        # Get parameter.
        api = "downloadAttach"

        # Request.
        data = {"msgId": id_}
        response = self.request(api, data)

        # Check.
        if response["code"] != 0:
            raise RClientAPIErorr("download file failed", response)


    def download_voice(
        self,
        id_: int,
        dir_: str
    ) -> None:
        """
        Download voice.

        Parameters
        ----------
        id_ : Message ID.
        dir_ : Save directory.
        """

        # Get parameter.
        api = "getVoiceByMsgId"
        dir_ = os_abspath(dir_)

        # Request.
        data = {
            "msgId": id_,
            "storeDir": dir_
        }
        response = self.request(api, data)

        # Check.
        if response["code"] not in (0, 1):
            raise RClientAPIErorr("download voice failed", response)


    def get_contact_table(
        self,
        type_: Optional[Literal["user", "room"]] = None
    ) -> List[
        Dict[
            Literal["id", "name"],
            str
        ]
    ]:
        """
        Get contact table, include chat user and chat room.

        Parameters
        ----------
        type_ : Filter contact type.
            - `None` : Not filter.
            - `Literal['user']` : Return user contact table.
            - `Literal['room']` : Return chat room contact table.

        Returns
        -------
        Contact table.
            - `Key 'id'` : User ID or room ID.
            - `Key 'name' : User nickname or room name.
        """

        # Get parameter.
        api = "getContactList"

        # Request.
        response = self.request(api)

        # Check.
        if response["code"] != 1:
            raise RClientAPIErorr("get contact table failed", response)

        # Convert.
        data: List[Dict] = response["data"]
        table = [
            {
                "id": info["wxid"],
                "name": info["nickname"]
            }
            for info in data
        ]

        # Filter.

        ## Filter system user.
        filter_names = (
            "朋友推荐消息",
            "语音记事本",
            "漂流瓶",
            "文件传输助手"
        )
        for name in filter_names:
            for row in table:
                if row["name"] == name:
                    table.remove(row)
                    break

        ## Filter type.
        if type_ == "user":
            table = [
                row
                for row in table
                if row["id"][-9:] != "@chatroom"
            ]
        elif type_ == "room":
            table = [
                row
                for row in table
                if row["id"][-9:] == "@chatroom"
            ]

        return table


    def get_contact_name(
        self,
        id_: str
    ) -> str:
        """
        Get contact name, can be chat friend and chat room and chat room member.

        Parameters
        ----------
        id_ : User ID or room ID.

        Returns
        -------
        User nickname or room name.
        """

        # Get parameter.
        api = "getContactProfile"

        # Request.
        data = {"wxid": id_}
        response = self.request(api, data)

        # Check.
        if response["code"] != 1:
            raise RClientAPIErorr("get contact name failed", response)

        # Extract.
        data: dict = response["data"]
        name = data["nickname"]

        return name


    def get_room_member_list(
        self,
        room_id: str
    ) -> List[str]:
        """
        Get list of room member user ID.

        Parameters
        ----------
        room_id : Room ID.

        Returns
        -------
        List of room member user ID.
        """

        # Get parameter.
        api = "getMemberFromChatRoom"

        # Request.
        data = {"chatRoomId": room_id}
        response = self.request(api, data)

        # Check.
        if response["code"] != 1:
            raise RClientAPIErorr("get list of room member user ID failed", response)

        # Convert.
        data: Dict = response["data"]
        members_list = data["members"].split("^G")

        return members_list


    def get_room_member_table(
        self,
        room_id: str
    ) -> List[str]:
        """
        Get table of room member user ID and user name.

        Parameters
        ----------
        room_id : Room ID.

        Returns
        -------
        Table of room member user ID and user name.
        """

        # Get members.
        members = self.get_room_member_list(room_id)

        # Loop.
        table = {
            id_: self.get_contact_name(id_)
            for id_ in members
        }

        return table
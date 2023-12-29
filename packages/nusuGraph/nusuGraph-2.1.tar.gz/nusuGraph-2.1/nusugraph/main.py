import json
import asyncio

import httpx
import aiofiles

try:
    from .utils import html_to_nodes
except ImportError:
    from utils import html_to_nodes


class Telegraph:
    def __init__(
        self, token: str = None, timeout: int = 10, tokenList: list or tuple = None
    ):
        self.__session = httpx.AsyncClient(timeout=timeout)
        self.__token = token
        self.__tokenList = tokenList
        self.__length = len(tokenList) if tokenList else 0
        self.__count = 0

    async def getToken(self):
        if self.__token:
            return self.__token

        if not self.__token and not self.__tokenList:
            # creates a new account if not token nor a list of tokes were
            # passed
            res = await self.createAccount()
            self.__token = res.get("access_token")
            return self.__token

        # if a token list was passed, then:
        if self.__count >= self.__length:
            self.__count = 0

        x = self.__tokenList[self.__count]
        self.__count += 1
        return x

    async def createAccount(
        self,
        shortName: str = "Anonymous",
        authorName: str = "Anonymous",
        authorUrl: str = None,
    ):
        url = "https://api.telegra.ph/createAccount"
        params = {
            "short_name": shortName,
            "author_name": authorName,
            "author_url": authorUrl,
        }
        res = (await self.__session.get(url, params=params)).json()

        return res["result"] if res["ok"] else res

    async def createPage(
        self, author: str, htmlContent: str, title: str, returnContent: bool = False
    ):
        if not self.__token and not self.__tokenList:
            print("Access Token Not Found. An Anonymous Account Will Be Created")

        url = "https://api.telegra.ph/createPage"
        token = await self.getToken()
        params = {
            "access_token": token,
            "title": title,
            "author_name": author,
            "content": json.dumps(html_to_nodes(htmlContent)),
            "return_content": returnContent,
        }
        res = (await self.__session.get(url, params=params)).json()
        return res["result"] if res["ok"] else res

    async def uploadMediaFromFile(self, pathToFile: str):
        """
        Upload media to telegra.ph from local file

        Arguments:
            pathToFile (str): Path to the file to be uploaded

        Returns:
            str: telegra.ph link to the uploaded file

        Raises:
            Exception: If the file type is not supported

        Note:
            Only supports gif, jpeg, jpg, png and mp4 files
        """
        supportedFileTypes = {i: f"image/{i}" for i in ("gif", "jpeg", "jpg", "png")}
        supportedFileTypes["mp4"] = "video/mp4"

        fileExt = pathToFile.split(".")[-1]

        if fileExt in supportedFileTypes:
            fileType = supportedFileTypes[fileExt]
        else:
            raise Exception(f"Unsupported file type: {fileExt}")

        async with aiofiles.open(pathToFile, "rb") as f:
            content = await f.read()

        return await self.__uploadMediaToTelegraph(content, fileType)

    async def uploadMediaFromBytes(self, content: bytes, fileType: str):
        """
        Upload media to telegra.ph from file's bytes content

        Arguments:
            content (bytes): Content of the file to be uploaded
            fileType (str): File type of the content

        Returns:
            str: telegra.ph link to the uploaded file

        Note:
            Only supports gif, jpeg, jpg, png and mp4 files
        """
        return await self.__uploadMediaToTelegraph(content, fileType)

    async def __uploadMediaToTelegraph(self, content: bytes, fileType: str):
        url = "https://telegra.ph/upload"
        response = await self.__session.post(
            url, files={"file": ("file", content, fileType)}
        )
        resp = json.loads(response.content)
        return f"https://telegra.ph{resp[0]['src']}"

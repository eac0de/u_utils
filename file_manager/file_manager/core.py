"""
Модуль с сервисом для работы с файлами через GridFS
"""

from beanie import PydanticObjectId
from bson import ObjectId
from gridfs import NoFile
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorGridFSBucket,
    AsyncIOMotorGridOut,
    AsyncIOMotorGridOutCursor,
)

grid_fs_bucket: AsyncIOMotorGridFSBucket


class GridFSService:
    """
    Сервис для работы с файлами через GridFS
    """

    @staticmethod
    async def upload_file(
        file_content: bytes | str,
        filename: str,
        metadata: dict,
    ) -> ObjectId:
        """
        Загрузка файла в grid_fs

        Args:
            file_content(bytes): Данные файла
            filename (list): Название файла
            metadata (dict): Метаданные файла

        Returns:
            ObjectId: Идентификатор загруженного файла

        Notes:
            - Функция может отдавать ошибки motor библиотеки в ходе выполнения
        """

        file_id = await grid_fs_bucket.upload_from_stream(
            filename,
            file_content,
            metadata=metadata,
        )
        return file_id

    @staticmethod
    async def find_files(
        query: dict,
    ) -> AsyncIOMotorGridOutCursor:
        """
        Получение курсора на файлы из grid_fs по параметрам запроса

        Args:
            query(dict): Параметры запроса

        Returns:
            AsyncIOMotorGridOut: Курсор на файлы

        Notes:
            - Функция может отдавать ошибки motor библиотеки в ходе выполнения
        """

        return grid_fs_bucket.find(query)

    @staticmethod
    async def download_file(file_id: PydanticObjectId) -> AsyncIOMotorGridOut:
        """
        Получение файла из grid_fs

        Args:
            file_id(str | ObjectId | PydanticObjectId): Идентификатор файла

        Returns:
            AsyncIOMotorGridOut

        Notes:
            - Функция может отдавать ошибки motor библиотеки в ходе выполнения
        """

        return await grid_fs_bucket.open_download_stream(file_id)

    @staticmethod
    async def delete_file(
        file_id: PydanticObjectId,
    ) -> bool:
        """
        Удаление файла из grid_fs

        Args:
            file_id(str | ObjectId | PydanticObjectId): Идентификатор файла

        Returns:
            bool: Был ли удален файл
        """

        try:
            await grid_fs_bucket.delete(file_id)
            return True
        except NoFile:
            return False

    @staticmethod
    async def open_download_stream(
        file_id: PydanticObjectId,
    ) -> AsyncIOMotorGridOut:
        """
        Удаление файла из grid_fs

        Args:
            file_id(str | ObjectId | PydanticObjectId): Идентификатор файла

        Returns:
            bool: Был ли удален файл
        """

        return await grid_fs_bucket.open_download_stream(file_id)


async def config_file_manager(mongo_uri: str, db_name: str):
    client = AsyncIOMotorClient(str(mongo_uri))
    db = client.get_database(db_name)
    global grid_fs_bucket
    grid_fs_bucket = AsyncIOMotorGridFSBucket(db)

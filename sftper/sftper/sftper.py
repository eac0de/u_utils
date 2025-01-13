import asyncssh
from file_manager import File

SFTP_FILE_TAG = "sftp"

_HOST: str = ""
_USERNAME: str = ""
_PASSWORD: str = ""
_PRIVATE_KEY: asyncssh.SSHKey = None # type: ignore


class SFTPService:
    """Класс для управления файлами через SFTP"""

    @staticmethod
    async def put(
        file: File,
        remote_path: str,
    ):
        """
        Загрузка локального файла на удалённый сервер

        Args:
            file (File): Файл для загрузки
            remote_path (str): Путь к папке, в которую должен быть загружен файл

        Notes:
            - Функция может отдавать ошибки asyncssh библиотеки в ходе отправки письма
            - При работе на тестовом сервере to_email подменяется на тестовый
        """
        async with asyncssh.connect(
            host=_HOST,
            username=_USERNAME,
            password=_PASSWORD if _PASSWORD else None,
            client_keys=[_PRIVATE_KEY] if _PRIVATE_KEY else None,
            known_hosts=None,  # Указание None отключает проверку
        ) as conn:
            async with conn.start_sftp_client() as sftp:
                async with sftp.open(remote_path + file.name, "wb") as f:
                    await f.write(await file.read())

    @staticmethod
    async def get(
        filename: str,
        remote_path: str,
        tag: str = SFTP_FILE_TAG,
    ) -> File | None:
        """
        Загрузка файла с удалённого сервера в своё хранилище

        Args:
            filename (str): Название файла для загрузки
            remote_path (str): Путь к папке, из которой должен быть загружен файл
            tag (FILE_TAG_CHOICES): Тег файла

        Notes:
            - Функция может отдавать ошибки asyncssh библиотеки в ходе отправки письма
            - При работе на тестовом сервере to_email подменяется на тестовый
        """
        async with asyncssh.connect(
            host=_HOST,
            username=_USERNAME,
            password=_PASSWORD if _PASSWORD else None,
            client_keys=[_PRIVATE_KEY] if _PRIVATE_KEY else None,
            known_hosts=None,  # Указание None отключает проверку
        ) as conn:
            async with conn.start_sftp_client() as sftp:
                remote_file_path = remote_path + filename
                async with sftp.open(remote_file_path, "rb") as remote_file:
                    return await File.create(
                        file_content=await remote_file.read(),
                        filename=filename,
                        tag=tag,
                    )

    @staticmethod
    async def remove(
        filename: str,
        remote_path: str,
    ):
        """
        Удаление файла с удалённого сервера

        Args:
            filename (str): Название файла для удаления
            remote_path (str): Путь к папке, из которой должен быть удален файл

        Notes:
            - Функция может отдавать ошибки asyncssh библиотеки в ходе отправки письма
            - При работе на тестовом сервере to_email подменяется на тестовый
        """
        async with asyncssh.connect(
            host=_HOST,
            username=_USERNAME,
            password=_PASSWORD if _PASSWORD else None,
            client_keys=[_PRIVATE_KEY] if _PRIVATE_KEY else None,
            known_hosts=None,  # Указание None отключает проверку
        ) as conn:
            async with conn.start_sftp_client() as sftp:
                remote_file_path = remote_path + filename
                await sftp.remove(remote_file_path)


async def config_sftp_service(
    host: str,
    username: str,
    password: str | None = None,
    private_key: str | None = None,
):
    global _HOST
    _HOST = host
    global _USERNAME
    _USERNAME = username
    if password:
        global _PASSWORD
        _PASSWORD = password
    if private_key:
        global _PRIVATE_KEY
        _PRIVATE_KEY = asyncssh.import_private_key(private_key)

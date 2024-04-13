from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from tsk.settings import settings


class Database:

    def __init__(self):
        self.engine = create_async_engine(url=settings.DB_URL, echo=settings.ECHO_DB)
        self.session_maker = async_sessionmaker(
            bind=self.engine
        )

    async def get_session(self) -> AsyncSession:
        """
        Передаем сессию
        :return:
        """

        async with self.session_maker.begin() as session:
            yield session
            await session.close()


db_connect = Database()
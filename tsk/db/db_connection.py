from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from settings import settings
from db.mainbase import MainBase
from db.models.UserModel import UserTable
from db.models.PostModel import PostTable


class Database:

    def __init__(self):
        self.engine = create_async_engine(url=settings.db_url, echo=settings.echo_db)
        self.session_maker = async_sessionmaker(
            bind=self.engine
        )

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(MainBase.metadata.create_all)

    async def get_session(self) -> AsyncSession:
        """
        Передаем сессию
        :return:
        """

        async with self.session_maker.begin() as session:
            return session


db_connect: Database = Database()
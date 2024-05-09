from typing import Any, Dict, List, Literal, Tuple, Type, TypeAlias

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import BinaryExpression

from .database import Base, engine, session_factory, session_manager
from .models import StationInfoOrm, StationSocketOrm, StationStatusOrm

StationOrmType: TypeAlias = Type[StationInfoOrm | StationSocketOrm | StationStatusOrm]


class OrmMethods:
    @staticmethod
    async def create_tables() -> None:
        """
        Asynchronously create all database tables based on the SQLAlchemy models' metadata.
        This method initializes the database schema.
        """
        async with engine.connect() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()

    @staticmethod
    async def delete_tables() -> None:
        """
        Asynchronously drop all database tables, effectively clearing the database.
        This method removes all data and schema from the database.
        """
        async with engine.connect() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.commit()

    @staticmethod
    async def insert_unique_data(model: StationOrmType, attributes: Dict[str, Any]) -> int | None:
        """
        Asynchronously inserts new data into the database if it does not exist already.
        Checks for existing data with the same attributes before inserting new entries.

        Args:
            model: The ORM model class for the data to be added.
            attributes: A dictionary of attributes for the new model instance.

        Returns:
            The ID of the newly inserted data, or None if data already exists.
        """
        async with session_factory() as session:
            async with session.begin():
                data = await session.execute(select(model).filter_by(**attributes))
                data = data.scalars().first()
                if data is None:
                    new_data = model(**attributes)
                    session.add(new_data)
                    await session.flush()  # Fix changes to get an id of a new data
                    return new_data.id
                return None


class StationOrmMethod:
    @session_manager
    async def add_stations(self, session: AsyncSession, station_list: List[Dict[str, Dict[str, Any]]]) -> None:
        """
        Adds or updates station entries in the database. Utilizes upsert operations to ensure that
        station data is inserted or updated based on unique constraints.

        Args:
            session: An AsyncSession instance provided by the session manager.
            station_list: A list of dictionaries describing the station data.
        """
        for station in station_list:
            await self._upsert_data(session, StationInfoOrm, station["info"], ["number"])

            station["socket"]["station_id"] = await self._fetch_id(
                session,
                StationInfoOrm,
                StationInfoOrm.number == station["info"]["number"],
            )
            await self._upsert_data(session, StationSocketOrm, station["socket"], ["station_id", "socket"])

            station["status"]["station_type_id"] = await self._fetch_id(
                session,
                StationSocketOrm,
                StationSocketOrm.station_id == station["socket"]["station_id"],
                StationSocketOrm.socket == station["socket"]["type"],
            )
            await self._insert_data(session, StationStatusOrm, station["status"])

    @staticmethod
    def _conditions(
        station: Dict[str, Dict[str, Any]], info_type: Literal["info", "socket"]
    ) -> Tuple[BinaryExpression, ...]:
        if info_type == "info":
            return StationInfoOrm.number == station["info"]["number"]
        return (
            StationSocketOrm.station_id == station["socket"]["station_id"],
            StationSocketOrm.socket == station["socket"]["socket"],
        )

    @staticmethod
    async def _upsert_data(session: AsyncSession, model: StationOrmType, data: dict, unique: list[str]) -> None:
        """
        Performs an upsert operation on the database for the given model using the provided data.
        An upsert operation either inserts a new row or updates an existing row if there is a conflict
        on the unique constraints.

        Args:
            session: The database session to use.
            model: The ORM model class.
            data: Dictionary of data to insert or update.
            unique: List of attributes that define uniqueness for the upsert operation.

        Example SQL (PostgreSQL):
            INSERT INTO station_info (number, other_column) VALUES ('123', 'data')
            ON CONFLICT (number) DO UPDATE SET other_column = EXCLUDED.other_column;
        """
        set_ = {k: v for k, v in data.items() if k not in unique}
        stmt = insert(model).values(**data).on_conflict_do_update(
            index_elements=unique,
            set_=set_,
        )
        await session.execute(stmt)

    @staticmethod
    async def _fetch_id(session: AsyncSession, model: StationOrmType, *conditions: bool) -> int:
        """
        Fetches the ID of an entry that matches the given conditions.

        Args:
            session: The database session to use.
            model: The ORM model class.
            conditions: Conditions to filter the query.

        Returns:
            The ID of the found entry.
        """
        record = await session.execute(select(model.id).where(*conditions))
        return record.scalar_one()

    @staticmethod
    async def _insert_data(session: AsyncSession, model: StationOrmType, data: dict) -> None:
        """
        Inserts new data into the database for the specified model. This method only handles
        insertions and does not check for conflicts with existing data.

        Args:
            session: The database session to use.
            model: The ORM model class.
            data: Dictionary of data to be inserted.

        Example SQL (PostgreSQL):
            INSERT INTO station_status (station_id, status) VALUES (1, 'Active');
        """
        new_status = model(**data)
        session.add(new_status)

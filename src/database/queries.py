from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from .database import engine, session_factory, Base
from .models import StationInfoOrm, StationTypeOrm, StationStatusOrm


class OrmMethods:
    @staticmethod
    async def create_tables():
        """
        Asynchronously create all tables in the database using metadata.
        This should be called to initialize the database schema.
        """
        async with engine.connect() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()

    @staticmethod
    async def delete_tables():
        """
        Asynchronously drop all tables in the database.
        This will remove all data and the schema from the database.
        """
        async with engine.connect() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.commit()

    @staticmethod
    async def add_new_data(model, attributes):
        """
        Asynchronously add new data to the database if it does not already exist.
        :param model: The ORM model class to which the data should be added.
        :param attributes: A dictionary of attributes to be set on the new model instance.
        :return: The ID of the new or existing data.
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


class StationOrmMethod:
    async def add_stations(self, station_list):
        async with session_factory() as session:
            for station in station_list:
                await self._upsert(session, StationInfoOrm, station["StationInfo"], ["number"])

                station["StationType"]["station_id"] = await self._get_id(
                    session,
                    StationInfoOrm,
                    StationInfoOrm.number == station["StationInfo"]["number"],
                )
                await self._upsert(session, StationTypeOrm, station["StationType"], ["station_id", "type"])

                station["StationStatus"]["station_type_id"] = await self._get_id(
                    session,
                    StationTypeOrm,
                    StationTypeOrm.station_id == station["StationType"]["station_id"],
                    StationTypeOrm.type == station["StationType"]['type']
                )
                await self._insert(session, StationStatusOrm, station["StationStatus"])

            await session.commit()

    @staticmethod
    def _conditions(station, info_type):
        if info_type == "StationInfo":
            return StationInfoOrm.number == station["StationInfo"]["number"]
        elif info_type == "StationType":
            return (StationTypeOrm.station_id == station["StationType"]["station_id"],
                    StationTypeOrm.type == station["StationType"]["type"])

    @staticmethod
    async def _upsert(session, model, data: dict, unique: list[str]):
        set_ = {k: v for k, v in data.items() if k not in unique}
        stmt = insert(model).values(**data).on_conflict_do_update(
            index_elements=unique,
            set_=set_,
        )
        await session.execute(stmt)

    @staticmethod
    async def _get_id(session, model, *conditions) -> int:
        record = await session.execute(
            select(model.id).where(*conditions)
        )
        return record.scalar_one()

    @staticmethod
    async def _insert(session, model, data: dict):
        new_status = model(**data)
        session.add(new_status)

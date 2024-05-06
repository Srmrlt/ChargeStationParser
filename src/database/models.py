import datetime

from typing import Annotated
from sqlalchemy import ForeignKey, text, Column, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint

from .database import Base, str_256


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class StationInfoOrm(Base):
    __tablename__ = 'station_info'

    id: Mapped[intpk]
    number: Mapped[int] = Column(Integer, unique=True)
    # city: Mapped[str]
    # address = Mapped[str]
    # name = Mapped[str]
    city: Mapped[str] = Column(String)
    address: Mapped[str] = Column(String)
    name: Mapped[str] = Column(String)
    created_at: Mapped[created_at]

    station_type: Mapped[list['StationTypeOrm']] = relationship(
        back_populates='station_info',
    )


class StationTypeOrm(Base):
    __tablename__ = 'station_type'

    id: Mapped[intpk]
    station_id: Mapped[int] = mapped_column(ForeignKey('station_info.id', ondelete='CASCADE'))
    type: Mapped[str] = Column(String)
    power: Mapped[int] = Column(Integer)
    created_at: Mapped[created_at]

    __table_args__ = (UniqueConstraint('station_id', 'type', name='station_id_type_unique'),)

    station_info: Mapped['StationInfoOrm'] = relationship(
        back_populates='station_type'
    )
    station_status: Mapped[list['StationStatusOrm']] = relationship(
        back_populates='station_type',
    )


class StationStatusOrm(Base):
    __tablename__ = 'station_status'

    id: Mapped[intpk]
    station_type_id: Mapped[int] = mapped_column(ForeignKey('station_type.id', ondelete='CASCADE'))
    status: Mapped[str_256]
    timestamp: Mapped[datetime.datetime]

    station_type: Mapped['StationTypeOrm'] = relationship(
        back_populates='station_status'
    )

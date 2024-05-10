import datetime
from typing import Annotated

from sqlalchemy import DateTime, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import PrimaryKeyConstraint, UniqueConstraint

from .database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class StationInfoOrm(Base):
    __tablename__ = "station_info"

    id: Mapped[intpk]
    number: Mapped[int] = mapped_column(unique=True)
    city: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str]
    name: Mapped[str]
    created_at: Mapped[created_at]

    station_socket: Mapped[list["StationSocketOrm"]] = relationship(back_populates="station_info")


class StationSocketOrm(Base):
    __tablename__ = "station_socket"
    __table_args__ = (UniqueConstraint("station_id", "socket", name="station_id_socket_unique"),)

    id: Mapped[intpk]
    station_id: Mapped[int] = mapped_column(ForeignKey("station_info.id", ondelete="CASCADE"))
    socket: Mapped[str]
    power: Mapped[int]
    created_at: Mapped[created_at]

    station_info: Mapped["StationInfoOrm"] = relationship(back_populates="station_socket")
    station_status: Mapped[list["StationStatusOrm"]] = relationship(back_populates="station_socket")


class StationStatusOrm(Base):
    __tablename__ = "station_status"
    __table_args__ = (
        PrimaryKeyConstraint("station_socket_id", "timestamp"),
    )

    station_socket_id: Mapped[int] = mapped_column(ForeignKey("station_socket.id", ondelete="CASCADE"))
    status: Mapped[str]
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))

    station_socket: Mapped["StationSocketOrm"] = relationship(back_populates="station_status")

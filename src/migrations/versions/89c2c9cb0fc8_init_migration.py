"""init migration

Revision ID: 89c2c9cb0fc8
Revises:
Create Date: 2024-05-13 16:19:45.175669

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "89c2c9cb0fc8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "station_info",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("number"),
    )
    op.create_table(
        "station_socket",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("station_id", sa.Integer(), nullable=False),
        sa.Column("charger_port", sa.Integer(), nullable=False),
        sa.Column("socket", sa.String(), nullable=False),
        sa.Column("power", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["station_id"], ["station_info.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "station_id",
            "charger_port",
            "socket",
            name="station_id_charger_port_socket_unique",
        ),
    )
    op.create_table(
        "station_status",
        sa.Column("station_socket_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["station_socket_id"], ["station_socket.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("station_socket_id", "timestamp"),
    )
    op.create_index(
        "station_status_timestamp_idx",
        "station_status",
        ["timestamp"],
        unique=False,
    )
    op.execute("SELECT create_hypertable('station_status', by_range('timestamp'))")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("station_status_timestamp_idx", table_name="station_status")
    op.drop_table("station_status")
    op.drop_table("station_socket")
    op.drop_table("station_info")
    # ### end Alembic commands ###

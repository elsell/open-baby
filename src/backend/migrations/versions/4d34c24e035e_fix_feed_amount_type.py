"""Fix bottle feed amount type and enforce non-null constraints.

Revision ID: 4d34c24e035e
Revises: 2acdd28299a7
Create Date: 2025-08-26 17:05:20.912901

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4d34c24e035e"
down_revision: Union[str, Sequence[str], None] = "2acdd28299a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "sqlite":
        # SQLite doesn't support ALTER COLUMN TYPE
        with op.batch_alter_table("bottle_feed_events", recreate="always") as batch_op:
            batch_op.alter_column(
                "amount_ml",
                existing_type=sa.VARCHAR(),
                type_=sa.Integer(),
                existing_nullable=False,
            )

        with op.batch_alter_table("events", recreate="always") as batch_op:
            batch_op.alter_column("name", existing_type=sa.VARCHAR(), nullable=False)
            batch_op.alter_column(
                "description", existing_type=sa.VARCHAR(), nullable=False
            )

    else:
        # Postgres/MySQL/etc. can alter in place
        op.alter_column(
            "bottle_feed_events",
            "amount_ml",
            existing_type=sa.VARCHAR(),
            type_=sa.Integer(),
            existing_nullable=False,
        )
        op.alter_column("events", "name", existing_type=sa.VARCHAR(), nullable=False)
        op.alter_column(
            "events", "description", existing_type=sa.VARCHAR(), nullable=False
        )


def downgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "sqlite":
        with op.batch_alter_table("events", recreate="always") as batch_op:
            batch_op.alter_column(
                "description", existing_type=sa.VARCHAR(), nullable=True
            )
            batch_op.alter_column("name", existing_type=sa.VARCHAR(), nullable=True)

        with op.batch_alter_table("bottle_feed_events", recreate="always") as batch_op:
            batch_op.alter_column(
                "amount_ml",
                existing_type=sa.Integer(),
                type_=sa.VARCHAR(),
                existing_nullable=False,
            )
    else:
        op.alter_column(
            "events", "description", existing_type=sa.VARCHAR(), nullable=True
        )
        op.alter_column("events", "name", existing_type=sa.VARCHAR(), nullable=True)
        op.alter_column(
            "bottle_feed_events",
            "amount_ml",
            existing_type=sa.Integer(),
            type_=sa.VARCHAR(),
            existing_nullable=False,
        )

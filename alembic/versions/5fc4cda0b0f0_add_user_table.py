"""Add user table

Revision ID: 5fc4cda0b0f0
Revises: cae1a6f2cb35
Create Date: 2023-11-01 09:02:06.806238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5fc4cda0b0f0'
down_revision: Union[str, None] = 'cae1a6f2cb35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass

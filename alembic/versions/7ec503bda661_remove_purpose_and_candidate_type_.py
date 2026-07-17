"""remove purpose and candidate_type columns in otp_verifications table

Revision ID: 7ec503bda661
Revises: 8c3b1a4d9e20
Create Date: 2026-07-16 21:51:17.326538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ec503bda661'
down_revision: Union[str, Sequence[str], None] = '8c3b1a4d9e20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column("otp_verifications", "purpose")
    op.drop_column("otp_verifications", "candidate_type")


def downgrade():
    op.add_column(
        "otp_verifications",
        sa.Column("purpose", sa.String(50), nullable=True)
    )

    op.add_column(
        "otp_verifications",
        sa.Column("candidate_type", sa.String(30), nullable=True)
    )
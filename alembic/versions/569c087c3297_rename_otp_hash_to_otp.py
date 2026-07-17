"""rename otp_hash to otp

Revision ID: 8c3b1a4d9e20
Revises: 5fa35f84d8a5
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision = "8c3b1a4d9e20"
down_revision = "5fa35f84d8a5"
branch_labels = None
depends_on = None


def upgrade():

    op.alter_column(
        "otp_verifications",
        "otp_hash",
        new_column_name="otp"
    )


def downgrade():

    op.alter_column(
        "otp_verifications",
        "otp",
        new_column_name="otp_hash"
    )
"""create password_reset_otps

Revision ID: b7c2d4e6f8a1
Revises: a1f6810d14b7
Create Date: 2026-09-30 13:00:00.000000

Stores forgot-password OTPs separately from the registration
OTPs in otp_verifications, so the two flows do not clash.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b7c2d4e6f8a1"
down_revision: Union[str, Sequence[str], None] = "a1f6810d14b7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "password_reset_otps",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("otp_hash", sa.String(255), nullable=False),
        sa.Column("is_used", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_index(
        "ix_password_reset_otps_id",
        "password_reset_otps",
        ["id"],
    )

    op.create_index(
        "ix_password_reset_otps_email",
        "password_reset_otps",
        ["email"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_password_reset_otps_email",
        table_name="password_reset_otps",
    )

    op.drop_index(
        "ix_password_reset_otps_id",
        table_name="password_reset_otps",
    )

    op.drop_table("password_reset_otps")

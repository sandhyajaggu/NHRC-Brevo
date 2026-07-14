"""create otp_verifications

Revision ID: f765b62476b7
Revises: 3912457500a3
Create Date: 2026-07-13 14:44:02.149197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f765b62476b7'
down_revision: Union[str, Sequence[str], None] = '3912457500a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "otp_verifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("otp_hash", sa.String(255), nullable=False),
        sa.Column("purpose", sa.String(50), nullable=False),
        sa.Column("candidate_type", sa.String(30), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_sent_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_index(
        "ix_otp_verifications_email",
        "otp_verifications",
        ["email"],
    )


def downgrade():
    op.drop_index(
        "ix_otp_verifications_email",
        table_name="otp_verifications",
    )

    op.drop_table("otp_verifications")
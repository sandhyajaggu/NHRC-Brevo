"""add otp fields

Revision ID: 3912457500a3
Revises: 3f868395bcec
"""

from alembic import op
import sqlalchemy as sa


revision = "3912457500a3"
down_revision = "3f868395bcec"
branch_labels = None
depends_on = None


def upgrade():

    op.add_column(
        "employees",
        sa.Column("email_otp", sa.String(length=10), nullable=True)
    )

    op.add_column(
        "employees",
        sa.Column("otp_expiry", sa.DateTime(timezone=True), nullable=True)
    )

    op.add_column(
        "employees",
        sa.Column(
            "otp_verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false")
        )
    )

    op.add_column(
        "employees",
        sa.Column(
            "otp_attempts",
            sa.Integer(),
            nullable=False,
            server_default="0"
        )
    )

    op.add_column(
        "employees",
        sa.Column("last_otp_sent", sa.DateTime(timezone=True), nullable=True)
    )


def downgrade():

    op.drop_column("employees", "last_otp_sent")
    op.drop_column("employees", "otp_attempts")
    op.drop_column("employees", "otp_verified")
    op.drop_column("employees", "otp_expiry")
    op.drop_column("employees", "email_otp")
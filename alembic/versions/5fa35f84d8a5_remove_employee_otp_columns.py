"""remove employee otp columns

Revision ID: 5fa35f84d8a5
Revises: f765b62476b7
Create Date: 2026-07-14 14:04:16.278915

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = "5fa35f84d8a5"
down_revision: Union[str, Sequence[str], None] = "f765b62476b7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Remove old OTP columns from employees table."""

    op.drop_column("employees", "email_otp")
    op.drop_column("employees", "otp_expiry")
    op.drop_column("employees", "otp_verified")
    op.drop_column("employees", "otp_attempts")
    op.drop_column("employees", "last_otp_sent")


def downgrade() -> None:
    """Restore old OTP columns."""

    op.add_column(
        "employees",
        sa.Column("email_otp", sa.String(length=10), nullable=True),
    )

    op.add_column(
        "employees",
        sa.Column("otp_expiry", sa.DateTime(timezone=True), nullable=True),
    )

    op.add_column(
        "employees",
        sa.Column(
            "otp_verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )

    op.add_column(
        "employees",
        sa.Column(
            "otp_attempts",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "employees",
        sa.Column(
            "last_otp_sent",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )
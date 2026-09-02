"""add ticket comments

Revision ID: 547613dafd2c
Revises: fe3506106a2c
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "547613dafd2c"
down_revision: Union[str, Sequence[str], None] = "fe3506106a2c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ticket_comments",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "ticket_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "comment",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["ticket_id"],
            ["tickets.id"],
            ondelete="CASCADE",
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
    )

    op.create_index(
        "ix_ticket_comments_ticket_id",
        "ticket_comments",
        ["ticket_id"],
        unique=False,
    )

    op.create_index(
        "ix_ticket_comments_user_id",
        "ticket_comments",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_ticket_comments_user_id",
        table_name="ticket_comments",
    )

    op.drop_index(
        "ix_ticket_comments_ticket_id",
        table_name="ticket_comments",
    )

    op.drop_table("ticket_comments")
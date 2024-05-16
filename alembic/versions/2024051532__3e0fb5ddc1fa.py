"""empty message

Revision ID: 3e0fb5ddc1fa
Revises:
Create Date: 2024-05-15 18:32:04.858312

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "3e0fb5ddc1fa"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "attorneys",
        sa.Column("attorney_id", sa.Uuid(as_uuid=False), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("email", sa.String(length=256), nullable=False),
        sa.Column("hashed_password", sa.String(length=128), nullable=False),
        sa.Column(
            "create_time",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "update_time",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("attorney_id"),
    )
    op.create_index(op.f("ix_attorneys_email"), "attorneys", ["email"], unique=True)
    op.create_table(
        "prospects",
        sa.Column("prospect_id", sa.Uuid(as_uuid=False), nullable=False),
        sa.Column("email", sa.String(length=256), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("resume", sa.String(length=128), nullable=False),
        sa.Column(
            "create_time",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "update_time",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("prospect_id"),
    )
    op.create_index(op.f("ix_prospects_email"), "prospects", ["email"], unique=True)
    op.create_table(
        "leads",
        sa.Column("lead_id", sa.Uuid(as_uuid=False), nullable=False),
        sa.Column("attorney_id", sa.Uuid(as_uuid=False), nullable=False),
        sa.Column("prospect_id", sa.Uuid(as_uuid=False), nullable=False),
        sa.Column("state", sa.String(length=64), nullable=False),
        sa.Column(
            "create_time",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "update_time",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["attorney_id"], ["attorneys.attorney_id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["prospect_id"], ["prospects.prospect_id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("lead_id"),
    )
    op.create_table(
        "refresh_token",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("refresh_token", sa.String(length=512), nullable=False),
        sa.Column("used", sa.Boolean(), nullable=False),
        sa.Column("exp", sa.BigInteger(), nullable=False),
        sa.Column("attorney_id", sa.Uuid(as_uuid=False), nullable=False),
        sa.Column(
            "create_time",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "update_time",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["attorney_id"], ["attorneys.attorney_id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_refresh_token_refresh_token"),
        "refresh_token",
        ["refresh_token"],
        unique=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_refresh_token_refresh_token"), table_name="refresh_token")
    op.drop_table("refresh_token")
    op.drop_table("leads")
    op.drop_index(op.f("ix_prospects_email"), table_name="prospects")
    op.drop_table("prospects")
    op.drop_index(op.f("ix_attorneys_email"), table_name="attorneys")
    op.drop_table("attorneys")
    # ### end Alembic commands ###
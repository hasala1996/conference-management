import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = "7d58b669b76b"
down_revision = "6782476d034d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "speaker_assignment",
        "session_id",
        existing_type=sa.Integer(),
        type_=UUID(as_uuid=True),
        existing_nullable=False,
    )
    op.alter_column(
        "speaker_assignment",
        "speaker_id",
        existing_type=sa.Integer(),
        type_=UUID(as_uuid=True),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "speaker_assignment",
        "session_id",
        existing_type=UUID(as_uuid=True),
        type_=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        "speaker_assignment",
        "speaker_id",
        existing_type=UUID(as_uuid=True),
        type_=sa.Integer(),
        existing_nullable=False,
    )

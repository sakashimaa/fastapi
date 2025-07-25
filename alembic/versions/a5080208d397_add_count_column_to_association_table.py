"""add count column to association table

Revision ID: a5080208d397
Revises: 29227ce339a5
Create Date: 2025-06-07 11:00:57.699706

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a5080208d397"
down_revision: Union[str, None] = "29227ce339a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "order_product_association",
        sa.Column("count", sa.Integer(), server_default="1", nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("order_product_association", "count")
    # ### end Alembic commands ###

"""init

Revision ID: 436f71a01a07
Revises: 
Create Date: 2023-09-17 14:50:08.326385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '436f71a01a07'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:# ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('vk_id', sa.INTEGER(), nullable=False),
    sa.Column('first_name', sa.VARCHAR(), nullable=True),
    sa.Column('last_name', sa.VARCHAR(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('state', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('vk_id')
    )
    op.create_index('ix_users_vk_id', 'users', ['vk_id'], unique=False)
    op.create_index('ix_users_last_name', 'users', ['last_name'], unique=False)
    op.create_index('ix_users_first_name', 'users', ['first_name'], unique=False)
    op.create_table('messages',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('text', sa.VARCHAR(), nullable=True),
    sa.Column('sender_id', sa.INTEGER(), nullable=True),
    sa.Column('sent_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['sender_id'], ['users.vk_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_messages_id', 'messages', ['id'], unique=False)
    # ### end Alembic commands ###



def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_messages_id', table_name='messages')
    op.drop_table('messages')
    op.drop_index('ix_users_first_name', table_name='users')
    op.drop_index('ix_users_last_name', table_name='users')
    op.drop_index('ix_users_vk_id', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###

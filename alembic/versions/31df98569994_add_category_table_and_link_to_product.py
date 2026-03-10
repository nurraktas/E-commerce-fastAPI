"""add category table and link to product 

Revision ID: 31df98569994
Revises: c5d59fe43ae2
Create Date: 2026-02-21 15:33:29.992534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31df98569994'
down_revision=  None



def upgrade() -> None:
   op.create_table(
    'category',
      sa.Column('id', sa.Integer(), primary_key = True),
      sa.Column('name', sa.String(length=100), nullable=False),
      sa.Column('description', sa.String(length=200),nullable=True )
   )

   op.add_column('product', sa.Column('category_id', sa.Integer(), nullable= True))

   op.create_foreign_key(
     'fk_product_category',
     'product', 'category',
     ['category_id'], ['id'],
      ondelete='CASCADE'
   )



   


def downgrade() -> None:
   op.drop_constraint('fk_product_category', 'product', type_='foreignkey')

   op.drop_column('product', 'category_id')

   op.drop_table('category')
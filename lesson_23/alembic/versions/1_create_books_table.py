from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'books',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('author', sa.String),
        sa.Column('date_of_release', sa.Date),
        sa.Column('description', sa.String),
        sa.Column('genre', sa.String)
    )

def downgrade():
    op.drop_table('books')

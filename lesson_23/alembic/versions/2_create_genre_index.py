from alembic import op

def upgrade():
    op.create_index('idx_genre', 'books', ['genre'])

def downgrade():
    op.drop_index('idx_genre', 'books')

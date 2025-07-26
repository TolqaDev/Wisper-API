from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('converted_sounds',
        sa.Column('uuid', sa.String(length=36), nullable=False),
        sa.Column('talent_id', sa.String(length=50), nullable=False),
        sa.Column('acc_id', sa.String(length=50), nullable=False),
        sa.Column('text', sa.Text(), nullable=True),
        sa.Column('encoded_text', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('uuid')
    )

    op.create_index('ix_converted_sounds_talent_id', 'converted_sounds', ['talent_id'], unique=False)
    op.create_index('ix_converted_sounds_acc_id', 'converted_sounds', ['acc_id'], unique=False)
    op.create_index('ix_converted_sounds_status', 'converted_sounds', ['status'], unique=False)

def downgrade() -> None:
    op.drop_index('ix_converted_sounds_status', table_name='converted_sounds')
    op.drop_index('ix_converted_sounds_acc_id', table_name='converted_sounds')
    op.drop_index('ix_converted_sounds_talent_id', table_name='converted_sounds')

    op.drop_table('converted_sounds')

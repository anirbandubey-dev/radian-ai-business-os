"""add Clerk identity and explicit memberships"""
from alembic import op
import sqlalchemy as sa
import uuid
revision = "0002_clerk_identity"
down_revision = "0001_identity"
branch_labels = None
depends_on = None
def upgrade() -> None:
    op.add_column("organizations", sa.Column("clerk_organization_id", sa.String(191), nullable=True))
    op.create_index("ix_organizations_clerk_organization_id", "organizations", ["clerk_organization_id"], unique=True)
    op.add_column("users", sa.Column("clerk_user_id", sa.String(191), nullable=True))
    op.create_index("ix_users_clerk_user_id", "users", ["clerk_user_id"], unique=True)
    op.alter_column("users", "password_hash", existing_type=sa.String(255), nullable=True)
    op.create_table("organization_memberships", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("organization_id", sa.Uuid(), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("role", sa.String(32), nullable=False, server_default="member"), sa.Column("created_at", sa.DateTime(), nullable=False), sa.UniqueConstraint("organization_id", "user_id", name="uq_org_user"))
def downgrade() -> None:
    op.drop_table("organization_memberships"); op.drop_index("ix_users_clerk_user_id", "users"); op.drop_column("users", "clerk_user_id"); op.drop_index("ix_organizations_clerk_organization_id", "organizations"); op.drop_column("organizations", "clerk_organization_id")

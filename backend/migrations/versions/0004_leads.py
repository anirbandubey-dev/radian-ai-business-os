"""create leads"""
from alembic import op
import sqlalchemy as sa
revision="0004_leads"; down_revision="0003_accounts_contacts"; branch_labels=None; depends_on=None
def upgrade():
    op.create_table("leads",sa.Column("id",sa.Uuid(),primary_key=True),sa.Column("organization_id",sa.Uuid(),sa.ForeignKey("organizations.id",ondelete="CASCADE"),nullable=False),sa.Column("first_name",sa.String(100),nullable=False),sa.Column("last_name",sa.String(100),nullable=False),sa.Column("full_name",sa.String(205),nullable=False),sa.Column("email",sa.String(320)),sa.Column("phone",sa.String(40)),sa.Column("company_name",sa.String(200)),sa.Column("job_title",sa.String(120)),sa.Column("source",sa.String(60),nullable=False),sa.Column("status",sa.String(40),nullable=False),sa.Column("score",sa.Integer(),nullable=False),sa.Column("owner_id",sa.Uuid(),sa.ForeignKey("users.id",ondelete="SET NULL")),sa.Column("account_id",sa.Uuid(),sa.ForeignKey("accounts.id",ondelete="SET NULL")),sa.Column("contact_id",sa.Uuid(),sa.ForeignKey("contacts.id",ondelete="SET NULL")),sa.Column("notes",sa.Text),sa.Column("created_at",sa.DateTime(),nullable=False),sa.Column("updated_at",sa.DateTime(),nullable=False))
    op.create_index("ix_leads_org_status","leads",["organization_id","status"])
def downgrade(): op.drop_index("ix_leads_org_status",table_name="leads"); op.drop_table("leads")

"""admin user init

Revision ID: 1f1e08b75011
Revises: dac592bd4b85
Create Date: 2025-01-02 17:47:14.421177

"""
from typing import Sequence, Union
from uuid import uuid4
import os

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f1e08b75011'
down_revision: Union[str, None] = 'dac592bd4b85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


admin_fullname = os.getenv("ADMIN_FULLNAME")
admin_login = os.getenv("ADMIN_LOGIN")
admin_password = os.getenv("ADMIN_PASSWORD")


def upgrade():

    # Define the roles table
    roles_table = sa.table(
        "roles",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
    )

    # Insert the admin role
    op.bulk_insert(roles_table, [{"name": "admin"}])
    op.bulk_insert(roles_table, [{"name": "stuff"}])

    # Define the users table
    users_table = sa.table(
        "users",
        sa.column("id", sa.UUID),
        sa.column("fullname", sa.String),
        sa.column("login", sa.String),
        sa.column("password", sa.String),
    )

    # Insert the admin user
    admin_id = str(uuid4())
    op.bulk_insert(users_table, [{
        "id": admin_id,
        "fullname": admin_fullname,
        "login": admin_login,
        "password": admin_password,
    }])

    # Define the user_roles table
    user_roles_table = sa.table(
        "user_roles",
        sa.column("user_id", sa.UUID),
        sa.column("role_id", sa.Integer),
    )

    # Assign the admin role to the admin user
    op.bulk_insert(user_roles_table, [{
        "user_id": admin_id,
        "role_id": 1,
    }])


def downgrade():
    # Define the user_roles table
    user_roles_table = sa.table(
        "user_roles",
        sa.column("user_id", sa.UUID),
        sa.column("role_id", sa.Integer),
    )

    # Define the users table
    users_table = sa.table(
        "users",
        sa.column("id", sa.UUID),
    )

    # Define the roles table
    roles_table = sa.table(
        "roles",
        sa.column("id", sa.Integer),
    )

    # Remove the admin role from the admin user
    op.execute(user_roles_table.delete().where(user_roles_table.c.role_id == 1))

    # Remove the admin user
    op.execute(users_table.delete().where(users_table.c.login == admin_login))

    # Remove the admin role
    op.execute(roles_table.delete().where(roles_table.c.name == "admin"))

    op.execute(roles_table.delete().where(roles_table.c.name == "stuff"))

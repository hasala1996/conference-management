"""
Seed data script to initialize the database with a user, role, and permissions.
"""

import uuid

from adapters.database import Base
from adapters.database.models.permission_model import Permission
from adapters.database.models.role_model import Role
from adapters.database.models.role_permission_model import RolePermission
from adapters.database.models.user_model import User
from adapters.database.models.user_role_model import UserRole
from config import settings
from passlib.hash import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ensure the tables are created in the database
Base.metadata.create_all(bind=engine)


def seed_data(db: Session):
    """
    Seeds the database with an admin user, an admin role, and all permissions.

    Args:
        db (Session): The database session.
    """
    # Create permissions
    permissions = [
        {"name": "create_event", "description": "Create an event"},
        {"name": "update_event", "description": "Update an event"},
        {"name": "delete_event", "description": "Delete an event"},
        {"name": "view_event", "description": "View an event"},
        {"name": "manage_users", "description": "Manage users in the system"},
    ]

    for perm_data in permissions:
        permission = Permission(
            id=uuid.uuid4(),
            name=perm_data["name"],
            description=perm_data["description"],
        )
        db.add(permission)

    db.commit()

    # Create Admin role
    admin_role = Role(
        id=uuid.uuid4(),
        name="Admin",
        description="Administrator role with full permissions",
    )
    db.add(admin_role)
    db.commit()

    # Assign all permissions to Admin role
    all_permissions = db.query(Permission).all()
    for perm in all_permissions:
        role_permission = RolePermission(
            id=uuid.uuid4(),
            role_id=admin_role.id,
            permission_id=perm.id,
        )
        db.add(role_permission)

    db.commit()

    # Create Admin user
    admin_user = User(
        id=uuid.uuid4(),
        email="admin@example.com",
        password=bcrypt.hash("admin123"),  # Use hashed password
        is_active=True,
    )
    db.add(admin_user)
    db.commit()

    # Assign Admin role to the user
    user_role = UserRole(
        id=uuid.uuid4(),
        user_id=admin_user.id,
        role_id=admin_role.id,
    )
    db.add(user_role)
    db.commit()

    print("Seed data created successfully!")


if __name__ == "__main__":
    with SessionLocal() as db:
        seed_data(db)

"""
Seed data script to initialize the database with users, roles, permissions, sessions, and speakers.
"""

import uuid
from datetime import datetime, timedelta

from adapters.database import Base
from adapters.database.models import (
    Permission,
    Role,
    RolePermission,
    ScheduledSession,
    Speaker,
    SpeakerAssignment,
    User,
    UserRole,
)
from config import settings
from passlib.hash import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Database connection
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ensure the tables are created in the database
Base.metadata.create_all(bind=engine)


def seed_data(data_base: Session):
    """
    Seeds the database with admin users, roles, permissions, sessions, and speakers.

    Args:
        data_base (Session): The database session.
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
        data_base.add(permission)

    data_base.commit()

    # Create Admin role
    admin_role = Role(
        id=uuid.uuid4(),
        name="Admin",
        description="Administrator role with full permissions",
    )
    data_base.add(admin_role)
    data_base.commit()

    # Assign all permissions to Admin role
    all_permissions = data_base.query(Permission).all()
    for perm in all_permissions:
        role_permission = RolePermission(
            id=uuid.uuid4(),
            role_id=admin_role.id,
            permission_id=perm.id,
        )
        data_base.add(role_permission)

    data_base.commit()

    # Create Admin user
    admin_user = User(
        id=uuid.uuid4(),
        email="admin@example.com",
        password=bcrypt.hash("admin123"),  # Use hashed password
        is_active=True,
    )
    data_base.add(admin_user)
    data_base.commit()

    # Assign Admin role to the user
    user_role = UserRole(
        id=uuid.uuid4(),
        user_id=admin_user.id,
        role_id=admin_role.id,
    )
    data_base.add(user_role)
    data_base.commit()

    # Create speakers
    speakers_data = [
        {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "biography": "Expert in AI.",
        },
        {
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "biography": "Data Science Professional.",
        },
    ]

    speakers = []
    for speaker_data in speakers_data:
        speaker = Speaker(
            id=uuid.uuid4(),
            name=speaker_data["name"],
            email=speaker_data["email"],
            biography=speaker_data["biography"],
        )
        data_base.add(speaker)
        speakers.append(speaker)

    data_base.commit()

    # Create sessions
    sessions_data = [
        {
            "title": "Introduction to AI",
            "description": "Learn the basics of AI and machine learning.",
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=2),
            "capacity": 50,
        },
        {
            "title": "Data Science Workshop",
            "description": "Hands-on workshop on data analysis techniques.",
            "start_time": datetime.now() + timedelta(days=1),
            "end_time": datetime.now() + timedelta(days=1, hours=3),
            "capacity": 30,
        },
    ]

    for session_data in sessions_data:
        session = ScheduledSession(
            id=uuid.uuid4(),
            title=session_data["title"],
            description=session_data["description"],
            start_time=session_data["start_time"],
            end_time=session_data["end_time"],
            capacity=session_data["capacity"],
        )
        data_base.add(session)
        data_base.commit()

        # Assign speakers to the session
        for speaker in speakers:
            speaker_assignment = SpeakerAssignment(
                id=uuid.uuid4(),
                session_id=session.id,
                speaker_id=speaker.id,
                role="Presenter",
            )
            data_base.add(speaker_assignment)

        data_base.commit()

    print("Seed data created successfully!")


if __name__ == "__main__":
    with SessionLocal() as data_base:
        seed_data(data_base)

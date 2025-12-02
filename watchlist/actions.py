import logging
import json

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert

from .model import Media, User, engine

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def lookup_user(user, session):
    stmt = select(User.username).where(User.username == user.name)
    return session.execute(stmt).one_or_none()

def add_user(member, session):
    saved_user = session.scalars(
        insert(User).values(
            username=member.name,
            display_name=member.display_name
        ).returning(User)
    )
    return saved_user

def get_db_user(member, session):
    saved_user = lookup_user(member, session)
    if not saved_user:
        logger.debug(f"User {member.name} not found. Creating...")
        saved_user = add_user(member, session)
        logger.debug(f"User {member.name} created.")
    return saved_user

def add_to_watchlist(media, member):
    with Session(engine) as session:
        user = get_db_user(member, session)
        logger.debug(f"User found: {user!r}")
        logger.debug(json.dumps(media, indent=4, sort_keys=True))
        session.commit()
    return False


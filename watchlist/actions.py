import logging
import json

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert

from .model import Media, User, engine
from .utils import media_title, media_title_original, media_date

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def lookup_user(user, session):
    stmt = select(User).where(User.username == user.name)
    return session.scalars(stmt).first()

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

def lookup_media(media, session):
    stmt = select(Media).where(Media.id == media['id'])
    return session.scalars(stmt).first()

def add_media(media, session):
    title = media_title(media)
    original_title = media_title_original(media)
    release_date = media_date(media)
    saved_media = session.scalars(
        insert(Media).values(
            id=media['id'],
            title=title,
            original_title=original_title,
            release_date=release_date,
            poster_path=media['poster_path'],
            overview=media['overview'],
            type=media['media_type'],
        ).returning(Media)
    ).first()
    return saved_media

def get_db_media(media, session):
    saved_media = lookup_media(media, session)
    title = media_title(media)
    if not saved_media:
        logger.debug(f"{title} not found. Creating...")
        saved_media = add_media(media, session)
        logger.debug(f"{saved_media!r} created.")
    return saved_media

def add_to_watchlist(media, member):
    added = False
    with Session(engine) as session:
        user = get_db_user(member, session)
        logger.debug(f"User found: {user!r}")
        logger.debug(json.dumps(media, indent=4, sort_keys=True))
        saved_media = get_db_media(media, session)
        logger.debug(f"Media found: {saved_media!r}")
        added = vote_for_media(session, saved_media, user)
        logger.debug(saved_media.voters)
        session.commit()
    return added

def vote_for_media(session, media, user):
    if user not in media.voters:
        media.voters.append(user)
        return True
    return False

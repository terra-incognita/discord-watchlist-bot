import os
import logging
import discord
from discord.ext import commands
from themoviedb import TheMovieDB
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine

load_dotenv(find_dotenv())
engine = create_engine("sqlite+pysqlite:///watchlist.db", echo=True)

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
DISCORD_MESSAGE_DELETE_AFTER = int(os.environ.get("DISCORD_MESSAGE_DELETE_AFTER", 60))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

class MediaView(discord.ui.View):
    def __init__(self, media_type, media):
        super().__init__(timeout=180)
        self.media_type = media_type
        self.media = media
    @discord.ui.button(label="Add to Watchlist", style=discord.ButtonStyle.primary, emoji="➕")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        button.label = "Added!"
        title = self.media.get('title')
        await interaction.response.edit_message(content=f"{title} added to {self.media_type} watchlist!", view=self)

def format_movie_data(movie_data):
    title = movie_data.get('title')
    original_title = movie_data.get('original_title')
    name = movie_data.get('name')
    release_date = movie_data.get('release_date')
    # overview = movie_data.get('overview')
    rating = movie_data.get('vote_average')
    media_type = 'movie'
    # poster = f"https://image.tmdb.org/t/p/w1280{movie_data.get('poster_path')}"
    id = movie_data.get('id')
    url = f"https://www.themoviedb.org/{media_type}/{id}"

    return f":rocket: **Title**: {title} | {original_title} | {name}\n:cricket_game: **Rating**: {rating}\n:calendar: **Release Date**: {release_date}\n:film_frames: **Media Type**: {media_type}\n:link: **URL**: {url}\n-----\n\n\n\n\n\n"

def format_tv_data(data):
    original_name = data.get('original_name')
    name = data.get('name')
    first_air_date = data.get('first_air_date')
    # overview = data.get('overview')
    rating = data.get('vote_average')
    media_type = 'tv'
    # poster = f"https://image.tmdb.org/t/p/w1280{data.get('poster_path')}"
    id = data.get('id')
    url = f"https://www.themoviedb.org/{media_type}/{id}"

    return f":rocket: **Title**: {original_name} | {name}\n:cricket_game: **Rating**: {rating}\n:calendar: **First Air Date**: {first_air_date}\n:film_frames: **Media Type**: {media_type}\n:link: **URL**: {url}\n-----\n\n\n\n\n\n"


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')
    else:
        logger.error(f"An error occurred: {str(error)}")


@bot.command(name='hindi_movies')
async def hindi_movies(ctx):
    try:
        movie_db = TheMovieDB()
        movies = movie_db.get_this_weeks_movies('hindi')
        for movie in movies.get('results', []):
            content = format_movie_data(movie)
            msg = await ctx.send(content)
            await msg.delete(delay=DISCORD_MESSAGE_DELETE_AFTER)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


@bot.command(name='hindi_shows')
async def hindi_shows(ctx):
    try:
        movie_db = TheMovieDB()
        shows = movie_db.get_this_weeks_shows('hindi')
        for show in shows.get('results', []):
            content = format_movie_data(show)
            msg = await ctx.send(content)
            await msg.delete(delay=DISCORD_MESSAGE_DELETE_AFTER)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


@bot.command(name='trending')
async def trending(ctx):
    try:
        movie_db = TheMovieDB()
        trending = movie_db.get_trending('week')
        for trend in trending.get('results', []):
            content = format_movie_data(trend)
            msg = await ctx.send(content)
            await msg.delete(delay=DISCORD_MESSAGE_DELETE_AFTER)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


@bot.command(name='trending_today')
async def trending_today(ctx):
    try:
        movie_db = TheMovieDB()
        trending = movie_db.get_trending('day')
        for trend in trending.get('results', []):
            content = format_movie_data(trend)
            msg = await ctx.send(content)
            await msg.delete(delay=DISCORD_MESSAGE_DELETE_AFTER)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


@bot.command(name='upcoming')
async def upcoming(ctx):
    try:
        movie_db = TheMovieDB()
        upcoming = movie_db.get_upcoming('movie')
        for movie in upcoming.get('results', []):
            content = format_movie_data(movie)
            msg = await ctx.send(content)
            await msg.delete(delay=DISCORD_MESSAGE_DELETE_AFTER)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


@bot.command(name='upcoming_shows')
async def upcoming(ctx):
    try:
        movie_db = TheMovieDB()
        upcoming = movie_db.get_upcoming('tv')
        for movie in upcoming.get('results', []):
            content = format_movie_data(movie)
            msg = await ctx.send(content)
            await msg.delete(delay=DISCORD_MESSAGE_DELETE_AFTER)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


@bot.command(name='now_playing')
async def now_playing(ctx):
    try:
        movie_db = TheMovieDB()
        now_playing = movie_db.get_now_playing('movie')
        for movie in now_playing.get('results', []):
            content = format_movie_data(movie)
            msg = await ctx.send(content)
            await msg.delete(delay=DISCORD_MESSAGE_DELETE_AFTER)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


@bot.command(name='now_playing_shows')
async def now_playing(ctx):
    try:
        movie_db = TheMovieDB()
        now_playing = movie_db.get_now_playing('tv')
        for movie in now_playing.get('results', []):
            content = format_movie_data(movie)
            msg = await ctx.send(content)
            await msg.delete(delay=DISCORD_MESSAGE_DELETE_AFTER)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


@bot.command(name='find')
async def find(ctx, media_type, query, year=None):
    try:
        media_type = media_type.lower()
        if media_type not in ['tv', 'movie']:
            logger.warn(f'Unknown media type passed to find command: {media_type}')
            msg = await ctx.send(f'{media_type} is not a recognized media type.')
            return
        movie_db = TheMovieDB()
        response = movie_db.find(media_type, query, year)
        for result in response.get('results', []):
            if media_type == 'movie':
                content = format_movie_data(result)
            else:
                content = format_tv_data(result)
            msg = await ctx.send(content, view=MediaView(media_type=media_type, media=result))
            return
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

@bot.command(name='shutdown')
@commands.is_owner()  # This ensures only the owner of the bot can use this command
async def shutdown(ctx):
    await ctx.send('Shutting down...')
    await ctx.bot.close()


def main():
    bot.run(DISCORD_BOT_TOKEN)


if __name__ == '__main__':
    main()

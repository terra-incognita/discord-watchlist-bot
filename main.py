import os
import logging
import discord
from discord.ext import commands
from dotenv import find_dotenv, load_dotenv

from themoviedb import TheMovieDB
from watchlist.views import MediaView, format_media_data

load_dotenv(find_dotenv())

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
DISCORD_MESSAGE_DELETE_AFTER = int(os.environ.get("DISCORD_MESSAGE_DELETE_AFTER", 60))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')
    else:
        logger.error(f"An error occurred: {str(error)}")

@bot.command(name='trending')
async def trending(ctx):
    try:
        movie_db = TheMovieDB()
        trending = movie_db.get_trending('week')
        for trend in trending.get('results', []):
            content = format_media_data(trend)
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
            content = format_media_data(trend)
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
            content = format_media_data(movie)
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
            content = format_media_data(movie)
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
            content = format_media_data(movie)
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
            content = format_media_data(movie)
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
            content = format_media_data(result)
            msg = await ctx.send(content, view=MediaView(media=result, author=ctx.author))
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

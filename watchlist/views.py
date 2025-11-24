import discord

from .actions import add_to_watchlist

class MediaView(discord.ui.View):
    def __init__(self, media_type, media):
        super().__init__(timeout=180)
        self.media_type = media_type
        self.media = media
    @discord.ui.button(label="Add to Watchlist", style=discord.ButtonStyle.primary, emoji="➕")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        title = media_title(self.media)
        if (add_to_watchlist(self.media)):
            button.disabled = True
            button.label = "Added!"
            await interaction.response.edit_message(content=f"**{title}** added to {self.media_type} watchlist!", view=self)
        else:
            await interaction.response.edit_message(content=f"😞 Unable to add **{title}** to {self.media_type} watchlist.", view=self)

"""
Get the English title of a TV show or movie.
"""
def media_title(media_data):
    if 'title' in media_data:
        title = media_data.get('title')
        return title
    elif 'name' in media_data:
        name = media_data.get('name')
        return name
    return None

"""
Get the English and original title of a TV show or movie.
"""
def media_title_expanded(media_data):
    if 'title' in media_data:
        title = media_data.get('title')
        original_title = media_data.get('original_title')
    elif 'name' in media_data:
        title = media_data.get('name')
        original_title = media_data.get('original_name')
    if title is None:
        return None
    return title if title == original_title else f"{title} ({original_title})"

def format_movie_data(movie_data):
    title = media_title_expanded(movie_data)
    release_date = movie_data.get('release_date')
    # overview = movie_data.get('overview')
    rating = movie_data.get('vote_average')
    media_type = 'movie'
    # poster = f"https://image.tmdb.org/t/p/w1280{movie_data.get('poster_path')}"
    id = movie_data.get('id')
    url = f"https://www.themoviedb.org/{media_type}/{id}"

    return f":rocket: **Title**: {title}\n:cricket_game: **Rating**: {rating}\n:calendar: **Release Date**: {release_date}\n:film_frames: **Media Type**: {media_type}\n:link: **URL**: {url}\n-----\n\n\n\n\n\n"

def format_tv_data(data):
    title = media_title_expanded(data)
    name = data.get('name')
    first_air_date = data.get('first_air_date')
    # overview = data.get('overview')
    rating = data.get('vote_average')
    media_type = 'tv'
    # poster = f"https://image.tmdb.org/t/p/w1280{data.get('poster_path')}"
    id = data.get('id')
    url = f"https://www.themoviedb.org/{media_type}/{id}"

    return f":rocket: **Title**: {title}\n:cricket_game: **Rating**: {rating}\n:calendar: **First Air Date**: {first_air_date}\n:film_frames: **Media Type**: {media_type}\n:link: **URL**: {url}\n-----\n\n\n\n\n\n"


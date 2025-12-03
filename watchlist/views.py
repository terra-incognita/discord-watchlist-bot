import discord

from .actions import add_to_watchlist
from .utils import media_title, media_title_expanded

class MediaView(discord.ui.View):
    def __init__(self, media, author):
        super().__init__(timeout=180)
        self.media_type = media['media_type']
        self.media = media
        self.author = author
    @discord.ui.button(label="Add to Watchlist", style=discord.ButtonStyle.primary, emoji="➕")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        title = media_title(self.media)
        if (add_to_watchlist(self.media, self.author)):
            button.disabled = True
            button.label = "Added!"
            await interaction.response.edit_message(content=f"**{title}** added to {self.media_type} watchlist!", view=self)
        else:
            await interaction.response.edit_message(content=f"😞 Unable to add **{title}** to {self.media_type} watchlist.", view=self)

"""
Format a TMDB media result
"""
def format_media_data(media_data):
    if media_data['media_type'] == 'movie':
        return format_movie_data(media_data)
    else:
        return format_tv_data(media_data)

"""
Format a TMDB movie result
"""
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

"""
Format a TMDB TV program result
"""
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



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
Get the original title of a TV show or movie.
"""
def media_title_original(media_data):
    original_title = None
    if 'original_title' in media_data:
        original_title = media_data.get('original_title')
    elif 'name' in media_data:
        original_title = media_data.get('original_name')
    return original_title

"""
Get the English and original title of a TV show or movie.
"""
def media_title_expanded(media_data):
    title = media_title(media_data)
    original_title = media_title_original(media_data)
    return title if title == original_title else f"{title} ({original_title})"

"""
Get the release date of a TV show or movie.
"""
def media_date(media_data):
    release_date = None
    if 'release_date' in media_data:
        release_date = media_data.get('release_date')
    elif 'first_air_date' in media_data:
        release_date = media_data.get('first_air_date')
    return release_date


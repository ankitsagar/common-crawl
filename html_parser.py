from bs4 import BeautifulSoup


def parser(html):
    songs = []
    artists = []
    ranks = []
    weeks = []

    soup = BeautifulSoup(html, 'html.parser')

    artist_tags = soup.find_all(class_="chart-row__artist")
    if len(artist_tags) < 1:
        artist_tags = soup.find_all(class_="chart-row__artist")
    song_tags = soup.find_all(class_="chart-row__song")
    rank_tags = soup.find_all(class_="chart-row__current-week")
    week_tag = soup('time')

    for week in week_tag:
        weeks.append(week.get_text())
    for tag in artist_tags:
        tag = tag.get_text()
        tag = tag.strip()
        if len(tag) > 0:
            artists.append(tag)

    for tag in song_tags:
        tag = tag.get_text()
        if len(tag) > 0:
            songs.append(tag)

    for tag in rank_tags:
        tag = tag.get_text()
        ranks.append(tag)

    return songs, ranks, artists, weeks

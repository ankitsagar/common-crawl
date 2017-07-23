# Billboard top 100 songs of the week parser (Common crawl)

This is a simple example how to get web archive from common crawland parse the data.
In this example, [The top 100 songs of the week on Billboard](http://www.billboard.com/charts/hot-100) is parsed. 

## billboard.py

This script will search for domain in common crawl index and record all json data and download the gzip file and uncompress it. It uses year_index.py to get the list of indexes and html_parser.py for parsing data.
Data will recorded into csv files and the file names will be the week.

Struture of csv file: Rank, Song, Artist

## html_parser.py

This will parse the given html and returns week,rank, song and artist.

## year_index.py

This will index all the years from 2016 by crawling into common crwal website.
The year is from 2016 because before that html site was diffrent.

This program requires BeautifulSoup4 and request module


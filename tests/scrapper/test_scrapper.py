"""
Test Scarpping the data
"""

# Builtin imports
import os

# Local imports
from recommend_app.scrapper.scrapper import Scrapper

PWD = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(PWD, 'resources')

#-----------------------------------------------------------------------------#
# Functions
#-----------------------------------------------------------------------------#

def get_resource(filename):
    return os.path.join(RESOURCES_DIR, filename)

def get_html_content(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

#-----------------------------------------------------------------------------#
# Tests
#-----------------------------------------------------------------------------#
def test_ldjson_content():
    text = get_html_content( get_resource('netflix.html') )
    s = Scrapper(text)
    data = s.scrap()

    assert data['url'] == 'https://www.netflix.com/gb/title/81767635'
    assert data['title'] == 'Godzilla Minus One'
    assert data['description']
    assert data['thumbnail']

def test_og_content():
    text = get_html_content( get_resource('netflix_og.html') )
    s = Scrapper(text)
    data = s.scrap()

    assert data['url'] == 'https://www.netflix.com/gb/title/81767635'
    assert data['title'] == 'Watch Godzilla Minus One | Netflix'
    assert data['description']
    assert data['thumbnail'] == 'https://occ-0-5262-1168.1.nflxso.net/dnm/api/v6/E8vDc_W8CLv7-yMQu8KMEC7Rrr8/AAAABWjC7P6QGqbJE4-WNeQLIvxo2EbymKHOPzMks6hqRGEkmFTjkStmOG2JVuK9QQHL9essfGnEuOuEGlhTqvMwfq9Nosc2HNwzmyWR.jpg?r=381'

def test_meta_title_description():
    text = get_html_content( get_resource('prime.html') )
    s = Scrapper(text)
    data = s.scrap()

    assert data['title'] == 'Watch The Batman | Prime Video'
    assert data['description']

    assert 'url' not in data.keys()
    assert 'thumbnail' not in data.keys()

def test_no_data_extracted():
    text = get_html_content( get_resource('disney.html') )
    s = Scrapper(text)
    data = s.scrap()
    assert not data

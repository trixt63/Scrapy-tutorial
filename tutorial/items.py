# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
# use MapCompose to apply multiple processing functions to a field
from itemloaders.processors import MapCompose, TakeFirst
from datetime import datetime

class TutorialItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# Functions to format inputs:

# strip the unicode quotes
def remove_quotes(text):
    text = text.strip(u'\u201c'u'\u201d')
    return text

# convert string to Python date
def convert_date(text):
    text = datetime.strptime(text, '%B %d, %Y')

# parse location "in Ulm, Germany"
# this simply remove "in ", you can further parse city, state, country, etc.
def parse_location(text):
    return text[3:]

class QuoteItem(Item):
    # define one Scrapy item: 
    quote_content = Field(
        input_processor = MapCompose(remove_quotes),
        output_processor = TakeFirst()
    )
    author_name = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    author_birthday = Field(
        input_processor = MapCompose(convert_date),
        output_processor=TakeFirst()
    )
    author_bornlocation = Field(
        input_processor=MapCompose(parse_location),
        output_processor=TakeFirst()
    )
    author_bio = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    tags = Field()


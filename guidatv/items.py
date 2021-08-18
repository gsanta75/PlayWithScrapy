# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
from datetime import datetime
import json

def remove_slash(text):
    # strip the unicode slash
    text = text.strip(u'\u002f')
    return text

class GuidatvItem(Item):

    day = Field(
        input_processor=MapCompose(remove_slash),
        output_processor=TakeFirst()
        )
    channels = Field()

class ChannelItem(Item):

    ch_name = Field( output_processor=TakeFirst() )
    ch_logo = Field( output_processor=TakeFirst() )
    ch_schedule = Field()

class ProgramItem(Item):

    show_title = Field( output_processor=TakeFirst() ) 
    show_category = Field( output_processor=TakeFirst() )
    show_time = Field( output_processor=TakeFirst() )

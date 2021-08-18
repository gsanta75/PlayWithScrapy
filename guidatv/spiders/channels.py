import scrapy
from scrapy.loader import ItemLoader
from .. items import ChannelItem, ProgramItem, GuidatvItem
from scrapy.utils.log import configure_logging
import logging

class ChannelSpider(scrapy.Spider):
    
    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename='channel_crawl.log',
    #     filemode = 'a',
    #     format='%(levelname)s: %(message)s',
    #     level=logging.DEBUG
    # )

    name = "channels"
    start_urls = ['https://guidatv.quotidiano.net']
    # start_urls = ['https://guidatv.quotidiano.net/09-06-2020']
    
    def parse(self, response):
        days_url = response.css('div.day-number a')
        yield from response.follow_all(days_url, callback=self.parse_guidaForDay)
        # return self.parse_guidaForDay(response=response)

    def parse_guidaForDay(self, response):
        guidatv_il = ItemLoader(item=GuidatvItem(), response=response)
        guidatv_il.add_css('day', 'div.day.active a::attr(href)')
        
        channels = response.css('div.channels section.channel')
        chs = []
        for ch in channels:
            channel_il = ItemLoader(item=ChannelItem(), selector=ch)
            channel_il.add_css('ch_name', 'a span.channel-name::text')
            channel_il.add_css('ch_logo', 'img::attr(data-src)')
            
            programs = ch.css('div.programs a.program')
            pgrs = []
            for pr in programs:
                program_il = ItemLoader(item=ProgramItem(), selector=pr)
                program_il.add_css('show_title', 'div.program-title::text')
                program_il.add_css('show_category', 'div.program-category::text')
                program_il.add_css('show_time', 'div.program-time div.hour::text')
                programItem = program_il.load_item()
                pgrs.append(programItem)

            channel_il.add_value('ch_schedule', pgrs)
            
            channelItem = channel_il.load_item()
            chs.append(channelItem)
        
        guidatv_il.add_value('channels', chs)
        guidatvItem = guidatv_il.load_item()

        return guidatvItem
        

    # def parse(self, response):
    #     item = GuidatvItem()
    #     item['day'] = response.css('div.day.active a::attr(href)').get()
        
    #     item['channels'] = []

    #     channels = response.css('div.channels section.channel')
    #     for ch in channels:
    #         ch_item = ChannelItem()    
    #         ch_item['ch_name'] = ch.css('a span.channel-name::text').get()
    #         ch_item['ch_logo'] = ch.css('img::attr(data-src)').get()
    #         ch_item['ch_schedule'] = []
            
    #         programs = ch.css('div.programs a.program')
    #         for pr in programs:
    #             ch_program = ProgramItem()
    #             ch_program['show_title'] = pr.css('div.program-title::text').get()
    #             ch_program['show_category'] = pr.css('div.program-category::text').get()
    #             ch_program['show_time'] = pr.css('div.program-time div.hour::text').get()
                
    #             ch_item['ch_schedule'].append(ch_program)

    #         item['channels'].append(ch_item)
            
    #     yield item

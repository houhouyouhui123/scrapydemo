# -*- coding: utf-8 -*-
import scrapy
from scrapyDemo.items import BookItem
class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    def start_requests(self):
        urls = [
            'https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A1000%2Cn%3A3377866011&qid=1556977765&ref=sr_pg_1',
        ]
        for url in urls:
            yield scrapy.Request(url,headers=self.headers,callback=self.parseResult)

    def parseResult(self,response):
        books=response.xpath('//*[@id="mainResults"]/ul/li/div/div[2]/div/div[2]')
        item =BookItem()
        for book in books:
            name=book.css('div:nth-child(1) div:nth-child(1) a h2::text').get()
            author=book.css('div:nth-child(1) div:nth-child(2) span:nth-child(2) a::text').get()
            if author is None:
                author=''
                spanList=book.css('div:nth-child(1) div:nth-child(2) span.a-size-small::text').getall()
                spanList.remove('by ')
                for span in spanList:
                    author+=span
            date=book.css('div:nth-child(1) div:nth-child(1) .a-size-small::text').get()
            star=book.css('div:nth-child(3) div:nth-child(2) div span span a i span::text').get()
            reviewCount=book.css('div:nth-child(3) div:nth-child(2) div a::text').get()
            price=book.css('div:nth-child(3) div:nth-child(1) div:nth-child(2) a span:nth-child(1)::text').get()
            item['name'] = name
            item['author'] = author
            item['date'] = date
            if star != None:
                item['star'] = float(star[:-15])
                item['reviewCount'] = int(reviewCount.replace(',', ''))
            if price is not None:
                item['price'] = float(price[1:])
            yield item
        nextPage=response.css('#pagnNextLink::attr(href)').get()
        yield response.follow(nextPage,callback=self.parse,headers=self.headers)


    def parse(self, response):
        books=response.xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div')
        item=BookItem()
        for book in books:
            name=book.css('.sg-col-inner div.sg-row:nth-child(1) .sg-col-inner div:nth-child(1) h2 span::text').get()
            author=book.css('.sg-col-inner div.sg-row:nth-child(1) .sg-col-inner div:nth-child(1) div a::text').get()
            if author==None:
                author=book.css('.sg-col-inner div.sg-row:nth-child(1) .sg-col-inner div:nth-child(1) div span:nth-child(2)::text').get()
            author=str.strip(str(author))
            date = book.css('.sg-col-inner div.sg-row:nth-child(1) .sg-col-inner div:nth-child(1) div .a-size-base.a-color-secondary.a-text-normal::text').get()
            star= book.css('.sg-col-inner div.sg-row:nth-child(1) .sg-col-inner div:nth-child(2) div span:nth-child(1) span a i:nth-child(1) span::text').get()
            reviewCount=book.css('.sg-col-inner div.sg-row:nth-child(1) .sg-col-inner div:nth-child(2) div span:nth-child(2) a span::text').get()
            price = book.css('.sg-col-inner div.sg-row:nth-child(2) .sg-col-inner div:nth-child(1) div:nth-child(2) a span:nth-child(1) span::text').get()
            item['name']=name
            item['author']=author
            item['date']=date
            if star!=None:
                item['star']=float(star[:-15])
                item['reviewCount']=int(reviewCount.replace(',',''))
            if price is not None:
                item['price']=float(price[1:])
            yield item
        ul=response.xpath('//*[@id="search"]/div[1]/div[2]/div/span[7]/div/div/div/ul')
        nextPage=ul.css('li.a-last a::attr(href)').get()
        if nextPage is not None:
            yield response.follow(nextPage,callback=self.parse,headers=self.headers)

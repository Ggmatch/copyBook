# -*- coding: utf-8 -*-
import os

from bookspider.items import BiQuGeItem
import scrapy
import urllib


class BiQuGeSpider(scrapy.Spider):
    name = 'biquge'
    allowed_domains = ['biquge7']
    start_urls = ['https://www.biquge7.top/34936']

    def parse(self, response):
        # 爬取图书元信息：书名、作者、封面图片、简介
        bookName = response.xpath(
            "//div[@class='tits']/h1/text()").extract()[0]
        author = response.xpath(
            "//span[@class='author']/text()").extract()[0].strip("作者：")
        intro = response.xpath(
            "//p[@class='des']/text()").extract()[0].strip("\"")

        imgUrl = response.xpath("//div[@class='tit']/img/@src").extract()[0]
        filename = bookName + '.jpg'
        dirpath = './cover'
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        filepath = os.path.join(dirpath, filename)
        urllib.request.urlretrieve(imgUrl, filepath)

        cover = 'cover/' + filename
        # 爬取每个章节
        chapters = response.xpath("//div[@class='list']/li/a")
        number = 0

        for chapter in chapters:
            number += 1
            chapterName = chapter.xpath("./text()").extract()[0]
            chapterUrl = chapter.xpath("./@href").extract()[0]
            yield scrapy.Request(chapterUrl, meta={
                'bookName': bookName,
                'author': author,
                'intro': intro,
                'cover': cover,
                'number': number,
                'chapterName': chapterName,
                'chapterUrl': chapterUrl
            }, callback=self.getContent)
        pass

    def getContent(self, response):
        bookName = response.meta["bookName"]
        author = response.meta["author"]
        intro = response.meta["intro"]
        cover = response.meta["cover"]
        number = response.meta["number"]
        chapterName = response.meta["chapterName"]
        chapterUrl = response.meta["chapterUrl"]

        chapterContent = "".join(response.xpath(
            "//div[@class='list list_text']/div[@class='text']/text()").extract())
        # 替换一些字符
        chapterContent = chapterContent.replace(r'''
        ''', "<br>")
        chapterContent = chapterContent.replace(r" ", "&nbsp")

        item = BiQuGeItem()
        item["bookName"] = bookName
        item["author"] = author
        item["intro"] = intro
        item["cover"] = cover
        item["number"] = number
        item["chapterName"] = chapterName
        item["chapterUrl"] = chapterUrl
        item["chapterContent"] = chapterContent

        return item

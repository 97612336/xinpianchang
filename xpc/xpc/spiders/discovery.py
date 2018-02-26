# -*- coding: utf-8 -*-
import scrapy


class DiscoverySpider(scrapy.Spider):
    name = 'discovery'
    allowed_domains = ['www.xinpianchang.com']
    start_urls = ['http://www.xinpianchang.com/channel/index/'
                  'id-0/sort-like/type-0?from=articleListPage']

    def parse(self, response):
        vedio_url='http://www.xinpianchang.com/a%s?from=ArticleList'
        post_list=response.xpath('//ul[@class="video-list"]/li')
        for one_post in post_list:
            post_id=one_post.xpath('./@data-articleid').extract_first()
            post_title=one_post.xpath('./div/a/p/text()').extract_first()
            #获取视频的进入地址的网页url
            post_vedio_url=vedio_url%post_id
            print(post_vedio_url,'这是视频的进入链接')

        #获取下一页的url
        next_page_url=response.xpath('//a[@title="下一页"]/@href').extract_first()
        if next_page_url:
            yield scrapy.Request(next_page_url,callback=self.parse)
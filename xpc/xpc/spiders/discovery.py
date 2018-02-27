# -*- coding: utf-8 -*-
import json

import scrapy

from xpc.items import PostItem, CommentItem

comment_api='https://www.xinpianchang.com/article/filmplay/ts-getCommentApi?pagesize=6&page=%s&id=%s'

class DiscoverySpider(scrapy.Spider):
    name = 'discovery'
    allowed_domains = ['www.xinpianchang.com']
    start_urls = ['http://www.xinpianchang.com/channel/index/'
                  'id-0/sort-like/type-0?from=articleListPage']

    def parse(self, response):
        vedio_url='http://www.xinpianchang.com/a%s?from=ArticleList'
        post_list=response.xpath('//ul[@class="video-list"]/li')
        for one_post in post_list:
            #获得视频的id
            post_id=one_post.xpath('./@data-articleid').extract_first()
            #获取视频的标题
            post_title=one_post.xpath('./div/a/p/text()').extract_first()
            #获取视频的小缩略图
            little_img=one_post.xpath('//a[@class="video-cover"]/img/@_src').get()
            #获取视频的进入地址的网页url
            post_vedio_url=vedio_url%post_id
            request=scrapy.Request(post_vedio_url,callback=self.parse_detail)
            request.meta['title']=post_title
            request.meta['post_id']=post_id
            request.meta['thumbnail']=little_img
            yield request
        #获取下一页的url
        next_page_url=response.xpath('//a[@title="下一页"]/@href').extract_first()
        if next_page_url:
            yield response.follow(next_page_url,callback=self.parse)

    def parse_detail(self,response):
        postitem=PostItem()
        #视频的id
        postitem['pid']=response.meta['post_id']
        #视频的标题
        postitem['title']=response.meta['title']
        #视频的小缩略图
        postitem['thumbnail']=response.meta['thumbnail']
        #视频的大图
        postitem['preview']=response.xpath('//div[@class="filmplay"]//img/@src').extract_first()
        #视频的地址
        video_url=response.xpath('//a[@id="player"]/@href').get()
        video_url=video_url[2:]
        postitem['video']=video_url
        #这个是视频的格式
        video_format=str(video_url).split('.')[-1]
        postitem['video_format']=video_format
        #这个是视频的分类
        category=response.xpath('//div[contains(@class,"filmplay-intro")]/span/text()').get()
        postitem['category']=category
        #这个是视频创建时间
        created_at=response.xpath('//span[contains(@class,"update-time")]/i/text()').get()
        postitem['created_at']=created_at
        #这个是视频的播放次数
        play_counts=response.xpath('//i[contains(@class,"play-counts")]/text()').get()
        postitem['play_counts']=play_counts
        #视频的喜爱次数
        like_counts=response.xpath('//span[contains(@class,"like-counts")]/text()').get()
        postitem['like_counts']=like_counts
        #视频的描述
        description=response.xpath('//p[contains(@class,"desc")]/text()').get()
        postitem['description']=description
        yield postitem

        #把这篇文章的评论解析出来,跳转到评论方法上
        request=scrapy.Request(comment_api%(1,postitem['pid']),callback=self.parse_comment)
        request.meta['pid']=postitem['pid']
        request.meta['page']=1
        yield request

    def parse_comment(self,response):
        #得到api返回的数据
        json_data=response.text
        #获取pid
        pid=response.meta['pid']
        #获取page的值
        page=response.meta['page']
        data=json.loads(json_data)
        total_page=data['data']['total_page']
        print('*-*_'*50)
        data_list=data['data']['list']
        #遍历接口数据,然后填充到item
        for one_data in data_list:
            #实例化item类
            item=CommentItem()
            item['commentid']=one_data['commentid']
            item['pid']=one_data['articleid']
            item['cid']=one_data['userInfo']['userid']
            item['created_at']=one_data['addtime']
            item['content']=one_data['content']
            item['like_counts']=one_data['count_approve']
            #提交item
            yield item
        #执行循环遍历接口,得到数据
        while page<=total_page:
            page=page+1
            # 把新的url传给解析方法,并解析
            request = scrapy.Request(comment_api % (page, pid), callback=self.parse_comment)
            request.meta['page'] = page
            request.meta['pid'] = pid



# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

#视频信息的item
class PostItem(scrapy.Item):
    #表名
    table_name='posts'
    # define the fields for your item here like:
    # name = scrapy.Field()
    #这个是视频的id
    pid = Field()
    #这个是视频的标题
    title = Field()
    #这个是视频的小图
    thumbnail = Field()
    #这个是视频的大图
    preview = Field()
    #这个是视频的地址
    video = Field()
    #这个是视频的格式
    video_format = Field()
    #这个是视频的分类
    category = Field()
    #这个是视频的创建时间
    created_at = Field()
    #这个是视频的播放次数
    play_counts = Field()
    #这个是视频的喜欢次数
    like_counts = Field()
    #这个是视频的描述
    description = Field()

#这个是评论的item
class CommentItem(scrapy.Item):
    table_name='comments'
    #评论的id
    commentid = Field()
    #回复的文章的id
    pid = Field()
    #用户的id
    cid = Field()
    #评论的时间
    created_at = Field()
    #评论的内容
    content = Field()
    #点赞数
    like_counts = Field()

#作者的详细信息类
class ComposerItem(scrapy.Item):
    table_name='composers'
    #作者的id
    cid=Field()
    #作者详情页的banner图
    banner=Field()
    #作者的头像
    avatar=Field()
    #是否是认证的
    verified=Field()
    #作者的名字
    name=Field()
    #作者的介绍
    intro=Field()
    #作者的人气
    like_counts=Field()
    #作者的粉丝数
    fans_counts=Field()
    #作者的关注数
    follow_counts=Field()

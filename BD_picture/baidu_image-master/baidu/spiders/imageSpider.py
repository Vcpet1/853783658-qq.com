import scrapy
import sys
from baidu.items import *
from scrapy_splash import SplashRequest
class ImageSpider(scrapy.Spider):
    name='imageSpider'                        #爬虫名字
    start_urls=[]                      #开始爬取的地址，它包含了Spider在启动时爬取的URL列表，初始请求时由它来定义的（）
    def start_requests(self):
        words =input("请输入搜索词：")
        search_words= words.split()    #转化为列表
        for search_word in search_words:
            print(search_word)
            url='https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='+search_word
            request=scrapy.Request(url,callback=self.parse,meta={'search_word':search_word})#meta传递额外参数
            yield request

    # 该方法负责解析返回的响应、提取数据或者进一步生成要处理的请求
    def parse(self,response):
        #获取图片，以列表形式保存
        arrs = response.xpath('//div[@id="imgid"]/ul[@class="imglist"]/li/a/img/@src').extract()  #返回一个List
        details = response.xpath('//div[@id="imgid"]/ul[@class="imglist"]/li/a/@href').extract()
        search_word = response.meta['search_word']
        for key , one in enumerate(arrs):
            image_item = ImageItem()
            image_item["name"]=search_word.replace('外观', '')#过滤掉搜索词中不要的问题
            image_item["search_word"]=search_word
            image_item["image_url"]=one
            image_item["referer"]=response.url
            detail_url=response.urljoin(details[key])
            image_item["detail_url"]=detail_url
            if True:
                #抓取原图时，百度是先加载页面～～然后再延时执行js获取大图，所以要设置获取页面后要检查是否已经获取到原图url
                request=scrapy.Request(detail_url,callback=self.parseDetail,meta={'item':image_item,'is_detail':1})
                yield request
            else:
                yield image_item
        next_page=response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next_page is not None:
            url=response.urljoin(next_page)
            request=scrapy.Request(url,callback=self.parse,meta={'search_word':search_word})#meta传递额外参数
            yield request

    def parseDetail(self,response):
        image_item=response.meta['item']
        detail_image_url=response.xpath('//img[@id="currentImg"]/@src').extract_first() 
        image_item["image_url"]=detail_image_url
        return image_item



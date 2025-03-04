# -*- coding: utf-8 -*-

# Scrapy settings for baidu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPLASH_URL = 'http://127.0.0.1:8050/'
BOT_NAME = 'baidu'

SPIDER_MODULES = ['baidu.spiders']   #Scrapy搜索spider的模块列表
NEWSPIDER_MODULE = 'baidu.spiders'   #使用 genspider 命令创建新spider的模块。默认: 'xxx.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0C; .NET4.0E)'

# Obey robots.txt rules  机器人协议要关闭掉
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 3              #并发请求(concurrent requests)的最大值,默认: 16

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1               #为同一网站的请求配置延迟
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)   禁用cookies（默认是打开的）
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'baidu.middlewares.BaiduSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'baidu.middlewares.BaiduDownloaderMiddleware': 543,
    'baidu.middlewares.ChromeSpiderMiddleware': 544,
   # 'scrapy_splash.SplashCookiesMiddleware': 723,
   # 'scrapy_splash.SplashMiddleware': 725,
   # 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
   #'scrapy.pipelines.images.ImagesPipeline':5,
   #'baidu.pipelines.DownloadImagePipeline': 999,
}
#设置去重
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'baidu.pipelines.BaiduPipeline': 300,
   'baidu.pipelines.DownloadImagePipeline': 301,
   #'baidu.pipelines.MyDownloadImagePipeline': 302,
   'baidu.pipelines.MongoDBPipeline': 303,
    
}
#以防对目标网站造成一定影响或防范被其网站封杀，以下可对爬虫程序作限速处理
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html

#启动autoThrottle扩展
#AUTOTHROTTLE_ENABLED = True

#初始下载延迟（单位：秒）
#AUTOTHROTTLE_START_DELAY = 5

# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


#设置存放图片的路径
IMAGES_STORE = '/data/baidu'
#图片失效期限
IMAGES_EXPIRES = 30  #30天内抓取的都不会被重抓

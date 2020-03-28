使用Scarapy框架设计爬虫程序

在settings.py配置中通过添加Referer、修改USER_AGENT和禁用robots协议等手段绕过网站反爬虫策略

选用Selenium+chromedriver抓取数据

通过框架的ImagesPipeline专用图片下载管道处理和储存数据

将图片简单分类写入本地指定路径的同时，把图片url等信息保存至MongoDB数据库。





1）修改USER_AGENT，伪装成浏览器，防止被服务器识别。这里在settings.py中设置：

```python
  USER_AGENT = 'Mozilla/4.0  (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0C;  .NET4.0E)'  
```

 

2）禁用robots协议和cookies，因为百度图片不需要登录账号便可直接下载原图，因此可以直接将cookies禁用，以防被网站识别到爬虫的运行轨迹，可在settings.py中设置：

```python
  ROBOTSTXT_OBEY = False  #COOKIES_ENABLED = False   #注释掉即表示禁用  
```

 

3）使用google提供的chromedriver做js动态渲染。百度图片是ajax动态获取数据的，而对于爬取动态网页，这里选用稳定性高、渲染效果和速度相对比较好的chromedriver。Scrapy通过selenium使用Chromedriver进行headless操作，抓取动态生成html的页面。主要代码在middlewares.py中实现：

  

```python
class ChromeSpiderMiddleware(object):
	def __init__(self):        
		option = Options()        
        option.add_argument('--headless')            
        print("初始化浏览器")        
        self.browser = webdriver.Chrome(executable_path=”C:\\ProgramFiles(x86)
                                        \\Google\\Chrome\\Application\\chromedriver”,
                                        hrome_options=option)  
    def process_request(self, request, spider):        
        if request.meta.get("is_image"):         
            print("存在is_image")#如果是图片就不进行渲染了        
            return None        
        else:        
            self.browser.get(request.url)          
            print("页面开始渲染")        
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')         
            if request.meta.get("is_detail"):         
                image_item=request.meta.get("item")          
                image_url=image_item["image_url"]            
                wait =WebDriverWait(self.browser,20)   
               browser=self.browserwait.until(lambdabrowser:browser.find_element_by_xpath
                                              ('//img[@id="currentImg"]').
                                              get_attribute("src")!=image_url)        
            rendered_body = self.browser.page_source        
            print("页面完成渲染")        
            return HtmlResponse(request.url, body=rendered_body,  encoding="utf-8")           def spider_closed(self, spider, reason):        
            print("关闭浏览器")        
            self.browser.quit()     
```

 

4）在爬取图片时加入Referer，以防止图片防盗链技术致使我们抓取不了图片。在Scrapy中，如果某个页面URL是通过之前爬取的页面提取到的，Scrapy会自动把之前爬取的页面url作为Referer，当然也可以通过自定义的方式定义Referer字段。主要代码在pipeline.py中实现，这里只展示部分：

```python
  req = urllib.request.Request(image_url)     req.add_header('Referer', referer)  
```



items定义字段，以下代码在items.py中：

  

```
class **ImageItem**(scrapy.**Item**):      
    # define the fields for your item here like:      
    name = scrapy.Field()      
    search_word = scrapy.Field()      
    image_url=scrapy.Field()      
    image_urls = scrapy.Field()      
    images = scrapy.Field()      
    referer=scrapy.Field()      
    img_path=scrapy.Field()      
    detail_url=scrapy.Field()      
    pass  
```

这里定义了几个爬取所需要的字段，分别为关键词、图片地址、图片地址群、Referer、图片路径、图片详细类别地址等。

 

 

  编写Spider，自定义爬虫规则，爬取自己所要的网页图片内容。这里我将其命名为imageSpider.py：

```python
class ImageSpider(scrapy.Spider):      
    name='imageSpider'       
    start_urls=[]       
    def start_requests(self):        
        words =input("请输入搜索词：")        
        search_words= words.split()         
        for search_word in search_words:        
            print(search_word)  
            url='https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='
                 +search_word  
            request=scrapy.Request(url,callback=self.parse,meta=		
                                   {'search_word':search_word})        
            yield request         
    def parse(self,response):        
        arrs =response.xpath('//div[@id="imgid"]/ul[@class="imglist"]  
                             /li/a/img/@src').extract()         
        details = response.xpath('//div[@id="imgid"]/ul[@class=  
                                 "imglist"]/li/a/@href').extract()        
        search_word = response.meta['search_word']        
        for key , one in enumerate(arrs):        
            image_item = ImageItem()        
            image_item["name"]=search_word.replace('外观', '')        
            image_item["search_word"]=search_word        
            image_item["image_url"]=one        
            image_item["referer"]=response.url          
            detail_url=response.urljoin(details[key])        
            image_item["detail_url"]=detail_url          
            if True:  
                request=scrapy.Request(detail_url,callback=self.parseDetail,meta={'item':                                        image_item,'is_detail':1})            
                yield request          
            else:          
                yield image_item        
       next_page=response.xpath('//a[text()="下一页"]/@href').extract_first()        
       if next_page is not None:
            url=response.urljoin(next_page)        
            request=scrapy.Request(url,callback=self.parse,meta
                                   {'search_word':search_word})        
            yield request         
    def parseDetail(self,response):      
            image_item=response.meta['item']        
            detail_image_url=response.xpath
                                 ('//img[@id="currentImg"]/@src').extract_first()         
            image_item["image_url"]=detail_image_url  
```

在Spider中重写了start_requests的方法获取初始URL，使用了requests解析获取，并将获取到的URL传递给parse；parse方法解析返回的响应、提取数据或者进一步生成要处理的请求，在这里特别要注意的是，百度图片的网站是先加载页面，然后再延时执行js获取图片的，所以要在获取到页面后检验是否已经获得原图url，并判断是否含有下一页信息；最后将筛选后的数据传递给parseDetail，该方法负责解析出图片的url并赋值给image_url字段。另外，因为Scrapy框架自带去重原理，所以在Parse中不需要编写去重逻辑。

 

 

在Settings中设置所需参数，以下核心代码在Settings.py中实现：

为防止被网站反爬虫策略识别或对其服务器造成压力，还需要设定以下几个参数设置，在其中设置

```python
#限制爬取网页的速度（以秒为单位）  
DOWNLOAD_DELAY = 1   
#并发，请求的最大数量（默认16）  
CONCURRENT_REQUESTS = 3    
```

设置和激活下载中间件：

```
  DOWNLOADER_MIDDLEWARES = {'baidu.middlewares.BaiduDownloaderMiddleware': 543,      
                            'baidu.middlewares.ChromeSpiderMiddleware': 544,  }  
```

 设置和激活管道文件：

```
ITEM_PIPELINES = {'baidu.pipelines.BaiduPipeline': 300,                    
                  'baidu.pipelines.DownloadImagePipeline': 301,     
                  'baidu.pipelines.MongoDBPipeline': 303,}  
```

 

设置图片数据的本地存放路径以及有效期：

```python
  #设置存放图片的路径  
  IMAGES_STORE = '/data/baidu'  
  #图片失效期限  
  IMAGES_EXPIRES = 30 #xx天内抓取的都不会被重抓  
```

 

 

   对选取好的数据进行处理和存储，这些皆在pipelines.py中实现，而这里先对图片数据进行下载并实现一些简单的预处理，导入Scrapy框架中专用于处理图片的专用管道文件ImagesPipeline，重载get_media_requests和item_completed这两个函数：

```python
 from scrapy.pipelines.images import ImagesPipeline  
 from scrapy.utils.project import get_project_settings 

 settings = get_project_settings()  
    
 class DownloadImagePipeline(ImagesPipeline):      
    def get_media_requests(self,item,info):        
        image_url=item["image_url"]        
        yield scrapy.Request(url=image_url,meta={'is_image': True})     
```

定义DownloadImagePipeline这个类，它继承了ImagesPipeline。在该类中需要重新定义两个函数，其中一个为get_media_requests根据传入的url发起请求，且不需要指定回调函数，因为图像处理管道会自动调用item_completed函数处理图片.

另一个函数item_completed，它用于处理图片路径，代码如下：

```python
def item_completed(self, results, item, info):        
    #将下载的图片路径（传入到results中）存储到 imaae_paths 项目中，如果其中没有图片，我们将丢弃项目:  
    image_paths = [x['path'] for ok, x in results if ok]        
    if not image_paths:        
        #raise DropItem("Item contains no images")        
        return item        
    IMAGES_STORE=settings.get('IMAGES_STORE')        
    if image_paths[0]:          
        target_path="/data/baidu"        
        #图片存储路径        
        name_dir=target_path+"/"+item["name"]        
        #判断目录是否已存在        
        if not os.path.exists(name_dir):          
            #根据当前页面创建对应目录           
            os.makedirs(name_dir)        
            origin_file=IMAGES_STORE+"/"+image_paths[0]        
            filename = os.path.basename(origin_file)        
            ext=filename.split(".")[1]        
            ext=ext.lower()        
            if ext!="jpg" and ext!="png" and ext!="jpeg":            
                item["img_path"]=""            
                return item        
            target_file=name_dir+"/"+filenameshutil.copyfile(origin_file,target_file)     
            item['img_path'] = target_file        
            return item  
```

导入os模块使图片能下载到自定义的文件夹中，文件夹名称以每次搜索关键字命名，并筛选掉除jpg、png、jpeg以外的图片格式。另外，在这里还用到了Python的shutil文件操作工具，使用copyfile的方法直接将过滤后的文件内容复制到另一个文件中。

 

最后，下载图片至设定好的路径，根据个人需求自定义Item Pipeline，使用其指定的方法之一process_item(self,item,spider)实现，以下是主要代码（pipelines.py）：

```python
 class MyDownloadImagePipeline(object):      
        def process_item(self, item, spider):        
            img_path="/data/baidu"        
            image_url=item["image_url"]        
            referer=item["referer"]        
            referer=referer.encode("utf8")        
            filename = os.path.basename(image_url)        
            ext=filename.split(".")[1]        
            if ext!="jpg" :        
                item["img_path"]=""        
                return item       
            #以图片哈希值命名        
            new_name=""        
            h1 = hashlib.md5(image_url.encode("utf8"))        
            new_name=h1.hexdigest() #返回十六进制数据字符串        
            new_name+="."+ext        
            name_dir=img_path+"/"+item["name"]        
            if not os.path.exists(name_dir):        
                os.mkdir(name_dir)        
                file_full_name = name_dir+"/"+new_name #拼接图片名        
                if os.path.exists(file_full_name):        
                    print("图片已经存在,不进行下载:"+file_full_name)        
                    item["img_path"]=file_full_name          
                    return item        
                else:        
                    try:          
                        req = urllib.request.Request(image_url)             req.add_header('Referer', referer)          
                        f = urllib.request.urlopen(req,  timeout=3)          
                        pic = f.read()            
                        fp = open(file_full_name ,'wb')          
                        fp.write(pic) #写入图片            
                        item["img_path"]=file_full_name        
                        except Exception as e:          
                            print(e)          
                            item["img_path"]=""        
                        return item     
```

根据个人需求，首先对数据进行筛选，只下载.jpg格式的图片；重命名图片，以图片自身哈希值命名，使用os.path.exists() 方法直接判断图片是否存在，若图片以存在则返回给item，若不存在则写入图片。（scrapy内置的ImagesPipeline下载图片之后，默认使用图片下载链接的哈希值来命名图片，使得图片具有唯一性。其基本原理为从图片开头、中间、末尾各取100个字节，将这300个字节结合在一块，通过MD5（哈希算法）得到一个哈希字符串，而这字符串便可当作是每一张图片的唯一标识符。）





将数据储存至MongoDB：

```python
class MongoDBPipeline(ImageItem):
    def process_item(self, item, spider):
        conn = MongoClient('127.0.0.1', 27017)
        db = conn.baidu
        image = db.image
        name=item['name']
        search_word=item['search_word']
        img_path=item["img_path"]
        image_url=item["image_url"]
        if img_path !="":
            isFind=image.find_one({"image_url":image_url})
            if isFind is None:
                  image.insert_one({"name":name,"image_url":image_url,
                                   "search_word":search_word,"img_path":
                 				   img_path})
                print("插入数据："+image_url)
            else:
                print("已经存在，不进行数据插入:"+image_url)
            return item
        else:
            print("img_path为空"+image_url)

```


import scrapy
from json import loads

class CarSpider(scrapy.Spider):
    name = "car"
    allowed_domains = ["www.renrenche.com"]
    # 设置要发送的请求url地址
    start_urls = "https://www.renrenche.com/lurker/search/pc_select"
    # 设置要发送的请求参数
    args = {'city':'北京'}
    # 设置页码
    page = 1
    def start_requests(self):
        # for page in range(0,2):
        #     self.args['start'] = str( page * 40 )
            # 构造请求对象，并请求对推送到调度器
        yield scrapy.FormRequest(url= self.start_urls,method='POST',formdata=self.args,callback=self.parse)
    def parse(self, response):
        # response.text 为响应内容
        resp_json = loads(response.text)
        # 获取数据
        item_list = resp_json.get('data').get('response').get('docs')
        # 遍历数据集
        for item in item_list:
            # 创建一个字典，用于存储数据
            data = {}
            # 提取数据-品牌
            data['brand'] = item.get('title').split('-')[0]
            # 提取数据-标签
            # 判断是否有标签
            if item.get('tags'):
                tmp_tag = []
                # 遍历标签
                for tag in item.get('tags'):
                    tmp_tag.append(tag.get('txt'))
                # 将标签列表转换为字符串
                data['tags'] = '_'.join(tmp_tag)
            else:
                data['tags']= None
            # 提取数据-价格 
            data['price'] = item.get('price')
            # print(data)
            # 将数据推动到管道
            yield data
        # 判断是否有下一页数据
        if self.page > 2:
            return
        # 发送请求获取下一页数据
        # 设置要获取第几页的数据
        self.args['start'] = str( self.page * 40 )
        # 创建请求对象，并放到调度器
        yield scrapy.FormRequest(url= self.start_urls,method='POST',formdata=self.args,callback=self.parse)
        # 设置下次要请求的页码数
        self.page += 1
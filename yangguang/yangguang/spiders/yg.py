import scrapy
from ..items import YangguangItem
import urllib
import re


class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['sun0769.com']
    start_urls = ['https://wz.sun0769.com/political/index/politicsNewest']

    # start_urls = ['https://wz.sun0769.com/political/index/politicsNewest?id=1&page=2']

    def parse(self, response):
        # 分组
        li_list = response.xpath("//ul[@class='title-state-ul']/li")
        # print('-' * 30, response.status_code, '-' * 30)
        print('-' * 30, response.url, '-' * 30)
        page = response.url.split("page=")
        for li in li_list:
            item = YangguangItem()
            item["page"] = page[-1] if len(page) > 1 else "1"
            item["num"] = li.xpath(".//span[@class='state1']/text()").extract_first()
            item["status"] = li.xpath(".//span[@class='state2']/text()").extract_first()
            item["title"] = li.xpath(".//span[@class='state3']//a/text()").extract_first()
            item["href"] = li.xpath(".//span[@class='state3']//a/@href").extract_first()
            item["href"] = urllib.parse.urljoin(response.url, item["href"])
            item["time"] = li.xpath(".//span[@class='state4']/text()").extract_first()
            item["publish_date"] = li.xpath(".//span[@class='state5 ']/text()").extract_first()
            # print("------li--------")
            # yield item
            yield scrapy.Request(
                item["href"],
                callback=self.parse_detail,
                meta={"item": item}
            )
        # next_url
        next_url = response.xpath("//a[@class='arrow-page prov_rota']/@href").extract_first()
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url, next_url)
            # print("------next_url--------")
            # print(next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def parse_detail(self, response):  # 处理详情页
        item = response.meta["item"]
        print('-' * 30, "Starting detail", '-' * 30)
        # print(response.text)
        # 定位
        # html的真实内容在爬取的response.text中（不在element或浏览器的response的响应中）2023-3-12 19:44
        # mr_three = response.xpath("//div[@class='width-12 mr-three']/div[@class='mr-three']")
        # item["content"] = mr_three.xpath(".//pre//text()").extract()
        # item["content_img"] = mr_three.xpath(".//div[@class='clear details-img-list Picture-img']/img//@src").extract()
        # author = mr_three.xpath(".//span[@class='fl details-head']/text()").extract()
        # come_from = mr_three.xpath(".//span[@class='fl']/text()").extract()
        # author_img = mr_three.xpath(".//span[@class='fl details-head']/img/@src").extract_first()
        # item["content_video"] = mr_three.xpath(".//video/@src").extract()
        item["content"] = response.xpath(".//div[@class='content']/p/text()").extract()
        item["content_img"] = response.xpath(".//div[@class='thumb flex']/img//@src").extract()
        item["content_author"] = response.xpath(".//div[@class='author flex']//p/text()").extract_first()
        item["content_from"] = response.xpath(".//div[@class='author flex']//span/text()").extract_first()
        item["author_img"] = response.xpath(".//div[@class='author flex']//img/@src").extract_first()
        item["score_list"] = response.xpath(".//div[@class='score-list']//div[@class='fl score-fen']/text()").extract_first()
        # item["content_video"] = response.xpath(".//video/@src").extract()
        item["content_video"] = "".join(re.findall('"mp4": "(.*?)",', response.body.decode()))
        # print(item)
        # print('-' * 30, "End detail", '-' * 30)
        yield item

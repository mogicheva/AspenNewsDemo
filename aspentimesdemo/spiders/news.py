import scrapy
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


from aspentimesdemo.items import AspenNews
class NewsLocalSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['www.aspentimes.com']
    start_urls = ['https://www.aspentimes.com/recent-stories/local/',
                  'https://www.aspentimes.com/recent-stories/crime/',
                  'https://www.aspentimes.com/recent-stories/regional/'
                 ]

    def start_requests(self):
        website = ['https://www.aspentimes.com/recent-stories/local/', 'https://www.aspentimes.com/recent-stories/crime/', 'https://www.aspentimes.com/recent-stories/regional/']
        index = 0
        while index <= 2:
            url = website[index]
            options = ChromeOptions()
            options.headless = True
            path = 'C:/Users/webdrivers/chromedriver.exe'
            driver = Chrome(executable_path=path, options=options)
            driver.get(url)
            driver.maximize_window()

            container = driver.find_element(by=By.XPATH, value='//article[contains(@class, "flex-fill")]')
            main = container.find_elements(by=By.XPATH, value=".//div[contains(@class, 'col text')]")

            for m in main:
                link = m.find_element(by=By.TAG_NAME, value='a')
                url = link.get_attribute('href')
                yield scrapy.Request(url)
            index += 1
            driver.quit()

    def parse(self, response):
        item = AspenNews()
        date = response.css('time::attr(datetime)').get()
        item['date'] = str(date[0:10])
        item['title'] = response.xpath('//article/h1/text()').get()
        item['article'] = response.xpath("//div[contains(@class, 'p402_premium')]/p[contains(@class, 'oc-body')]/text()").getall()
        item['author'] = response.xpath("//h6/a/text()").get()
        item['url'] = response.request.url

        yield {
            'Title': item['title'],
            'Article': item['article'],
            'Author': item['author'],
            'URL': item['url'],
            'Date': item['date']
        }


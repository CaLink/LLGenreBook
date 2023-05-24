import scrapy
import json
import lib
import re
from LiveLibGenre.items import BookCard

import datetime

class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['www.livelib.ru']
    start_urls = ['http://www.livelib.ru/']
    handle_httpstatus_list  = [404,502,503]

    custom_settings = {"LOG_FILE":f"db/log/{name}.log",'DOWNLOAD_DELAY':0,'ROBOTSTXT_OBEY':False}

    cookie = {}
    header = {}

    curPage = 0

    def __init__(self, urlList, ):
        super(BookSpider, self).__init__()
        self.urlList = list(set(urlList))
        #self.listLen = len(self.urlList)-1
        self.cookie = lib.initCookieHeader("OptionsCookie.txt")
        self.header = lib.initCookieHeader("OptionsHeader.txt")
        #print(self.cookie)
        #print(self.header)

        


    def start_requests(self):
        
        for curUrl in self.urlList:
            yield scrapy.Request(
                url=curUrl[0],
                cookies=self.cookie,
                headers=self.header,
                callback=self.parse,
                cb_kwargs={'mainGenre':curUrl[1]}
            )


    #Метод для обработки кол-ва страниц
    def getPage(self, resp):
        ans = None
        if resp.xpath("//p/text()[contains(.,'Количество страниц:')]"):
            ans = resp.xpath("//p/text()[contains(.,'Количество страниц:')]").get().split(":")[1].strip()
        elif resp.xpath("//p/text()[contains(.,'Кол-во страниц:')]"):
            ans = resp.xpath("//p/text()[contains(.,'Кол-во страниц:')]").get().split(":")[1].strip()
        elif resp.xpath("//p/text()[contains(.,'Страниц:')]"):
            ans = resp.xpath("//p/text()[contains(.,'Страниц:')]").get().split(":")[1].strip()

        if "стр." in ans:
            ans = ans.replace("стр.","")
        elif "стр" in ans:
            ans = ans.replace("стр","")
        elif "(Офсет)" in ans:
            ans = ans.replace("(Офсет)","")
        elif "(Газетная)" in ans:
            ans = ans.replace("(Газетная)","")
            
        #Дополнительные методы. Собирают мусор
        #elif resp.xpath("//p/text()[contains(.,'Мягкая обложка,')]"):
        #    resp.xpath("//p/text()[contains(.,'Мягкая обложка,')]").get().split(",")[1].strip()
        #elif resp.xpath("//p/text()[contains(.,'Твердый переплет,')]"):
        #    ans = resp.xpath("//p/text()[contains(.,'Твердый переплет,')]").get().split(",")[1].strip()
        #elif resp.xpath("//p/text()[contains(.,'количество страниц ')]"):
        #    ans = resp.xpath("//p/text()[contains(.,'количество страниц ')]").get().split("количество страниц ")[0].strip()
        

        return ans

    #Метод сбора основных данных
    def parse(self, response, mainGenre):

        if response.status in self.handle_httpstatus_list:
            lib.WriteLog(response,mainGenre)
            return
        if response.url == "https://www.livelib.ru/service/ratelimitcaptcha":
            lib.WriteLog(response,mainGenre)
            return

        ans = BookCard

        ans.id = response.url.split("/")[-1].split("-")[0]
        try:
            ans.title = response.xpath("//h1[@class='bc__book-title ']/text()").get()
        except Exception as ex:
            print(ex)
            ans.title = None
        try:
            ans.author = ";".join(response.xpath("//h2[@class='bc-author']/a/text()").getall())
        except Exception as ex:
            print(ex)
            ans.author = None
        try:
            ans.type_book = response.xpath("//li[@class='bc-header__link bc-header__link--active bc-detailing-about']/details/div/a/text()").get()
        except Exception as ex:
            print(ex)
            ans.type_book = None            
        try:        
            ans.description = ''.join(response.xpath("//div[@id='lenta-card__text-edition-escaped' or @id='lenta-card__text-work-escaped']/text()").getall()).strip()

        except Exception as ex:
            print(ex)
            ans.description = None
        try:        
            temp = ';'.join(response.xpath("//p/text()[contains(.,'Жанры')]/../a/text()").getall())
            ans.genres_from_book = re.sub(r"№([1-9][0-9][0-9]|[1-9][0-9]|[1-9])\sв\s","",temp)
        except Exception as ex:
            print(ex)
            ans.genres_from_book = None

        ans.main_genre = mainGenre

        try:        
            ans.rating = response.xpath("//a[@class='bc-rating-medium']/span/text()").get()
        except Exception as ex:
            print(ex)
            ans.rating = None
        try:
            ans.number_of_pages = self.getPage(response)
        except Exception as ex:
            print(ex)
            ans.number_of_pages = None
        try:
            ans.language = response.xpath("//p/text()[contains(.,'Язык')]").get().split(":")[1].strip()
        except Exception as ex:
            print(ex)
            ans.language = None
        try:
            ans.age_limit = response.xpath("//p/text()[contains(.,'Возрастные ограничения')]").get().split(":")[1].strip()
        except Exception as ex:
            print(ex)
            ans.age_limit = None
        try:
            ans.publication_year = response.xpath("//p/text()[contains(.,'Год издания')]").get().split(":")[1].strip()
        except Exception as ex:
            print(ex)
            ans.publication_year = None
        try:
            ans.circulations = response.xpath("//p/text()[contains(.,'Тираж')]").get().split(":")[1].strip()
        except Exception as ex:
            print(ex)
            ans.circulations = None
        try:
            ans.ISBN = response.xpath("//p/text()[contains(.,'ISBN')]/../span/text()").get()
        except Exception as ex:
            print(ex)
            ans.ISBN = None
        try:
            ans.publisher = response.xpath("//td/text()[contains(.,'Издательство')]/../../td/a/text()").get()
        except Exception as ex:
            print(ex)
            ans.publisher = None
        try:
            scraped = json.loads(response.css('script::text').extract_first().strip(), strict=False)
            ans.number_of_reviews = scraped['aggregateRating']['ratingCount']
        except Exception as ex:
            print(ex)
            ans.number_of_reviews = None
        try:
            ans.number_of_users_read = response.xpath("//a[@title='Прочитали эту книгу']/b/text()").get()
        except Exception as ex:
            print(ex)
            ans.number_of_users_read = None
        try:
            ans.number_of_users_planning = response.xpath("//a[@title='Хотят прочитать']/b/text()").get()
        except Exception as ex:
            print(ex)
            ans.number_of_users_planning = None

        ans.sourceLink = response.url
        ans.parsing_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #Добавление в БД
        lib.AddBookToDB(ans)

import scrapy
import json
import lib
from LiveLibGenre.items import BookCard

import datetime

class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['www.livelib.ru']
    start_urls = ['http://www.livelib.ru/']

    custom_settings = {"LOG_FILE":f"db/log/{name}.log",'DOWNLOAD_DELAY':0,'ROBOTSTXT_OBEY':False}

    cookie = {
        "__ll_tum":"662613418",
        "__llutmz":"240",
        "__llutmf":"0",
        "_ga":"GA1.2.426077316.1682586915",
        "_gid":"GA1.2.1760576544.1682586915",
        "_ym_uid":"1682586915223789006",
        "_ym_d":"1682586915",
        "tmr_lvid":"1c37b50983049aec4ab48632c1723ab5",
        "tmr_lvidTS":"1682586915854",
        "__ll_fv":"1682586915",
        "_ym_isad":"2",
        "__ll_popup_count_pviews":"regc1_",
        "__ll_ab_mp":"1",
        "__popupmail_showed":"1000",
        "__popupmail_showed_uc":"1",
        "__ll_popup_count_shows":"regc1_mailc1_",
        "__ll_unreg_session":"3a6c3ded3770923ec678f991c5bb6638",
        "__ll_unreg_sessions_count":"2",
        "LiveLibId":"262037675a1420033e3135da2d4d7082",
        "_gat":"1",
        "_ym_visorc":"b",
        "__ll_dvs":"5",
        "ll_asid":"1259305471",
        "__ll_cp":"32",
        "tmr_detect":"0%7C1682608413824",
        "__ll_dv":"1682608421"
    }
    header = {
        "Cache-Control":"max-age=0",
        "Sec-Ch-Ua":'"Chromium";v="103", ".Not/A)Brand";v="99"',
        "Sec-Ch-Ua-Mobile":"?0",
        "Sec-Ch-Ua-Platform":"Linux",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site":"none",
        "Sec-Fetch-Mode":"navigate",
        "Sec-Fetch-User":"?1",
        "Sec-Fetch-Dest":"document",
        "Accept-Language":"en-US,en;q=0.9",
        "Accept-Encoding":"gzip, deflate"
    }

    curPage = 0

    def __init__(self, urlList, ):
        super(BookSpider, self).__init__()
        self.urlList = list(set(urlList))
        self.listLen = len(self.urlList)-1

    def start_requests(self):
        
        for curUrl in self.urlList:
            yield scrapy.Request(
                url=curUrl[0],
                cookies=self.cookie,
                headers=self.header,
                callback=self.parse,
                cb_kwargs={'mainGenre':curUrl[1]}
            )


    #Старый метод
    def getAdditionalInfo(ans,resp):

        ans.number_of_pages = None
        ans.language = None
        ans.age_limit = None
        ans.publication_year = None
        ans.circulations = None
        ans.ISBN = None
        ans.publisher = None

        for div in resp.xpath("//div[@class='bc-info__wrapper']"):
            if div.xpath("label/text()[contains(.,'Дополнительная информация')]").get():
                for info in div.xpath("div/p").getall():
                    if('ISBN' in info.xpath("text()").get()):
                        ans.ISBN = info.xpath("span/text()").get().strip()
                        continue
                    
                    if('Язык' in info.xpath("text()").get()):
                        ans.language = info.xpath("text()").get().split(":")[1].strip()
                        continue
                                            
                    if('Возрастные ограничения' in info.xpath("text()").get()):
                        ans.age_limit = info.xpath("text()").get().split(":")[1].strip()
                        continue
                                            
                    if('Твердый переплет' in info.xpath("text()").get()):
                        ans.number_of_pages = info.xpath("text()").get().split(",")[1].replace("стр.","").strip()
                        continue

                    if('страниц' in info.xpath("text()").get().lower()):
                        ans.number_of_pages = info.xpath("text()").get().split(":")[1].strip()
                        continue
                                            
                    if('Год издания' in info.xpath("text()").get()):
                        ans.publication_year = info.xpath("text()").get().split(":")[1].strip()
                        continue
                                            
                    if('ISBN' in info.xpath("text()").get()):

                        continue
                                            
                    if('ISBN' in info.xpath("text()").get()):

                        continue


                break


    def getPage(resp):
        ans = None
        if resp.xpath("//p/text()[contains(.,'Количество страниц:')]"):
            ans = resp.xpath("//p/text()[contains(.,'Количество страниц:')]").get().split(":")[1].strip()
        elif resp.xpath("//p/text()[contains(.,' страниц')]"):
            ans = resp.xpath("//p/text()[contains(.,' страниц')]").get().split(" ")[0].strip()
        elif resp.xpath("//p/text()[contains(.,'Страниц')]"):
            ans = resp.xpath("//p/text()[contains(.,'Страниц')]").get().split(":")[1].strip()
        elif resp.xpath("//p/text()[contains(.,'Мягкая обложка,')]"):
            resp.xpath("//p/text()[contains(.,'Мягкая обложка,')]").get().split(",")[1].strip()
        elif resp.xpath("//p/text()[contains(.,'Твердый переплет,')]"):
            ans = resp.xpath("//p/text()[contains(.,'Твердый переплет,')]").get().split(",")[1].strip()
        elif resp.xpath("//p/text()[contains(.,'количество страниц ')]"):
            ans = resp.xpath("//p/text()[contains(.,'количество страниц ')]").get().split("количество страниц ")[0].strip()
        

        return ans


    def parse(self, response, mainGenre):
        ans = BookCard

        ans.id = response.url.split("/")[-1].split("-")[0]
        try:
            ans.title = response.xpath("//h1[@class='bc__book-title ']/text()").get()
        except:
            ans.title = None
        try:
            ans.author = ";".join(response.xpath("//h2[@class='bc-author']/a/text()").getall())
        except:
            ans.author = None
        try:
            ans.type_book = response.xpath("//li[@class='bc-header__link bc-header__link--active bc-detailing-about']/details/div/a/text()").get()
        except:
            ans.type_book = None            
        try:        
            ans.description = ''.join(response.xpath("//div[@id='lenta-card__text-edition-escaped' or @id='lenta-card__text-work-escaped']/text()").getall()).strip()

        except:
            ans.description = None
        try:        
            ans.genres_from_book = ';'.join(response.xpath("//p/text()[contains(.,'Жанры')]/../a/text()").getall())
        except:
            ans.genres_from_book = None

        ans.main_genre = mainGenre

        try:        
            ans.rating = response.xpath("//a[@class='bc-rating-medium']/span/text()").get()
        except:
            ans.rating = None
        try:
            ans.number_of_pages = self.getPage(response)
        except:
            ans.number_of_pages = None
        try:
            ans.language = response.xpath("//p/text()[contains(.,'Язык')]").get().split(":")[1].strip()
        except:
            ans.language = None
        try:
            ans.age_limit = response.xpath("//p/text()[contains(.,'Возрастные ограничения')]").get().split(":")[1].strip()
        except:
            ans.age_limit = None
        try:
            ans.publication_year = response.xpath("//p/text()[contains(.,'Год издания')]").get().split(":")[1].strip()
        except:
            ans.publication_year = None
        try:
            ans.circulations = response.xpath("//p/text()[contains(.,'Тираж')]").get().split(":")[1].strip()
        except:
            ans.circulations = None
        try:
            ans.ISBN = response.xpath("//p/text()[contains(.,'ISBN')]/../span/text()").get()
        except:
            ans.ISBN = None
        try:
            ans.publisher = response.xpath("//td/text()[contains(.,'Издательство')]/../../td/a/text()").get()
        except:
            ans.publisher = None
        try:
            scraped = json.loads(response.css('script::text').extract_first().strip(), strict=False)
            ans.number_of_reviews = scraped['aggregateRating']['ratingCount']
        except:
            ans.number_of_reviews = None
        try:
            ans.number_of_users_read = response.xpath("//a[@title='Прочитали эту книгу']/b/text()").get()
        except:
            ans.number_of_users_read = None
        try:
            ans.number_of_users_planning = response.xpath("//a[@title='Хотят прочитать']/b/text()").get()
        except:
            ans.number_of_users_planning = None

        ans.sourceLink = response.url
        ans.parsing_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        lib.AddBookToDB(ans)

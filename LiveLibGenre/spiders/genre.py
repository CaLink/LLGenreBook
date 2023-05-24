import scrapy
from LiveLibGenre.items import Book
import lib


class GenreSpider(scrapy.Spider):
    name = 'genre'
    allowed_domains = ['www.livelib.ru']
    start_urls = ['http://www.livelib.ru/']
    homePage = "https://www.livelib.ru"
    custom_settings = {"LOG_FILE":f"db/log/{name}.log",'DOWNLOAD_DELAY':0,'ROBOTSTXT_OBEY':False}
    

    cookie = {  
        "__ll_tum":"662613418",
        "__llutmz":"240",
        "__llutmf":"0",
        "_ga":"GA1.2.426077316.1682586915",
        "_ym_uid":"1682586915223789006",
        "_ym_d":"1682586915",
        "tmr_lvid":"1c37b50983049aec4ab48632c1723ab5",
        "tmr_lvidTS":"1682586915854",
        "__ll_fv":"1682586915",
        "__ll_popup_count_pviews":"regc1_",
        "__ll_ab_mp":"1",
        "__popupmail_showed_uc":"1",
        "__ll_popup_count_shows":"regc1_mailc1_",
        "LiveLibId":"2a5d37abf3082e5f82d175e2b8185e28",
        "__utnt":"g0_y0_a15721_u0_c0",
        "__ll_unreg_session":"2a5d37abf3082e5f82d175e2b8185e28",
        "__ll_unreg_sessions_count":"3",
        "_gid":"GA1.2.1079432615.1684548340",
        "_gat":"1",
        "_ym_isad":"2",
        "_ym_visorc":"b",
        "iwatchyou":"840891ddddf58ffa159aa5becfb62922",
        "ll_asid":"1285630802",
        "__ll_dvs":"2",
        "promoLLid":"d1vhil0qqdrma83pj4e20dgln3",
        "__ll_dv":"1684548355",
        "__ll_cp":"36",
        "tmr_detect":"0%7C1684548357679"
    }
    header = {
        'Sec-Ch-Ua':'"Chromium";v="103", ".Not/A)Brand";v="99"',
        'Sec-Ch-Ua-Mobile':'?0',
        'Sec-Ch-Ua-Platform':'"Linux"',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site':'none',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-User':'?1',
        'Sec-Fetch-Dest':'document',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.9'
    }

    curPage = 1

    def __init__(self, startUrl,name):
        super(GenreSpider,self).__init__()
        self.startUrl = startUrl
        self.genreName = name
        

    def start_requests(self):
        lib.InitDB("GenreBook")

        yield scrapy.Request(
            url = self.startUrl,
            cookies=self.cookie,
            headers=self.header,
            callback=self.parse
        )

    def parse(self, response):
        
        self.curPage += 1
        
        books = response.xpath("//div[@class='brow-data']/div")
        for book in books:
            ans = Book

            ans.name = book.xpath("a[@class='brow-book-name with-cycle']/text()").get()
            ans.url = self.homePage + book.xpath("a[@class='brow-book-name with-cycle']/@href").get()
            ans.genre = self.genreName

            lib.AddToDB("GenreBook",ans)

        yield scrapy.Request(
            url = f"{self.startUrl}/listview/biglist/~{self.curPage}",
            cookies=self.cookie,
            headers=self.header,
            callback=self.parse
        )



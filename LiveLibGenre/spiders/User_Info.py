import scrapy
from LiveLibGenre.items import Book
import sqlite3
import re
import lib

class UserInfo(scrapy.Spider):
    name = 'livelib.user_info'
    allowed_domains = ['livelib.ru', 'www.livelib.ru']
    custom_settings = {"LOG_FILE":f"db/log/{name}.log",'DOWNLOAD_DELAY':0,'ROBOTSTXT_OBEY':False}
#    handle_httpstatus_list  = [404,502]

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

    def __init__(self):
        super(UserInfo, self).__init__()

        self.user_list = []
        with(open("UserList.txt","r") as fs):
            lines = fs.readlines()
            self.user_list = [line[:-1] for line in lines]
        


    def start_requests(self):
        self.count = 0

        for curUrl in self.user_list:
            yield scrapy.Request(
                url=curUrl,
                cookies=self.cookie,
                headers=self.header,
                callback=self.parse)

    def parse(self, response, **kwargs):

        self.user_login = response.css('.header-profile-login::text').extract()[0]

        self.user_info_dict = {
            'Имя': None, 'Фамилия': None, 'Пол': None,
            'Дата рождения': None, 'Местоположение': None, 'Читалки': None,
            'Дата регистрации': None, 'Статус': None, 'Рейтинг': None,
            'Индекс активности': None, 'Теги': None,
        }

        user_info_scraped = response.css('.profile-info-column .group-row-title').extract()

        for i in user_info_scraped:
            item_key = re.findall('<b>(.*?)</b>', re.sub(':', '', i))
            if item_key != []:
                if item_key[0] in self.user_info_dict.keys():
                    if item_key[0] == 'Рейтинг':
                        try:
                            user_rating = re.findall('title="(.*?)">', i)[0]
                            if user_rating == 'График изменения рейтинга':
                                user_rating = re.findall('рейтинга">(.*?)</a>', i)[0].split()[0]
                            self.user_info_dict[item_key[0]] = int(user_rating)
                        except:
                            self.user_info_dict[item_key[0]] = None

                    elif item_key[0] == 'Индекс активности':
                        try:
                            activity_rating = re.findall('title="(.*?)">', i)[0]
                            if activity_rating == 'График изменения индекса активности':
                                activity_rating = re.findall('активности">(.*?)</a>', i)[0].split()[0]
                            self.user_info_dict[item_key[0]] = int(activity_rating)
                        except:
                            self.user_info_dict[item_key[0]] = None

                    else:
                        try:
                            self.user_info_dict[item_key[0]] = re.findall('</b>(.*?)</span>', re.sub(': ', '', i))[0].strip()
                        except:
                            self.user_info_dict[item_key[0]] = None


        tags_scraped = list({re.findall('">(.*?)</a>', i)[0] for i in response.css('.card-block .marg-fix-labels a').extract()
                             if re.findall('">(.*?)</a>', i) != []})
        if tags_scraped != []:
            try:
                self.user_info_dict['Теги'] = '; '.join(tags_scraped)
            except:
                self.user_info_dict['Теги'] = None

        print(self.user_info_dict)

        self.connection = sqlite3.connect('user_info.db')
        self.cursor = self.connection.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                                       (UserLogin TEXT, UserLink TEXT, FirstName TEXT,
                                       LastName TEXT, Sex TEXT, BirthDate TEXT,
                                       Location TEXT, ReadingDevices TEXT, RegistrationDate TEXT,
                                       Status TEXT, Rating INTEGER, ActivityIndex INTEGER,
                                       Tags TEXT)''')

        self.cursor.execute('INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
                            (
                                self.user_login, response.url, self.user_info_dict['Имя'],
                                self.user_info_dict['Фамилия'], self.user_info_dict['Пол'],
                                self.user_info_dict['Дата рождения'],
                                self.user_info_dict['Местоположение'], self.user_info_dict['Читалки'],
                                self.user_info_dict['Дата регистрации'],
                                self.user_info_dict['Статус'], self.user_info_dict['Рейтинг'],
                                self.user_info_dict['Индекс активности'],
                                self.user_info_dict['Теги']
                            )
                            )

        self.connection.commit()
        self.connection.close()

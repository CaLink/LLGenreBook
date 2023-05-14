import lib
import sqlite3
from LiveLibGenre.spiders import genre, book
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging



lib.InitDir()           #создаем каталоги
lib.InitDB("GenreBook")
configure_logging()     #Штука для логов

#массив Ссылка, Жанр
#Все варианты находятся в "GenreList.csv"
genreList = [("https://www.livelib.ru/genre/%D0%9C%D0%B0%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9-%D1%80%D0%B5%D0%B0%D0%BB%D0%B8%D0%B7%D0%BC", "Магический реализм")]



parserConfig = CrawlerRunner(settings={'DOWNLOAD_DELAY':0,'ROBOTSTXT_OBEY':False})

@defer.inlineCallbacks
def genreParser():
    #for mainGenre in genreList:
    #    yield parserConfig.crawl(genre.GenreSpider,mainGenre[0],mainGenre[1])

    connection = sqlite3.connect("db/book.db")
    cursor = connection.cursor()
    cursor.execute('SELECT url, genre FROM GenreBook')
    query = cursor.fetchall()
    cursor.close()
    connection.close()

    yield parserConfig.crawl(book.BookSpider,query)

genreParser()
       

reactor.run()


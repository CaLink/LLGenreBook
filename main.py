import lib
import sqlite3
from LiveLibGenre.spiders import genre, book
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging



lib.InitDir()           #создаем каталоги
lib.InitDB("GenreBook") #Инициализация БД
configure_logging()     #Штука для логов

#массив Ссылка, Жанр
#Все варианты находятся в "GenreList.csv"
#Нужные жанры необходимо добавить в файл GenreToParse.txt в формате 'Ссылка;НазваниеЖанра'

genreList = []

with (open("GenreToParse.txt","r") as fs):
    line = fs.readline()
    
    while(line):
        genreList.append((line.split(";")[0],line.split(";")[1].strip()))
        line = fs.readline()



parserConfig = CrawlerRunner(settings={'DOWNLOAD_DELAY':0,'ROBOTSTXT_OBEY':False})

@defer.inlineCallbacks
def genreParser():
    #Сборк кнги
    for mainGenre in genreList:
        yield parserConfig.crawl(genre.GenreSpider,mainGenre[0],mainGenre[1])


    #Сбор карточек книг
    connection = sqlite3.connect("db/book.db")
    cursor = connection.cursor()
    cursor.execute('SELECT url, genre FROM GenreBook')
    query = cursor.fetchall()
    cursor.close()
    connection.close()

    yield parserConfig.crawl(book.BookSpider,query)

genreParser()
       

reactor.run()


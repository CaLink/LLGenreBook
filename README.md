# Сборщик информации из жанров

## Для запуска скрипта необходимо:
1. Подготовить файл **GenreToParse.txt**. Сейчас там находится 2 жанра - Исторический роман и Магический реализм.
Необходимо добавить в файл жанры, которые необходимо обработать. Они записываются в формате **"Ссылка;НазваниеЖанра"**
Информацию по жанрам можно найти в файле **GenreList.csv** (Здесь хранятся все жанры в формате **"Подуровень жанра;Ссылка;Название;Кол-воКниг"**)
    - Возможно потребуется заменить coockies и header. Они находятся внутри пауков и имеют соответствующие название
2. Выполнить скрипт main.py. Скрипты необходимо выполнять из корня (там, где находится main.py)
3. Во время выполнения скрипта формируются логи (**db/log**). В них можно отслеживать выполнение скрипта. Так же логи выводятся в консоль. Здесь может возникать множество ошибок. Они связаны с тем, что не всегда находится нужный <\tag> в html'е.
4. По окончанию выполнения скрипта в консоль перестанут поступать сообщения об ошибках, а в логах будет уведомления о закрытии пауков


## Сборщик собирает информацию в два этапа:
1. Обход по жанру и сбор url'ов на книги, входящих в его состав. Они добавляются в базу данных. Здесь используется паук genre
2. Из базы данных берутся все url'ы книг, чтобы пройтись по ним и собрать данные о книге. Здесь используется паук book

import scrapy
import csv

# rodar com scrapy crawl myspider

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.letras.mus.br/taylor-swift/discografia/midnights-the-late-night-edition-2023/']

   
    song_data_list = []
    current_track_title = None  
    line_number = 1 

    def parse(self, response):
        song_list = response.css('ul.songList-table-content li.songList-table-row')
        track_n = 1

        for song in song_list:
            song_link = song.css('a::attr(href)').get()
            if song_link:
                yield response.follow(song_link, self.parse_song, meta={'track_n': track_n})
                track_n += 1

    def parse_song(self, response):
     
        song_title = response.css('.head-title::text').get()

        lyric_lines = response.css('.lyric-original p::text').getall()

        if song_title and lyric_lines:
            # Se o título da faixa atual for diferente do anterior, atualize o título da faixa atual e redefina a contagem de linha
            if song_title != self.current_track_title:
                self.current_track_title = song_title
                self.line_number = 1

            for lyric_line in lyric_lines:
                song_data = {
                    "album_name": "midnights",
                    "track_title": song_title.strip(),
                    "track_n": response.meta.get('track_n'),
                    "lyric": lyric_line.strip(),
                    "line": self.line_number
                }

                # Incrementa a contagem de linha
                self.line_number += 1

                # Adicione os dados da música à lista de dados
                self.song_data_list.append(song_data)

    def closed(self, reason):
        sorted_song_data = sorted(self.song_data_list, key=lambda x: x["track_n"])

        with open('music_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ["album_name", "track_title", "track_n", "lyric", "line"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for song_data in sorted_song_data:
                writer.writerow(song_data)






# import scrapy
# import csv

# class MySpider(scrapy.Spider):
#     name = 'myspider'
#     start_urls = ['https://www.letras.mus.br/taylor-swift/discografia/1989-taylors-version-deluxe-2023/']

#     def parse(self, response):
#         # Encontre a lista de músicas na página
#         song_list = response.css('ul.songList-table-content li.songList-table-row')

#         # Inicialize a contagem de faixas
#         track_n = 1

#         # Itere pelos elementos da lista e colete os links das músicas
#         for song in song_list:
#             song_link = song.css('a::attr(href)').get()
#             if song_link:
#                 # Passe a contagem de faixas para a função de análise da música
#                 yield response.follow(song_link, self.parse_song, meta={'track_n': track_n})
#                 track_n += 1

#     def parse_song(self, response):
#         # Coleta o nome da música

#         # Coleta o título da música
#         song_title = response.css('.head-title::text').get()

#         # Coleta a letra da música linha por linha
#         lyric_lines = response.css('.lyric-original p::text').getall()

#         # Verifique se o nome da música, título e letra existem
#         if song_title and lyric_lines:
#             # Junte as linhas da letra em um único texto
#             lyric = "\n".join(lyric_lines).strip()

#             # Coleta a contagem de faixas da meta
#             track_n = response.meta.get('track_n')
#             print(song_title)
#             print(track_n)
#             print(lyric_lines)

#             # Armazene os resultados em um dicionário
#             song_data = {
#                 "Título da música": song_title.strip(),
#                 "Letra da música": lyric,
#                 "Track Number": track_n
#             }

#             # Retorne os dados da música
#             yield song_data

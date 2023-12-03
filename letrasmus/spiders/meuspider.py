import scrapy
import csv

# rode com scrapy crawl myspider

class MySpider(scrapy.Spider):
    #Coloque o link do álbum do site Letras
    name = 'myspider'
    start_urls = ['https://www.letras.mus.br/andy-shauf/discografia/the-party-2016/']

   
    song_data_list = []
    current_track_title = None  
    line_number = 1 

    def parse(self, response):
        song_list = response.css('ul.songList-table-content li.songList-table-row')
        print(song_list)
        track_n = 1

        for song in song_list:
            song_link = song.css('a::attr(href)').get()
            if song_link:
                yield response.follow(song_link, self.parse_song, meta={'track_n': track_n})
                track_n += 1

    def parse_song(self, response):
     
        song_title = response.css('.head-title::text').get()
        print(song_title)

        lyric_lines = response.css('.lyric-original p::text').getall()

        if song_title and lyric_lines:
            if song_title != self.current_track_title:
                self.current_track_title = song_title
                self.line_number = 1

            # É necessário por o nome do álbum manualmente
            for lyric_line in lyric_lines:
                song_data = {
                    "album_name": "the party",
                    "track_title": song_title.strip(),
                    "track_n": response.meta.get('track_n'),
                    "lyric": lyric_line.strip(),
                    "line": self.line_number
                }

                self.line_number += 1
                self.song_data_list.append(song_data)

    def closed(self, reason):
        sorted_song_data = sorted(self.song_data_list, key=lambda x: x["track_n"])

        with open('music_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ["album_name", "track_title", "track_n", "lyric", "line"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for song_data in sorted_song_data:
                writer.writerow(song_data)

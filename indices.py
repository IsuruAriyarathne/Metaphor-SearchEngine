from elasticsearch_dsl import Index
import json,re
from elasticsearch import Elasticsearch, helpers
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

es = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    http_auth=(config['ELASTIC']['user'], config['ELASTIC']['password'])
)

INDEX = 'sinhala-metaphors-new1'

def createIndex():
    index = Index(INDEX,using=es)
    res = index.create()
    print (res)

def read_all_songs():
    with open('summary-corpus/data.json','r') as f:
        all_songs = json.loads(f.read())
        res_list = [i for n, i in enumerate(all_songs) if i not in all_songs[n + 1:]]
        return res_list

def clean_lyrics(lyrics):
    if lyrics:
        cleaned_lyrics_list = []
        lines = lyrics.split('\n')
        for index,line in enumerate(lines):
            line_stripped = re.sub('\s+',' ',line)
            line_punc_stripped = re.sub('[.!?\\-]', '', line_stripped)
            cleaned_lyrics_list.append(line_punc_stripped)
        last = len(cleaned_lyrics_list)
        final_list = []
        for index,line in enumerate(cleaned_lyrics_list):
            if line=='' or line==' ':
                if index!= last-1 and (cleaned_lyrics_list[index+1]==' ' or cleaned_lyrics_list[index+1]=='') :
                    pass
                else:
                    final_list.append(line)
            else:
                final_list.append(line)
        cleaned_lyrics = '\n'.join(final_list)
        return cleaned_lyrics
    else:
        return None


def genData(song_array):
    for song in song_array:

        # English
        english_name = song.get("Title_en", None)
        english_lyricist = song.get("Lyricist_en", None)
        english_singer = song.get("Singer_en", None)
        english_composer = song.get("Composer_en", None)

        # Sinhala

        sinhala_name = song.get("Title_si", None)
        sinhala_lyricist = song.get("Lyricist", None)
        sinhala_singer = song.get("Singer", None)
        sinhala_composer = song.get("Composer", None)

        lyrics = clean_lyrics(song.get("Lyrics",None))

        sinhala_metaphor = song.get("Metaphor", None)
        sinhala_source = song.get("Source", None)
        sinhala_target = song.get("Target", None)
        sinhala_interpretation = song.get("Intepretation", None)

        yield {
            "_index": "sinhala-metaphors-new1",
            "_source": {
                "english_name": english_name,
                "english_lyricist": english_lyricist,
                "english_composer": english_composer,
                "english_singer": english_singer,
                "sinhala_name": sinhala_name,
                "sinhala_lyricist": sinhala_lyricist,
                "sinhala_composer": sinhala_composer,
                "sinhala_singer": sinhala_singer,
                "lyrics": lyrics,
                "sinhala_metaphor": sinhala_metaphor,
                "sinhala_source": sinhala_source,
                "sinhala_target": sinhala_target,
                "sinhala_interpretation": sinhala_interpretation
            },
        }


# createIndex()
all_songs = read_all_songs()
helpers.bulk(es,genData(all_songs))


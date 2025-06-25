import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import lyricsgenius
import re
from sentence_transformers import SentenceTransformer


genius = lyricsgenius.Genius('2dYqSvUNCMoRboDR60nHLo7OsHqANk8BehiQ2WxExnKgqyBbLwdB-ePTjyxgRdsm', remove_section_headers = True)

def get_lyrics(song_title, artist_title):
    song = genius.search_song(song_title, artist_title)
    return song.lyrics if song else None


### Cleaning


def clean_lyrics(text):

    text = re.sub(r'^\d+\s+Contributors.*$', '', text, flags=re.MULTILINE)
    text = text.replace('—', ' — ').replace('–', ' – ')
    text = re.sub(r'\[(.*?)\]', '', text)
    text = re.sub(r'[^a-zA-Z\s\-]', '', text, flags=re.DOTALL)
    text = '\n'.join(re.sub(r'\s+', ' ', line).strip() for line in text.split('\n'))
    

    return text


def filter_and_split_lines(text, max_length=200):
    lines = text.split('\n')
    filtered_lines = [line for line in lines if len(line.strip()) <= max_length and line.strip() != '']
    return filtered_lines



def lyrics_preprocessing(song):
    text = clean_lyrics(song)
    lines = filter_and_split_lines(text)
    return lines



def embed_lyrics(lyrics, model = SentenceTransformer('all-MiniLM-L6-v2')):
    return model.encode(lyrics)


def plot_pca(embeddings, lyrics):
    pca = PCA(n_components = 2)
    reduced = pca.fit_transform(embeddings)

    plt.figure(figsize = (12, 8))
    plt.scatter(reduced[:, 0], reduced[:, 1], alpha = 0.7)

    for i, line in enumerate(lyrics[:50]):  # only label first 50 lines to avoid clutter
        short = line[:20] + "..." if len(line) > 20 else line
        plt.text(reduced[i, 0], reduced[i, 1], short, fontsize=8)

    plt.title("2D Visualization of BERT Embeddings for Lyric Lines")
    plt.xlabel("Component 1")
    plt.ylabel("Component 2")
    plt.tight_layout()
    plt.show()


def get_song_embeddings(song_title, artist_title, model = SentenceTransformer('all-MiniLM-L6-v2'), plot = False):

    song = genius.search_song(song_title, artist_title)
    
    cleaned_lyrics = lyrics_preprocessing(song.lyrics)

    embeddings = embed_lyrics(cleaned_lyrics, model)

    if plot:
        plot_pca(embeddings, cleaned_lyrics)

    return embeddings

    

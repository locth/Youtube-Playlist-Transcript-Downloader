from youtube_transcript_api import YouTubeTranscriptApi as transTool
from pytube import Playlist
import os
import argparse
from tqdm import tqdm

subject = Playlist("https://www.youtube.com/playlist?list=PLb62OySGqC9xDQAzPDy9FEATPemic8F0l")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download YouTube video transcript')
    parser.add_argument('--subject', help='Name of subject', default=None)
    parser.add_argument('--playlist_url', help='URL of subject playlist', default=None)
    parser.add_argument('--language', help='Language of transcript: vn / en', default=None)

    args = parser.parse_args()

    subject = args.subject
    if not subject:
        subject = input("Nhap ten mon hoc: ")

    playlist_url = args.playlist_url
    if not playlist_url:
        playlist_url = input("Nhap link playlist: ")

    language = args.language
    if not language:
        language = input("Nhap ngon ngu muon tai transcript [vi/en]: ")

    if not os.path.exists(subject):
        os.mkdir(subject)
    
    subjectPlaylist = Playlist(playlist_url)

    for video in tqdm(subjectPlaylist.videos):
        title = video.title.replace(":", "")
        video_id = video.video_id

        transcript = transTool.get_transcript(video_id, languages=[language, 'vi', 'en'])
        transcript_text = ' '.join(element['text'] for element in transcript)

        with open(os.path.join(subject, title + ".txt"), "w", encoding='utf-8') as f:
            f.write(transcript_text)
from youtube_transcript_api import YouTubeTranscriptApi as transTool
from pytubefix import Playlist, YouTube
import os
import argparse
from tqdm import tqdm

subject = Playlist("https://www.youtube.com/playlist?list=PLb62OySGqC9xDQAzPDy9FEATPemic8F0l")

def downloadTranscript(subject, video):
    title = video.title.replace(":", "")
    video_id = video.video_id

    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            transcript = transTool.get_transcript(video_id, languages=[language, 'vi', 'en'])
            transcript_text = ' '.join(element['text'] for element in transcript)

            with open(os.path.join(subject, title + ".txt"), "w", encoding='utf-8') as f:
                f.write(transcript_text)
            success = True
        except Exception:
            print(f"Khong tai duoc transcript cho video {title}. Thu lai lan thu {attempts + 1}...")
            attempts += 1

    if not success:
        print(f"Video {title} bi loi! Tai transcript khong thanh cong sau 3 lan thu.")
        with open("LUU Y.txt", "a", encoding='utf-8') as note:
            note.write(f"Video {title} bi loi! Tai transcript khong thanh cong sau 3 lan thu.\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download YouTube video transcript')
    parser.add_argument('--subject', help='Name of subject', default=None)
    parser.add_argument('--playlist_url', help='URL of subject playlist', default=None)
    parser.add_argument('--language', help='Language of transcript: vn / en', default=None)

    args = parser.parse_args()
    cont = "y"

    while (cont == "y"):
        mode = input("Vui long chon che do su dung: \n \
                    1. Tai transcript cho 1 video \n \
                    2. Tai transcript cho 1 playlist\n \
                    Che do [ 1 / 2 ]: ")

        subject = args.subject
        if not subject:
            subject = input("Nhap ten mon hoc: ")

        playlist_url = args.playlist_url
        if not playlist_url:
            playlist_url = input("Nhap link video/playlist: ")

        language = args.language
        if not language:
            language = input("Nhap ngon ngu muon tai transcript [ vi / en ]: ")

        if not os.path.exists(subject):
            os.mkdir(subject)
        
        if mode == "1":
            video = YouTube(playlist_url)
            downloadTranscript(subject, video)
        elif mode == "2":
            subjectPlaylist = Playlist(playlist_url)
            for video in tqdm(subjectPlaylist.videos):
                downloadTranscript(subject, video)
        
        cont = input("\nBan co muon tiep tuc [ y / n ]?: ")

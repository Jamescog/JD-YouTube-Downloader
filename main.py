from pytube import YouTube
from collections import OrderedDict

# Initialize an empty dictionary to store cached YouTube objects
cached_videos = OrderedDict()


def seconds_to_hms(seconds):
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def information(url, download=False, itag=None):
    if url in cached_videos:
        if download:
            itag = itag
        my_video = cached_videos[url]
        down = my_video.get_by_itag(itag)
        down_url = down.url
        return down_url, f"{down.title}.{down.subtype}"
    else:
        my_video = YouTube(url)
        print("Youtebe object created")
        streams = my_video.streams.filter(progressive=True)
        print("Streams filtered")
        cached_videos[url] = streams
        if len(cached_videos) > 10:
            cached_videos.popitem(last=False)
        videos = {}
        audio = {}
        data = {}

        filename = my_video.title
        length = my_video.length
        data["title"] = filename
        data["duration"] = seconds_to_hms(length)
        for s in streams:
            tempo = {
                "file_size": f"{s.filesize_mb:.1f} MB",
                "subtype": s.subtype,
            }
            if s.type == "video":
                tempo["resolution"] = s.resolution
                videos[s.itag] = tempo
            else:
                audio[s.itag] = tempo
        data["videos"] = videos
        return data

from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse as urlparse
import re

def get_text(url_link):

    video_id = get_video_id(url_link)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    final_text = ""

    for text in transcript:
        temp_text = text['text'].lower()
        if len(final_text) == 0:
            temp_text = temp_text.capitalize()
            final_text += temp_text
        else:
            if final_text[-1] == ".":
                temp_text = temp_text.capitalize()
            
            if final_text[-1] == ' ' or temp_text[0] == ' ':
                final_text += temp_text
            else:
                final_text += ' ' + temp_text
        
    return final_text

def get_video_id(value):
    test_links = """
    'http://www.youtube.com/watch?v=5Y6HSHwhVlY',
    'http://www.youtube.com/watch?/watch?other_param&v=5Y6HSHwhVlY',
    'http://www.youtube.com/v/5Y6HSHwhVlY',
    'http://youtu.be/5Y6HSHwhVlY', 
    'http://www.youtube.com/embed/5Y6HSHwhVlY?rel=0" frameborder="0"',
    'http://m.youtube.com/v/5Y6HSHwhVlY',
    'https://www.youtube-nocookie.com/v/5Y6HSHwhVlY?version=3&amp;hl=en_US',
    'http://www.youtube.com/',
    'http://www.youtube.com/?feature=ytca
    """

    pattern = r'(?:https?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtube|youtu|youtube-nocookie)\.(?:com|be)\/(?:watch\?v=|watch\?.+&v=|embed\/|v\/|.+\?v=)?([^&=\n%\?]{11})'

    result = re.findall(pattern, value, re.MULTILINE | re.IGNORECASE)

    print(result)
    return result[0]

#print(get_text("https://youtu.be/3zLOihUVd2g"))
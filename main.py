import argparse
import datetime
import m3u8
import time
import requests
import streamlink


# Trying to get the media playlist or segment raises 404 Not Found error
# when the stream ends. Need to stop after a certain number of retries.
MAX_NOT_FOUND_COUNT = 5

STREAM_URL = 'https://a.upload.youtube.com/http_upload_hls?cid={stream_key}&copy=0&file='
# TODO: Use backup URL for better reliability
BACKUP_STREAM_URL = 'https://b.upload.youtube.com/http_upload_hls?cid={stream_key}&copy=1&file='


# Generate a simple HLS media playlist to push to Youtube
def generate_playlist(sequence, segment):
  return '\n'.join([
    '#EXTM3U',
    '#EXT-X-VERSION:3',
    '#EXT-X-MEDIA-SEQUENCE: %d' % sequence,
    '#EXT-X-TARGETDURATION:5',
    '#EXTINF: %f' % segment.duration,
    '%d.ts' % sequence])


class LivestreamRelay:
  # TODO: Use stream quality parameters  
  # TODO: Use Twitch oauth token
  def __init__(self, username: str, stream_key: str, sleep_seconds: float=5.0):
    self.username: str = username
    self.stream_key: str = stream_key
    self.sleep_seconds: float = sleep_seconds

  def start_check(self):
    twitch_stream_url = f'https://twitch.tv/{self.username}'
    while True:
      try:
        streams = streamlink.streams(twitch_stream_url)
        if streams:
          playlist_url = streams['best'].url
          print('Stream found for', self.username)
          print('Source media playlist URL:', playlist_url)
          self.start_livestream_relay(playlist_url)
        else:
          print('No stream of', self.username, 'as of', datetime.datetime.now())
      except Exception as e:
        print('Error getting Twitch streams:', e)
      time.sleep(self.sleep_seconds)

  def start_livestream_relay(self, playlist_url: str):  
    sequence = 0
    not_found_count = 0
    stream_url = STREAM_URL.format(stream_key=self.stream_key)
    processed_segment_uris = set()
    while True:
      try:
        source_playlist = m3u8.load(playlist_url)
        for segment in source_playlist.segments:
          if segment.uri in processed_segment_uris:  # Skip processed segment URIs
            continue
          processed_segment_uris.add(segment.uri)
          
          if '|' in segment.title:  # Skip ads
            print('Skipping ads..')
            continue

          # TODO: error handling and backup server trial
          media_playlist = generate_playlist(sequence, segment)
          requests.post(stream_url + 'master.m3u8', data=media_playlist)
          print('Uploaded playlist for sequence', sequence)
          
          response = requests.get(segment.uri)
          filename = f'{sequence}.ts'
          requests.post(stream_url + filename, data=response.content)
          print('Uploaded segment', filename, 'of length', len(response.content))
          
          sequence += 1 

        not_found_count: int = 0
      except Exception as e:
        print('Error getting or uploading playlist/segment:', e)
        
        # TODO: Is there a better way to check the end of the stream?
        if '404' in str(e):
          not_found_count += 1
          if not_found_count >= MAX_NOT_FOUND_COUNT:
            return
          print((f'Playlist/segment is not found for {not_found_count} times.'
                 'The stream has probably ended. Retrying..'))
          time.sleep(3)

      time.sleep(2)
    
    
if __name__ == '__main__':
  argparser = argparse.ArgumentParser()
  argparser.add_argument(
      '-c', '--channel', required=True, help='Twitch channel name')
  argparser.add_argument(
      '-s', '--stream-key', required=True, help='Youtube stream key')
  args = argparser.parse_args()
  relay = LivestreamRelay(args.channel, args.stream_key) 
  relay.start_check()
  

### 한국어 (For Korean users)
한국어 설명서는 [여기](README.ko.md)에 있습니다.


# Relaying Twitch streams to Youtube
This script regularly checks if a Twitch channel is live. If a channel goes online, it relays the Twitch stream to an unlisted Youtube livestream, while skipping any ads. Once the stream goes offline, the script waits for the next stream.

# Usage
```plaintext
usage: main.py [-h] -c CHANNEL -s STREAM_KEY
  -c / --channel       The Twitch channel name to check
  -s / --stream-key    Youtube stream key from #6 in Prepare for Youtube Livestream. Looks like "OOOO-OOOO-OOOO-OOOO"
```

# Prepare for Youtube Livestream
Pleaes note that it can take 24 hours to enable livestream in Youtube.
1. Go to https://youtube.com/livestreaming
2. Request to enable livestream, wait for 24 hours.
3. Go to the dashboard in https://youtube.com/livestreaming 
4. Click the stream key dropdown, and click "Create a new stream key"
5. Configure the new stream key
  a. **Name**: any name you want. It will be the default stream name.
  b. **Streaming Protocol**: must be "HLS"
6. Copy "Stream key" to use later


# Technical Details
## HLS pull/push
Twitch uses [HLS (HTTP Live Streaming)](https://en.wikipedia.org/wiki/HTTP_Live_Streaming) to output its streams, and we are also using HLS to upload stream to Youtube. 

In general, HLS has two components: (1) .m3u8 playlists and (2) .ts segments. Ths script downloads playlists and segments from Twitch, generates simplified playlists, and uploads the repackaged playlists and the same segment files to Youtube.
## No encoding/decoding (no FFMPEG)
Since the script only downloads/uploads .m3u8 media playlist and.ts segment files, it does not re-encode to relay the stream, therefore uses significantly less CPU.
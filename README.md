# M3U8 Video Playback Website

## Project Description

This is a simple M3U8 video playback website developed using the Flask framework. It allows users to upload video files, convert them to the HLS (HTTP Live Streaming) format, and play them through a web interface.

## Key Features

- Users can upload video files, and the system automatically converts them to the HLS format.
- Smooth video playback.
- Implemented using Flask and FFmpeg.

## Directory Structure

```
FLASK-M3U8-VIDEO/
│
├── app.py           # Main Flask application
├── templates/       # HTML template files
├── static/          # Static files (CSS, JavaScript, video files, etc.)
├── requirements.txt  # List of dependencies
├── README.md        # Project documentation (this file)
```

## Installation and Running

1. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the project:

   ```bash
   python app.py
   ```

   The project will run on http://localhost:5000/.

## Usage

1. Visit the website's homepage and click the "Upload Video" button to upload video files.
2. Wait for the video conversion to complete, and then click the video link to watch.

## Technology Stack

- Python
- Flask
- FFmpeg
- LayUI (used for the front-end interface)

## HLS
HLS is an HTTP-based streaming protocol used for live streaming and video-on-demand. It works by dividing the video stream into small HTTP-based files, and only one segment is downloaded at a time.

The HLS protocol was introduced by Apple and consists of three components:
1. HTTP: The transport protocol.
2. m3u8: The index file.
3. TS files: Containing audio and video media information.

The m3u8 file is a UTF-8 encoded plain text index file that acts like a playlist, listing individual video segments (ts files).

On the client side, the m3u8 file is first parsed, and then HTTP requests are made for each segment (ts file). The Media Source Extensions (MSE) appendBuffer method is used to encapsulate the buffer, resulting in seamless playback, which is then handed off to the player.

FFmpeg is a command-line tool for manipulating and converting multimedia streams.

## TODO List
1. Implement user account login.
2. Implement an administrator role for video management.
3. Support video bitrate and playback speed switching.

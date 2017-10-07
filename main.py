import argparse
from flask import Flask, render_template, Response
from tristream import CameraStream

app = Flask(__name__)
STREAM_TYPE = 'unknown'

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (
        b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
        )

@app.route('/video_feed')
def video_feed():
    Stream = None
    if STREAM_TYPE == 'camera':
        Stream = CameraStream
    return Response(
        gen(Stream()),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TriRemote server.')
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        dest='host',
        help='host to be used'
    )
    parser.add_argument(
        '--port',
        type=str,
        default='8747',
        dest='port',
        help='port to be used'
    )
    parser.add_argument(
        '--stream',
        type=str,
        default='camera',
        dest='stream',
        help='stream type to be used'
    )
    args = parser.parse_args()
    STREAM_TYPE = args.stream
    app.run(host=args.host, port=args.port)

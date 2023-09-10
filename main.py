import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "0.0.0.0"
hostPort = 5334


class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            new_file = open("data.wav", "wb")
            new_file.write(bytearray(post_data))

            # convert audio to 16bit x 16kHz, data.wav -> output.wav
            subprocess.check_call(['ffmpeg -y -i data.wav -ar 16000 -ac 1 -c:a pcm_s16le output.wav'], shell=True)
            # run whisper.cpp "small" model, for speech recognition, output.wav -> res.json
            subprocess.check_call(['./main -m ./ggml-small.bin -f ./output.wav -t 8 -l ru -of res -oj'], shell=True)

            with open('res.json') as f:
                contents = f.read()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes(contents, encoding='utf8'))

            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


myServer = HTTPServer((hostName, hostPort), MyHandler)
try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()

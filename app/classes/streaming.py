from twython.streaming.api import TwythonStreamer

class Streamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print data['text'].encode('utf-8')

    def on_error(self, status_code, data):
        print status_code
        print data
        self.disconnect()   # ???
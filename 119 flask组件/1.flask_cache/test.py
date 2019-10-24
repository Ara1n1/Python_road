import datetime

from flask import Flask
from flask.ext.cache import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)
cache.init_app(app)


@app.route('/')
def hello():
    return "hello, world!"


@app.route('/t')
@cache.cached(timeout=60 * 30)
def cached_page():
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return "hello, world, what's your name, thank you!!...  localtime: " + time


if __name__ == '__main__':
    app.run()

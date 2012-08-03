import os
from flask import Flask
import nbconvert.nbconvert as nbconvert
import requests
from nbformat import current as nbformat

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/<int:id>')
def fetch_and_render(id):
    """Fetch and render a post from the Github API"""
    print 'am here, with id', id
    r = requests.get('https://api.github.com/gists/{}'.format(id))

    print 'requests..'
    if r.status_code != 200:
        return None

    print 'decoding...'
    decoded = r.json.copy()
    jsonipynb = decoded['files'].values()[0]['content']

    print 'init converter...'
    converter = nbconvert.ConverterHTML()
    print 'setting json'
    converter.nb = nbformat.reads_json(jsonipynb)
    print 'running convert...';
    result = converter.convert()
    return result




if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

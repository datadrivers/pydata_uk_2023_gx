import logging
import os
from flask import Flask, request
from google.cloud import storage

app = Flask(__name__)
CLOUD_STORAGE_BUCKET = "pydata-demo"
prefix = "default_data_docs_site"


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def index(path):
    gcs = storage.Client()
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    try:
        blob = bucket.get_blob(prefix + "/" + path)
        content = blob.download_as_string()
        if blob.content_encoding:
            resource = content.decode(blob.content_encoding)
        else:
            resource = content
    except Exception as e:
        logging.exception("couldn't get blob")
        resource = "<p></p>"
    return resource


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return '''
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    '''.format(e), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

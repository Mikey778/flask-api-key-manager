from api_key_manager.api_key_manager import ApiKeyManager
from functools import wraps
from flask import Flask, request, abort, jsonify
import ssl
from api_key_manager.key_expiration_alerts import KeyExpirationAlert


# TODO generate ssl files
#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#context.load_cert_chain('host.cert', 'host.key')

api_key_manager = ApiKeyManager()
key_expiration_alert = KeyExpirationAlert()


app = Flask(__name__)


@app.route('/hello', methods=['GET'])
@api_key_manager.require_appkey
def hello():
    return 'hello!'


if __name__ == '__main__':
    key_expiration_alert.start_corn_job()
    try:
        app.run('localhost', '5001')
    except (KeyboardInterrupt, SystemExit):
        key_expiration_alert.shutdown()

    # TODO generate cert files
    #context = ('host.cert', 'host.key')
    # app.run(host='0.0.0.0', port=80, ssl_context=context,
    #        threaded=True, debug=True)

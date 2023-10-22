import os
from app import app
import ssl

cert_file = os.getcwd() + "/cert/certificate.crt"
key_file = os.getcwd() + "/cert/private.key"
# contetxt = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# contetxt.load_cert_chain(cert_file, key_file)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(cert_file, key_file)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=443, ssl_context=context)

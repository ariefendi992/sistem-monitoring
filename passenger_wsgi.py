import os
from app import app
import ssl

cert_file = os.getcwd() + "/cert.pem"
key_file = os.getcwd() + "/key.pem"
# contetxt = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# contetxt.load_cert_chain(cert_file, key_file)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

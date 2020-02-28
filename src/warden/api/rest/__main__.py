
import ptvsd
ptvsd.enable_attach(address = ('0.0.0.0', 10504))

from warden.api.rest.wsgi import app
app.run(host='0.0.0.0', port=10502, debug=False)


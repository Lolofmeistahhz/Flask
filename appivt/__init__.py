import os

from flask import Flask
from appivt.config import Config

app = Flask(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path,"f_ivt.db")))
app.config.from_object(Config)


from appivt import routes

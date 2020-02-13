from .setup import create_app, create_mongo
from .settings import MONGO_URI



# CREATE APP AND MONGO
app   = create_app()
mongo = create_mongo(app, MONGO_URI) 

# REGISTER
mongo.init_app(app)
# The database needs to be initialised in a separate module to avoid circular imports
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

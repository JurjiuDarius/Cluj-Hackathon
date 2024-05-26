from .appointment import appointment_bp
from .chat import chat_bp
from .diagnostic import diagnostic_bp
from .login import login_bp
from .pet import pet_bp
from .user import user_bp

blueprints = [appointment_bp, login_bp, user_bp, diagnostic_bp, pet_bp, chat_bp]

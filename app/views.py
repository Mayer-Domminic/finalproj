from flask import Blueprint, request, jsonify
from .models import Workout

def get_db():
    from flask import current_app
    return current_app.db
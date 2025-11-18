from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Page(db.Model):
    """Dynamic page model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    show_in_menu = db.Column(db.Boolean, default=True)
    menu_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User', backref='pages')

    def __repr__(self):
        return f'<Page {self.title}>'


class Media(db.Model):
    """Media files (images, logos) model"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)  # image, logo, etc.
    mime_type = db.Column(db.String(100), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    alt_text = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    uploaded_by = db.relationship('User', backref='media_files')

    def __repr__(self):
        return f'<Media {self.original_filename}>'


class Theme(db.Model):
    """Theme customization settings"""
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(200), default='Mon Site Web')
    primary_color = db.Column(db.String(7), default='#007bff')  # Hex color
    secondary_color = db.Column(db.String(7), default='#6c757d')
    accent_color = db.Column(db.String(7), default='#28a745')
    background_color = db.Column(db.String(7), default='#ffffff')
    text_color = db.Column(db.String(7), default='#212529')
    logo_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True)
    logo = db.relationship('Media', foreign_keys=[logo_id])
    favicon_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True)
    favicon = db.relationship('Media', foreign_keys=[favicon_id])
    footer_text = db.Column(db.Text, default='© 2024 Mon Site Web. Tous droits réservés.')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Theme {self.site_name}>'

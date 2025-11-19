from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, Regexp

class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')


class PageForm(FlaskForm):
    """Page creation/edit form"""
    title = StringField('Titre', validators=[DataRequired(), Length(max=200)])
    slug = StringField('URL (slug)', validators=[
        DataRequired(),
        Length(max=200),
        Regexp(r'^[a-z0-9-]+$', message='Le slug ne peut contenir que des lettres minuscules, chiffres et tirets')
    ])
    content = TextAreaField('Contenu', validators=[DataRequired()])
    is_published = BooleanField('Publié')
    show_in_menu = BooleanField('Afficher dans le menu', default=True)
    menu_order = IntegerField('Ordre dans le menu', default=0)
    submit = SubmitField('Enregistrer')


class MediaUploadForm(FlaskForm):
    """Media upload form"""
    file = FileField('Fichier', validators=[
        DataRequired(),
        FileAllowed(['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'], 'Images uniquement!')
    ])
    alt_text = StringField('Texte alternatif', validators=[Optional(), Length(max=255)])
    file_type = StringField('Type', default='image')
    submit = SubmitField('Télécharger')


class ThemeForm(FlaskForm):
    """Theme customization form"""
    site_name = StringField('Nom du site', validators=[DataRequired(), Length(max=200)])
    primary_color = StringField('Couleur primaire', validators=[
        DataRequired(),
        Regexp(r'^#[0-9A-Fa-f]{6}$', message='Format: #RRGGBB')
    ])
    secondary_color = StringField('Couleur secondaire', validators=[
        DataRequired(),
        Regexp(r'^#[0-9A-Fa-f]{6}$', message='Format: #RRGGBB')
    ])
    accent_color = StringField('Couleur d\'accent', validators=[
        DataRequired(),
        Regexp(r'^#[0-9A-Fa-f]{6}$', message='Format: #RRGGBB')
    ])
    background_color = StringField('Couleur de fond', validators=[
        DataRequired(),
        Regexp(r'^#[0-9A-Fa-f]{6}$', message='Format: #RRGGBB')
    ])
    text_color = StringField('Couleur du texte', validators=[
        DataRequired(),
        Regexp(r'^#[0-9A-Fa-f]{6}$', message='Format: #RRGGBB')
    ])
    footer_text = TextAreaField('Texte du pied de page', validators=[Optional()])
    submit = SubmitField('Enregistrer')


class UserForm(FlaskForm):
    """User creation/edit form"""
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(max=80)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(),
        Length(min=6, message='Le mot de passe doit contenir au moins 6 caractères')
    ])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(),
        EqualTo('password', message='Les mots de passe ne correspondent pas')
    ])
    is_admin = BooleanField('Administrateur')
    submit = SubmitField('Créer l\'utilisateur')

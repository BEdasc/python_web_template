import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from functools import wraps
from app import db
from app.models import Page, Media, Theme, User
from app.forms import PageForm, MediaUploadForm, ThemeForm, UserForm

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Accès refusé. Vous devez être administrateur.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    pages_count = Page.query.count()
    media_count = Media.query.count()
    users_count = User.query.count()
    recent_pages = Page.query.order_by(Page.updated_at.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                         pages_count=pages_count,
                         media_count=media_count,
                         users_count=users_count,
                         recent_pages=recent_pages)

# Page Management
@bp.route('/pages')
@login_required
@admin_required
def pages():
    """List all pages"""
    all_pages = Page.query.order_by(Page.updated_at.desc()).all()
    return render_template('admin/pages/list.html', pages=all_pages)

@bp.route('/pages/new', methods=['GET', 'POST'])
@login_required
@admin_required
def page_new():
    """Create new page"""
    form = PageForm()
    if form.validate_on_submit():
        page = Page(
            title=form.title.data,
            slug=form.slug.data,
            content=form.content.data,
            is_published=form.is_published.data,
            show_in_menu=form.show_in_menu.data,
            menu_order=form.menu_order.data,
            created_by=current_user
        )
        db.session.add(page)
        db.session.commit()
        flash(f'Page "{page.title}" créée avec succès!', 'success')
        return redirect(url_for('admin.pages'))

    return render_template('admin/pages/form.html', form=form, title='Nouvelle page')

@bp.route('/pages/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def page_edit(id):
    """Edit existing page"""
    page = Page.query.get_or_404(id)
    form = PageForm(obj=page)

    if form.validate_on_submit():
        page.title = form.title.data
        page.slug = form.slug.data
        page.content = form.content.data
        page.is_published = form.is_published.data
        page.show_in_menu = form.show_in_menu.data
        page.menu_order = form.menu_order.data
        page.updated_at = datetime.utcnow()
        db.session.commit()
        flash(f'Page "{page.title}" mise à jour avec succès!', 'success')
        return redirect(url_for('admin.pages'))

    return render_template('admin/pages/form.html', form=form, title='Modifier la page', page=page)

@bp.route('/pages/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def page_delete(id):
    """Delete page"""
    page = Page.query.get_or_404(id)
    title = page.title
    db.session.delete(page)
    db.session.commit()
    flash(f'Page "{title}" supprimée avec succès!', 'success')
    return redirect(url_for('admin.pages'))

# Media Management
@bp.route('/media')
@login_required
@admin_required
def media():
    """List all media files"""
    all_media = Media.query.order_by(Media.uploaded_at.desc()).all()
    return render_template('admin/media/list.html', media_files=all_media)

@bp.route('/media/upload', methods=['GET', 'POST'])
@login_required
@admin_required
def media_upload():
    """Upload new media file"""
    form = MediaUploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)

        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(filename)
        unique_filename = f"{name}_{timestamp}{ext}"

        # Save file
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)

        # Create media record
        media = Media(
            filename=unique_filename,
            original_filename=filename,
            file_path=file_path,
            file_type=form.file_type.data,
            mime_type=file.content_type,
            file_size=os.path.getsize(file_path),
            alt_text=form.alt_text.data,
            uploaded_by=current_user
        )
        db.session.add(media)
        db.session.commit()
        flash(f'Fichier "{filename}" téléchargé avec succès!', 'success')
        return redirect(url_for('admin.media'))

    return render_template('admin/media/upload.html', form=form)

@bp.route('/media/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def media_delete(id):
    """Delete media file"""
    media = Media.query.get_or_404(id)
    filename = media.original_filename

    # Delete file from filesystem
    try:
        if os.path.exists(media.file_path):
            os.remove(media.file_path)
    except Exception as e:
        flash(f'Erreur lors de la suppression du fichier: {e}', 'danger')

    db.session.delete(media)
    db.session.commit()
    flash(f'Fichier "{filename}" supprimé avec succès!', 'success')
    return redirect(url_for('admin.media'))

# Theme Management
@bp.route('/theme', methods=['GET', 'POST'])
@login_required
@admin_required
def theme():
    """Edit theme settings"""
    theme = Theme.query.first()
    if not theme:
        theme = Theme()
        db.session.add(theme)
        db.session.commit()

    form = ThemeForm(obj=theme)

    if form.validate_on_submit():
        theme.site_name = form.site_name.data
        theme.primary_color = form.primary_color.data
        theme.secondary_color = form.secondary_color.data
        theme.accent_color = form.accent_color.data
        theme.background_color = form.background_color.data
        theme.text_color = form.text_color.data
        theme.footer_text = form.footer_text.data
        theme.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Thème mis à jour avec succès!', 'success')
        return redirect(url_for('admin.theme'))

    # Get all media for logo selection
    all_media = Media.query.all()
    return render_template('admin/theme.html', form=form, theme=theme, all_media=all_media)

@bp.route('/theme/logo/<int:media_id>', methods=['POST'])
@login_required
@admin_required
def theme_set_logo(media_id):
    """Set logo for theme"""
    theme = Theme.query.first()
    if not theme:
        theme = Theme()
        db.session.add(theme)

    media = Media.query.get_or_404(media_id)
    theme.logo_id = media_id
    db.session.commit()
    flash('Logo mis à jour avec succès!', 'success')
    return redirect(url_for('admin.theme'))

@bp.route('/theme/favicon/<int:media_id>', methods=['POST'])
@login_required
@admin_required
def theme_set_favicon(media_id):
    """Set favicon for theme"""
    theme = Theme.query.first()
    if not theme:
        theme = Theme()
        db.session.add(theme)

    media = Media.query.get_or_404(media_id)
    theme.favicon_id = media_id
    db.session.commit()
    flash('Favicon mis à jour avec succès!', 'success')
    return redirect(url_for('admin.theme'))

# User Management
@bp.route('/users')
@login_required
@admin_required
def users():
    """List all users"""
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users/list.html', users=all_users)

@bp.route('/users/new', methods=['GET', 'POST'])
@login_required
@admin_required
def user_new():
    """Create new user"""
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            is_admin=form.is_admin.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Utilisateur "{user.username}" créé avec succès!', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/users/form.html', form=form, title='Nouvel utilisateur')

@bp.route('/users/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def user_delete(id):
    """Delete user"""
    if id == current_user.id:
        flash('Vous ne pouvez pas supprimer votre propre compte!', 'danger')
        return redirect(url_for('admin.users'))

    user = User.query.get_or_404(id)
    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f'Utilisateur "{username}" supprimé avec succès!', 'success')
    return redirect(url_for('admin.users'))

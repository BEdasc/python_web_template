from flask import Blueprint, render_template, abort
from app.models import Page, Theme

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Homepage"""
    theme = Theme.query.first()
    home_page = Page.query.filter_by(slug='home', is_published=True).first()
    menu_pages = Page.query.filter_by(show_in_menu=True, is_published=True).order_by(Page.menu_order).all()

    return render_template('pages/index.html',
                         page=home_page,
                         theme=theme,
                         menu_pages=menu_pages)

@bp.route('/page/<slug>')
def page(slug):
    """Dynamic page view"""
    page = Page.query.filter_by(slug=slug, is_published=True).first_or_404()
    theme = Theme.query.first()
    menu_pages = Page.query.filter_by(show_in_menu=True, is_published=True).order_by(Page.menu_order).all()

    return render_template('pages/view.html',
                         page=page,
                         theme=theme,
                         menu_pages=menu_pages)

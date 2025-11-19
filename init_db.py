#!/usr/bin/env python3
"""
Initialize the database with sample data
"""
from app import create_app, db
from app.models import User, Page, Theme

def init_database():
    """Initialize database with sample data"""
    app = create_app()

    with app.app_context():
        # Drop all tables and recreate
        print("Dropping existing tables...")
        db.drop_all()

        print("Creating new tables...")
        db.create_all()

        # Create admin user
        print("Creating admin user...")
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # Create default theme
        print("Creating default theme...")
        theme = Theme(
            site_name='Mon Site Web',
            primary_color='#007bff',
            secondary_color='#6c757d',
            accent_color='#28a745',
            background_color='#ffffff',
            text_color='#212529',
            footer_text='© 2024 Mon Site Web. Tous droits réservés.'
        )
        db.session.add(theme)

        # Create sample pages
        print("Creating sample pages...")

        home_page = Page(
            title='Accueil',
            slug='home',
            content='''
                <h2>Bienvenue sur notre site web!</h2>
                <p>Ceci est la page d'accueil de votre nouveau site web géré par un CMS moderne.</p>
                <p>Vous pouvez modifier ce contenu et personnaliser votre site depuis le panneau d'administration.</p>
                <h3>Fonctionnalités principales</h3>
                <ul>
                    <li>Gestion de pages dynamiques</li>
                    <li>Médiathèque pour vos images et logos</li>
                    <li>Personnalisation complète des couleurs</li>
                    <li>Interface d'administration intuitive</li>
                </ul>
            ''',
            is_published=True,
            show_in_menu=True,
            menu_order=0,
            created_by=admin
        )
        db.session.add(home_page)

        about_page = Page(
            title='À propos',
            slug='a-propos',
            content='''
                <h2>À propos de nous</h2>
                <p>Cette page présente votre entreprise ou votre projet.</p>
                <p>Personnalisez ce contenu selon vos besoins depuis le panneau d'administration.</p>
                <h3>Notre mission</h3>
                <p>Fournir un template de site web moderne et facilement personnalisable.</p>
            ''',
            is_published=True,
            show_in_menu=True,
            menu_order=1,
            created_by=admin
        )
        db.session.add(about_page)

        contact_page = Page(
            title='Contact',
            slug='contact',
            content='''
                <h2>Nous contacter</h2>
                <p>N'hésitez pas à nous contacter pour toute question.</p>
                <div class="row mt-4">
                    <div class="col-md-6">
                        <h4>Informations de contact</h4>
                        <p>
                            <strong>Email:</strong> contact@example.com<br>
                            <strong>Téléphone:</strong> +33 1 23 45 67 89<br>
                            <strong>Adresse:</strong> 123 Rue Example, 75001 Paris
                        </p>
                    </div>
                    <div class="col-md-6">
                        <h4>Horaires</h4>
                        <p>
                            Lundi - Vendredi: 9h00 - 18h00<br>
                            Samedi: 10h00 - 16h00<br>
                            Dimanche: Fermé
                        </p>
                    </div>
                </div>
            ''',
            is_published=True,
            show_in_menu=True,
            menu_order=2,
            created_by=admin
        )
        db.session.add(contact_page)

        # Commit all changes
        db.session.commit()

        print("\n" + "="*50)
        print("Database initialized successfully!")
        print("="*50)
        print("\nDefault credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nIMPORTANT: Change the admin password after first login!")
        print("="*50)

if __name__ == '__main__':
    init_database()

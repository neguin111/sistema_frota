import os
from flask import Flask, redirect, url_for
from app.models import db

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    app = Flask(
        __name__, 
        template_folder=os.path.join(base_dir, 'app', 'templates'),
        static_folder=os.path.join(base_dir, 'app', 'static')
    )
    
    app.config['SECRET_KEY'] = 'chave_secreta_frota_2026'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(base_dir, 'frota.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    @app.route('/')
    def index():
        return redirect(url_for('main.listar_veiculos'))

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
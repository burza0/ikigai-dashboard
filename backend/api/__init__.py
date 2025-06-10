# IKIGAI Dashboard API Module Init v2.0.0
from .zawodnicy import zawodnicy_bp
from .qr_generation import qr_generation_bp
from .centrum_startu import centrum_startu_bp
from .orders import orders_bp
from .products import products_bp

def init_app(app):
    app.register_blueprint(zawodnicy_bp)
    app.register_blueprint(qr_generation_bp)
    app.register_blueprint(centrum_startu_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(products_bp)
    print("✅ IKIGAI v2.0.0 blueprinty zarejestrowane")
    return app
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    flash
)
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from faker import Faker
from models import (
    db,
    User,
    Product,
    Cart,
    Order,
    OrderItem,
    Review
)
import random
import uuid
# =====================================================
# APP CONFIG
# =====================================================
app = Flask(__name__)
app.config["SECRET_KEY"] = "shopsphere_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///marketplace.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
# =====================================================
# LOGIN MANAGER
# =====================================================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"
fake = Faker()
# =====================================================
# USER LOADER
# =====================================================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# =====================================================
# DATABASE + DUMMY DATA
# =====================================================
def create_dummy_data():
    if Product.query.count() > 0:
        return
    print("Creating dummy marketplace data...")
    # ---------------------------------
    # Vendors
    # ---------------------------------
    vendors = []
    for i in range(5):
        vendor = User(
            name=f"Vendor {i+1}",
            email=f"vendor{i+1}@shopsphere.com",
            password=generate_password_hash(
                "123456"
            ),
            role="vendor"
        )
        db.session.add(vendor)
        vendors.append(vendor)
    # ---------------------------------
    # Customers
    # ---------------------------------
    for i in range(20):
        customer = User(
            name=fake.name(),
            email=f"user{i+1}@mail.com",
            password=generate_password_hash(
                "123456"
            ),
            role="customer"
        )
        db.session.add(customer)
    db.session.commit()
    vendors = User.query.filter_by(
        role="vendor"
    ).all()
    categories = [

        "Electronics",
        "Fashion",
        "Books",
        "Home",
        "Sports",
        "Beauty"
    ]
    # ---------------------------------
    # 1000 Products
    # ---------------------------------
    for i in range(1000):
        product = Product(
            name=fake.catch_phrase(),
            description=fake.text(
                max_nb_chars=400
            ),
            category=random.choice(
                categories
            ),
            price=round(
                random.uniform(
                    100,
                    50000
                ),
                2
            ),
            stock=random.randint(
                1,
                200
            ),
            image_url=
            f"https://picsum.photos/400/300?random={i}",
            vendor_id=random.choice(
                vendors
            ).id
        )
        db.session.add(product)
        if i % 100 == 0:
            db.session.commit()
    db.session.commit()
    print("1000 products created successfully")
# =====================================================
# INITIALIZE DATABASE
# =====================================================
with app.app_context():
    db.create_all()
    create_dummy_data()
# =====================================================
# HOME
# =====================================================
@app.route("/")
def home():
    return redirect(
        url_for("login")
    )
# =====================================================
# REGISTER
# =====================================================
@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get(
            "password"
        )
        role = request.form.get("role")
        existing_user = User.query.filter_by(
            email=email
        ).first()
        if existing_user:
            flash(
                "Email already exists",
                "danger"
            )
            return redirect(
                url_for("register")
            )
        user = User(
            name=name,
            email=email,
            password=
            generate_password_hash(
                password
            ),
            role=role
        )
        db.session.add(user)
        db.session.commit()
        flash(
            "Registration successful",
            "success"
        )
        return redirect(
            url_for("login")
        )
    return render_template(
        "register.html"
    )
# =====================================================
# LOGIN
# =====================================================
@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():
    if request.method == "POST":
        email = request.form.get(
            "email"
        )
        password = request.form.get(
            "password"
        )
        user = User.query.filter_by(
            email=email
        ).first()
        if (
            user and
            check_password_hash(
                user.password,
                password
            )
        ):
            login_user(user)
            flash(
                "Login Successful",
                "success"
            )
            return redirect(
                url_for(
                    "dashboard"
                )
            )
        flash(
            "Invalid Email or Password",
            "danger"
        )
    return render_template(
        "login.html"
    )
# =====================================================
# LOGOUT
# =====================================================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(
        "Logged out successfully",
        "info"
    )
    return redirect(
        url_for("login")
    )
# =====================================================
# DASHBOARD
# =====================================================
@app.route("/dashboard")
@login_required
def dashboard():
    products = Product.query.order_by(
        Product.id.desc()
    ).limit(12).all()
    return render_template(
        "dashboard.html",
        products=products
    )
# =====================================================
# PRODUCTS
# =====================================================
@app.route("/products")
@login_required
def products():
    search = request.args.get(
        "search",
        ""
    )
    products_query = Product.query
    if search:
        products_query = (
            products_query.filter(
                Product.name.contains(
                    search
                )
            )
        )
    all_products = (
        products_query
        .order_by(
            Product.id.desc()
        )
        .all()
    )
    return render_template(
        "products.html",
        products=all_products
    )
# =====================================================
# PRODUCT DETAILS
# =====================================================
@app.route(
    "/product/<int:product_id>"
)
@login_required
def product_details(product_id):
    product = Product.query.get_or_404(
        product_id
    )
    reviews = Review.query.filter_by(
        product_id=product.id
    ).all()
    return render_template(
        "product_details.html",
        product=product,
        reviews=reviews
    )
# =====================================================
# ADD TO CART
# =====================================================
@app.route(
    "/add_to_cart/<int:product_id>"
)
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(
        product_id
    )
    cart_item = Cart.query.filter_by(
        user_id=current_user.id,
        product_id=product.id
    ).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(
            user_id=current_user.id,
            product_id=product.id,
            quantity=1
        )
        db.session.add(cart_item)
    db.session.commit()
    flash(
        "Product added to cart",
        "success"
    )
    return redirect(
        url_for(
            "product_details",
            product_id=product.id
        )
    )
# =====================================================
# CART
# =====================================================
@app.route("/cart")
@login_required
def cart():
    cart_items = Cart.query.filter_by(
        user_id=current_user.id
    ).all()
    total = 0
    for item in cart_items:
        total += item.subtotal()
    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=round(total, 2)
    )
# =====================================================
# REMOVE CART ITEM
# =====================================================
@app.route(
    "/remove_cart/<int:item_id>"
)
@login_required
def remove_cart(item_id):
    item = Cart.query.get_or_404(
        item_id
    )
    if item.user_id != current_user.id:
        flash(
            "Unauthorized",
            "danger"
        )
        return redirect(
            url_for("cart")
        )
    db.session.delete(item)
    db.session.commit()
    flash(
        "Item removed from cart",
        "warning"
    )
    return redirect(
        url_for("cart")
    )
# =====================================================
# CHECKOUT
# =====================================================
@app.route("/checkout")
@login_required
def checkout():
    cart_items = Cart.query.filter_by(
        user_id=current_user.id
    ).all()
    if not cart_items:
        flash(
            "Cart is empty",
            "warning"
        )
        return redirect(
            url_for("cart")
        )
    total_amount = 0
    for item in cart_items:
        total_amount += item.subtotal()
    order = Order(
        order_number=
        str(uuid.uuid4())[:8].upper(),
        user_id=current_user.id,
        total_amount=
        round(total_amount, 2),
        status="Processing"
    )
    db.session.add(order)
    db.session.commit()
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.session.add(order_item)
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()
    flash(
        "Order placed successfully",
        "success"
    )
    return redirect(
        url_for("orders")
    )
# =====================================================
# ORDERS
# =====================================================
@app.route("/orders")
@login_required
def orders():

    user_orders = Order.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Order.id.desc()
    ).all()
    return render_template(
        "orders.html",
        orders=user_orders
    )
# =====================================================
# VENDOR DASHBOARD
# =====================================================
@app.route("/vendor_dashboard")
@login_required
def vendor_dashboard():
    if current_user.role != "vendor":
        flash(
            "Vendor access only",
            "danger"
        )
        return redirect(
            url_for("dashboard")
        )
    products = Product.query.filter_by(
        vendor_id=current_user.id
    ).order_by(
        Product.id.desc()
    ).all()
    return render_template(
        "vendor_dashboard.html",
        products=products
    )
# =====================================================
# ADD PRODUCT
# =====================================================
@app.route(
    "/add_product",
    methods=["GET", "POST"]
)
@login_required
def add_product():
    if current_user.role != "vendor":
        flash(
            "Vendor access only",
            "danger"
        )
        return redirect(
            url_for("dashboard")
        )
    if request.method == "POST":
        product = Product(
            name=request.form.get(
                "name"
            ),
            category=request.form.get(
                "category"
            ),
            description=request.form.get(
                "description"
            ),
            price=float(
                request.form.get(
                    "price"
                )
            ),
            stock=int(
                request.form.get(
                    "stock"
                )
            ),
            image_url=request.form.get(
                "image_url"
            ),
            vendor_id=current_user.id
        )
        db.session.add(product)
        db.session.commit()
        flash(
            "Product added successfully",
            "success"
        )
        return redirect(
            url_for(
                "vendor_dashboard"
            )
        )
    return render_template(
        "add_product.html"
    )
# =====================================================
# EDIT PRODUCT
# =====================================================
@app.route(
    "/edit_product/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_product(id):
    product = Product.query.get_or_404(
        id
    )
    if product.vendor_id != current_user.id:
        flash(
            "Unauthorized access",
            "danger"
        )
        return redirect(
            url_for(
                "vendor_dashboard"
            )
        )
    if request.method == "POST":
        product.name = request.form.get(
            "name"
        )
        product.category = request.form.get(
            "category"
        )
        product.description = request.form.get(
            "description"
        )
        product.price = float(
            request.form.get(
                "price"
            )
        )
        product.stock = int(
            request.form.get(
                "stock"
            )
        )
        product.image_url = request.form.get(
            "image_url"
        )
        db.session.commit()
        flash(
            "Product updated successfully",
            "success"
        )
        return redirect(
            url_for(
                "vendor_dashboard"
            )
        )
    return render_template(
        "edit_product.html",
        product=product
    )
# =====================================================
# DELETE PRODUCT
# =====================================================
@app.route(
    "/delete_product/<int:id>"
)
@login_required
def delete_product(id):
    product = Product.query.get_or_404(
        id
    )
    if product.vendor_id != current_user.id:
        flash(
            "Unauthorized access",
            "danger"
        )
        return redirect(
            url_for(
                "vendor_dashboard"
            )
        )
    db.session.delete(product)
    db.session.commit()
    flash(
        "Product deleted successfully",
        "success"
    )
    return redirect(
        url_for(
            "vendor_dashboard"
        )
    )
# =====================================================
# ADD REVIEW
# =====================================================
@app.route(
    "/add_review/<int:product_id>",
    methods=["POST"]
)
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(
        product_id
    )
    rating = int(
        request.form.get(
            "rating"
        )
    )
    comment = request.form.get(
        "comment"
    )
    review = Review(
        user_id=current_user.id,
        product_id=product.id,
        rating=rating,
        comment=comment
    )
    db.session.add(review)
    db.session.commit()
    reviews = Review.query.filter_by(
        product_id=product.id
    ).all()
    total_rating = sum(
        r.rating for r in reviews
    )
    product.average_rating = round(
        total_rating / len(reviews),
        1
    )
    product.total_reviews = len(
        reviews
    )
    db.session.commit()
    flash(
        "Review added successfully",
        "success"
    )
    return redirect(
        url_for(
            "product_details",
            product_id=product.id
        )
    )
# =====================================================
# ERROR HANDLERS
# =====================================================
@app.errorhandler(404)
def not_found(error):
    return (
        "<h2>404 - Page Not Found</h2>",
        404
    )
@app.errorhandler(500)
def internal_error(error):
    return (
        "<h2>500 - Internal Server Error</h2>",
        500
    )
# =====================================================
# RUN APP
# =====================================================
if __name__ == "__main__":

    app.run(
        debug=True
    )
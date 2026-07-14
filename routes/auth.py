from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    current_user
)

from models.user import User

auth = Blueprint(
    "auth",
    __name__
)


# =====================================================
# User Registration
# =====================================================

@auth.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if current_user.is_authenticated:
        return redirect(
            url_for("index")
        )

    if request.method == "POST":

        full_name = request.form.get("full_name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:

            flash(
                "Passwords do not match",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

        existing_user = User.get_by_email(email)

        if existing_user:

            flash(
                "Email already registered",
                "warning"
            )

            return redirect(
                url_for("auth.register")
            )

        User.create(
            full_name,
            username,
            email,
            password
        )

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "register.html"
    )


# =====================================================
# User Login
# =====================================================

@auth.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for("index")
        )

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.get_by_email(email)

        if user and user.check_password(password):

            if user.status == "blocked":

                flash(
                    "Your account has been blocked",
                    "danger"
                )

                return redirect(
                    url_for("auth.login")
                )

            login_user(
                user,
                remember=True
            )

            flash(
                "Login successful",
                "success"
            )

            if user.is_admin():

                return redirect(
                    url_for("admin.dashboard")
                )

            return redirect(
                url_for("user.dashboard")
            )

        flash(
            "Invalid email or password",
            "danger"
        )

    return render_template(
        "login.html"
    )


# =====================================================
# Logout
# =====================================================

@auth.route("/logout")
def logout():

    logout_user()

    flash(
        "You have been logged out",
        "info"
    )

    return redirect(
        url_for("index")
    )


# =====================================================
# Change Password
# =====================================================

@auth.route(
    "/change-password",
    methods=["POST"]
)
def change_password():

    if not current_user.is_authenticated:

        return redirect(
            url_for("auth.login")
        )

    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")

    if not current_user.check_password(old_password):

        flash(
            "Old password incorrect",
            "danger"
        )

        return redirect(
            request.referrer
        )

    current_user.change_password(new_password)

    flash(
        "Password updated successfully",
        "success"
    )

    return redirect(
        request.referrer
    )
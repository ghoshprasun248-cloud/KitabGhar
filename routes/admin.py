from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from functools import wraps


from app import mysql

from models.user import User

from models.book import Book

from models.category import Category





admin = Blueprint(
    "admin",
    __name__
)





# =====================================================
# Admin Access Decorator
# =====================================================

def admin_required(function):


    @wraps(function)

    def wrapper(*args, **kwargs):


        if not current_user.is_authenticated:

            return redirect(

                url_for(
                    "auth.login"
                )

            )



        if not current_user.is_admin():

            flash(

                "Admin access required",

                "danger"

            )


            return redirect(

                url_for(
                    "index"
                )

            )



        return function(
            *args,
            **kwargs
        )


    return wrapper







# =====================================================
# Admin Dashboard
# =====================================================

@admin.route(
    "/"
)

@login_required

@admin_required

def dashboard():


    cursor = mysql.connection.cursor()



    # Total Users

    cursor.execute(

        "SELECT COUNT(*) FROM users"

    )

    users_count = cursor.fetchone()[0]




    # Total Books

    cursor.execute(

        "SELECT COUNT(*) FROM books"

    )

    books_count = cursor.fetchone()[0]




    # Total Downloads

    cursor.execute(

        "SELECT COUNT(*) FROM downloads"

    )

    downloads_count = cursor.fetchone()[0]



    cursor.close()



    return render_template(

        "admin/dashboard.html",

        users_count=users_count,

        books_count=books_count,

        downloads_count=downloads_count

    )








# =====================================================
# Manage Users
# =====================================================

@admin.route(
    "/users"
)

@login_required

@admin_required

def users():


    all_users = User.get_all()



    return render_template(

        "admin/users.html",

        users=all_users

    )








# =====================================================
# Block User
# =====================================================

@admin.route(
    "/users/block/<int:user_id>"
)

@login_required

@admin_required

def block_user(
    user_id
):


    User.change_status(

        user_id,

        "blocked"

    )


    flash(

        "User blocked",

        "success"

    )


    return redirect(

        url_for(
            "admin.users"
        )

    )









# =====================================================
# Activate User
# =====================================================

@admin.route(
    "/users/activate/<int:user_id>"
)

@login_required

@admin_required

def activate_user(
    user_id
):


    User.change_status(

        user_id,

        "active"

    )


    flash(

        "User activated",

        "success"

    )


    return redirect(

        url_for(
            "admin.users"
        )

    )








# =====================================================
# Manage Books
# =====================================================

@admin.route(
    "/books"
)

@login_required

@admin_required

def books():


    cursor = mysql.connection.cursor()



    cursor.execute(

        """

        SELECT

        id,
        title,
        author,
        status,
        created_at


        FROM books


        ORDER BY created_at DESC


        """

    )



    books = cursor.fetchall()



    cursor.close()



    return render_template(

        "admin/books.html",

        books=books

    )









# =====================================================
# Approve Book
# =====================================================

@admin.route(
    "/books/approve/<int:book_id>"
)

@login_required

@admin_required

def approve_book(
    book_id
):


    Book.update_status(

        book_id,

        "approved"

    )


    flash(

        "Book approved",

        "success"

    )


    return redirect(

        url_for(
            "admin.books"
        )

    )








# =====================================================
# Reject Book
# =====================================================

@admin.route(
    "/books/reject/<int:book_id>"
)

@login_required

@admin_required

def reject_book(
    book_id
):


    Book.update_status(

        book_id,

        "rejected"

    )


    flash(

        "Book rejected",

        "warning"

    )


    return redirect(

        url_for(
            "admin.books"
        )

    )









# =====================================================
# Delete Book
# =====================================================

@admin.route(
    "/books/delete/<int:book_id>"
)

@login_required

@admin_required

def delete_book(
    book_id
):


    Book.delete(

        book_id

    )


    flash(

        "Book deleted",

        "success"

    )


    return redirect(

        url_for(
            "admin.books"
        )

    )








# =====================================================
# Categories Management
# =====================================================

@admin.route(
    "/categories"
)

@login_required

@admin_required

def categories():


    categories = Category.get_all()



    return render_template(

        "admin/categories.html",

        categories=categories

    )








# =====================================================
# Add Category
# =====================================================

@admin.route(
    "/categories/add",
    methods=[
        "POST"
    ]
)

@login_required

@admin_required

def add_category():


    name = request.form.get(

        "category_name"

    )


    description = request.form.get(

        "description"

    )



    Category.create(

        name,

        description

    )


    flash(

        "Category added",

        "success"

    )


    return redirect(

        url_for(
            "admin.categories"
        )

    )








# =====================================================
# Delete Category
# =====================================================

@admin.route(
    "/categories/delete/<int:id>"
)

@login_required

@admin_required

def delete_category(
    id
):


    Category.delete(

        id

    )


    flash(

        "Category deleted",

        "success"

    )


    return redirect(

        url_for(
            "admin.categories"
        )

    )
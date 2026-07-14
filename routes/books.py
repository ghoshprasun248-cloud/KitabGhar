from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
    current_app
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import secure_filename

import os


from models.book import Book
from models.category import Category
from models.download import Download



books = Blueprint(
    "books",
    __name__
)





# =====================================================
# View All Books
# =====================================================

@books.route(
    "/"
)

def index():


    all_books = Book.get_all()


    categories = Category.get_all()



    return render_template(

        "books.html",

        books=all_books,

        categories=categories

    )








# =====================================================
# Search Books
# =====================================================

@books.route(
    "/search"
)

def search():


    keyword = request.args.get(

        "q",

        ""

    )



    result = Book.search(

        keyword

    )



    return render_template(

        "books.html",

        books=result

    )








# =====================================================
# Filter By Category
# =====================================================

@books.route(
    "/category/<int:category_id>"
)

def category_books(
    category_id
):


    result = Book.filter_by_category(

        category_id

    )



    return render_template(

        "books.html",

        books=result

    )








# =====================================================
# Book Details
# =====================================================

@books.route(
    "/details/<int:book_id>"
)

def details(
    book_id
):


    book = Book.get_by_id(

        book_id

    )



    if not book:


        flash(

            "Book not found",

            "danger"

        )


        return redirect(

            url_for(
                "books.index"
            )

        )




    return render_template(

        "book_details.html",

        book=book

    )








# =====================================================
# Upload Book
# =====================================================

@books.route(
    "/upload",
    methods=[
        "GET",
        "POST"
    ]
)

@login_required

def upload():



    if request.method == "POST":


        title = request.form.get(

            "title"

        )


        author = request.form.get(

            "author"

        )


        description = request.form.get(

            "description"

        )


        isbn = request.form.get(

            "isbn"

        )


        category_id = request.form.get(

            "category_id"

        )


        price = request.form.get(

            "price",

            0

        )



        cover = request.files.get(

            "cover"

        )


        file = request.files.get(

            "book_file"

        )




        cover_name = None

        file_name = None




        if cover:


            cover_name = secure_filename(

                cover.filename

            )


            cover.save(

                os.path.join(

                    current_app.config[
                        "COVER_UPLOAD_FOLDER"
                    ],

                    cover_name

                )

            )




        if file:


            file_name = secure_filename(

                file.filename

            )


            file.save(

                os.path.join(

                    current_app.config[
                        "BOOK_UPLOAD_FOLDER"
                    ],

                    file_name

                )

            )



        extension = file_name.split(".")[-1]



        Book.create(

            title,

            author,

            description,

            isbn,

            category_id,

            current_user.id,

            cover_name,

            file_name,

            extension,

            price

        )



        flash(

            "Book uploaded successfully. Waiting for approval.",

            "success"

        )



        return redirect(

            url_for(
                "books.index"
            )

        )




    categories = Category.get_all()



    return render_template(

        "upload_book.html",

        categories=categories

    )









# =====================================================
# Download Book
# =====================================================

@books.route(
    "/download/<int:book_id>"
)

@login_required

def download(
    book_id
):


    book = Book.get_by_id(

        book_id

    )



    if not book:


        flash(

            "Book not found",

            "danger"

        )


        return redirect(

            url_for(
                "books.index"
            )

        )




    Download.create(

        current_user.id,

        book_id

    )



    Book.increase_download(

        book_id

    )



    return send_from_directory(

        current_app.config[
            "BOOK_UPLOAD_FOLDER"
        ],

        book.book_file,

        as_attachment=True

    )








# =====================================================
# Preview Book
# =====================================================

@books.route(
    "/preview/<int:book_id>"
)

def preview(
    book_id
):


    book = Book.get_by_id(

        book_id

    )



    if not book:


        flash(

            "Book not found",

            "danger"

        )


        return redirect(

            url_for(
                "books.index"
            )

        )



    return render_template(

        "book_reader.html",

        book=book

    )








# =====================================================
# Add Review
# =====================================================

@books.route(
    "/review/<int:book_id>",
    methods=["POST"]
)

@login_required

def review(
    book_id
):


    rating = request.form.get(

        "rating"

    )


    review = request.form.get(

        "review"

    )



    cursor = mysql.connection.cursor()



    cursor.execute(

        """

        INSERT INTO reviews

        (
            user_id,

            book_id,

            rating,

            review

        )

        VALUES

        (
            %s,%s,%s,%s
        )

        """,

        (

            current_user.id,

            book_id,

            rating,

            review

        )

    )



    mysql.connection.commit()



    cursor.close()



    Book.update_rating(

        book_id

    )



    flash(

        "Review added",

        "success"

    )



    return redirect(

        url_for(

            "books.details",

            book_id=book_id

        )

    )
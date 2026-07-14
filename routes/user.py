from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import secure_filename

import os


from app import mysql

from models.download import Download

from models.book import Book



user = Blueprint(
    "user",
    __name__
)





# =====================================================
# User Dashboard
# =====================================================

@user.route(
    "/dashboard"
)

@login_required

def dashboard():


    downloads = Download.get_user_downloads(

        current_user.id

    )


    return render_template(

        "dashboard.html",

        downloads=downloads

    )








# =====================================================
# User Profile
# =====================================================

@user.route(
    "/profile"
)

@login_required

def profile():


    return render_template(

        "profile.html",

        user=current_user

    )








# =====================================================
# Update Profile
# =====================================================

@user.route(
    "/profile/update",
    methods=[
        "POST"
    ]
)

@login_required

def update_profile():


    username = request.form.get(

        "username"

    )


    email = request.form.get(

        "email"

    )



    current_user.update_profile(

        username,

        email

    )



    flash(

        "Profile updated successfully",

        "success"

    )


    return redirect(

        url_for(
            "user.profile"
        )

    )









# =====================================================
# Upload Profile Image
# =====================================================

@user.route(
    "/profile/image",
    methods=[
        "POST"
    ]
)

@login_required

def update_image():


    image = request.files.get(

        "profile_image"

    )



    if image:


        filename = secure_filename(

            image.filename

        )



        path = os.path.join(

            current_app.config[
                "UPLOAD_FOLDER"
            ],

            filename

        )



        image.save(

            path

        )



        current_user.update_profile_image(

            filename

        )



        flash(

            "Profile image updated",

            "success"

        )



    return redirect(

        url_for(
            "user.profile"
        )

    )








# =====================================================
# Reading Progress Save
# =====================================================

@user.route(
    "/reading-progress",
    methods=[
        "POST"
    ]
)

@login_required

def save_progress():


    book_id = request.form.get(

        "book_id"

    )


    page = request.form.get(

        "page"

    )


    percentage = request.form.get(

        "percentage"

    )



    cursor = mysql.connection.cursor()



    cursor.execute(

        """

        INSERT INTO reading_progress

        (

            user_id,

            book_id,

            current_page,

            progress_percentage

        )


        VALUES

        (

            %s,%s,%s,%s

        )


        ON DUPLICATE KEY UPDATE


        current_page=%s,

        progress_percentage=%s


        """,

        (

            current_user.id,

            book_id,

            page,

            percentage,

            page,

            percentage

        )

    )



    mysql.connection.commit()



    cursor.close()



    return {

        "status":"success"

    }









# =====================================================
# Reading History
# =====================================================

@user.route(
    "/history"
)

@login_required

def history():


    downloads = Download.get_user_downloads(

        current_user.id

    )



    return render_template(

        "dashboard.html",

        downloads=downloads

    )








# =====================================================
# User Notifications
# =====================================================

@user.route(
    "/notifications"
)

@login_required

def notifications():


    cursor = mysql.connection.cursor()



    cursor.execute(

        """

        SELECT

        id,

        title,

        message,

        is_read,

        created_at


        FROM notifications


        WHERE user_id=%s


        ORDER BY created_at DESC


        """,

        (

            current_user.id,

        )

    )



    notifications = cursor.fetchall()



    cursor.close()



    return render_template(

        "dashboard.html",

        notifications=notifications

    )








# =====================================================
# Mark Notification Read
# =====================================================

@user.route(
    "/notification/read/<int:id>"
)

@login_required

def mark_read(
    id
):


    cursor = mysql.connection.cursor()



    cursor.execute(

        """

        UPDATE notifications


        SET is_read=TRUE


        WHERE id=%s


        """,

        (

            id,

        )

    )



    mysql.connection.commit()



    cursor.close()



    return redirect(

        url_for(

            "user.notifications"

        )

    )
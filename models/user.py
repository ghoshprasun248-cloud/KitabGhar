from flask_login import UserMixin
from app import mysql, bcrypt
from datetime import datetime



class User(UserMixin):

    def __init__(
        self,
        id,
        username,
        email,
        password=None,
        profile_image=None,
        role="user",
        status="active",
        created_at=None
    ):

        self.id = id

        self.username = username

        self.email = email

        self.password = password

        self.profile_image = profile_image

        self.role = role

        self.status = status

        self.created_at = created_at




    # =====================================================
    # Create New User
    # =====================================================

    @staticmethod
    def create(
        full_name,
        username,
        email,
        password
    ):

        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        cursor = mysql.connection.cursor()

        query = """
        INSERT INTO users
        (
            full_name,
            username,
            email,
            password
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
        """

        cursor.execute(
            query,
            (
                full_name,
                username,
                email,
                hashed_password
            )
        )

        mysql.connection.commit()

        user_id = cursor.lastrowid

        cursor.close()

        return User.get_by_id(
            user_id
        )




    # =====================================================
    # Get User By ID
    # =====================================================

    @staticmethod
    def get_by_id(
        user_id
    ):

        cursor = mysql.connection.cursor()


        cursor.execute(
            """
            SELECT
            id,
            username,
            email,
            password,
            profile_image,
            role,
            status,
            created_at

            FROM users

            WHERE id=%s
            """,
            (
                user_id,
            )
        )


        data = cursor.fetchone()


        cursor.close()



        if data:

            return User(

                id=data[0],

                username=data[1],

                email=data[2],

                password=data[3],

                profile_image=data[4],

                role=data[5],

                status=data[6],

                created_at=data[7]

            )


        return None





    # =====================================================
    # Get User By Email
    # =====================================================

    @staticmethod
    def get_by_email(
        email
    ):

        cursor = mysql.connection.cursor()


        cursor.execute(

            """
            SELECT
            id,
            username,
            email,
            password,
            profile_image,
            role,
            status,
            created_at

            FROM users

            WHERE email=%s
            """,

            (
                email,
            )

        )


        data = cursor.fetchone()


        cursor.close()



        if data:

            return User(

                id=data[0],

                username=data[1],

                email=data[2],

                password=data[3],

                profile_image=data[4],

                role=data[5],

                status=data[6],

                created_at=data[7]

            )


        return None





    # =====================================================
    # Verify Password
    # =====================================================

    def check_password(
        self,
        password
    ):

        return bcrypt.check_password_hash(

            self.password,

            password

        )





    # =====================================================
    # Update Profile
    # =====================================================

    def update_profile(
        self,
        username,
        email
    ):

        cursor = mysql.connection.cursor()


        cursor.execute(

            """
            UPDATE users

            SET
            username=%s,
            email=%s

            WHERE id=%s
            """,

            (
                username,
                email,
                self.id
            )

        )


        mysql.connection.commit()


        cursor.close()





    # =====================================================
    # Change Password
    # =====================================================

    def change_password(
        self,
        new_password
    ):


        hashed_password = bcrypt.generate_password_hash(

            new_password

        ).decode("utf-8")



        cursor = mysql.connection.cursor()



        cursor.execute(

            """
            UPDATE users

            SET password=%s

            WHERE id=%s
            """,

            (
                hashed_password,
                self.id
            )

        )


        mysql.connection.commit()


        cursor.close()






    # =====================================================
    # Upload Profile Image
    # =====================================================

    def update_profile_image(
        self,
        image_name
    ):

        cursor = mysql.connection.cursor()


        cursor.execute(

            """
            UPDATE users

            SET profile_image=%s

            WHERE id=%s

            """,

            (
                image_name,
                self.id
            )

        )


        mysql.connection.commit()


        cursor.close()






    # =====================================================
    # Admin Check
    # =====================================================

    def is_admin(
        self
    ):

        return self.role == "admin"





    # =====================================================
    # Get All Users (Admin)
    # =====================================================

    @staticmethod
    def get_all():


        cursor = mysql.connection.cursor()


        cursor.execute(

            """
            SELECT
            id,
            username,
            email,
            profile_image,
            role,
            status,
            created_at

            FROM users

            ORDER BY created_at DESC

            """

        )


        users = cursor.fetchall()


        cursor.close()



        result = []


        for user in users:

            result.append(

                User(

                    id=user[0],

                    username=user[1],

                    email=user[2],

                    profile_image=user[3],

                    role=user[4],

                    status=user[5],

                    created_at=user[6]

                )

            )


        return result





    # =====================================================
    # Block / Activate User
    # =====================================================

    @staticmethod
    def change_status(
        user_id,
        status
    ):

        cursor = mysql.connection.cursor()


        cursor.execute(

            """
            UPDATE users

            SET status=%s

            WHERE id=%s

            """,

            (
                status,
                user_id
            )

        )


        mysql.connection.commit()


        cursor.close()
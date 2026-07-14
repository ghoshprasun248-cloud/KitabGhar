from app import mysql
from datetime import datetime



class Category:


    def __init__(
        self,
        id,
        category_name,
        description=None,
        created_at=None
    ):

        self.id = id

        self.category_name = category_name

        self.description = description

        self.created_at = created_at





    # =====================================================
    # Create Category
    # =====================================================

    @staticmethod
    def create(
        category_name,
        description
    ):


        cursor = mysql.connection.cursor()



        cursor.execute(

            """

            INSERT INTO categories

            (
                category_name,
                description
            )

            VALUES

            (
                %s,
                %s
            )

            """,

            (

                category_name,

                description

            )

        )



        mysql.connection.commit()



        category_id = cursor.lastrowid



        cursor.close()



        return Category.get_by_id(
            category_id
        )







    # =====================================================
    # Get Category By ID
    # =====================================================

    @staticmethod
    def get_by_id(
        category_id
    ):


        cursor = mysql.connection.cursor()



        cursor.execute(

            """

            SELECT

            id,
            category_name,
            description,
            created_at


            FROM categories


            WHERE id=%s


            """,

            (

                category_id,

            )

        )


        data = cursor.fetchone()



        cursor.close()




        if data:


            return Category(

                id=data[0],

                category_name=data[1],

                description=data[2],

                created_at=data[3]

            )


        return None






    # =====================================================
    # Get All Categories
    # =====================================================

    @staticmethod
    def get_all():


        cursor = mysql.connection.cursor()



        cursor.execute(

            """

            SELECT

            id,
            category_name,
            description,
            created_at


            FROM categories


            ORDER BY category_name ASC


            """

        )


        categories = cursor.fetchall()



        cursor.close()



        result = []



        for category in categories:


            result.append(

                Category(

                    id=category[0],

                    category_name=category[1],

                    description=category[2],

                    created_at=category[3]

                )

            )



        return result






    # =====================================================
    # Update Category
    # =====================================================

    @staticmethod
    def update(
        category_id,
        category_name,
        description
    ):


        cursor = mysql.connection.cursor()



        cursor.execute(

            """

            UPDATE categories


            SET

            category_name=%s,

            description=%s


            WHERE id=%s


            """,

            (

                category_name,

                description,

                category_id

            )

        )



        mysql.connection.commit()



        cursor.close()






    # =====================================================
    # Delete Category
    # =====================================================

    @staticmethod
    def delete(
        category_id
    ):


        cursor = mysql.connection.cursor()



        cursor.execute(

            """

            DELETE FROM categories


            WHERE id=%s


            """,

            (

                category_id,

            )

        )



        mysql.connection.commit()



        cursor.close()






    # =====================================================
    # Search Category
    # =====================================================

    @staticmethod
    def search(
        keyword
    ):


        cursor = mysql.connection.cursor()



        value = "%" + keyword + "%"



        cursor.execute(

            """

            SELECT

            id,
            category_name,
            description,
            created_at


            FROM categories


            WHERE category_name LIKE %s


            """,

            (

                value,

            )

        )



        categories = cursor.fetchall()



        cursor.close()



        result = []



        for category in categories:


            result.append(

                Category(

                    id=category[0],

                    category_name=category[1],

                    description=category[2],

                    created_at=category[3]

                )

            )


        return result





    # =====================================================
    # Count Books In Category
    # =====================================================

    def book_count(
        self
    ):


        cursor = mysql.connection.cursor()



        cursor.execute(

            """

            SELECT COUNT(*)


            FROM books


            WHERE category_id=%s


            """,

            (

                self.id,

            )

        )



        count = cursor.fetchone()[0]



        cursor.close()



        return count
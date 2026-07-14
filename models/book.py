from app import mysql
from datetime import datetime



class Book:


    def __init__(
        self,
        id,
        title,
        author,
        description=None,
        isbn=None,
        category_id=None,
        uploaded_by=None,
        cover_image=None,
        book_file=None,
        file_type="pdf",
        price=0,
        total_downloads=0,
        average_rating=0,
        status="pending",
        created_at=None
    ):

        self.id = id

        self.title = title

        self.author = author

        self.description = description

        self.isbn = isbn

        self.category_id = category_id

        self.uploaded_by = uploaded_by

        self.cover_image = cover_image

        self.book_file = book_file

        self.file_type = file_type

        self.price = price

        self.total_downloads = total_downloads

        self.average_rating = average_rating

        self.status = status

        self.created_at = created_at




    # =====================================================
    # Add New Book
    # =====================================================

    @staticmethod
    def create(
        title,
        author,
        description,
        isbn,
        category_id,
        uploaded_by,
        cover_image,
        book_file,
        file_type,
        price
    ):


        cursor = mysql.connection.cursor()


        query = """

        INSERT INTO books

        (
            title,
            author,
            description,
            isbn,
            category_id,
            uploaded_by,
            cover_image,
            book_file,
            file_type,
            price
        )

        VALUES

        (
            %s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s
        )

        """



        cursor.execute(

            query,

            (

                title,
                author,
                description,
                isbn,
                category_id,
                uploaded_by,
                cover_image,
                book_file,
                file_type,
                price

            )

        )


        mysql.connection.commit()


        book_id = cursor.lastrowid


        cursor.close()



        return Book.get_by_id(
            book_id
        )





    # =====================================================
    # Get Book By ID
    # =====================================================

    @staticmethod
    def get_by_id(
        book_id
    ):


        cursor = mysql.connection.cursor()


        cursor.execute(

            """

            SELECT

            id,
            title,
            author,
            description,
            isbn,
            category_id,
            uploaded_by,
            cover_image,
            book_file,
            file_type,
            price,
            total_downloads,
            average_rating,
            status,
            created_at


            FROM books

            WHERE id=%s


            """,

            (
                book_id,
            )

        )


        data = cursor.fetchone()


        cursor.close()



        if data:


            return Book(

                id=data[0],

                title=data[1],

                author=data[2],

                description=data[3],

                isbn=data[4],

                category_id=data[5],

                uploaded_by=data[6],

                cover_image=data[7],

                book_file=data[8],

                file_type=data[9],

                price=data[10],

                total_downloads=data[11],

                average_rating=data[12],

                status=data[13],

                created_at=data[14]

            )


        return None





    # =====================================================
    # Get All Approved Books
    # =====================================================

    @staticmethod
    def get_all():


        cursor = mysql.connection.cursor()


        cursor.execute(

            """

            SELECT

            id,
            title,
            author,
            description,
            isbn,
            category_id,
            uploaded_by,
            cover_image,
            book_file,
            file_type,
            price,
            total_downloads,
            average_rating,
            status,
            created_at


            FROM books


            WHERE status='approved'


            ORDER BY created_at DESC


            """

        )


        books = cursor.fetchall()


        cursor.close()



        return Book.convert_list(
            books
        )






    # =====================================================
    # Search Books
    # =====================================================

    @staticmethod
    def search(
        keyword
    ):


        cursor = mysql.connection.cursor()


        query = """

        SELECT

        id,
        title,
        author,
        description,
        isbn,
        category_id,
        uploaded_by,
        cover_image,
        book_file,
        file_type,
        price,
        total_downloads,
        average_rating,
        status,
        created_at


        FROM books


        WHERE

        title LIKE %s

        OR

        author LIKE %s


        AND status='approved'


        """



        value = "%" + keyword + "%"



        cursor.execute(

            query,

            (

                value,

                value

            )

        )


        books = cursor.fetchall()


        cursor.close()



        return Book.convert_list(
            books
        )






    # =====================================================
    # Category Filter
    # =====================================================

    @staticmethod
    def filter_by_category(
        category_id
    ):


        cursor = mysql.connection.cursor()


        cursor.execute(

            """

            SELECT

            id,
            title,
            author,
            description,
            isbn,
            category_id,
            uploaded_by,
            cover_image,
            book_file,
            file_type,
            price,
            total_downloads,
            average_rating,
            status,
            created_at


            FROM books


            WHERE category_id=%s

            AND status='approved'


            """,

            (
                category_id,
            )

        )


        books = cursor.fetchall()


        cursor.close()



        return Book.convert_list(
            books
        )







    # =====================================================
    # Increase Download Count
    # =====================================================

    @staticmethod
    def increase_download(
        book_id
    ):


        cursor = mysql.connection.cursor()


        cursor.execute(

            """

            UPDATE books

            SET total_downloads =
            total_downloads + 1


            WHERE id=%s


            """,

            (
                book_id,
            )

        )


        mysql.connection.commit()


        cursor.close()







    # =====================================================
    # Add Rating
    # =====================================================

    @staticmethod
    def update_rating(
        book_id
    ):


        cursor = mysql.connection.cursor()



        cursor.execute(

            """

            UPDATE books

            SET average_rating =

            (

            SELECT AVG(rating)

            FROM reviews

            WHERE book_id=%s

            )


            WHERE id=%s


            """,

            (

                book_id,

                book_id

            )

        )



        mysql.connection.commit()


        cursor.close()







    # =====================================================
    # Admin Approve Book
    # =====================================================

    @staticmethod
    def update_status(
        book_id,
        status
    ):


        cursor = mysql.connection.cursor()


        cursor.execute(

            """

            UPDATE books

            SET status=%s


            WHERE id=%s


            """,

            (

                status,

                book_id

            )

        )


        mysql.connection.commit()


        cursor.close()






    # =====================================================
    # Delete Book
    # =====================================================

    @staticmethod
    def delete(
        book_id
    ):


        cursor = mysql.connection.cursor()


        cursor.execute(

            """

            DELETE FROM books

            WHERE id=%s


            """,

            (
                book_id,
            )

        )


        mysql.connection.commit()


        cursor.close()






    # =====================================================
    # Convert Database Result
    # =====================================================

    @staticmethod
    def convert_list(
        books
    ):


        result = []


        for book in books:


            result.append(

                Book(

                    id=book[0],

                    title=book[1],

                    author=book[2],

                    description=book[3],

                    isbn=book[4],

                    category_id=book[5],

                    uploaded_by=book[6],

                    cover_image=book[7],

                    book_file=book[8],

                    file_type=book[9],

                    price=book[10],

                    total_downloads=book[11],

                    average_rating=book[12],

                    status=book[13],

                    created_at=book[14]

                )

            )


        return result
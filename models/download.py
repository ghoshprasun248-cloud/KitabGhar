from app import mysql
from datetime import datetime



class Download:


    def __init__(
        self,
        id,
        user_id,
        book_id,
        download_date=None
    ):

        self.id = id

        self.user_id = user_id

        self.book_id = book_id

        self.download_date = download_date





    # =====================================================
    # Create Download Record
    # =====================================================

    @staticmethod
    def create(
        user_id,
        book_id
    ):


        cursor = mysql.connection.cursor()



        cursor.execute(

            """

            INSERT INTO downloads

            (

                user_id,

                book_id

            )


            VALUES

            (

                %s,

                %s

            )


            """,

            (

                user_id,

                book_id

            )

        )



        mysql.connection.commit()



        download_id = cursor.lastrowid



        cursor.close()



        return Download.get_by_id(
            download_id
        )







    # =====================================================
    # Get Download By ID
    # =====================================================

    @staticmethod
    def get_by_id(
        download_id
    ):


        cursor = mysql.connection.cursor()



        cursor.execute(

            """

            SELECT

            id,

            user_id,

            book_id,

            download_date


            FROM downloads


            WHERE id=%s


            """,

            (

                download_id,

            )

        )



        data = cursor.fetchone()



        cursor.close()




        if data:


            return Download(

                id=data[0],

                user_id=data[1],

                book_id=data[2],

                download_date=data[3]

            )


        return None







    # =====================================================
    # Get User Download History
    # =====================================================

    @staticmethod
    def get_user_downloads(
        user_id
    ):


        cursor = mysql.connection.cursor()



        cursor.execute(

            """

            SELECT

            d.id,

            d.user_id,

            d.book_id,

            d.download_date


            FROM downloads d


            WHERE d.user_id=%s


            ORDER BY d.download_date DESC


            """,

            (

                user_id,

            )

        )



        downloads = cursor.fetchall()



        cursor.close()



        result = []



        for download in downloads:


            result.append(

                Download(

                    id=download[0],

                    user_id=download[1],

                    book_id=download[2],

                    download_date=download[3]

                )

            )


        return result







    # =====================================================
    # Get Book Download History
    # =====================================================

    @staticmethod
    def get_book_downloads(
        book_id
    ):


        cursor = mysql.connection.cursor()



        cursor.execute(

            """

            SELECT

            id,

            user_id,

            book_id,

            download_date


            FROM downloads


            WHERE book_id=%s


            ORDER BY download_date DESC


            """,

            (

                book_id,

            )

        )



        downloads = cursor.fetchall()



        cursor.close()



        result = []



        for download in downloads:


            result.append(

                Download(

                    id=download[0],

                    user_id=download[1],

                    book_id=download[2],

                    download_date=download[3]

                )

            )


        return result







    # =====================================================
    # Check User Downloaded Book
    # =====================================================

    @staticmethod
    def check_download(
        user_id,
        book_id
    ):


        cursor = mysql.connection.cursor()



        cursor.execute(

            """

            SELECT id


            FROM downloads


            WHERE user_id=%s

            AND book_id=%s


            """,

            (

                user_id,

                book_id

            )

        )



        result = cursor.fetchone()



        cursor.close()



        if result:

            return True



        return False







    # =====================================================
    # Total Downloads Count
    # =====================================================

    @staticmethod
    def total_downloads():

        cursor = mysql.connection.cursor()



        cursor.execute(

            """

            SELECT COUNT(*)


            FROM downloads


            """

        )



        count = cursor.fetchone()[0]



        cursor.close()



        return count







    # =====================================================
    # Monthly Download Statistics
    # =====================================================

    @staticmethod
    def monthly_statistics():


        cursor = mysql.connection.cursor()



        cursor.execute(

            """

            SELECT

            MONTH(download_date),

            COUNT(*)


            FROM downloads


            GROUP BY MONTH(download_date)


            ORDER BY MONTH(download_date)


            """

        )



        data = cursor.fetchall()



        cursor.close()



        return data
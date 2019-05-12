import mysql.connector

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        mydb = mysql.connector.connect(host='SchoolGradeBook.mysql.pythonanywhere-services.com',
                                        user="SchoolGradeBook", passwd="Saibaba123!",
                                        database="SchoolGradeBook$schoolgradebook")
        mycursor = mydb.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = mycursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        mydb.close()
        return user


    @classmethod
    def find_by_id(cls, _id):
        mydb = mysql.connector.connect(host='SchoolGradeBook.mysql.pythonanywhere-services.com',
                                        user="SchoolGradeBook", passwd="Saibaba123!",
                                        database="SchoolGradeBook$schoolgradebook")
        mycursor = mydb.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = mycursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        mydb.close()
        return user


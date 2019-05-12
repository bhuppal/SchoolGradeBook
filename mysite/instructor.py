import mysql.connector

class Instructor:
    TABLE_NAME = 'sgb_Instructor'

    def __init__(self, _id, first_name, last_name, title, position, email, phone, notes, instructor_id):
        self.id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.position = position
        self.email = email
        self.phone = phone
        self.notes = notes
        self.instructor_id = instructor_id

    @classmethod
    def get_all_instructor(cls):
        mydb = mysql.connector.connect(host='SchoolGradeBook.mysql.pythonanywhere-services.com',
                                        user="SchoolGradeBook", passwd="Saibaba123!",
                                        database="SchoolGradeBook$schoolgradebook")
        mycursor = mydb.cursor()
        query = "SELECT * FROM sgb_Instructor"
        result = mycursor.execute(query)
        row = result.fetchall()
        instructors = []
        for row in result:
            instructors.append({'id': row[0], 'first_name': row[1], 'last_name': row[2], 'title': row[3], 'position': row[4], 'email': row[5], 'phone': row[6], 'notes': row[7], 'instructor_id': row[8] })
        mydb.close()

        return {'instructors': instructors}
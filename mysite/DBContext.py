import mysql.connector

mydb = mysql.connector.connect(
  host='SchoolGradeBook.mysql.pythonanywhere-services.com',
  user="SchoolGradeBook",
  passwd="Saibaba123!",
  database="SchoolGradeBook$schoolgradebook"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM sgb_Instructor")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
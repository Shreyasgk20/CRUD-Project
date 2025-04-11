from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Configure MySQL connection
db_config = {
    'host': 'suranardsdemo.cdtqd6jgia7i.ap-south-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'test1234',
    'database': 'mysqldemo'
}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/students')
def students():
    print("view students")
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name, Email, contact_number, section, collage FROM students")
            students = cursor.fetchall()
            for student in students:
                print(student[0], student[1], student[2], student[3], student[4])
    finally:
        connection.close()
    return render_template('view_students.html', students=students)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['Email']
        contact_number = request.form['contact_number']
        section = request.form['section']
        college = request.form['collage']

        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO students (name, Email, contact_number, section, collage) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, email, contact_number, section, college))
            connection.commit()
        finally:
            connection.close()

        return redirect(url_for('students'))
    return render_template('add_student.html')


@app.route('/edit_student/<string:email>', methods=['GET', 'POST'])
def edit_student(email):
    print("edit student::", email)

    connection = pymysql.connect(**db_config)

    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT name, Email, contact_number, section, collage FROM students WHERE Email=%s", (email,))
            student = cursor.fetchone()

        return render_template('edit_student.html', student=student)

    if request.method == 'POST':
        name = request.form['name']
        contact_number = request.form['contact_number']
        section = request.form['section']
        college = request.form['collage']

        try:
            with connection.cursor() as cursor:
                sql = "UPDATE students SET name=%s, contact_number=%s, section=%s, collage=%s WHERE Email=%s"
                cursor.execute(sql, (name, contact_number, section, college, email))
                connection.commit()
        finally:
            connection.close()

        return redirect(url_for('students'))


@app.route('/delete_student/<string:email>', methods=['GET', 'POST'])
def delete_student(email):
    print("delete student::", email)
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM students WHERE Email=%s", (email,))
            connection.commit()
    finally:
        connection.close()
    return redirect(url_for('students'))


if __name__ == '__main__':
    app.run(debug=True)
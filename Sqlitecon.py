from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    try:
        with sql.connect("Enrollment.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM Student WHERE StdID=?", (id_data,))
            con.commit()
            msg="record is successfully deleted"
    except:
        msg="error in delete operation"
        con.rollback()
    finally:
        return render_template("deleteresult.html", msg = msg)
        con.close()


@app.route('/GetStudentByID/<int:id_data>',methods=['POST', 'GET'])
def GetStudentByID(id_data):
    #flash(id_data)
    con = sql.connect("Enrollment.db")
    con.row_factory = sql.Row
    cur=con.cursor()
    cur.execute("select * from student where stdid=?", (id_data,))
    rows= cur.fetchall();
    #flash (rows)
    return render_template("getstudentbyid.html", rows = rows)


@app.route('/UpdateStudentByID', methods=['POST','GET'])
def UpdateStudentByID():

    if request.method =='GET':

        try:

            stdid = request.args.get('stdid')
            FirstName = request.args.get('FirstName')
            LastName = request.args.get('LastName')
            Address = request.args.get('Address')
            City = request.args.get('City')

            with sql.connect("Enrollment.db") as con:

                cur = con.cursor()
                cur.execute("UPDATE Student SET FirstName=?, LastName=?, Address=?, City=? WHERE StdID=?", \
                            (FirstName, LastName, Address, City, stdid) )
                msg="Data Updated Sucessfully"
                con.commit()

        except:
            msg="error in update operation"
            con.rollback()

        finally:
            return render_template("updateresult.html", msg = msg)


@app.route('/search', methods=['GET', 'POST'])
def search():
    rows = []
    query = ""
    
    if request.method == 'POST':
        query = request.form.get('search_query', '').strip()
        if query:
            try:
                con = sql.connect("Enrollment.db")
                con.row_factory = sql.Row
                cur = con.cursor()
                search_term = f"%{query}%"
                cur.execute("""
                    SELECT * FROM Student 
                    WHERE StdID LIKE ? OR FirstName LIKE ? OR LastName LIKE ?
                """, (search_term, search_term, search_term))
                rows = cur.fetchall()
            except Exception as e:
                print(f"Database error: {e}")
            finally:
                con.close()
                
    return render_template("search.html", rows=rows, query=query)


@app.route('/enternew')
def new_student():
    return render_template('student.html')


@app.route('/addrec', methods=['GET', 'POST'])
def contatct():

    if request.method == 'POST':
        try:
            FirstName = request.form['FirstName']
            LastName = request.form['LastName']
            Address = request.form['Address']
            City = request.form['City']
            if not FirstName or LastName or Address or City:

                with sql.connect("Enrollment.db") as con:
                    cur = con.cursor()
                    cur.execute("insert into Student(FirstName, LastName, Address, City) values(?,?,?,?)", (FirstName, LastName, Address, City))
                    con.commit()
                    msg ="Record successfull added"
                
            else:
                msg="error in insert operation"
                con.rollback()
            
        except:
            msg="error in insert operation"
            con.rollback()

        finally:
            return render_template("addresult.html", msg = msg)
            con.close()

@app.route('/list')
def list():
    con = sql.connect("Enrollment.db")
    con.row_factory = sql.Row
    cur=con.cursor()
    cur.execute("select * from Student")
    rows= cur.fetchall();
    return render_template("list.html", rows= rows)

if __name__ =='__main__':
    app.run(debug = True)
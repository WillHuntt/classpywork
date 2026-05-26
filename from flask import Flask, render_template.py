from flask import Flask, render_template, request, make_response
app= Flask(__name__)

@app.route('/')
def index():
    return render_template('setcookie.html')

@app.route('/setcookie', methods=['POST','GET'])
def setcookie():
    if request.method=='POST':
        username=request.form['nm']
        resp= make_response(render_template('readcookie.html'))
        resp.set_cookie("username",username)

        return resp
    
@app.route('/getcookie')
def getcookie():
    name=request.cookies.get('username')
    age=request.cookies.get('age')
    return f"hello {name}, your age is {age}"

if __name__ == '__main__':
    app.run(debug=True)

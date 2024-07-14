import pandas as pd
from prediction import predict_label
from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)
app.secret_key = 'hii'


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["password"]
        r1 = pd.read_excel('user.xlsx')
        for index, row in r1.iterrows():
            if row["email"] == str(email) and row["password"] == str(pwd):
                name = row['name']
                return redirect(url_for('home'))
        else:
            msg = 'Invalid Login Try Again'
            return render_template('login.html', msg=msg)
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['Email']
        password = request.form['Password']
        sex = request.form['gender']
        age = request.form['age']
        city = request.form['city']
        country = request.form['country']
        number = request.form['number']
        result = 'Not yet tested'
        col_list = ["name", "email", "password", "gender", "age", "city", "country", "ph.no", "result"]
        r1 = pd.read_excel('user.xlsx', usecols=col_list)
        new_row = {'name': name, 'email': email, 'password': password, 'gender': sex, 'age': age, 'city': city, 'country': country, 'ph.no': number, 'result': result}
        r1 = r1.append(new_row, ignore_index=True)
        r1.to_excel('user.xlsx', index=False)
        print("Records created successfully")
        # msg = 'Entered Mail ID Already Existed'
        msg = 'Registration Successful !! U Can login Here !!!'
        return render_template('login.html', msg=msg)
    return render_template('register.html')


@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route("/submit", methods=['GET', 'POST'])
def get_hours():
    if request.method == 'POST':
        file = request.files['audio']
        # _path = "static/input/" + file.filename
        # filename = "inp.avi"
        filename = file.filename
        _path = "static/input/" + filename
        file.save(_path)
        p = predict_label(_path)
        return render_template("home.html", prediction=p[0], acc=p[1], file=file)
    return render_template("home.html")

# @app.route("/submit", methods=['GET', 'POST'])
# def get_hours():
#     if request.method == 'POST':
#         file = request.files['audio']
#         # _path = "static/input/" + file.filename
#         filename = "inp.avi"
#         _path = "static/input/" + filename
#         file.save(_path)
#         p = predict_label(_path)
#         r1 = pd.read_excel('user.xlsx')
#         if len(user_mail) > 0:
#             for index, row in r1.iterrows():
#                 if row["email"] == user_mail and row["name"] == user_name:
#                     r1.replace(to_replace='Not yet tested', value=p[0], inplace=True)
#                     r1.to_excel("user.xlsx", index=False)
#                     print('Test result uploaded successfully')
#             return render_template("home.html", prediction=p[0], acc=p[1], file=file)
#         else:
#             prediction = 'Session Completed Please Login Again'
#             # return render_template("lo.html", prediction=prediction)
#             return render_template("login.html", msg=prediction)


@app.route("/passwordPage", methods=['GET', 'POST'])
def passwordPage():
    return render_template("password.html")


@app.route('/password', methods=['POST', 'GET'])
def password():
    if request.method == 'POST':
        current_pass = request.form['current']
        new_pass = request.form['new']
        verify_pass = request.form['verify']
        r1 = pd.read_excel('user.xlsx')
        if new_pass == verify_pass:
            for index, row in r1.iterrows():
                # if row["email"] == user_mail and row["password"] == str(current_pass):
                if row["password"] == str(current_pass):
                    r1.replace(to_replace=current_pass, value=verify_pass, inplace=True)
                    r1.to_excel("user.xlsx", index=False)
                    msg1 = 'Password changed successfully'
                    return render_template('password.html', msg1=msg1)
            else:
                msg3 = 'Incorrect password'
                return render_template('password.html', msg3=msg3)
        else:
            msg2 = 'Re-entered password is not matched'
            return render_template('password.html', msg2=msg2)
    return render_template('password.html')


@app.route('/graphs', methods=['POST', 'GET'])
def graphs():
    return render_template('graphs.html')


@app.route('/lstm')
def lstm():
    return render_template('lstm.html')


@app.route('/logout')
def logout():
    session.clear()
    msg = 'You are now logged out', 'success'
    return redirect(url_for('login', msg=msg))


if __name__ == '__main__':
    app.run(port=3000, debug=True)

from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
from cmail import sendmail
from otp import genotp
app=Flask(__name__)
app.secret_key = "super secret key"
mydb=mysql.connector.connect(host="localhost",user="root",
password="system",db="blog")
with mysql.connector.connect(host='localhost',user='root',password='system',
db='blog'):
    cursor=mydb.cursor(buffered=True)
    cursor.execute("create table if not exists registration(username varchar(50) primary key,mobile varchar(20) unique,email varchar(50) unique,address varchar(50),password varchar(20))")
@app.route('/',methods=['GET','POST'])
def reg():
    if request.method=='POST':
        username=request.form['username']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        password=request.form['password']
        otp=genotp()
        sendmail(to=email,subject="thanks for registration",body=f'otp is :{otp}')
        return render_template('verification.html',username=username,mobile=mobile,email=email,address=address,password=password,otp=otp)
    return render_template("registration.html")
@app.route('/otp/<username>/<mobile>/<email>/<address>/<password>/<otp>',methods=['GET','POST'])
def otp(username,mobile,email,address,password,otp):
    if request.method=="POST":
        uotp=request.form['uotp']
        if otp==uotp:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into registration values(%s,%s,%s,%s,%s)',[username,mobile,email,address,password])
            mydb.commit()
            cursor.close()
            if data==1:
                session['username']=username
                if not session.get(session['username']):
                    session[session['username']]={}
                return redirect(url_for('login'))
            else:
                return"invalid username and password"
        return render_template("login. html") 
     
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from registration where username=%s && password=%s',[username,password])
        data=cursor.fetchone()[0]
        print(data)
        if data==1:
            session['username']=username
            if not session.get(session['username']):
                session[session['username']]={}
            return redirect(url_for('h'))
        else:
            return 'invald username and password'
            

    return render_template('login.html')
@app.route('/logout')
def logout():
    if session.get('username'):
        session.pop('username')

    return redirect(url_for('login'))


@app.route('/home')
def h():
    return render_template('homepage.html')
 
@app.route('/add_post',methods=['GET','POST'])
def add_post():
    if request.method=="POST":
        title=request.form['title']
        content=request.form['content']
        slug=request.form['slug']
        print(title)
        print(content)
        print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into posts(title,content,slug) values(%s,%s,%s)',(title,content,slug))
        mydb.commit()
        cursor.close()
    return render_template('add_post.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/view_post')
def view_post():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select*from posts')
    posts=cursor.fetchall()
    print(posts)
    cursor.close()
    return render_template('view_post.html',posts=posts )


@app.route('/delete_post/<int:id>',methods=['POST'])
def delete_post(id):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts where id=%s',(id,))
    post=cursor.fetchone()
    cursor.execute('delete from posts where id=%s',(id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('view_post'))

@app.route('/update_post/<int:id>',methods=['GET','POST'])
def update_post(id):
    if request.method=="POST":
        title=request.form['title']
        content=request.form['content']
        slug=request.form['slug']
        print(title)
        print(content)
        print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('update posts set title=%s,content=%s,slug=%s where id=%s',(title,content,slug,id))
        mydb.commit()
        cursor.close()
        return redirect(url_for('view_post'))
    else:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from posts where id=%s',(id,))
        post=cursor.fetchone()
        cursor.close()
        return render_template('update_post.html',post=post )



    


app.run(debug=True,use_reloader=True)
from flask import Flask, render_template,request,redirect,session,flash,url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/career'
db=SQLAlchemy(app)

#Class

class Jobs(db.Model):
    jid=db.Column(db.Integer, primary_key=True)
    Job_Title=db.Column(db.String(40), nullable=False)
    Job_Location=db.Column(db.String(40), nullable=False)
    Salary=db.Column(db.Integer, nullable=False)
    Currency=db.Column(db.String(10), nullable=False)
    Responsibilities=db.Column(db.String(2000), nullable=False)
    Requirements=db.Column(db.String(2000), nullable=False)
    Date_Posted=db.Column(db.DateTime(),nullable=False)

#Class 

class Applications(db.Model):
    uid=db.Column(db.Integer, primary_key=True)
    job_id=db.Column(db.Integer, foriegn_key=True)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    pno=db.Column(db.Integer(),nullable=False)
    quali=db.Column(db.String(30),nullable=False)  
    file=db.Column(db.String(50),nullable=False) 
    Date_Applied=db.Column(db.DateTime(),nullable=False)

#Class

class Query(db.Model):
    qid=db.Column(db.Integer, primary_key=True)
    qname=db.Column(db.String(40),nullable=False)
    qemail=db.Column(db.String(40),nullable=False)
    queries=db.Column(db.String(1000),nullable=False)

class Feedback(db.Model):
    f_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(40),nullable=False)
    email=db.Column(db.String(30),nullable=False)
    message=db.Column(db.String(1000),nullable=False)


@app.route("/")
def home():
    return render_template('home.html')

app.secret_key="login"
@app.route("/login1")
def login1():
    return render_template("login.html")

#Admin Login

@app.route("/login",methods=['POST'])
def login():
    if(request.method=='POST'):
        username=request.form.get('username')
        password=request.form.get('password')
        if (username=='pragati' and password=='abc'):
            session['username']=username
            return redirect("/admin")
        else:
            msg="Invalid username/password"
            return render_template('login.html',msg=msg) 
        
#Admin Panel Page

@app.route("/admin")
def admin():
    return render_template('admin.html')

#Admin Logout

@app.route("/logout")
def logout():
    session.pop('username',None)
    return render_template('home.html')


#Adding new Job Posting

@app.route("/add",methods=['POST','GET'])
def add():
    if('username' in session):
        msg="Job Added Successfully"
        if(request.method=='POST'):
            Job_Title=request.form.get('Job_Title')
            Job_Location=request.form.get('Job_Location')
            Salary=request.form.get('Salary')
            Currency=request.form.get('Currency')
            Responsibilities=request.form.get('Responsibilities')
            Requirements=request.form.get('Requirements')
            entry=Jobs(Job_Title=Job_Title,Job_Location=Job_Location,Salary=Salary,Currency=Currency,Responsibilities=Responsibilities,Requirements=Requirements)
            db.session.add(entry)
            db.session.commit()
            return render_template('admin.html',msg=msg)
        else:
                return render_template('add.html')
    else:
        return render_template('home.html')

#Show jobs to admin 

@app.route("/showj", methods=['POST','GET'])
def showj():
    if('username' in session):
        allproducts=Jobs.query.all()
        return render_template('showjobs.html',allproducts=allproducts)
    else:
        return render_template('home.html')
    
#Deleting Jobs

@app.route('/delete/<int:jid>') 
def delete(jid):
    if ('username' in session):
        user=Jobs.query.filter_by(jid=jid).first()
        db.session.delete(user)
        db.session.commit()
        flash("Deleted Successfully")
        return redirect('/showj')
    else:
        return render_template('home.html')
    
#Showing products to user 

@app.route("/job", methods=['POST','GET'])
def job():
    allproducts=Jobs.query.all()
    return render_template('job.html',allproducts=allproducts)

#Showing Product Details

@app.route('/details/<int:jid>') 
def details(jid):
    user=Jobs.query.filter_by(jid=jid).first()
    return render_template('description.html',user=user)

#Apply for Jobs

@app.route("/apply/<int:jid>")
def apply(jid):
        user=Jobs.query.filter_by(jid=jid).first()
        return render_template('apply.html',user=user)

#filling application form from the user   

@app.route('/submit/<int:jid>',methods=['POST','GET']) 
def submit(jid):
    user=Jobs.query.filter_by(jid=jid).first()
    if(request.method=='POST'):
        job_id=jid
        name=request.form.get('name')
        email=request.form.get('email')
        pno=request.form.get('pno')
        quali=request.form.get('quali')
        f=request.files['file']
        f.save('static/files'+f.filename)
        resume = f.filename
        entry=Applications(name=name,email=email,pno=pno,quali=quali,file=resume,job_id=job_id)
        db.session.add(entry)
        db.session.commit()
    return render_template('submit.html',user=user,name=name)

@app.route("/showa", methods=['POST','GET'])
def showa():
    if('username' in session):
        allproducts=Applications.query.all()
        alljobs=Jobs.query.all()
        return render_template('showappli.html',allproducts=allproducts,alljobs=alljobs)
    else:
        return render_template('home.html')

#Deleting Applications

@app.route('/deletea/<int:uid>') 
def deletea(uid):
    if ('username' in session):
        user=Applications.query.filter_by(uid=uid).first()
        db.session.delete(user)
        db.session.commit()
        flash("Deleted Successfully")
        return redirect('/showa')
    else:
        return render_template('home.html')

#About Us
@app.route("/about")
def about():
    return render_template('aboutus.html')     

#Services
@app.route("/services")   
def services():
    return render_template('sevices.html') 

#Querying
@app.route("/query",methods=['POST','GET'])
def query():
    if(request.method=='POST'):
        qname=request.form.get('qname')
        qemail=request.form.get('qemail')
        queries=request.form.get('queries')
        entry=Query(qname=qname,qemail=qemail,queries=queries)
        db.session.add(entry)
        db.session.commit()
    return render_template('query.html')

#Show Queries
@app.route("/showq", methods=['POST','GET'])
def showq():
    allproducts=Query.query.all()
    return render_template('showq.html',allproducts=allproducts)


#Giving Feedback
@app.route("/feed",methods=['POST','GET'])
def feed():
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        message=request.form.get('message')
        entry=Feedback(name=name,email=email,message=message)
        db.session.add(entry)
        db.session.commit()
    return render_template('feedback.html')


#Show Feedback
@app.route("/feedback", methods=['POST','GET'])
def feedback():
    allproducts=Feedback.query.all()
    return render_template('showf.html')

#Delete Queries

@app.route('/deleteq/<int:qid>') 
def deleteq(qid):
    if ('username' in session):
        user=Query.query.filter_by(qid=qid).first()
        db.session.delete(user)
        db.session.commit()
        flash("Deleted Successfully")
        return redirect('/showq')
    else:
        return render_template('home.html')


#Deleting Feedback
@app.route('/deletef/<int:f_id>') 
def deletef(f_id):
    if ('username' in session):
        user=Feedback.query.filter_by(f_id=f_id).first()
        db.session.delete(user)
        db.session.commit()
        flash("Deleted Successfully")
        return redirect('/showf')
    else:
        return render_template('home.html')



@app.route('/search',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        seach_query= request.form['location']
        locations = Jobs.query.filter(Jobs.Job_Location.ilike(f'%{seach_query}')).all()
        return render_template('search_results.html', locations=locations)
    return render_template('job.html')
app.run(debug = True)

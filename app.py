from flask import Flask, render_template, request,jsonify
from database import load_jobs_from_db, load_job_from_db, add_application_to_db
app = Flask(__name__)

#Routes here#
@app.route('/')
def home():
    jobs= load_jobs_from_db()
    return render_template('home.html',jobs=jobs, company_name='Colltech')
  
@app.route('/jobs')
def list_jobs():
  jobs = load_jobs_from_db()
  return render_template('open_positions.html',
                         jobs=jobs)

@app.route("/job/<id>")
def show_job(id):
  job = load_job_from_db(id)
  if not job:
    return "Not Found", 404
  return render_template('jobpage.html', 
                         job=job)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/signup')
def signup():
  return render_template('signup.html')
  
@app.route('/form/<id>')
def fill_form(id):
  job=load_job_from_db(id)
  return render_template('applicform.html',
                         job=job)


@app.route("/form/<id>/submit",methods=["POST"])
def submit_form(id):
  job= load_job_from_db(id)
  data= request.form
  add_application_to_db(job['id'], data)
  return render_template('submitted.html', 
                         application=data,
                        job=job)
  return render_template('applicsuccess.html')


  

  
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
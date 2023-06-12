from flask import Flask, render_template, request
from database import load_jobs_from_db, load_job_from_db
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


@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/form/<id>')
def fill_form(id):
  job=load_job_from_db(id)
  return render_template('applicform.html',
                         job=job)


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    first_name = request.form.get('fname')
    last_name = request.form.get('lastname')
    country = request.form.get('country')
    email = request.form.get('email')
    resume = request.files.get('resume')
    certificate = request.files.get('certificate')
    
    return 'Form submitted successfully'
  


@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/signup')
def signup():
  return render_template('signup.html')

  
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
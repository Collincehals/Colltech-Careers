from flask import Flask, render_template, request,redirect,url_for

from database import load_jobs_from_db, load_job_from_db, add_application_to_db, add_user_to_db

from email_sender import send_confirmation_email

from sign_up_email import send_registration_email
import os

app = Flask(__name__)
app.secret_key = os.environ['APP.SECRET_KEY']

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
  #EXPERIMENTAL
@app.route('/newlog')
def login_reg():
  return render_template ('imageoverlay.html')
  

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/form/<id>')
def fill_form(id):
  job=load_job_from_db(id)
  return render_template('applicform.html',
                         job=job)


# Form Submission here

import requests

@app.route("/form/<id>/submit", methods=["POST"])
def submit_form(id):
    job = load_job_from_db(id)
    data = request.form
    add_application_to_db(job['id'], data)

    # Get the hCaptcha response from the form submission
    hCaptchaResponse = data.get('h-captcha-response')

    # Verify the hCaptcha response using the hCaptcha API
    verification_data = {
        'secret': os.environ['HCPATCHA_SECRET'],
        'response': hCaptchaResponse
    }
    verification_response = requests.post('https://hcaptcha.com/siteverify', data=verification_data)
    verification_result = verification_response.json()

    # Check if the hCaptcha response is valid
    if verification_result['success']:
        applicant_email = data['email']
        applicant_name = data['firstname']
        last_name = data['lastname']
        country = data['country']
        job_title = job['title']
        send_confirmation_email(job_title, applicant_email, applicant_name, last_name, country)

        return render_template('submitted.html', application=data, job=job)
    else:
        return 'Invalid hCaptcha response. Please try again.'


##Sign_up route here-->
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        add_user_to_db(request.form)
        send_registration_email(first_name, last_name, email,username)
      
        flash('Sign up successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
  
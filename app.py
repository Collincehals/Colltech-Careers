from flask import Flask, render_template, request,redirect,url_for,flash,session

from passlib.hash import bcrypt

from database import load_jobs_from_db, load_job_from_db, add_application_to_db, add_user_to_db, add_employer_to_db, add_subscriber_to_db,add_job_to_db,load_subscribers_from_db,load_users_from_db, load_employers_from_db, add_feedback_to_db, load_feedbacks_from_db, update_subscriber_confirmation_status, generate_confirmation_token

from email_sender import send_confirmation_email

from employer_reg_email import send_employerreg_email

from sign_up_email import send_registration_email

from subscriber_email import send_subscriber_email

from job_notification import send_job_notification

from comment_notification import send_admin_comment_email
import os

app = Flask(__name__)
app.secret_key = os.environ['APP.SECRET_KEY']

# Decorator function to check if the user or employer is logged in
from functools import wraps
def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if 'username' in session:
            return route_function(*args, **kwargs)
        else:
            return redirect('/user-login')
    return wrapper

def employer_login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if 'company_name' in session:
            return route_function(*args, **kwargs)
        else:
            return redirect('/employer-login')
    return wrapper
import math 
#Routes here#
@app.route('/')
def home():
    page = int(request.args.get('page', 1))
    items_per_page = 5 # Number of jobs per page

    all_jobs = load_jobs_from_db()
    total_jobs = len(all_jobs)

    total_pages = math.ceil(total_jobs / items_per_page)

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    jobs = all_jobs[start_index:end_index]
  
    return render_template('home.html',jobs=jobs, company_name='Colltech',page=page, total_pages=total_pages)


@app.route('/jobs')
def list_jobs():
    page = int(request.args.get('page', 1))
    items_per_page = 5 # Number of jobs per page

    all_jobs = load_jobs_from_db()
    total_jobs = len(all_jobs)

    total_pages = math.ceil(total_jobs / items_per_page)

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    jobs = all_jobs[start_index:end_index]

     # Calculate the range of results being displayed
    results_start = start_index + 1
    results_end = min(start_index + items_per_page, total_jobs)

    # Calculate the previous and next page numbers
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    # Calculate the range of page numbers to display
    max_display_pages = 5
    half_max_display_pages = max_display_pages // 2

    if total_pages <= max_display_pages:
        page_nums = range(1, total_pages + 1)
    elif page <= half_max_display_pages:
        page_nums = range(1, max_display_pages + 1)
    elif page >= total_pages - half_max_display_pages:
        page_nums = range(total_pages - max_display_pages + 1, total_pages + 1)
    else:
        page_nums = range(page - half_max_display_pages, page + half_max_display_pages + 1)

    return render_template('open_positions.html', jobs=jobs, page=page, prev_page=prev_page,
                           next_page=next_page, page_nums=page_nums, total_pages=total_pages,  results_start=results_start, results_end=results_end, total_jobs=total_jobs)



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
@app.route('/merged_signup')
def merged_reg():
  return render_template ('merged_regforms.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/int_programs')
def int_programmes():
  return render_template('int_programmes.html')

@app.route('/prof_guidance')
def prof_guidance():
  return render_template('prof_guidance.html')

@app.route('/industry_services')
def industry_services():
  return render_template('industry_services.html')

@app.route('/resume-builder')
def resume_bulder():
  return render_template ('resume_builder.html')

@app.route('/job-posting')
def job_posting():
  return render_template('job_posting.html')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/contact')
def contact_details():
  return render_template('contact.html')

@app.route('/form/<id>')
@login_required
def fill_form(id):
  job=load_job_from_db(id)
  return render_template('applicform.html',
                         job=job,
                         username=session['username'])


# Application Form Submission here
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


#User Sign_up route here-->
@app.route('/user-signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.hash(password)
        confirm_password = request.form['confirm_password']
        
        # Check if username or email already exists in the database
        users = load_users_from_db()
        for user in users:
            if user['username'] == username:
                flash('Username already exists. Please choose a different username!!!', 'error')
                return render_template('signup.html')
            if user['email'] == email:
                flash('Email already exists. Please use a different email !!!', 'error')
                return render_template('signup.html')

        # Check if terms and conditions checkbox is checked
        if 'terms' not in request.form:
            flash('You must accept the terms and conditions to sign up!', 'error')
            return render_template('signup.html')

        # Password validation checks
        if len(password) < 8:
            flash('Password must be at least 8 characters long!', 'error')
            return render_template('signup.html')

        import string
        if not any(char in string.punctuation for char in password):
            flash('Password must contain at least one special character!', 'error')
            return render_template('signup.html')

        if not any(char.isdigit() for char in password):
            flash('Password must contain at least one numeric digit!', 'error')
            return render_template('signup.html')

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('signup.html')
        user_data = {
            'firstname': first_name,
            'lastname': last_name,
            'email': email,
            'username': username,
            'password': hashed_password,
        }
        add_user_to_db(user_data)
        send_registration_email(first_name, last_name, email, username)
        flash('Sign up successful! Please log in.', 'success')
        return redirect(url_for('user_login'))

    return render_template('signup.html')



#Employer Signup here.
@app.route('/employer-signup', methods=['POST', 'GET'])
def employer_signup():
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        company_name = request.form['company_name']
        company_category = request.form['category']
        password = request.form['password']
        hashed_password = bcrypt.hash(password)
        confirm_password = request.form['confirm_password']

        # Check if username or email already exists in the database
        employers = load_employers_from_db()
        for employer in employers:
            if employer['company_name'] == company_name:
                flash('Company already exists. Please choose a different name!!!', 'error')
                return render_template('recruiter_signup.html')

            if employer['email'] == email:
                flash('Email already exists. Please use a different email !!!', 'error')
                return render_template('recruiter_signup.html')

        # Check if terms and conditions checkbox is checked
        if 'terms' not in request.form:
            flash('You must accept the terms and conditions to sign up!', 'error')
            return render_template('recruiter_signup.html')

        # Password validation checks
        if len(password) < 8:
            flash('Password must be at least 8 characters long!', 'error')
            return render_template('recruiter_signup.html')

        import string
        if not any(char in string.punctuation for char in password):
            flash('Password must contain at least one special character!', 'error')
            return render_template('recruiter_signup.html')

        if not any(char.isdigit() for char in password):
            flash('Password must contain at least one numeric digit!', 'error')
            return render_template('recruiter_signup.html')

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('recruiter_signup.html')
        user_data = {
           'firstname': first_name,
           'lastname':  last_name,
           'email': email,
           'company_name': company_name,
           'category': company_category,
           'password' : hashed_password,
        }
        add_employer_to_db(user_data)
        send_employerreg_email(first_name, last_name, email, company_name, company_category)

        flash('Sign up successful! Please log in.', 'success')
        return redirect(url_for('employer_login'))

    return render_template('recruiter_signup.html')

#Subscription to Job Alerts here --->
@app.route('/subscribe', methods=['POST', 'GET'])
def subscription():
    if request.method == 'POST':
        email = request.form['email']
        token = generate_confirmation_token()
        confirmed = False

        subscriber_data = {
            'email': email,
            'token': token,
            'confirmed': confirmed
        }
        add_subscriber_to_db(subscriber_data)

        confirmation_token = token
        confirmation_link = f"https://colltech-careers--collincehals.repl.co/subscription-confirmation/confirm?token={confirmation_token}"
        send_subscriber_email(email, confirmation_link)
        return redirect(url_for('home'))

    return render_template('home.html')

@app.route('/subscription-confirmation/confirm', methods=["GET"])
def subscription_confirmation():
    token = request.args.get('token')
    subscriber_tokens = load_subscribers_from_db()

    for subscriber_token in subscriber_tokens:
        if subscriber_token['token'] == token:
            # Mark the subscriber as confirmed in the database
            subscriber_id = subscriber_token['id']
            update_subscriber_confirmation_status(subscriber_id)
            return "Subscription Confirmation successful!"

    return "Subscription not Successful"


#Job Posting URL here
@app.route('/post-job', methods=['POST', 'GET'])
@employer_login_required
def post_job():
  if request.method  == 'POST':
    title = request.form['title']
    company = request.form['company']
    location = request.form['location']
    currency = request.form['currency']
    salary = request.form['salary']
    data = request.form
    add_job_to_db(data)
    subscribers = load_subscribers_from_db()
    for subscriber in subscribers:
        email = subscriber['email'] 
        send_job_notification(title,company,location,currency,salary,email)
    return redirect(url_for('post_job'))
  return render_template('job_posting.html',company_name=session['company_name'])


@app.route('/merged-login')
def merged_login():
  return render_template('merged_login.html')


#User Login and Logout Routes here
@app.route('/user-dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    else:
        return render_template('merged_login.html')

@app.route('/user-login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users_from_db()
        for user in users:
            hashed_password = user['password']
            if user['username'] == username and bcrypt.verify(password, hashed_password):
                session['username'] = username
                return redirect('user-dashboard')
        flash ('Wrong username or password. Please try again!!!')
        return redirect(url_for('user_login'))
    else:
        return render_template('login.html')

@app.route('/user-logout')
def logout():
    session.pop('username', None)
    return redirect('/')


#Employer Login and Logout Routes here
@app.route('/employer-dashboard')
def employer_dashboard():
    if 'company_name' in session:
        company_name = session['company_name']
        return render_template('employer_dashboard.html', company_name=company_name)
    else:
        return render_template('employer_login.html')

@app.route('/employer-login', methods=['GET', 'POST'])
def employer_login():
    if request.method == 'POST':
        company_name = request.form['company_name']
        password = request.form['password']

        employers = load_employers_from_db()
        for employer in employers:
            hashed_password = employer['password']
            if employer['company_name'] == company_name and bcrypt.verify(password, hashed_password):
                session['company_name'] =company_name
                return redirect('/employer-dashboard')
        flash ('Wrong company name or password. Please try again!!!')
        return redirect(url_for('employer_login'))
    else:
        return render_template('employer_login.html')

@app.route('/employer-logout')
def employer_logout():
    session.pop('company_name', None)
    return redirect('/')


#Feedback Survey Route here--->
@app.route('/user-feedback')
def user_feedback():
  return render_template('user_feedbackform.html')

@app.route('/submitted_feedback', methods=["GET", "POST"])
def feedback_submitted():
  if request.method == "POST":
    firstname = request.form['firstname']
    email = request.form['email']
    experience=request.form['experience']
    listings = request.form['listings']
    suggestions=request.form['suggestions']
    communication = request.form['communication']
    usability=request.form['usability']
    response_time = request.form['response_time']
    add_feedback_to_db(request.form)
    flash('Feedback sent successfully.Thank you!','success')
    return render_template('feedback_page.html',firstname=firstname,email=email,experience=experience,listings=listings, suggestions = suggestions,communication=communication, usability = usability, response_time=response_time)
  return redirect(url_for('user_feedback'))
  
#Load feedback from db
@app.route('/all-feedbacks')
@employer_login_required
def all_feedbacks():
  feedbacks = load_feedbacks_from_db()
  return render_template('all_feedbacks.html',feedbacks=feedbacks)

#Send Comments and Questions to employer email:
@app.route('/comments', methods = ["POST", "GET"])
def comments():
  if request.method == "POST":
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    send_admin_comment_email(name=name,email=email,subject=subject,message=message)
    flash ('Message sent successfully!')
  return redirect(url_for('contact_details'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 
from flask import Flask, render_template, request,redirect,url_for,flash,session, jsonify

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
@app.route('/merged_signup')
def merged_reg():
  return render_template ('merged_regforms.html')

@app.route('/signup')
def sign_up():
  return render_template ('signup.html')

@app.route('/employer_signup')
def employer_signup():
  return render_template ('recruiter_signup.html')


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


@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

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


#Login and Logout Routes here
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check the username and password against your user database
        if username == 'admin' and password == 'password':
            # Successful login
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            # Invalid login
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')
#Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


from bs4 import BeautifulSoup

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        search_results = perform_search(query)
        return jsonify(search_results)
    else:
        return render_template('search.html', search_results=None)  # Pass search_results as None initially

def perform_search(query):
    search_results = []

    # Directory path where your website's HTML files are stored
    html_directory = os.path.join(os.getcwd(), 'templates')

    # Loop through each HTML file in the directory
    for filename in os.listdir(html_directory):
        if filename.endswith('.html'):
            file_path = os.path.join(html_directory, filename)

            # Read the contents of the HTML file
            with open(file_path, 'r') as file:
                html_content = file.read()

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Search for elements containing the query
            matching_elements = soup.find_all(text=lambda text: query.lower() in text.lower())

            # Process the matching elements and prepare them for rendering
            for element in matching_elements:
                # Extract relevant information from the element or its parent elements
                # For example, you can extract the element's text, parent's text, URL, etc.
                element_text = element.strip()
                if query.lower() in element_text.lower():
                    result = {
                        'title': filename,  # Use the filename as the title
                        'description': element_text  # Use the matching element's text as the description
                    }
                    search_results.append(result)

    return search_results


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)






  
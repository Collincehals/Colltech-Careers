from flask import Flask, render_template, request
from database import load_jobs_from_db
app = Flask(__name__)

#Routes here#
@app.route('/')
def home():
    jobs= load_jobs_from_db()
    return render_template('home.html',jobs=jobs, company_name='Colltech')

@app.route('/about/')
def about():
    return render_template('about.html')
  
@app.route('/hover')
def hover():
    return render_template('hover.html')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')
  
  
@app.route('/apply_job', methods=['GET', 'POST'])
def apply_job():
    jobs= load_jobs_from_db()
    if request.method == 'POST':
        name = request.form ['name']
        email =request.form ['email address']
        resume = request.files ['resume']
        import os

        # Create the 'resumes/' directory if it doesn't exist
        if not os.path.exists('resumes/'):
            os.makedirs('resumes/')

        # Save the uploaded resume to a specific location
        resume.save('resumes/' + resume.filename)

        # Perform additional processing or database operations here

        return render_template('applicsuccess.html', jobs=jobs, name=name)
    else:
        return render_template('applicform.html', jobs=jobs)

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



  
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
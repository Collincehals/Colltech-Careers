from flask import Flask, render_template, request

app = Flask(__name__)

# A list to store the job openings
JOBS= [
{
  'id':1,
  'title':"Full-Stack Engineer",
  'location':'Nairobi, Kenya',
  'job requirements': 'Entry Level',
  'Salary':'KShs.59,000'
},
{
  'id':2,
  'title':"Data Analyst",
  'location':'Mombasa, Kenya',
  'job requirements': '5 Years Experience',
  'Salary':'KShs.200,000'
},
{
  'id':3,
  'title':"Structural Engineer",
  'location':'Kisumu, Kenya',
  'job requirements': 'Minimum 3 years experience',
  'Salary':'KShs.158,000'
},
{
  'id':4,
  'title':"Software Engineer",
  'location':'Nairobi, Kenya',
  'job requirements': 'Minimum 10 years Experience',
  'Salary':'KShs.130,000'
},
{
  'id':5,
  'title':"Back-End Engineer",
  'location':'Remote',
  'job requirements': 'Entry Level',
  'Salary':'$59,000'
}
]

@app.route('/')
def home():
    return render_template('home.html',jobs=JOBS, company_name='Colltech')

@app.route('/about/')
def about():
    return render_template('about.html')

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
    job = JOBS
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

        return render_template('applicsuccess.html', job=job, name=name)
    else:
        return render_template('applicform.html', jobs=JOBS)

@app.route('/submit', methods=['POST'])
def submit_form():
    first_name = request.form.get('fname')
    last_name = request.form.get('lastname')
    country = request.form.get('country')
    email = request.form.get('email')
    resume = request.files.get('resume')
    certificate = request.files.get('certificate')
    
    return 'Form submitted successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
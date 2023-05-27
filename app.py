from flask import Flask, render_template, request

app = Flask(__name__)

# A list to store the job openings
JOBS= [
{
  'id':1,
  'title':"Software Engineer",
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
  'title':"Senior HR Practioner",
  'location':'Nairobi, Kenya',
  'job requirements': 'Minimum 10 years Experience',
  'Salary':'KShs.130,000'
},
{
  'id':5,
  'title':"Full-Stack Engineer",
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

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')
  
  
@app.route('/apply_job', methods=['GET', 'POST'])
def apply_job():
    job = JOBS
    if request.method == 'POST':
        name = request.form['name']
        email =request.form['email address']
        resume = request.files['resume']
        import os

        # Create the 'resumes/' directory if it doesn't exist
        if not os.path.exists('resumes/'):
            os.makedirs('resumes/')

        # Save the uploaded resume to a specific location
        resume.save('resumes/' + resume.filename)

        # Perform additional processing or database operations here

        return render_template('applicsuccess.html', job=job, name=name)
    else:
        return render_template('applicform.html', job=job)

@app.route('/submitted', methods=['POST'])
def submitted():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Perform further processing or store the data in a database

    return render_template('submitted.html', name=name, email=email, message=message)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
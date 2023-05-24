from flask import Flask, render_template, request, redirect

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

@app.route('/slideshow')
def slideshow():
    return render_template('slideshow.html')


@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        company = request.form['company']
        location = request.form['location']

        job = {
            'title': title,
            'description': description,
            'company': company,
            'location': location
        }

        job_openings.append(job)
        return redirect('/')
    else:
        return render_template('post_job.html')

@app.route('/apply_job/<int:job_id>', methods=['GET', 'POST'])
def apply_job(job_id):
    job = job_openings[job_id]

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        resume = request.files['resume']

        # Save the uploaded resume to a specific location
        resume.save('resumes/' + resume.filename)

        # Perform additional processing or database operations here

        return render_template('application_success.html', job=job, name=name)
    else:
        return render_template('apply_job.html', job=job)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
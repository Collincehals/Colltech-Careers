from mailjet_rest import Client
import os
def send_job_notification(title, company, location, currency, salary, email):
    api_key = os.environ['API_KEY']
    api_secret =os.environ['API_SECRET']

    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    email_data = {
        'Messages': [
            {
                'From': {
                    'Email':'Colltechcareers@gmail.com',
                    'Name': 'Colltech Careers'
                },
                'To': [
                    {
                        'Email': email
                    }
                ],
                'Subject': 'New Job Alert',
                'HTMLPart': '''
                    <html>
                        <body>
                            <h3>Subject: New Job Alert!</h3>
                            <p>
                                Dear Subscriber {email},
                            </p>
                            <p>
We are excited to inform you about a new job posting on our website. Here are the details:
                            </p>
                            <h4>Job Details:</h4>    
                            <ul>
                                <li>Job Title: {title}</li>
                                <li>Hiring Company: {company}</li>
                                <li>Location: {location}</li>
                                <li>Salary: {currency}{salary}</li>
                            </ul>
                            <p>
                                Visit our website careers page at https://colltech-careers.onrender.com/jobs to view the complete job posting and apply.<br>
Thank you for subscribing to our job alerts. We wish you the best in your job search!<br>
              
                            </p>
                            <p>
                                Best regards,<br></br>
                                Colltech Careers Team
                            </p>
                        </body>
                    </html>
                '''.format(title=title, company=company, location=location, currency= currency, salary=salary, email=email)
            }
        ]
    }

    result = mailjet.send.create(data=email_data)

    if result.status_code == 200:
        print('Registration Confirmation email sent successfully.')
    else:
        print('Failed to send Registration Confirmation email.')
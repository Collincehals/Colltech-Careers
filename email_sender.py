from mailjet_rest import Client
import os
def send_confirmation_email(job_title, applicant_email, applicant_name,last_name, country):
    api_key = os.getenv('API_KEY')
    api_secret =os.getenv('API_SECRET')

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
                        'Email': applicant_email
                    }
                ],
                'Subject': 'Application Confirmation',
                'HTMLPart': '''
                    <html>
                        <body>
                            <h3>Subject: Application Confirmation - {job_title} Role</h3>
                            <p>
                                Dear {applicant_name},
                            </p>
                            <p>
                                Thank you for applying for the position of {job_title} role. We have received your application and would like to confirm its successful submission.
                            </p>
                            <h4>Application Details:</h4>    
                            <ul>
                                <li>Job Title: {job_title}</li>
                                <li>Applicant Name: {applicant_name} {last_name}</li>
                                <li>Country: {country}</li>
                                <li>Email: {applicant_email}</li>
                            </ul>
                            <p>
                                Our team will carefully review your application and get back to you soon regarding the next steps.<br>
                                If you have any questions, feel free to reach out to our HR department at colltechcareers@gmail.com or through our toll-free landline number at +010200100.<br>
                                Thank you for your Job application through Colltech Careers website. <br>
                                Best of luck with your application!<br></br>
                            </p>
                            <p>
                                Best regards,<br></br>
                                Hals,<br></br>
                                Talents Manager,<br></br>
                                Colltech Careers ltd.
                            </p>
                        </body>
                    </html>
                '''.format(applicant_name=applicant_name, applicant_email=applicant_email, job_title=job_title,last_name=last_name, country=country)
            }
        ]
    }

    result = mailjet.send.create(data=email_data)

    if result.status_code == 200:
        print('Confirmation email sent successfully.')
    else:
        print('Failed to send confirmation email.')
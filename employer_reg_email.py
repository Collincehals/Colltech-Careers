from mailjet_rest import Client
import os
def send_employerreg_email(first_name, last_name, email,company_name, company_category):
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
                'Subject': 'Employer Registration Confirmation',
                'HTMLPart': '''
                    <html>
                        <body>
                            <h3>Subject: Employer Registration Confirmation</h3>
                            <p>
                                Dear {first_name},
                            </p>
                            <p>
                                Thank you for registering as an Employer on Colltech Careers website. We are excited to have you join our community.We look forward to working together with you to explore job opportunities that you will be having. Your registration details are as follows:
                            </p>
                            <h4>Registration Details:</h4>    
                            <ul>
                                <li>Full Names: {first_name} {last_name}</li>
                                <li>Email: {email}</li>
                                <li>Company Name: {company_name}</li>
                                <li>Company Category: {company_category}</li>
                                
                            </ul>
                            <p>
                                If you have any questions, feel free to reach out to our support team at colltechcareers.support@gmail.com or through our toll-free landline at +010200100.Thank You!<br>
              
                            </p>
                            <p>
                                Best regards,<br></br>
                                Colltech Careers Team
                            </p>
                        </body>
                    </html>
                '''.format(first_name=first_name,last_name=last_name, email=email, company_name=company_name, company_category= company_category)
            }
        ]
    }

    result = mailjet.send.create(data=email_data)

    if result.status_code == 200:
        print('Registration Confirmation email sent successfully.')
    else:
        print('Failed to send Registration Confirmation email.')
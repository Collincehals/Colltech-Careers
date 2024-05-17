from mailjet_rest import Client
import os
from dotenv import load_dotenv
load_dotenv()

def send_registration_email(email,username):
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
                        'Email': email
                    }
                ],
                'Subject': 'Registration Confirmation',
                'HTMLPart': '''
                    <html>
                        <body>
                            <h3>Subject: Registration Confirmation</h3>
                            <p>
                                Dear {username},
                            </p>
                            <p>
                                Thank you for registering on Colltech Careers website. We are excited to have you join our community. Your registration details are as follows:
                            </p>
                            <h4>Registration Details:</h4>    
                            <ul>
                                <li>Username: {username}</li>
                                <li>Email: {email}</li>
                            </ul>
                            <p>
                                If you have any questions, feel free to reach out to our support team at colltechcareers.support.@gmail.com or through our toll-free landline number at +010200100.We are here to help!<br>
              
                            </p>
                            <p>
                                Best regards,<br></br>
                                Colltech Careers Team
                            </p>
                        </body>
                    </html>
                '''.format(email=email, username=username)
            }
        ]
    }

    result = mailjet.send.create(data=email_data)

    if result.status_code == 200:
        print('Registration Confirmation email sent successfully.')
    else:
        print('Failed to send Registration Confirmation email.')
from mailjet_rest import Client
import os
def send_admin_comment_email(name, email, subject,message):
    api_key = os.environ['API_KEY']
    api_secret =os.environ['API_SECRET']

    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    email_data = {
        'Messages': [
            {
                'From': {
                    'Email': 'odhiambocollince702@gmail.com',
                },
                'To': [
                    {
                        'Email': 'Colltechcareers@gmail.com'
                    }
                ],
                'Subject': f'Message about:  {subject}',
                'HTMLPart':f'''
                    <html>
                        <body>
                            <h3>Name: {name}</h3>
                            <h3>Subject:{subject}</h3>  
                            <div>
                            <h3>Message Body:</h3>
                            {message}
                            </div>
                            <p>
                                Best regards,<br></br>
                                {email}
                            </p>
                        </body>
                    </html>
                '''.format(name=name,email=email,subject=subject, message=message)
            }
        ]
    }

    result = mailjet.send.create(data=email_data)

    if result.status_code == 200:
        print('Registration Confirmation email sent successfully.')
    else:
        print('Failed to send Registration Confirmation email.')
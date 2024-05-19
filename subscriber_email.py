from mailjet_rest import Client
import os
def send_subscriber_email(email,confirmation_link):
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
                'Subject': 'Job Alert Subscription Confirmation',
                'HTMLPart': '''
                    <html>
                        <body>
                            <h3>Subject: Job Alert Subscription Confirmation</h3>
                            <p>
                                Dear {email},
                            </p>
                            <p>
                               Thank you for subscribing to our job alerts service with the email: {email}.Please confirm your subsrciption here: {confirmation_link}<br>

By subscribing to our job alerts, you will receive regular updates about new job postings, industry insights, and valuable career-related information directly in your inbox. We strive to provide you with the most relevant and valuable content to support your job search and career growth.<br>
                                If at any time you wish to unsubscribe from our job alerts service, you can do so by clicking on the "Unsubscribe" link provided at the bottom of our emails.Thank You!<br>
              
                            </p>
                            <p>
                                Best regards,<br></br>
                                Colltech Careers Team
                            </p>
                        </body>
                    </html>
                '''.format(email=email, confirmation_link=confirmation_link)
            }
        ]
    }

    result = mailjet.send.create(data=email_data)

    if result.status_code == 200:
        print('Registration Confirmation email sent successfully.')
    else:
        print('Failed to send Registration Confirmation email.')
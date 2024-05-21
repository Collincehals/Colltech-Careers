from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
# Optionally, create a session maker if you plan to use the ORM


root_dir = os.path.abspath(os.path.dirname(__file__))  
db_path = os.path.join(root_dir, 'database.db') 
# Define the path to your SQLite database file
DATABASE_URL = 'sqlite:///' + db_path

# Create the engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM job"))
    column_names = result.keys()
    result_all = result.fetchall()
    jobs = [dict(zip(column_names, row)) for row in   result_all]
    return jobs


def load_job_from_db(id):
    with engine.connect() as conn:
        query = text("SELECT * FROM job WHERE id = :val")
        result = conn.execute(query.bindparams(val=id))
        row = result.fetchone()
        if row is None:
            return None
        else:
            columns = result.keys()
            return dict(zip(columns, row))


def add_application_to_db(job_id, data):
    with engine.connect() as conn:
        query = text("INSERT INTO application(job_id, first_name, last_name, country, education, experience, resume_cv, certificate, email) VALUES (:job_id, :first_name, :last_name, :country, :education, :experience, :resume_cv, :certificate, :email)")
        conn.execute(query,
                     {"job_id": job_id,         
                     "first_name":data['firstname'], 
                     "last_name": data['lastname'], 
                     "education": data['education'], 
                     "experience": data['experience'], 
                     "resume_cv": data['resume'], 
                    "certificate": data['certificate'],
                     "email": data['email']})




def add_user_to_db(data):
    with engine.connect() as conn:
        query = text("INSERT INTO user(username, email,password1, password2) VALUES (:username,:email, :password1, :password2)")
        conn.execute(query,
                     {
                         "username":data['username'], 
                         "email": data['email'],
                         "password1": data['password1'],
                         "password2": data['password2']
                     })


def add_employer_to_db(data):
    with engine.connect() as conn:
        query = text("INSERT INTO employer(first_name, last_name, email,company_name, company_category, password) VALUES (:first_name, :last_name, :email, :company_name, :company_category, :password)")
        conn.execute(query,
                     {"first_name":data['firstname'], 
                     "last_name": data['lastname'],
                     "email": data['email'],
                     "company_name": data['company_name'],
                     "company_category": data['category'],
                     "password": data['password']
                     })



import secrets

# Generate a unique token for each subscriber
def generate_confirmation_token():
    return secrets.token_urlsafe(16)

# Save subscriber details and token to the database
def add_subscriber_to_db(data):
    with engine.connect() as conn:
        query = text("INSERT INTO subscriber(email, token, confirmed) VALUES (:email, :token, :confirmed)")
        conn.execute(query, {
            "email": data['email'],
            "token": data['token'],
            "confirmed": data['confirmed']
        })

# Update subscriber's confirmation status in the database
def update_subscriber_confirmation_status(subscriber_id):
    with engine.connect() as conn:
        query = text("UPDATE subscriber SET confirmed = :confirmed WHERE id = :subscriber_id")
        conn.execute(query, {"confirmed": True, "subscriber_id": subscriber_id})





def add_job_to_db(data):
    with engine.connect() as conn:
        query = text("INSERT INTO job(title, company, location, currency, salary, responsibilities, requirements) VALUES (:title, :company, :location, :currency, :salary, :responsibilities, :requirements)")
        conn.execute(query,
                     {"title": data["title"], 
                     "company": data['company'],
                     "location":data['location'], 
                     "currency": data['currency'], 
                     "salary": data['salary'],
                     "responsibilities": data['responsibilities'], 
                     "requirements": data['requirements']})


from datetime import datetime

def load_subscribers_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM subscriber"))
        column_names = result.keys()
        result_all = result.fetchall()
        
        subscribers = []
        for row in result_all:
            subscriber = dict(zip(column_names, row))
            # Convert datetime objects to strings
            for key, value in subscriber.items():
                if isinstance(value, datetime):
                    subscriber[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            subscribers.append(subscriber)
        
        return subscribers


def load_users_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM user"))
    column_names = result.keys()
    result_all = result.fetchall()
    users = [dict(zip(column_names, row)) for row in   result_all]
    return users


def load_employers_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM employer"))
    column_names = result.keys()
    result_all = result.fetchall()
    employers = [dict(zip(column_names, row)) for row in   result_all]
    return employers

def add_feedback_to_db(data):
    with engine.connect() as conn:
        query = text("INSERT INTO feedback(firstname, email, occupation, comment)")
        conn.execute(query,
                     {"firstname": data["firstname"], 
                     "email": data['email'],
                     "occupation":data['occupation'], 
                     "comment": data['comment'], 
                     })
#load feedback from db
def load_feedbacks_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM feedback"))
    column_names = result.keys()
    result_all = result.fetchall()
    feedbacks = [dict(zip(column_names, row)) for row in   result_all]
    return feedbacks



import pymysql
def delete_unconfirmed_subscribers():
    connection = pymysql.connect(
        host=os.getenv['HOST'],
        user=os.getenv['USER_NAME'],
        password=os.getenv['PASSWORD'],
        database=os.getenv['DB_NAME'],
        ssl= {
        "ssl_ca": "/etc/ssl/cert.pem"
        }
    )

    try:
        with connection.cursor() as cursor:
            # Execute the SQL query to delete unconfirmed subscribers
            sql = "DELETE FROM subscriber WHERE confirmed = 0"
            cursor.execute(sql)
            connection.commit()
            print("Deleted unconfirmed subscribers from the database.")
    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        connection.close()
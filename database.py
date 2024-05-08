from sqlalchemy import create_engine, text
import os
db_connection_string= os.environ['DB_CONNECTION_STRING']


engine = create_engine(
  db_connection_string, 
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  })

def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM jobs"))
    column_names = result.keys()
    result_all = result.fetchall()
    jobs = [dict(zip(column_names, row)) for row in   result_all]
    return jobs


def load_job_from_db(id):
    with engine.connect() as conn:
        query = text("SELECT * FROM jobs WHERE id = :val")
        result = conn.execute(query.bindparams(val=id))
        row = result.fetchone()
        if row is None:
            return None
        else:
            columns = result.keys()
            return dict(zip(columns, row))


def add_application_to_db(job_id, data):
    with engine.connect() as conn:
        query = text("INSERT INTO applications(job_id, first_name, last_name, country, education, experience, resume_cv, certificate, email) VALUES (:job_id, :first_name, :last_name, :country, :education, :experience, :resume_cv, :certificate, :email)")
        conn.execute(query,
                     {"job_id": job_id,         
                     "first_name":data['firstname'], 
                     "last_name": data['lastname'], 
                     "country": data['country'],
                     "education": data['education'], 
                     "experience": data['experience'], 
                     "resume_cv": data['resume'], 
                    "certificate": data['certificate'],
                     "email": data['email']})




def add_user_to_db(data):
    with engine.connect() as conn:
        query = text("INSERT INTO users(first_name, last_name, email,username, password) VALUES (:first_name, :last_name, :email, :username, :password)")
        conn.execute(query,
                     {"first_name":data['firstname'], 
                     "last_name": data['lastname'],
                     "email": data['email'],
                     "username": data['username'],
                     "password": data['password']
                     })


def add_employer_to_db(data):
    with engine.connect() as conn:
        query = text("INSERT INTO employers(first_name, last_name, email,company_name, company_category, password) VALUES (:first_name, :last_name, :email, :company_name, :company_category, :password)")
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
        query = text("INSERT INTO subscribers(email, token, confirmed) VALUES (:email, :token, :confirmed)")
        conn.execute(query, {
            "email": data['email'],
            "token": data['token'],
            "confirmed": data['confirmed']
        })

# Update subscriber's confirmation status in the database
def update_subscriber_confirmation_status(subscriber_id):
    with engine.connect() as conn:
        query = text("UPDATE subscribers SET confirmed = :confirmed WHERE id = :subscriber_id")
        conn.execute(query, {"confirmed": True, "subscriber_id": subscriber_id})





def add_job_to_db(data):
    with engine.connect() as conn:
        query = text("INSERT INTO jobs(title, company, location, currency, salary, responsibilities, requirements) VALUES (:title, :company, :location, :currency, :salary, :responsibilities, :requirements)")
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
        result = conn.execute(text("SELECT * FROM subscribers"))
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
    result = conn.execute(text("SELECT * FROM users"))
    column_names = result.keys()
    result_all = result.fetchall()
    users = [dict(zip(column_names, row)) for row in   result_all]
    return users


def load_employers_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM employers"))
    column_names = result.keys()
    result_all = result.fetchall()
    employers = [dict(zip(column_names, row)) for row in   result_all]
    return employers

def add_feedback_to_db(data):
    with engine.connect() as conn:
        query = text("INSERT INTO feedback(firstname, email, experience, listings, suggestions, communication, usability, response_time) VALUES (:firstname, :email, :experience,:listings, :suggestions, :communication, :usability, :response_time)")
        conn.execute(query,
                     {"firstname": data["firstname"], 
                     "email": data['email'],
                     "experience":data['experience'], 
                     "listings": data['listings'], 
                     "suggestions": data['suggestions'],
                     "communication": data['communication'], 
                     "usability": data['usability'],
                     "response_time": data['response_time']
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
        host=os.environ['HOST'],
        user=os.environ['USER_NAME'],
        password=os.environ['PASSWORD'],
        database=os.environ['DB_NAME'],
        ssl= {
        "ssl_ca": "/etc/ssl/cert.pem"
        }
    )

    try:
        with connection.cursor() as cursor:
            # Execute the SQL query to delete unconfirmed subscribers
            sql = "DELETE FROM subscribers WHERE confirmed = 0"
            cursor.execute(sql)
            connection.commit()
            print("Deleted unconfirmed subscribers from the database.")
    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        connection.close()
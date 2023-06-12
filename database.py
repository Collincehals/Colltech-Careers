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
        query = text("INSERT INTO applications(job_id, first_name, last_name, country, education, experience, resume_cv, certificate) VALUES (:job_id, :first_name, :last_name, :country, :education, :experience, :resume_cv, :certificate)")
        conn.execute(query,
                     {"job_id": job_id,         
                     "first_name":data['firstname'], 
                     "last_name": data['lastname'], 
                     "country": data['country'],
                     "education": data['education'], 
                     "experience": data['experience'], 
                     "resume_cv": data['resume'], 
                    "certificate": data['certificate']})
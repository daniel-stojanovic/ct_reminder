import psycopg2
import sys
import datetime
from psycopg2.extras import DictCursor
from psycopg2.extras import RealDictCursor
from psycopg2.extras import NamedTupleCursor


er_id=3142
class PostgreSQL:
    def __init__(self):
        # Define our connection string
        self.host = 'internalrecruiting.cq03nwpqmo5j.us-east-2.rds.amazonaws.com'
        self.db = 'recruiting'
        self.user = 'danny'
        self.password = '3n4ctUS!'
        self.conn_string = "host='{host}' dbname='{db}' user='{user}' password='{password}'"



    def connect_to_db(self, conn_string="", host_adress="", db="", username="", password="", cursor=""):
        #depending on what information is provided, connect to db
        connection_string = self.conn_string if conn_string is "" else conn_string
        host = self.host if host_adress is "" else host_adress
        user = self.user if username is "" else username
        database = self.db if db is "" else db
        pw = self.password if password is "" else password
        connection_string = connection_string.format(host = host, db = database, user = user, password = pw)


        # get a connection, if a connect cannot be made an exception will be raised here
        self.connection = psycopg2.connect(connection_string)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        if cursor == "namedtuple":
            self.cursor = self.connection.cursor(cursor_factory=NamedTupleCursor)
        elif cursor == "dictionary":
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        else:
            self.cursor = self.connection.cursor()

    def execute_query(self, query="", script="", **kwargs):
        self.connect_to_db(**kwargs)
        if script:
            q = open(script, "r").read().format(**kwargs)
        else:
            q = query
        self.cursor.execute(q)
        self.connection.commit()
        result = [line for line in self.cursor]
        self.connection.close()
        return result

    def show_table(self, table, **kwargs):
        query="SELECT * FROM {}".format(table)
        result = self.execute_query(query, **kwargs)
        return result

    def add_candidate(self, er_id, first_name, last_name, xing_link):
        query = open("add_candidate.sql", "r").read().format(er_id=er_id,
                                                                 first_name=first_name,
                                                                 last_name=last_name,
                                                                 xing_link=xing_link)
        self.execute_query(query)

    def add_candidate_to_job(self, candidate_id, job_id):
        query = """
        INSERT INTO candidates_{jobid}(
            candidate_ID,
            status
        ) VALUES(
            {candidate_ID},
            'added_to_job',
        )
        """.format(jobid=job_id, candidate_ID=candidate_id)

    def add_job(self, **kwargs):
        print self.execute_query(script="add_job.sql", **kwargs)

    def add_client(self, company_name, **kwargs):
        kwargs['company_name'] = company_name
        self.execute_query(script="add_client.sql", **kwargs)

    def get_client_id(self, company_name):
        q = "SELECT id FROM clients WHERE full_name='{}'".format(company_name)
        result = self.execute_query(q)
        print result
        '''if len(result) is 1:
            return result[0][0]
        else:
            raise AssertionError("Multiple clients identified")'''
if __name__ == "__main__":
    p = PostgreSQL()
    #p.execute_script("add_job.sql", recruiter_id=1, er_id=3141, client_id=123, position_title="")
    #p.add_candidate("213944", "daniel", "stojanovic", "xing.com/danny")
    #p.show_table("clients", dict=True)
    #p.execute_script("add_job.sql", jobid="12345")
    #p.add_client("PALTRON GmbH")
    #client_id = p.get_client_id("PALTRON GmbH")
    #print client_id
    #p.add_job(job_title="Personal Assistent",er_id=er_id,client_id=client_id,recruiter_id=1)

    #p.assign_candidate_to_job()
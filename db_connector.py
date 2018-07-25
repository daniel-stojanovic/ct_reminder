import psycopg2
import sys
import datetime
from psycopg2.extras import DictCursor
from psycopg2.extras import RealDictCursor
from psycopg2.extras import NamedTupleCursor
import time

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
        connection_string = conn_string if conn_string else self.conn_string
        host = host_adress if host_adress else self.host
        user = username if username else self.user
        database = db if db else self.db
        pw = password if password else self.password
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

    def execute_query(self, query, *args, **kwargs):
        """
        connects to the db (optionally using the specified cursor),
        executes the query and replaces placeholders with either a list of args (placeholders: %s)
        or kwargs (placerholders: %(keyword)s,
        commits the changes and returns the fetched result (if there is any);
        if no result is to be fetched, returns
        :param query: sql to be passed, including %s parameters; these will be replaced with args OR kwargs
        :param args: optional positional argumenmts to be passed into query; only args OR kwargs can be passed
        :param kwargs: optional keyword arguments to be passed into query; 'cursor' will be removed automatically
        :return: either the fetched result or the servers status message
        """
        if 'cursor' in kwargs:
            self.connect_to_db(cursor=kwargs['cursor'])
            del kwargs['cursor']
        else:
            self.connect_to_db()
        if 'script' in kwargs:
            q = open(kwargs['script'], "r").read()
        else:
            q = query
        if args:
            data = args
        elif kwargs:
            data = kwargs
        else:
            data=""
        self.cursor.execute(q, data)
        self.connection.commit()
        try:
            result = [line for line in self.cursor]
        except psycopg2.ProgrammingError:
            result = self.cursor.statusmessage
        finally:
            self.connection.close()
            time.sleep(0.5)
            return result

    def show_table(self, table):
        query = "SELECT * FROM %s" %table
        result = self.execute_query(query)
        print result
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

    '''def add_job(self, **kwargs):
        print self.execute_query(script="add_job.sql", **kwargs)'''

    def add_client(self, internal_name, **kwargs):
        kwargs['internal_name'] = internal_name
        self.execute_query(script="add_client.sql", **kwargs)

    def get_client_id(self, company_name, **kwargs):
        q = "SELECT id FROM clients WHERE full_name=%s"
        result = self.execute_query(q, company_name, **kwargs)
        if len(result) is 1:
            return result[0][0]
        else:
            raise AssertionError("Multiple or no clients identified")

    '''def get_id(self, table, **kwargs):
        q = "SELECT id FROM {} WHERE {}=%s".format(table, kwargs.keys()[0])
        return self.execute_query(q, **kwargs)'''


if __name__ == "__main__":
    starttime = datetime.datetime.now()
    p = PostgreSQL()
    print p.execute_query("SELECT * FROM candidates")
    endtime = datetime.datetime.now()
    print (endtime-starttime)
    #p.execute_script("add_job.sql", recruiter_id=1, er_id=3141, client_id=123, position_title="")
    #p.add_candidate("213944", "daniel", "stojanovic", "xing.com/danny")
    #p.execute_script("add_job.sql", jobid="12345")
    #p.add_client("PALTRON")
    #p.show_table("clients")
    #client_id = p.get_client_id("PALTRON GmbH21")
    #print client_id
    #p.add_job(job_title="Personal Assistent",er_id=er_id,client_id=client_id,recruiter_id=1)

    #p.assign_candidate_to_job()
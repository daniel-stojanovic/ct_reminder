import psycopg2
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
        self.cursor = self.connection.cursor()

    def execute_query(self, query, *args, **kwargs):
        self.connect_to_db()
        self.cursor.execute(query, *args, **kwargs)
        self.connection.commit()
        result = [line for line in self.cursor]
        print result

p=PostgreSQL()
p.connect_to_db()
p.cursor.execute("SELECT * FROM %(clients)s;", {'clients':"clients",})
for line in p.cursor:
    print line


def test(*args):

    def function2(args):
        for e in args:
            print e
    #function2(*args)



test("Hans","Wurast")
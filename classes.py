from db_connector import PostgreSQL

class BaseClass:
    def __init__(self, id):
        self.db = PostgreSQL()
        if id:
            self.load_db_info(self.table, id)
        else:
            self.get_attributes(self.table)

    def get_attributes(self, table):
        """
        Loads the column names from the specified table and sets them as class attributes
        :param table: string, name of table in db
        :return: None
        """
        query = "select column_name from information_schema.columns where table_name='%s';" %table
        result = self.db.execute_query(query)
        for element in result:
            setattr(self, element[0], None)

    def load_db_info(self, table, id):  #TODO: extend to multiple constructor methods
        """
        Loads data for class in question from provided table
        :param table: string, name of table in db
        :param id: integer, unique in every table
        :return: None
        """
        query = "SELECT * FROM %s WHERE id=%s" %(table,id)
        result = self.db.execute_query(query, cursor="namedtuple")
        try:
            assert len(result) is 1
        except AssertionError:
            raise AssertionError("More than one entry found in database. Unable to construct client instance.")
        else:
            for i, element in enumerate(result[0]._fields):
                setattr(self, element, result[0][i])


class Client(BaseClass):
    def __init__(self, id=None):
        self.table = "clients"
        BaseClass.__init__(self, id)



class Candidate(BaseClass):
    def __init__(self, id=None):
        self.table = "candidates"
        BaseClass.__init__(self, id)


class Job(BaseClass):
    def __init__(self, id=None):
        self.table = "jobs"
        BaseClass.__init__(self, id)

c = Client(12)
d = Candidate()

print c.main_contact
print d.id

def create_client(name, **kwargs):
    Client()

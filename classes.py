from db_connector import PostgreSQL
import pprint
from er_helper.api_calls.api_calls import Erecruiter
import itertools


class BaseClass:
    def __init__(self, id, **kwargs):
        self.db = PostgreSQL()
        # loads info from db if id is provided (=entry exists in DB), otherwise
        # derives empty instance attributes from DB columns when no id is provided (=new entry is being generated);
        # in each case, the last step will be to take all provided kwargs and to apply them to the instance
        if id:
            self.id = id
            self.load_db_info(self.table, id)
        else:
            print("Creating new databse object - category: {}").format(self.table)
            self.assign_attributes(self.get_attributes(self.table))
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_attributes(self, table):
        """
        Loads the column names from the specified table and transforms them into a clean list of strings
        :param table: string, name of table in db
        :return: list
        """
        query = "SELECT column_name FROM information_schema.columns WHERE table_name='{}';".format(table)
        attributes = []
        result = self.db.execute_query(query)  # returns list of 1-element tuples
        for element in result:
            attributes.append(element[0])
        return attributes  # 'clean' list of attributes

    def check_against_db(self, attribute):
        query = "SELECT * FROM {} WHERE {}=%s".format(self.table, attribute)
        value = getattr(self, attribute)
        result = self.db.execute_query(query, value, cursor="namedtuple")
        self.possible_duplicate = False if len(result) is 0 else True
        self.possible_duplicates = [entry.id for entry in result]

    def assign_attributes(self, attributes):
        """
        Assigns provided list of attributes and assigns them to as instance attributes with the value None
        :param table:
        :return: None
        """
        for attribute in attributes:
            setattr(self, attribute, None)

    def load_db_info(self, table, id):  #TODO: extend to multiple constructor methods
        """
        loads all data for specified entry and assigns it to attributes of newly create instance
        :param table: string, name of table in db
        :param id: integer, unique in every table
        :return: None
        """
        query = "SELECT * FROM {} WHERE id=%(id)s".format(table)
        result = self.db.execute_query(query, cursor="namedtuple", id=id)
        try:
            assert result is not []
        except AssertionError:
            raise AssertionError("No entry found in database. Unable to construct client instance.")
        try:
            assert len(result) is 1
        except AssertionError:
            raise AssertionError("More than one entry found in database. Unable to construct client instance.")
        else:
            for i, element in enumerate(result[0]._fields):
                setattr(self, element, result[0][i])

    def __repr__(self):
        """ Default value to return when calling the instance depending on object type """
        if self.table == "clients":
            rep = self.name
        elif self.table == "jobs":
            rep = self.job_title
        elif self.table == "candidates":
            rep = "{} {}".format(self.first_name, self.last_name)
        else:
            raise AttributeError("Could not assign instance name; check 'self.table'")
        return rep

    def commit(self):
        """
        commits all changes made to object to the database; for this, all columns from the relevant table are fetched,
        paired with the instance attributes and uploaded as changes to the entry (or as new entry if no id exists)
        :return: None
        """
        print("Committing changes to '{}'".format(self))    # TODO: consider adding a field "last_changed"
        keys = self.get_attributes(self.table)                      # retrieve relevant keys from DB, but
        keys.remove('id')                                           # remove 'id' and 'added_on' as they are being
        keys.remove('creation_date')                                # dynamically generated in the DB;
        values = [getattr(self, key) for key in keys]               # then retrieve values from instance and create list
        k_v_string = dict(itertools.izip(keys, values))             #
        placeholders = ""                                           #
        if self.id:                                                 # search for entry and change details using provided id
            for i in range(len(keys)):
                placeholders += "{}=%{}s".format(keys[i], keys[i]) if i == 0 else ", {}=%{}s".format(keys[i], keys[i])
            query = "UPDATE {object.table} SET {string} WHERE id={object.id};".format(object=self, string=placeholders)
            self.db.execute_query(query, **k_v_string)
            print("Changes successfully committed to database.") #TODO: insert test to ensure successful upload
        else:                                                   # create new entry and save id as instance attribute
            keystring = ', '.join(keys)                         # join list to comma-separated string
            for i in range(len(keys)):
                placeholders += "%({})s".format(keys[i]) if i == 0 else ", %({})s".format(keys[i])         # create placeholder string (e.g. "%(key)s, %(key)s, %(key)s)
            query = "INSERT INTO {} ({}) VALUES ({}) RETURNING id;".format(self.table, keystring, placeholders)
            self.id = self.db.execute_query(query, **k_v_string)[0][0]
            print("Entry successfully added.")


class Client(BaseClass):
    def __init__(self, id=None, name="", **kwargs):                        # new client must must have
        self.table = "clients"                                                      # internal_name; only necessary
        if not id and not name:                                            # if no id is provided (with ID,
            raise AttributeError("No internal name provided for new client!")       # internal_name comes from DB)
        BaseClass.__init__(self, id, name=name, **kwargs)


class Job(BaseClass):
    def __init__(self, id=None, job_title="", client_id="", **kwargs):
        self.table = "jobs"
        if not id:                                                                  #
            self.status = 'new'                                                     #
            if not job_title:                                                       # job_title and client_id must be
                raise AttributeError("No internal name provided for new job!")      # provided for new jobs; status
            if not client_id:                                                       # will be set to 'new'
                raise AttributeError("No client ID provided for new job!")
        BaseClass.__init__(self, id, job_title=job_title, client_id=client_id, **kwargs)


class Match(BaseClass):
    def __init__(self, id=None, **kwargs):
        self.table = "matches"
        BaseClass.__init__(self, id, **kwargs)


class Candidate(BaseClass):
    def __init__(self, id=None, **kwargs):
        self.table = "candidates"
        BaseClass.__init__(self, id, **kwargs)
        self.applications=[]

    @staticmethod
    def scrape_profile(referrer, link):
        if referrer.lower()=="xing":
            pass # execute xing scraping

    def assign_to_job(self, job_id):
        """
        assigns candidate to job both in Postgres DB and eR
        :param job_id: integer, job_id (from Postgres DB)
        :return: None
        """
        job = Job(job_id)
        Erecruiter().assign_candidate_to_job(candidate_id=self.er_id, job_id=job.er_id, referrer=self.referrer)
        self.db.execute_query(script="add_application.sql", candidate_id=self.id, job_id=job_id)
        self.db.execute_query(script="assign_candidate_to_job.sql", candidate_id=self.id, job_id=job_id)
        #TODO: double check that client job combination is unique
        application_id = ""
        self.applications.append(application_id)  # save application id to object

    def create_er_entry(self):
        """
        creates new applicant in eR-system (incl xing_link), then saves ApplicantId to object and postgresDB
        :return: None
        """
        self.er_id = Erecruiter().create_candidate(first_name=self.first_name, last_name=self.last_name)
        Erecruiter().assign_custom_field(self.er_id, "XingLink", self.xing_link)
        self.commit()




if __name__ =="__main__":
    #job = Job(job_title="Senior IT Recruiter", client_id="33", dayzee_link="www.test.de")
    #job.commit()
    c = Client(name="test")
    c.commit()


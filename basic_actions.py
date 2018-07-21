import psycopg2
import csv
import copy

from classes import Candidate, Client, Job

class Stuff:
    def __init__(self):
        pass

    def create_client(self, internal_name, **kwargs):
        client = Client(internal_name=internal_name, **kwargs)
        client.commit()
        print("Successfully created client %s %s" % self.id, self.internal_name)


    def create_job(self, internal_name, **kwargs):
        job = Job(internal_name=internal_name, **kwargs)
        job.commit()
        print("Successfully created job %s %s" % self.id, self.internal_name)

    def get_data_from_csv(self, filepath):
        """ read data from dictionary CSV into the corresponding instance attributes """
        with open(filepath,'rb') as file:
            reader = csv.DictReader(file, delimiter=';', skipinitialspace=True)
            for i in range(reader):            # skip the necessary amount of rows in the CSV
                next(reader)
            entry = next(reader)            # get the data from the current row
            for k, v in entry.iteritems():  # take each key-value pair from that dictionary
                setattr(self, k, v)         # and set as instance attribute

    @staticmethod
    def read_from_csv(filepath, column, skip_header=False):
        """ reads first column from CSV and return simple list """
        with open(filepath,'rb') as file:
            reader = csv.reader(file, delimiter=';', skipinitialspace=True)
            result = [entry[column] for entry in reader]
            if skip_header:
                result.pop(0)
            return result



    @staticmethod
    def add_xing_profiles_to_job(source_file, job_id):
        # create links
        links = Stuff.read_from_csv(source_file, 0, skip_header=True)       # read file and create list of links
        # create instances and populate with links
        blueprint = Candidate(xing_link="")                                 # construct candidate blueprint from DB
        instances = [copy.deepcopy(blueprint) for link in links]            # create list of instances from blueprint
        for i, instance in enumerate(instances):                            # and populate with xing_links;
            instance.xing_link = links[i]                                   #
            instance.referrer = "Xing"
            # check against db (duplicates)
            instance.check_against_db("xing_link")                          # check if xing_link is already in DB;
            if instance.possible_duplicate:                                 # if so, ensure only one entry is present
                if len(instance.possible_duplicates) is not 1:              # and assign that ID to current instance,
                    raise AttributeError("Multiple possibleduplicates "     # throw exception for multiple entries in 
                                         "detected for % s."                # DB
                                         % instance.xing_link)              #
                else:                                                       #
                    instance.id = instance.possible_duplicates[0]           #
                    instance = Candidate(instance.id)                       #
                    # check against db (active)
                    try:                                                    # now check if candidate is active in
                        assert instance.active_applications is None         # another job and, if not, assign to
                    except AssertionError:                                  # current job; otherwise, throw an exception
                        raise AssertionError("Candidate active in other"    #
                                             " job")                        #
            # assign to job
            instance.create_er_entry()
            instance.assign_to_job(job_id)







        pass  #TODO: create queue
        pass  # check for each link if it already exists in the DB and store those links separately
        pass  # if link is new: populate new candidate instance with link and store to list
        pass  # if link is known: construct candidate instance from DB and store to list
        pass  # merge candidate lists and create link queue
        pass  # log into xing and scrape each instances's name, position, company, save to object, commit changes
        pass  # save failed profile to separate list

        #TODO: continue


print Stuff.add_xing_profiles_to_job('test.csv', )


import glob
from database import *


def read_table(name_of_tbl_file):
    '''(str) -> Table

    Returns a Table object based on the table file that is passed into the
    method.
    '''
    # Create a dictionary to be made into a Table object
    dict_table = dict()

    # Create a list that holds the data of each column of the table in order to
    # append it to the key's value in the dictionary
    mod_data = list()

    # Open CSV file for reading
    file_handler = open(name_of_tbl_file, 'r')

    # Read the header of the columns
    line = file_handler.readline()

    # Read the data of each header
    raw_data = file_handler.readlines()

    # Close file - READING FROM FILE COMPLETED
    file_handler.close()

    # Loop through raw_data to split elements by "," and strip off any
    # whitespaces
    for each_data in raw_data:
        mod_each_data = each_data.strip().split(",")

        # Append all elements to mod_data to be used
        mod_data += mod_each_data

    # Create a Table object that can store the dict_table and return the Table
    # object
    table = Table()
    table.set_dict(table.create_table(line, mod_data))
    return table


def read_database():
    '''() -> Database

    Returns a Database object for all of the files ending in.csv.
    '''
    # Create a dictionary to store the database
    dict_database = dict()

    # Get a list of all file names that are CSV files in order to name each
    # table
    file_list = glob.glob('*.csv')

    # Loop through the file_list to get the name of the tables and build the
    # dictionary database
    for each_file in file_list:

        # Name of the tables are created by slicing the name of the CSV file
        # from the beginning to where the extension (..csv) is; the extension
        # is not included in the name of each table in the database
        name_of_table = each_file[:each_file.index('.')]

        # Build the database dictionary with name of the table as keys and
        # Table object as a value to each matching key
        dict_database[name_of_table] = read_table(each_file)

    # Create a Database object to store the database dictionary and return the
    # Databse object
    database = Database()
    database.set_dict(dict_database)
    return database

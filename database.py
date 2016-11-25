class Table():
    '''A class to represent a SQuEaL table'''

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType

        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        '''
        self._table = new_dict

    def get_dict(self):
        '''(Table) -> dict of {str: list of str}

        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        return self._table

    def create_table(self, key_list, data_list):
        '''(List, List) -> dict

        Create the dictionary that represents a table. The format of the
        dictionary is: column_name: list_of_values.
        '''
        # Create a dictionary to be returned
        self._table = dict()

        # Set where to start reading from the data list in order to append the
        # correct data to the correct key in the dictionary
        start = 0

        # Modify the format of the header list in order set them as the key
        # for the dictonary (dict_table)
        key_list = key_list.strip().split(",")

        # Set the interval to read the same type of data from the mod_data
        # list to append to the list in each key in dict_table
        interval = len(key_list)

        # Assign the keys of the dictionary (dict_table)
        for times in range(0, len(key_list)):

            # Values in the key are stored as a list
            self._table[key_list[times]] = []

            # For each key that is created, the data for the key (in the same
            # column) is also added as a list to it
            for each_key in range(start, len(data_list), interval):
                data_list[each_key] = data_list[each_key].strip()
                self._table[key_list[times]].append(data_list[each_key])

            # Increment the start index to read the data from data_list due to
            # key change
            if(start <= len(key_list)-1):
                start += 1
        return self._table

    def num_rows(self):
        '''(Table) -> int

        Returns the number of rows the table has in order to print out the
        table in squeal.py in function print_csv.
        '''
        # Populate list with the keys of the dictionary (columns names of the
        # table)
        key_list = list()

        # Loop through the dictionary to get the keys of the dictionary, in
        # order to get the number of rows
        for key in self._table.keys():
            key_list.append(key)

        # Test if the key list is empty, automatically returns 0
        if(key_list == []):
            row_num = 0

        # If not, get the length of the list in order to find the number of
        # rows in the table
        else:
            row_num = len(self._table[key_list[0]])
        return row_num

    def copy(self):
        '''(Table) -> Table
        Makes a copy of the table object
        '''
        # Create a dictionary to store the copied table
        result_dict = {}

        # Copy the table (keys and values (lists))
        for keys in self._table:
            result_dict[keys] = self._table[keys].copy()

        # Create a table object to return the copied table
        table = Table()
        table.set_dict(result_dict)
        return table


class Database():
    '''A class to represent a SQuEaL database'''

    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        self._database = new_dict

    def get_dict(self):
        '''(Database) -> dict of {str: Table}

        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        return self._database

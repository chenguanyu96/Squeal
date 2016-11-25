from reading import *
from database import *


def run_query(database, query):
    '''(Database, str) -> Table
    Given a query, returns a Table based on instructions given in the query,
    iff the query follows syntax.
    '''
    # File list to read
    sel_col_list = list()
    flag = str()

    # Split the query
    query = query.split()

    # Tokenize where separately in order to treat the spaces that might lead
    # it. This will let the program treat the spaces as 1 token instead of
    # 2 separate tokens.
    if('where' in query):
        for elements in range(5, len(query)):
            flag += query[elements] + " "
        flag = flag.strip(" ")

        query[:] = query[0:5] + [flag]

    # Get the index of the tokens
    select_index = get_index_of_keyword(query, 'select')
    from_index = get_index_of_keyword(query, 'from')
    try:
        where_index = get_index_of_keyword(query, 'where')
    except ValueError:
        where_index = len(query)

    # Joins the table specified using cartesian_product
    joined_table = compute_from(database, query, from_index, where_index)

    # Filter selected columns
    filtered_table = compute_select(joined_table, query, select_index,
                                    from_index)

    # Process where token based on the specific restriction set after the
    # where token
    if(where_index != len(query)):
        filter_table = filtered_table.get_dict()
        restriction_lists_raw = query[where_index+1:]
        restriction_lists = split_list_element(restriction_lists_raw)
        for every_restriction in restriction_lists:

            # The two cases after the where token is tested and executed
            # separately
            if(contains(every_restriction, '=')):
                restriction_equal(every_restriction, filter_table)
            elif(contains(every_restriction, '>')):
                restriction_greater(every_restriction, filter_table)

        # Set the table to be returned
        filtered_table.set_dict(filter_table)
    return filtered_table


def get_index_of_keyword(base_list, str_to_find):
    '''(list, str) -> int
    Get the index of a keyword in the query or list.
    >>> query = ['select', '*', 'from', 'imdb']
    >>> get_index_of_keyword(query, 'select')
    0
    '''
    return base_list.index(str_to_find)


def split_list_element(list_to_split):
    '''(list) -> list
    Returns a list when the elements in the list splitted based on commas in
    the content of the element.
    >>> test = ['a,b']
    >>> split_list_element(test)
    ['a', 'b']
    '''
    return_list = list()
    for element in list_to_split:
        return_list += element.split(',')
    return return_list


def contains(str_to_test, str_test_for):
    '''(str, str) -> bool
    Test if the string contains a character and returns a boolean
    >>> contains('oscar-films', '-')
    True
    >>> contains('kevin', '-')
    False
    '''
    for every_str in str_to_test:
        if(every_str == str_test_for):
            return True
    return False


def compute_from(database, query, from_index, where_index):
    '''(Database, str, int, int) -> Table
    Process the from token and returns the filtered table
    '''
    # Store the list of files
    file_list = list()

    # Join the table if needed
    file_list_raw = query[from_index+1:where_index]
    file_list = split_list_element(file_list_raw)
    base_table = file_list[0]
    joined_table = database.get_dict()[file_list[0]]
    if(len(file_list) >= 2):
        for table_names in range(1, len(file_list)):
            joined_table = cartesian_product(joined_table, database.get_dict
                                             ()[file_list[table_names]])
    return joined_table


def compute_select(joined_table, query, select_index, from_index):
    '''(Table, list, int, int) -> Table
    Process the select token and returns the filtered table
    '''
    # Make a copy of the table so the program doesn't mutate it
    joined_table_copy = joined_table.copy()

    # Get the required values in order to set the restrictions for the table
    sel_col_list_raw = query[select_index+1:from_index]
    sel_col_list = split_list_element(sel_col_list_raw)

    # If "select *" is entered, it won't filter anything
    if(sel_col_list[0] == '*'):
        filtered_table = joined_table_copy

    # Filter the columns as is typed in the query
    else:
        key_list = list()
        for key in joined_table_copy.get_dict().keys():
            key_list.append(key)
        for keys in key_list:
            if(keys not in sel_col_list):
                joined_table_copy.get_dict().pop(keys, None)
        filtered_table = joined_table_copy
    return filtered_table


def remove_row(table, list_of_index):
    '''(dict, list) -> NoneType
    Remove entire row that is listed in the list of indices to be removed
    '''
    for each_data in table:
        for index in sorted(list_of_index, reverse=True):
            del table[each_data][index]


def restriction_equal(every_restriction, filter_table):
    '''(list, Table) -> NoneType
    Filter the table based on the restrictions given.
    '''
    # Make a copy of the table so that it deosnt' mutate the original table
    filter_table_copy = filter_table.copy()

    # Stores the indices to be deleted
    del_index = []

    # Get all values that is needed in order to set the restriction in order
    # to filter the table based on the restrictions given.
    index_of_equal = every_restriction.find("=")
    val_restrict = every_restriction[index_of_equal+1:]
    col_to_look = every_restriction[:index_of_equal]

    # Test if the value is inside quotation marks in order to treat it as a
    # value instead of a column name
    if(contains(val_restrict, "'") is True):

        # Filters the table based on the restriction
        val_restrict = val_restrict[1:-1]
        for data in range(len(filter_table_copy[col_to_look])):
            if(filter_table_copy[col_to_look][data] != val_restrict):
                del_index.append(data)
        remove_row(filter_table_copy, del_index)
    else:

        # Filter the table given that the restriction is a column name
        for data in range(len(filter_table_copy[col_to_look])):
            if(filter_table_copy[col_to_look][data]
               != filter_table_copy[val_restrict][data]):
                del_index.append(data)
        remove_row(filter_table_copy, del_index)


def restriction_greater(every_restriction, filter_table):
    '''(list, Table) -> NoneType
    Filter the table based on the restrictions given.
    '''
    # Make a copy of the table so that it doesn't mutate it
    filter_table_copy = filter_table.copy()

    # Initialize a list that stores the indices to be deleted
    del_index = []

    # Get the indices of the tokens that is needed in order to get the value
    # to be restricted.
    index_of_equal = every_restriction.find(">")
    val_restrict = every_restriction[index_of_equal+1:]
    col_to_look = every_restriction[:index_of_equal]

    # Test if the restriction is value inside single quotation marks
    if(contains(val_restrict, "'") is True):

        # Filter the table based on the restriction
        val_restrict = val_restrict[1:-1]
        for data in range(len(filter_table_copy[col_to_look])):
            if(not float(filter_table_copy[col_to_look][data]) >
               float(val_restrict)):
                del_index.append(data)
        remove_row(filter_table_copy, del_index)

    # This case is for if the second restriction value after the equal sign
    # is a name of a column in the table
    else:

        # Compare the 2 columns and match it to the restriction, if it
        # doesn't match, the row will be deleted
        for data in range(len(filter_table_copy[col_to_look])):
            if(not float(filter_table_copy[col_to_look][data])
               > float(filter_table_copy[val_restrict][data])):
                del_index.append(data)
        remove_row(filter_table_copy, del_index)


def cartesian_product(table_one, table_two):
    '''(Table, Table) -> Table
    Returns the cartesian product of 2 tables in a dictionary format where
    the key is the column name and values is in a list.
    >>> d1 = {'a': ['a1', 'a2'], 'b': ['b1', 'b2']}
    >>> d2 = {'c': ['c1', 'c2'], 'd': ['d1', 'd2']}
    >>> t1 = Table()
    >>> t2 = Table()
    >>> t1.set_dict(d1)
    >>> t2.set_dict(d2)
    >>> cart_prod = cartesian_product(t1, t2).get_dict()
    >>> cart_prod == {'a': ['a1', 'a1', 'a2', 'a2'],
    ... 'd': ['d1', 'd2', 'd1', 'd2'], 'c': ['c1', 'c2', 'c1', 'c2'],
    ... 'b': ['b1', 'b1', 'b2', 'b2']}
    True
    >>> d1 = {'a': ['a1', 'a2'], 'b': ['b1', 'b2']}
    >>> d2 = {}
    >>> t1 = Table()
    >>> t2 = Table()
    >>> t1.set_dict(d1)
    >>> t2.set_dict(d2)
    >>> cart_prod = cartesian_product(t1, t2).get_dict()
    >>> cart_prod == {'a': [], 'b': []}
    True
    '''
    # Get the number of rows for each table in order to compute the cartesian
    # product of the 2 tables
    num_of_rows_table1 = table_one.num_rows()
    num_of_rows_table2 = table_two.num_rows()

    # Get both tables' data in a dictionary format
    table1 = table_one.get_dict()
    table2 = table_two.get_dict()

    # Declare a dictionary in order to store the cartesian product table
    cartesian_product = dict()

    # Loop through table1 in order to do the necessary changes to get the
    # cartesian product
    for key in table1:

        # Loop through the list that stored with the key (table column name)
        # to make necessary changes
        for value in table1[key]:

            # Check if key in table is in the cartesian_product in order to
            # add elements to the key in a list type
            if key not in cartesian_product:

                # Makes a key in the cartesian_product dictionary and makes
                # the value a list empty
                cartesian_product[key] = []

                # Appends all keys and the values in the list to the
                # cartesian product
                cartesian_product[key].extend([value]*num_of_rows_table2)

            # If it is in the cartesian product, add the values to it
            else:
                cartesian_product[key].extend([value]*num_of_rows_table2)

    # The same algorithm applies to table 2 but it duplicates the list for n
    # number of times.
    for key in table2:
        cartesian_product[key] = table2[key]*num_of_rows_table1

    # Set it to a table object and returns it
    table = Table()
    table.set_dict(cartesian_product)
    return table


def print_csv(table):
    '''(Table) -> NoneType
    Print a representation of table.
    '''
    dict_rep = table.get_dict()
    columns = list(dict_rep.keys())
    print(','.join(columns))
    rows = table.num_rows()
    for i in range(0, rows):
        cur_column = []
        for column in columns:
            cur_column.append(dict_rep[column][i])
        print(','.join(cur_column))

if(__name__ == "__main__"):
    query = input("Enter a SQuEaL query, or a blank line to exit:")

    # Try to execute the query line, if a blank line is entered, the program
    # will exit
    database = read_database()
    while(query != ""):
        if("select" in query and "from" in query):
            ret_table = run_query(database, query)
            print_csv(ret_table)
        query = input("Enter a SQuEaL query, or a blank line to exit:")

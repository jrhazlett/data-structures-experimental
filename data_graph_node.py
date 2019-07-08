"""
-----EXPERIMENTAL-----
-----EXPERIMENTAL-----
-----EXPERIMENTAL-----
-----EXPERIMENTAL-----
-----EXPERIMENTAL-----

Class meant for handling "graph" data structures.
"""
#
# Libraries - native
#
from collections import deque
import os
import sys
#
# Libraries - custom
#
try :

    from .base_data_node import Base_data_node

except :

    sys.path.append( os.path.dirname( __file__ ) )

    from base_data_node import Base_data_node
#
# Config
#
#
# Note: These globals support _setup_graph_based_on_data_structure_matrix(), which provides the dev
# with the means to turn a matrix / table into a graph structure
#
# This translates list indexes into dictionary keys
_DICT_TRANSLATOR_INDEXES_AND_KEYS_FOR_LIST_OF_NEXT_COORDINATES = {

    0 : "left",
    1 : "right",
    2 : "up",
    3 : "down",

}
#
# This is used for creating bi-directional links between nodes.
_DICT_TRANSLATOR_KEY_OPPOSITES = {

    "left" : "right",
    "right" : "left",
    "up" : "down",
    "down" : "up",

}
#
# Class
#
class Data_graph_node(Base_data_node):
    """
    This is a node meant for a graph data structure
    
    Key features (in contrast to a tree):
    
    -Not dependent on a root node
    """
    #
    # Public
    #
    #
    # Public - get
    #
    def get_int_count_edges( self, arg_node_start = None ):
        """
        This method counts the number of connections between nodes which exist within a graph.

        Test requirements and status:

        -Count is accurate - passed
        -Default count is *all* connections between nodes
        -No infinite loop - passed
        """
        #
        # Setup starting node
        #
        _node_start = self if arg_node_start == None else arg_node_start
        #
        # Setup return value
        #
        _int_count_edges = 0
        #
        # Iterate over graph
        #
        _set_of_nodes_visited = { _node_start }

        _deque_to_process_nodes = deque( [ _node_start ] )

        while _deque_to_process_nodes :

            item_node = _deque_to_process_nodes.popleft()
            #
            # Increment count
            #
            item_int_count_edges = len( item_node._dict_of_keys_and_nodes_next )

            _int_count_edges += item_int_count_edges
            #
            # Prep next iteration
            #
            for item_node_next in item_node._dict_of_keys_and_nodes_next.values() :

                if not item_node_next in _set_of_nodes_visited :

                    _set_of_nodes_visited.add( item_node_next )

                    _deque_to_process_nodes.append( item_node_next )
        #
        # Return result
        #
        return _int_count_edges

    def get_int_count_vertices( self, arg_node_start = None ):
        """
        Test requirements and status:

        -Accurate count - passed
        -No infinite loop - passed
        """
        #
        # Get starting node
        #
        _node_start = self if arg_node_start == None else arg_node_start
        #
        # Setup count
        #
        _int_count_vertices = 0
        #
        # Iterate through graph
        #
        _set_of_nodes_already_explored = { _node_start }

        _deque_to_process_nodes = deque( [ _node_start ] )

        while _deque_to_process_nodes :

            item_node = _deque_to_process_nodes.popleft()
            #
            # Increment count
            #
            _int_count_vertices += 1
            #
            # Prep next iteration
            #
            #
            # Add all unexplored nodes to deque
            #
            for item_node_next in item_node._dict_of_keys_and_nodes_next.values() :

                if not item_node_next in _set_of_nodes_already_explored :

                    _set_of_nodes_already_explored.add( item_node_next )

                    _deque_to_process_nodes.append( item_node_next )
        #
        # Return result
        #
        return _int_count_vertices

    def get_list_of_nodes( self, arg_node_start = None ):
        """
        This method returns a list of all nodes within the graph.

        Note: Since all links between nodes are handled via dict, the order of the returned
        list is likely to vary, especially in earlier python versions.

        Test requirements and status:

        -All nodes accounted for - passed
        -No infinite loop - passed
        """
        #
        # Get starting node
        #
        _node_start = self if arg_node_start == None else arg_node_start
        #
        # Prep list to return
        #
        _list_to_return = [ ]

        _list_to_return.append( _node_start )
        #
        # Iterate through nodes
        #
        _set_of_visited_nodes = { _node_start }

        _deque_to_process = deque( [ _node_start ] )

        while _deque_to_process :
            #
            # Pop-left to always get the shortest path
            #
            item_node = _deque_to_process.popleft()
            #
            # Iterate through node links
            #
            for item_key_next, item_node_next in item_node._dict_of_keys_and_nodes_next.items() :
                #
                # Only visit nodes not already traveled
                #
                if not item_node_next in _set_of_visited_nodes :
                    #
                    # Mark node as already visited
                    #
                    _set_of_visited_nodes.add( item_node_next )

                    _list_to_return.append( item_node_next )

                    _deque_to_process.append( item_node_next )
        #
        # Return list of nodes
        #
        return _list_to_return

    def get_list_of_paths( self, arg_node_start = None ):
        """
        Returns a list all paths from the starting node to any other node.
        
        Test requirements and status:

        *Tested against loaded matrix

        -All known paths included in list - passed
        -List in order from shortest to longest - passed
        -Multiple paths to same destination included in list - passed
        -No infinite loop - passed
        -No path returns to the starting node - passed
        """
        #
        # Setup list of paths to return
        #
        _list_to_return = []
        #
        # Iterate over graph
        #
        _node_start = self if arg_node_start == None else arg_node_start

        _set_of_visited_nodes = { _node_start }

        _deque_to_process_nodes = deque( [ [ tuple(),
                                             _node_start,
                                             None, ] ] )

        while _deque_to_process_nodes :

            item_list_of_path_parts, item_node, item_node_previous = _deque_to_process_nodes.popleft()
            #
            # Prep next iteration
            #
            for item_key_next, item_node_next in item_node._dict_of_keys_and_nodes_next.items() :

                if not item_node_next is item_node_previous :

                    _list_to_return.append( [ *item_list_of_path_parts, item_key_next, ] )

                if not item_node_next in _set_of_visited_nodes :

                    _set_of_visited_nodes.add( item_node_next )

                    _deque_to_process_nodes.append( [

                        # item_list_of_path_parts
                        [ *item_list_of_path_parts, item_key_next, ],

                        # Next item_node
                        item_node_next,

                        # item_node_previous
                        item_node,

                    ] )

        return sorted( _list_to_return )

    def get_list_of_paths_to_node( self, arg_node, arg_node_start = None ):
        """
        Returns a list of all viable paths to arg_node
        
        Test cases and status:

        -Handle cases where arg_node is not in the graph - functionality needed

        -Include all possible paths to same location - passed
        -No infinite loop - passed
        """
        #
        # Identify starting node
        #
        _node_start = self if arg_node_start == None else arg_node_start
        #
        # Setup list of paths to return
        #
        _list_of_paths_to_return = [ ]
        #
        # Iterate over graph
        #
        _set_of_nodes_visited = set()

        _deque_to_process = deque( [ [], _node_start, ] )

        while _deque_to_process :
            #
            # Pop node from the left, so the path is always the shortest
            #
            item_list_of_path_parts, item_node = _deque_to_process.popleft()
            #
            # If we detect the node, return the path
            #
            if item_node is arg_node :

                _list_of_paths_to_return.append( item_list_of_path_parts )

            _set_of_nodes_visited.add( item_node )
            #
            # Prep next iteration
            #
            for item_key_next, item_node_next in item_node._dict_of_keys_and_nodes_next.items() :

                if not item_node_next in _set_of_nodes_visited :

                    _deque_to_process.append( [ [ *item_list_of_path_parts, item_key_next, ],
                                                item_node_next, ] )
        #
        # Return result
        #
        return _list_of_paths_to_return

    def get_node_at_path( self, arg_path, **kwargs ):
        """
        Returns the node at arg_path in relation to arg_node_start / current node.
        
        Test cases and status:

        -Get default value if path does not exist - Not tested
        -No infinite loop - passed
        -Raise error if path fails - Not tested
        """
        #
        # Setup the default value to return if the node isn't found
        #
        _default_value_to_return_if_node_not_found = None

        if "arg_default_value_to_return_if_node_not_found" in kwargs.keys() :

            _bool_raise_error_if_arg_path_fails = False

            _default_value_to_return_if_node_not_found = kwargs[ "arg_default_value_to_return_if_node_not_found" ]

        else :

            _bool_raise_error_if_arg_path_fails = kwargs.get( "arg_bool_raise_error_if_arg_path_fails", True, )
        #
        # Iterate over nodes
        #
        _node_start = kwargs.get( "arg_node_start", self, )

        item_node = _node_start

        _list_of_path_parts = self._get_list_converted_from_object( arg_path )

        for item_path_part in _list_of_path_parts :

            try :

                item_node = item_node._dict_of_keys_and_nodes_next[ item_path_part ]

            except KeyError :

                if _bool_raise_error_if_arg_path_fails :

                    self._raise_error_because_key_or_path_failed( arg_node_start = _node_start,
                                                                  arg_key_or_path = _list_of_path_parts, )

                else :

                    return _default_value_to_return_if_node_not_found

        return item_node

    def get_path_to_node( self, arg_node, arg_node_start = None ):
        """
        Return the shortest path to arg_node relative to arg_node_start / current node.

        Test requirements and status:

        -Handle cases where arg_node doesn't exist - functionality needed
        -No infinite loop - passed
        -Shortest path - passed
        """
        #
        # Identify starting node
        #
        _node_start = self if arg_node_start == None else arg_node_start
        #
        # Track previously traveled nodes
        #
        _set_of_traveled_nodes = set()
        #
        # Iterate over graph
        #
        _deque_to_process = deque( [ [], _node_start, ] )

        while _deque_to_process :
            #
            # Pop node from the left, so the path is always the shortest
            #
            item_list_of_path_parts, item_node = _deque_to_process.popleft()
            #
            # If we detect the node, return the path
            #
            if item_node is arg_node :

                return item_list_of_path_parts

            _set_of_traveled_nodes.add( item_node )
            #
            # Prep next iteration
            #
            for item_key_next, item_node_next in item_node._dict_of_keys_and_nodes_next.items() :

                if not item_node_next in _set_of_traveled_nodes :

                    _deque_to_process.append( [ [ *item_list_of_path_parts, item_key_next, ],
                                                item_node_next, ] )
    #
    # Public - load
    #
    def load_dict_of_keys_and_nodes_next( self, arg_dict_of_keys_and_nodes_next ):
        """
        This method overrides a nodes existing dict of keys and connecting nodes

        Functionality needed:

        -Break reverse keys on neighboring nodes
        """
        self._dict_of_keys_and_nodes_next.update( arg_dict_of_keys_and_nodes_next )
    #
    # Public - print
    #
    def print_graph( self, **kwargs ):
        """
        Prints all nodes in the graph, starting with arg_node_start / current node
        
        Test cases and results:

        -No infinite loop - passed initial testing
        """
        _node_start = kwargs.get( "arg_node_start", self, )
        #
        # Iterate over graph
        #
        _set_of_nodes_visited = { _node_start }

        _deque_to_process = deque( [ [ [], _node_start, ] ] )

        while _deque_to_process :

            item_list_of_path_parts, item_node = _deque_to_process.popleft()
            #
            # Print node
            #
            self._print_node( arg_node = item_node,
                              arg_path = item_list_of_path_parts,
                              arg_list_of_names_for_attributes_to_print = kwargs.get( "arg_list_of_names_for_attributes" ), )
            #
            # Prep next iteration
            #
            for item_key_next, item_node_next in item_node._dict_of_keys_and_nodes_next.items() :

                if not item_node_next in _set_of_nodes_visited :

                    _set_of_nodes_visited.add( item_node_next )

                    _deque_to_process.append( [ [ *item_list_of_path_parts, item_key_next, ],
                                                  item_node_next, ] )
    #
    # Public - setup
    #
    def setup_graph_based_on_data_structure( self, arg_data, **kwargs ):
        """
        Sets up graph structure to mimic arg_data
        
        Tests and status:

        -No infinite loop - passed
        """
        if self._logic_data_structure_is_matrix( arg_data_structure = arg_data ) :

            _pair_starting_column_and_row = kwargs.get( "arg_tuple_starting_coordinates_column_and_row", ( 0, 0, ), )

            self._setup_graph_based_on_data_structure_matrix(
                arg_data = arg_data,

                # If no starting coordinates provided, then default to zero.
                arg_tuple_starting_coordinates_column_and_row = _pair_starting_column_and_row, )

        elif isinstance( arg_data, Data_graph_node, ) :

            self._setup_graph_based_on_data_structure_graph( arg_node_to_copy = arg_data )

    def _setup_graph_based_on_data_structure_graph( self, arg_node_to_copy ) :
        """
        This method iterates through all nodes in the incoming tree and creates the nodes,
        along with their links in the receiving graph.

        Notes:

        "input" identifies the nodes / keys / objects being copied

        "output" identifies the nodes / keys / objects which are the new copies

        Tests and status:

        -All nodes accounted for - passed (needs more detailed review though)
        -No infinite loop - passed
        """
        #
        # Copy object stored in node
        #
        self._object_stored_in_node = arg_node_to_copy._object_stored_in_node
        #
        # Setup iterations
        #
        _dict_translator_item_node_input_to_item_node_output = { arg_node_to_copy : self }

        _deque_to_process_nodes = deque( [ [ self, arg_node_to_copy, ] ] )

        while _deque_to_process_nodes :
            #
            # Get pair
            # "input" - original
            # "output" - new copy
            #
            item_node_output, item_node_input = _deque_to_process_nodes.popleft()
            #
            # Prep next iteration
            #
            for item_key_input_next, item_node_input_next in item_node_input._dict_of_keys_and_nodes_next.items() :
                #
                # If node already exists in dict translator, then just create the connection with the node network
                #
                if item_node_input_next in _dict_translator_item_node_input_to_item_node_output.keys() :
                    item_node_output_next = _dict_translator_item_node_input_to_item_node_output[ item_node_input_next ]
                #
                # If node doesn't exist yet, then create it and add it to the network
                #
                else :
                    #
                    # Create new receiving node
                    #
                    item_node_output_next = Data_graph_node()
                    #
                    # Add node to dict translator
                    #
                    _dict_translator_item_node_input_to_item_node_output[ item_node_input_next ] = item_node_output_next
                    #
                    # Store object stored in node
                    #
                    item_node_output_next._object_stored_in_node = item_node_input_next._object_stored_in_node
                    #
                    # Add new pair to deque
                    #
                    _deque_to_process_nodes.append( [ item_node_output_next, item_node_input_next, ] )
                #
                # Link node receiving next to item node receiving
                #
                item_node_output._dict_of_keys_and_nodes_next[ item_key_input_next ] = item_node_output_next
                #
                # Check if there's a return link in the next input node
                #
                for item_key_return_possible, item_node_return_possible in item_node_input_next._dict_of_keys_and_nodes_next.items() :
                    #
                    # Do a compare of memory addresses
                    #
                    if item_node_return_possible is item_node_input :
                        #
                        # Copy link if necessary
                        #
                        item_node_output_next._dict_of_keys_and_nodes_next[ item_key_return_possible ] = item_node_output

    def _setup_graph_based_on_data_structure_matrix( self, arg_data, arg_tuple_starting_coordinates_column_and_row ) :
        """
        This method builds the graph based on a matrix / table data structure.

        Each node gets potentially all cardinal directions defined in _DICT_TRANSLATOR_INDEXES_AND_KEYS_FOR_LIST_OF_NEXT_COORDINATES

        General definitions, format: <name> - <key used> - definition

        left cell - 'left' - cell to the left and on the same row as the current cell

        right cell - 'right' - cell to the right, and on the same row as the current cell

        upper cell - 'up' - cell in the same column as current cell, and up one row

        lower cell - 'down' - cell in the same column as current cell, and down one row

        Tests and status:

        -All nodes accounted for - passed
        -Exception handling for bad arg_tuple_starting_coordinates_column_and_row - funtionality needed
        -No index errors - passed
        """
        #
        # Get min and max indexes for columns
        #
        _length_columns = len( arg_data[ 0 ] )

        _index_column_max = _length_columns - 1

        _index_column_min = 0
        #
        # Get min and max indexes for rows
        #
        _length_rows = len( arg_data )

        _index_row_max = _length_rows - 1

        _index_row_min = 0
        #
        # Add starting coordinates to set of objects already checked
        #
        _dict_of_processed_coordinates_and_nodes = { arg_tuple_starting_coordinates_column_and_row : self }
        #
        # Iterate over nodes
        #
        _deque_to_process = deque( [ [ [ arg_tuple_starting_coordinates_column_and_row ],
                                       self,
                                       ] ] )

        while _deque_to_process :
            item_tuple_of_path_parts, item_node = _deque_to_process.popleft()
            #
            # Get current coordinates
            #
            item_pair_coordinates_column_and_row = item_tuple_of_path_parts[ -1 ]

            item_int_index_column, item_int_index_row = item_pair_coordinates_column_and_row
            #
            # Store value at matrix address in node
            #
            item_node._key_unique = item_pair_coordinates_column_and_row

            item_node._object_stored_in_node = arg_data[ item_int_index_row ][ item_int_index_column ]
            #
            # Prep next iteration
            #
            # Create a list of neighboring coordinates within the matrix
            #
            item_list_of_next_coordinates = [
                #
                # left cell - 'left'
                #
                (item_int_index_column - 1, item_int_index_row,),
                #
                # right cell - 'right'
                #
                (item_int_index_column + 1, item_int_index_row,),
                #
                # upper cell - 'up'
                #
                (item_int_index_column, item_int_index_row - 1,),
                #
                # lower cell - 'down'
                #
                (item_int_index_column, item_int_index_row + 1,),

            ]
            #
            # Go through each pair of neighboring coordinates and add
            #
            for item_index in range( len( item_list_of_next_coordinates ) ) :
                item_pair_coordinates_column_and_row_next = item_list_of_next_coordinates[ item_index ]

                if _index_column_min <= item_pair_coordinates_column_and_row_next[ 0 ] <= _index_column_max and \
                        _index_row_min <= item_pair_coordinates_column_and_row_next[ 1 ] <= _index_row_max :
                    #
                    # Process item_pair_coordinates_column_and_row_next ONLY if its new to the graph. Otherwise, its already resolved
                    #
                    if not item_pair_coordinates_column_and_row_next in _dict_of_processed_coordinates_and_nodes.keys() :
                        #
                        # Create new node
                        #
                        item_node_next = Data_graph_node()
                        #
                        # Add the coordinate pair as a key to _dict_of_processed_coordinates_and_nodes, and store item_node_next at
                        # their location.
                        #
                        _dict_of_processed_coordinates_and_nodes[ item_pair_coordinates_column_and_row_next ] = item_node_next

                        item_node_key = _DICT_TRANSLATOR_INDEXES_AND_KEYS_FOR_LIST_OF_NEXT_COORDINATES[ item_index ]
                        #
                        # Create bi-directional connections between item_node and item_node_next
                        #
                        item_node._dict_of_keys_and_nodes_next[ item_node_key ] = item_node_next

                        item_node_next._dict_of_keys_and_nodes_next[ _DICT_TRANSLATOR_KEY_OPPOSITES[ item_node_key ] ] = item_node
                        #
                        # Prep next iteration
                        #
                        _deque_to_process.append( [ [ *item_tuple_of_path_parts, item_pair_coordinates_column_and_row_next, ],
                                                    item_node_next,
                                                    ] )
                    #
                    # If the coordinates exist in _dict_of_processed_coordinates_and_nodes, then get the existing node from it
                    # and create a link between that node and item_node.
                    #
                    else :
                        item_node_next = _dict_of_processed_coordinates_and_nodes[ item_pair_coordinates_column_and_row_next ]

                        item_key_node_next = _DICT_TRANSLATOR_INDEXES_AND_KEYS_FOR_LIST_OF_NEXT_COORDINATES[ item_index ]

                        item_node._dict_of_keys_and_nodes_next[ item_key_node_next ] = item_node_next

                        item_node_next._dict_of_keys_and_nodes_next[ _DICT_TRANSLATOR_KEY_OPPOSITES[ item_key_node_next ] ] = item_node
                        #
                        # No additional iterations happen in this case since this represents the final outcome state, when all connctions
                        # and nodes have been traversed.
                        #
    #
    # Private
    #
    #
    # Private - get
    #
    def _get_dict_of_adjacent_pairs_indexes_row_and_column( self, arg_matrix, arg_pair_indexes_row_and_column ):
        """
        Returns a dict of node connections to load into a target node defined in _setup_graph_based_on_data_structure_matrix()

        Tests and status:

        -Returned only valid coordinates - passed
        """
        _index_row = arg_pair_indexes_row_and_column[ 0 ]

        _index_column = arg_pair_indexes_row_and_column[ 1 ]

        _dict_of_adjacent_pairs_indexes_row_and_column = {

            "left" : ( _index_row - 1, _index_column, ),
            "right" : ( _index_row + 1, _index_column, ),
            "up" : ( _index_row, _index_column + 1, ),
            "down" : ( _index_row, _index_column - 1, ),

        }

        _dict_of_adjacent_pairs_indexes_row_and_column = { item_key : item_value
                                                           for item_key, item_value in _dict_of_adjacent_pairs_indexes_row_and_column.items()
                                                           if self._logic_indexes_row_and_column_are_valid( arg_matrix = arg_matrix,
                                                                                                            arg_pair_indexes_row_and_column = item_value, ) }

        return _dict_of_adjacent_pairs_indexes_row_and_column
    #
    # Private - logic
    #
    def _logic_data_structure_is_matrix( self, arg_data_structure ):
        """
        In this case, a matrix is defined as an iterable of iterables.
        """
        if self._logic_is_iterable_other_than_string( arg_data_structure ) :

            # If it has at least one value, then check if that's iterable
            if arg_data_structure :

                return self._logic_is_iterable_other_than_string( arg_object = arg_data_structure[ 0 ] )

            # If the first-layer iterable is empty, then its not a matrix, its a list
            # else :

        # If none of the above triggers, then return False
        return False

    def _logic_indexes_row_and_column_are_valid( self, arg_matrix, arg_pair_indexes_row_and_column ):
        """
        Returns True if both indexes in arg_pair_indexes_row_and_column are within the index range of arg_matrix.
        
        Returns False if either index is out of range.
        
        Assumptions:
        
        -All matrices' smallest index is always 0
        
        Tests and status:
        
        -Accurate range assessments - passed
        """
        _min_index_column = 0

        _min_index_row = 0

        _max_index_row = len( arg_matrix ) - 1

        _max_index_column = len( arg_matrix[ 0 ] ) - 1

        return all( [ _min_index_row <= arg_pair_indexes_row_and_column[ 0 ] <= _max_index_row,
                      _min_index_column <= arg_pair_indexes_row_and_column[ 1 ] <= _max_index_column, ] )
    #
    # Private - setup
    #
    def __init__(self):

        super().__init__()

        self._key_unique = id( self )

        self._dict_of_keys_and_nodes_next = {}

        self._object_stored_in_node = None
#
# Test area
#
def _print_white_space_between_lines():

    print( "\n\n\n\n" )

if __name__ == "__main__" :

    _node_start = Data_graph_node()
    #
    # Example matrix setup
    #
    if True :

        # Reminder: count should be 25
        _matrix = [ [ "0", "1", "2", "3", "4", ],
                    [ "5", "6", "7", "8", "9", ],
                    [ "A", "B", "C", "D", "E", ],
                    [ "F", "G", "H", "I", "J", ],
                    [ "K", "L", "M", "N", "O", ], ]

    if False :

        _matrix = [ [ 0, 1, ],
                    [ 2, 3, ], ]

    _node_start.setup_graph_based_on_data_structure( arg_data = _matrix,
                                                    arg_tuple_starting_coordinates_column_and_row = ( 0, 0, ), )

    _list_of_nodes = _node_start.get_list_of_nodes()
    #
    # Get all possible paths to nodes other than root
    #
    _list_of_paths = _node_start.get_list_of_paths()

    for item_path in _list_of_paths :

        print( item_path )
"""
LICENSE (MIT)

MIT License

Copyright (c) 2019 James Hazlett

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

-----EXPERIMENTAL-----
-----EXPERIMENTAL-----
-----EXPERIMENTAL-----
-----EXPERIMENTAL-----
-----EXPERIMENTAL-----
"""












































































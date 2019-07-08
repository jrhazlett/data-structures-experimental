"""
-----EXPERIMENTAL-----
-----EXPERIMENTAL-----
-----EXPERIMENTAL-----
-----EXPERIMENTAL-----
-----EXPERIMENTAL-----

Changed from v. 0.0.1:

Originally it was part of data_tree_node but since introducing data_graph_node, it makes more sense to make it an inherited class.
"""
#
# Libraries - native
#
import pprint
import sys
import time
#
# Libraries - native - collections
#
from collections.abc import Iterable
#
# Libraries - native - collections
#
# Used for node traversals
from collections import deque
#
# Config
#
# Support values for printing information
#
# This is the default value set for all instances, unless either set_string_delimiter_for_path_default_for_all_classes() or
# the delimiter is set at the node's creation.
#
_STRING_DELIMITER_FOR_PATH_DEFAULT = "."
#
# Note: These are global variables meant to remain unchanged during execution. Since they are
# static in nature, they are stored here to ensure only a single instance exists.
#
_LIST_OF_CHARACTERS_WHICH_INDICATE_A_DATA_STRUCTURE_END = [ "]",
                                                            "}", ]

_SET_OF_CHARACTERS_WHICH_INDICATE_A_DATA_STRUCTURE_END = set( _LIST_OF_CHARACTERS_WHICH_INDICATE_A_DATA_STRUCTURE_END )
#
# Sets up pprint with friendly display settings
#
_PPRINT = pprint.PrettyPrinter( compact = True,

                                indent = 2,

                                # This ensures all sub-structures print vertically.
                                width = 1, )
#
# Class
#
class Base_data_node():
    """
    This class exists to support different node types. It uses very generalize methods that should work with theoretically any node
    type.


    """
    #
    # Public
    #
    def get_list_of_keys_from_path( self, *args ) :
        """
        This returns a flat list comprised of the keys to navigate from this node to
        the node at the path.

        I settled on this approach to balance execution time and flexibility.

        Reminder about competing approaches and performance:

        List with basic append requires a list reversal at the end, followed by
        a reconversion to a list. This makes the approach slower.

        List with insert( 0, item, ) is slightly faster than above, but slower than
        the stack option actually implemented here.
        """
        if not args :

            return [ ]

        else :

            _list = []

            _stack_to_process = deque( list( args ) )

            while _stack_to_process :

                item_object = _stack_to_process.pop()

                if isinstance( item_object, ( deque, list, tuple, ), ) :

                    _stack_to_process.extend( item_object )

                elif isinstance( item_object, str, ) :

                    if self._string_delimiter_for_path in item_object :

                        _stack_to_process.extend( item_object.split( self._string_delimiter_for_path ) )

                    else :

                        if item_object :

                            _list.insert( 0, item_object, )

                else :

                    if item_object :

                        _list.insert( 0, item_object, )

            return _list
    #
    # Public - get - list - path
    #
    def get_list_path_from_arguments( self, *args ) :
        """
        Returns args in the form of a list based on args' contents.
        """
        return self._get_list_by_combining_arguments( *args )
    #
    # Public - print
    #
    def print_object( self, arg_object, arg_name_for_object = None ) :
        """
        This method prints information in a reasonably easy to read format, and
        compensates for some formatting challenges in pprint.

        Reminder: Processes like Cythonize do not like a self.print() method, so this
        had to be changed to print_object.

        Arguments:

        arg_object - This can be pretty much anything.

        arg_name_for_object - If this contains a value, then the name provided
        is displayed above arg_object's printed information. If this value is None
        then only arg_object's info will print.
        """
        if not arg_name_for_object == None :

            print( arg_name_for_object, "=", )

        print( "\n".join( self._print_info_get_list_of_strings_formatted( arg_object ) ), "\n\n", )
    #
    # Private
    #
    #
    # Private - get
    #
    def _get_key_that_is_last_in_path( self, arg_path ) :
        """
        This returns the last key in a path, regardless of its size or data type.
        """
        if isinstance( arg_path, str, ) :

            return arg_path.rsplit( self._string_delimiter_for_path, 1, )[ -1 ] if self._string_delimiter_for_path in arg_path else arg_path

        else :

            return arg_path[ -1 ]
    #
    # Private - get - list
    #
    def _get_list_by_combining_arguments( self, *args ) :
        """
        This method returns a flat list of all arguments in args.

        args can be a single value, or any data type that supports indexes ( i.e. lists and tuples )

        If there's a nested list / tuple present, its flattened.
        Note: I tried the native equivalent of this functionality and it
        didn't seem to handle nested lists beyond two levels.

        There's no limit to how deep the nested list can be.

        Reminder:
        List with basic append requires a list reversal at the end, followed by
        a reconversion to a list. This makes the approach slower.

        List with insert( 0, item, ) is slightly faster than above, but slower than
        this stack option.

        Example of a nested argument:

        [ "1", [ "2", [ "3" ], [ [ "4" ] ], ], ]

        Result:

        [ "1", "2", "3", "4", ]
        """
        _list = [ ]

        # Deque is notably faster than lists for stacks
        _stack = deque( [ item for item in args ] )

        while _stack :

            item = _stack.pop()

            if isinstance( item, (deque, list, tuple,), ) :

                _stack.extend( item )
            #
            # If its a tuple, then extend
            #
            else :

                _list.insert( 0, item, )

        return _list

    def _get_list_converted_from_object( self, arg_object ) :
        """
        This method ensures we always know we're working with a list. Its a work-horse
        method for supporting multiple data types.

        If arg_object is None, it returns an empty list.

        If arg_object is a list-like iterable, it converts it to a list.

        In all other cases, it returns a list containing arg_object.

        Reminder: list() is slightly faster overall than list comprehension.

        Notes:

            Performance wise, lists appear to trounce most other data structures
            except in specific tasks, so in general, its better to default to
            these until there's a clear reason to use something else.
        """
        # All scenarios assume a list is coming out of this method, so if the
        # value is none, then make it an empty list
        if arg_object == None :

            return [ ]

        # By default, this returns the list argument "as-is."  If we want the copy
        # however, this calls the copy library.
        elif isinstance( arg_object, ( deque, list, set, tuple, ), ) :

            return list( arg_object )

        # This creates a new list regardless of the scenario.
        else :

            return [ arg_object ]
    #
    # Private - get - name
    #
    def _get_name_for_host_method( self, arg_int_depth = 1 ) :
        '''
        if arg_int_depth == 0 : output = "get_string_name_method"

        if arg_int_depth == 1 : output = the name of the method calling get_string_name_method()
        '''
        return sys._getframe( arg_int_depth ).f_code.co_name
    #
    # Private - get - strings
    #
    def _get_strings_combined( self, *args, arg_delimiters = "" ) :
        """
        This method is virtually the same as "".join() except it can handle nested objects with infinite
        depth.

        Arguments:

        args - This can be multiple values, and supported nested data structures like lists within lists.

        arg_delimiters - This is the same as what you would put between the quotes in "".join()
        """
        return arg_delimiters.join( [ str( item ) for item in self._get_list_by_combining_arguments( args ) ] )
    #
    # Private - logic
    #
    def _logic_is_iterable_other_than_string( self, arg_object ) :
        """
        Returns True if arg_object is iterable *and* not a string.

        This protects against common bugs where accidentally iterating over a string
        leads to individual characters getting passed as arguments.
        """
        if isinstance( arg_object, Iterable, ) :

            return not isinstance( arg_object, str, )

        else :

            return False
    #
    # Private - print
    #
    def _print_info_get_list_of_strings_formatted( self, arg_object ):
        """
        This method returns a formatted string which displays in a friendlier format
        than pprint's default approach.

        This is exclusively a support method for print_object(). This is why it returns
        a string, but doesn't start with "get" in its attribute name.
        """
        _string = self._pprint.pformat( arg_object )

        _list = _string.split( "\n" )

        _list_new = []

        item_index = 0

        while item_index < len( _list ) :

            if item_index >= len( _list ) :

                break

            item_string_current = _list[ item_index ]

            item_string_current_with_no_leading_or_trailing_white_space = item_string_current.strip()

            if item_string_current_with_no_leading_or_trailing_white_space :

                for item_character in _LIST_OF_CHARACTERS_WHICH_INDICATE_A_DATA_STRUCTURE_END :

                    item_sub_string_to_use_as_replacement = "".join( [ ", ", item_character, ] )

                    item_string_current = item_string_current.replace( item_character, item_sub_string_to_use_as_replacement, )
                #
                # Handle ':' for dicts
                #
                # if ": " in item_string_current : item_string_current = " : ".join( item_string_current.split( ": " ) )
                #
                # Handle spacing between lines
                #
                if item_string_current.endswith( "," ) :

                    if item_string_current[ -2 ] in _SET_OF_CHARACTERS_WHICH_INDICATE_A_DATA_STRUCTURE_END :

                        item_string_current = "".join( [ item_string_current, "\n", ] )

                elif item_string_current.endswith( " '" ) or item_string_current.endswith( " \"" ) :

                    item_index_next = item_index + 1

                    while ( item_string_current.endswith( " '" ) or item_string_current.endswith( " \"" ) ) and item_index_next < len( _list ) :

                                                         # Current
                        item_string_current = "".join( [ item_string_current.rstrip()[ : -1 ],

                                                         # Next
                                                         _list[ item_index_next ].lstrip()[ 1 : ], ] )

                        if item_string_current[ -1 ] in _LIST_OF_CHARACTERS_WHICH_INDICATE_A_DATA_STRUCTURE_END :

                            item_string_current = "".join( [ item_string_current[ : -1 ], ", ", item_string_current[ -1 ], ] )

                        _list.pop( item_index_next )

            _list_new.append( item_string_current )

            item_index += 1

        return _list_new

    def _print_node( self, arg_node, arg_path, arg_list_of_names_for_attributes_to_print = None ):
        """
        This method prints arg_node's information.

        arg_node is the node we want to see the information for.

        arg_path is the path to arg_node within the data tree.

        arg_names_for_attributes_to_print - This can be None, a single string attribute name,
        or a list of attribute names. If this argument is None, then only the path to the node prints.
        If this contains attribute names, then the method will attempt to print the name and the attribute's
        value.

        If the method fails to find a specific attribute, it will raise an exception and detail
        which attribute name failed and what attributes the node contains.
        """
        print( "--- PATH:", arg_path if arg_path else "(root)", "---\n", )

        if arg_list_of_names_for_attributes_to_print :

            _list_of_pairs_names_for_attributes_and_values_to_print = None

            try :

                # Reminder: ignore the ide when it highlights item_name_for_attribute. This isn't an issue.
                _list_of_pairs_names_for_attributes_and_values_to_print = [ [ item_name_for_attribute, getattr( arg_node, item_name_for_attribute, ), ]
                                                                            for item_name_for_attribute in arg_list_of_names_for_attributes_to_print ]

            except AttributeError :

                self._raise_error_because_attribute_does_not_exist_in_node( arg_node = arg_node,
                                                                            arg_list_of_names_for_attributes = arg_list_of_names_for_attributes_to_print, )

            for item_name_for_attribute, item_value in _list_of_pairs_names_for_attributes_and_values_to_print :

                print( item_name_for_attribute, "=", item_value, )

            print( "\n" )
    #
    # Private - raise
    #
    def _raise_error( self ) :
        """
        Reduces the chances of terminal output inter-mingling with exception info.

        Since this method should only run when raising an exception, the artificial delay
        isn't an issue during proper library execution.
        """
        time.sleep( 0.5 )

        raise ()

    def _raise_error_because_arg_data_is_an_invalid_format(self, arg_data):
        """
        This method provides additional context if this library can't handle the data supplied to
        setup_tree_based_on_data_structure()
        """
        print( "Error: arg_data is an invalid format.\n" )

        print( "Supported data formats and result ( format : bool )" )

        print( "Dict / nested dict:", isinstance( arg_data, dict, ), "\n", )

        _bool_is_list_of_dicts = isinstance( arg_data, list, )

        if _bool_is_list_of_dicts :

            _bool_is_list_of_dicts = isinstance( arg_data[ 0 ], dict, )

        print( "List of dicts:", _bool_is_list_of_dicts, "\n", )

        self.print_object( arg_object = arg_data,
                          arg_name_for_object = "arg_data", )

        self._raise_error()

    def _raise_error_because_attribute_does_not_exist_in_node( self, arg_node, arg_list_of_names_for_attributes ):
        """
        This method provides additional info if an attribute lookup fails for a node.
        """
        self._raise_error_if_object_is_not_a_list( arg_list_of_names_for_attributes )

        print( "Error: attribute does not exist in node.\n" )

        print( "arg_node =", arg_node, "\n", )

        print( "List of names and whether or not name exists in node ( 'name : bool, is present?' ):\n" )

        for item_name_for_attribute in sorted( arg_list_of_names_for_attributes ) :

            print( item_name_for_attribute, ":", hasattr( arg_node, item_name_for_attribute, ), )

        self.print_object( arg_object = sorted( dir( arg_node ) ),
                          arg_name_for_object = "List of names for existing attributes in node", )

        print( "\n" )

        self._raise_error()

    def _raise_error_because_key_or_path_failed( self, arg_key_or_path, arg_node_start ) :
        """
        This provides supplemental information in cases when a key or path lookup fails.
        """
        print( "Error: arg_key_or_path failed.\n" )

        print( "arg_key_or_path =", arg_key_or_path, "\n", )

        print( "type( arg_key_or_path ) =", type( arg_key_or_path ), "\n", )

        _list_of_path_parts_present = [ ]

        _list_of_path_parts_missing = [ ]

        _list_of_path_parts = self.get_list_of_keys_from_path( arg_key_or_path )

        item_node = arg_node_start

        _node_for_data_discrepancy_analysis = None

        for item_path_part in _list_of_path_parts :

            if item_path_part in item_node._dict_of_keys_and_node_children.keys() :

                _list_of_path_parts_present.append( item_path_part )

                item_node = item_node._dict_of_keys_and_node_children[ item_path_part ]

            else :

                _list_of_path_parts_missing = _list_of_path_parts[ len( _list_of_path_parts_present ) : ]

                for item_key in item_node._dict_of_keys_and_node_children.keys() :

                    if str( item_path_part ) == str( item_key ) :

                        _node_for_data_discrepancy_analysis = item_node

                        break

                break

        self.print_object( arg_object = _list_of_path_parts_present,
                          arg_name_for_object = "Path parts present in tree", )

        self.print_object( arg_object = _list_of_path_parts_missing,
                          arg_name_for_object = "Path parts missing from tree", )

        if not _node_for_data_discrepancy_analysis == None :

            _list_of_pairs_path_part_and_bool_data_type_discrepancy_detected = []

            item_node = _node_for_data_discrepancy_analysis

            for item_path_part_missing in _list_of_path_parts_missing :

                for item_key, item_node_child in item_node._dict_of_keys_and_node_children.items() :

                    if str( item_path_part_missing ) == str( item_key ) :

                        _list_of_pairs_path_part_and_bool_data_type_discrepancy_detected.append( [ item_path_part_missing, True, ] )

                        item_node = item_node_child

            print( "List of pairs, path_parts : ( bool ) if they failed due to data type discrepancy...\n" )

            for item_pair in _list_of_pairs_path_part_and_bool_data_type_discrepancy_detected :

                print( item_pair[ 0 ], ":", item_pair[ 1 ], )

        self._raise_error()

    def _raise_error_because_method_needs_defined( self ) :

        print( "Error: Calling method which needs defined.\n" )

        print( "Name for method:", self._get_name_for_host_method( arg_int_depth = 2 ), "\n", )

        self._raise_error()

    def _raise_error_because_node_next_is_not_in_tree( self, arg_node_next, arg_node_root ) :
        """
        This method raises an exception when arg_node_child is not found within arg_node_root's tree.
        """
        print( "Error: arg_node is not in this data tree.\n" )

        print( "arg_node_next =", arg_node_next, "\n", )

        _list_of_pairs_paths_and_nodes = arg_node_root.get_list_of_pairs_paths_and_node_children()

        _lambda_sort_key_for_pairs = lambda arg_pair : arg_pair[ 0 ]

        _list_of_pairs_paths_and_nodes = sorted( _list_of_pairs_paths_and_nodes,
                                                 key = _lambda_sort_key_for_pairs, )

        print( "--Tree Debugging Info ( node id : True / False node is arg_node : path to node )--\n", )

        for item_path, item_node in _list_of_pairs_paths_and_nodes :

            print( item_node._id_for_node if hasattr( item_node, "_id_for_node", ) else id( item_node ),
                   ":", item_node is arg_node_next,
                   ":", item_path, )

        self._raise_error()

    def _raise_error_because_node_child_is_still_part_of_another_tree( self, arg_node_next ) :
        """
        Raises an exception because arg_node_child is already part of another tree.

        Specifically: when the child's _node_parent value is not None.
        """
        print( "Error: arg_node is still part of another tree. Pop it from its previous tree before proceeding.\n" )

        print( "id( arg_node_next ) =", arg_node_next, "\n", )

        print( "arg_node_next._node_parent =", arg_node_next._node_parent, "\n", )

        print( "arg_node_next._node_root.get_path_to_node_child( arg_node_child ) =", arg_node_next._node_root.get_path_to_node_child( arg_node_next ), "\n", )

        self._raise_error()

    def _raise_error_if_object_is_not_a_list( self, arg_object ) :
        """
        For now, this validation only happens when listing names for attributes.

        Per James - Here for my own sanity. Usually I set up some methods to be more dynamic with the data types
        they take, but if I do that in this class, it prevents certain data annotations.
        """
        if not isinstance( arg_object, list, ) :

            print( "Error: arg_object is not a list.\n" )

            print( "arg_object =", arg_object, "\n", )

            print( "type( arg_object ) =", type( arg_object ), "\n", )

            self._raise_error()
    #
    # Private - setup
    #
    def __init__(self, **kwargs):

        self._BOOL_AT_LEAST_ONE_NODE_INSTANCE_EXISTS = True

        # This exists for faster compares when determining whether or not to pass self._string_delimiter_for_path as
        # an initial argument to any internally-created new nodes.
        self._bool_string_delimiter_for_path_is_default = True

        # This is an internal reference to PrettyPrint
        self._pprint = _PPRINT

        self._string_delimiter_for_path = self._STRING_DELIMITER_FOR_PATH_DEFAULT

        if "arg_string_delimiter_for_path" in kwargs.keys() :

            _string_original_value = self._string_delimiter_for_path

            self._string_delimiter_for_path = kwargs[ "arg_string_delimiter_for_path" ]

            self._bool_string_delimiter_for_path_is_default = self._string_delimiter_for_path == _string_original_value

    @classmethod
    def set_string_delimiter_for_path_default_for_all_classes( cls, arg_string_delimiter_for_path_default, **kwargs ) :
        """
        This method sets the global default delimiter for Data_tree_node and all inheriting classes.

        CAUTION: This method should only really run before any nodes exists.

        It will raise errors if used after first node created, or ran a 2nd time. These errors
        can be overridden in the arguments by setting either of these arguments to True:

        -arg_bool_override_safety_against_multiple_assignments
        -arg_bool_override_safety_against_setting_global_value_after_first_node_creation
        """
        if not kwargs.get( "arg_bool_override_safety_against_setting_global_value_after_first_node_creation", False, ) :

            if cls._BOOL_AT_LEAST_ONE_NODE_INSTANCE_EXISTS :

                print( "Error: Attempting to set the string delimiter for all paths after at least one node instance exists.\n" )

                print( "To avoid this error, do one of the following:" )
                print( "-Call set_string_delimiter_for_path_default_for_all_classes() before initializing any nodes." )
                print( "-Set arg_bool_override_safety_against_setting_global_value_after_first_node_creation to True ( WARNING: DOES NOT UPDATE DELIMITERS FOR EXISTING PATHS! )\n" )

                time.sleep( 0.5 )

                raise ()

        if not kwargs.get( "arg_bool_override_safety_against_multiple_assignments", False, ) :

            if not cls._BOOL_STRING_DELIMITER_FOR_PATH_IS_DEFAULT :

                print( "Error: cls._STRING_DELIMITER_FOR_PATH_DEFAULT already set to non-default value.\n" )

                print( "If you intended to do this, set arg_bool_override_safety_against_multiple_assignments to True.\n" )

                time.sleep( 0.5 )

                raise ()

        cls._STRING_DELIMITER_FOR_PATH_DEFAULT = arg_string_delimiter_for_path_default

        cls._BOOL_STRING_DELIMITER_FOR_PATH_IS_DEFAULT = False
    #
    # Class variables and class methods
    #
    # Note: These are in all caps and meant to change as little as possible.
    #
    # This variable becomes True upon the first ever instance in
    _BOOL_AT_LEAST_ONE_NODE_INSTANCE_EXISTS = False

    _BOOL_STRING_DELIMITER_FOR_PATH_IS_DEFAULT = True

    # Sets the class variable to the module global value for _STRING_DELIMITER_FOR_PATH_DEFAULT
    _STRING_DELIMITER_FOR_PATH_DEFAULT = _STRING_DELIMITER_FOR_PATH_DEFAULT
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





























































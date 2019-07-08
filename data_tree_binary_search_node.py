"""
-----EXPERIMENTAL-----
-----EXPERIMENTAL-----
-----EXPERIMENTAL-----
-----EXPERIMENTAL-----
-----EXPERIMENTAL-----

This module holds the library for a binary search tree.
"""
#
# Libraries - native
#
import os
import sys
#
# Libraries - native - collections
#
from collections import deque
#
# Libraries - custom
#
try :

    from .base_data_node import Base_data_node

except :

    sys.path.append( os.path.dirname( __file__ ) )

    from base_data_node import Base_data_node
#
# Class
#
class Data_tree_binary_search_node(Base_data_node):
    """
    Features needed:

    -Hook for event where node's _key_unique changes
    -More tree-focused functionality
    """
    #
    # Public
    #
    #
    # Public - append
    #
    def append_node( self, arg_bool_is_left_side, arg_node_next, arg_node_root = None ):
        """
        This method only replaces the immediate child nodes.

        For 'insert' functionality, refer to insert_node()

        Tests and status:

        -Basic add - passed
        -Exception handling for replacing nodes - functionality needs added
        """
        _node_root = arg_node_root if arg_node_root else self

        if arg_bool_is_left_side :
            
            _node_root._node_next_left = arg_node_next

        else :
            
            _node_root._node_next_right = arg_node_next
    #
    # Public - balance
    #
    def balance_tree( self, arg_node_root = None ):
        """
        This method automatically re-balances the search tree for efficiency. Since rebalancing typically leads
        to a new root node, this method returns that result.

        Notes:

        - This method calls self._balance_tree_via_list()

        I feel like there should be a way to do it without storing all the nodes in a list first. If
        I find it, then there will probably be pros and cons to each approach, which is why this method
        is setup to make calls to other methods.

        Tests and status:

        -All nodes accounted for - initial tests passed, but I'm not convinced yet

        -No infinite loop - passed
        """
        _node_root = arg_node_root if arg_node_root else self

        return self._balance_tree_via_list( self.get_list_of_nodes_traversal_level_order( _node_root ) )

    def _balance_tree_via_list( self, arg_list_of_nodes_from_tree ):
        """
        This method handles one possible approach for re-balancing a data tree for stack recursion.

        General approach:

        -At each layer the algorithm splits the list of possible nodes by calculating the index of the middle node

        -The node at the middle index gets added to the tree

        -The two halves of the list form the "left / lesser" and "right / higher" values respectively

        -This process continues until there are no nodes remaining in any of the broken up lists

        Tests and status:

        -No infinite loop - passed
        -No repeated nodes - passed
        -Resulting tree properly reflects the order of arg_list_of_nodes_from_tree - passed
        """
        #
        # Reminder: This lambda is here as a debugging asset for getting a list of unique keys rather than node memory signatures
        # when printing to the terminal.
        #
        # _lambda_get_list_of_keys = lambda arg_list_of_nodes : [ item_node._key_unique for item_node in arg_list_of_nodes ]
        #
        # Sort list of nodes according to their keys ahead of parsing it into a tree
        #
        _list_of_nodes_from_tree = sorted( arg_list_of_nodes_from_tree,
                                           key = lambda arg_node : arg_node._key_unique, )
        #
        # Reminders:
        # -The double division sign rounds down to the nearest whole number
        # -This is slightly faster than using int() to round down
        #
        item_index_middle = len( _list_of_nodes_from_tree ) // 2

        item_list_of_nodes_left = _list_of_nodes_from_tree[ : item_index_middle ]

        item_list_of_nodes_right = _list_of_nodes_from_tree[ item_index_middle + 1 : ]

        _node_root_new = _list_of_nodes_from_tree[ item_index_middle ]

        item_node = _node_root_new
        #
        # Iterate over sorted list of nodes
        #
        # Each triplet has the following:
        # -item_node at index 0
        # -item_list_of_nodes_left at index 1
        # -item_list_of_nodes_right at index 2
        #
        _deque_of_triplets_node_node_parent_list_left_and_list_right_to_process = deque( [ [ item_node,
                                                                                             item_list_of_nodes_left,
                                                                                             item_list_of_nodes_right, ] ] )

        while _deque_of_triplets_node_node_parent_list_left_and_list_right_to_process :

            item_triplet = _deque_of_triplets_node_node_parent_list_left_and_list_right_to_process.pop()
            #
            # Unpack the triplet
            #
            item_node, item_list_of_nodes_left, item_list_of_nodes_right = item_triplet
            #
            # Clear item_node's children to avoid bad links
            #
            item_node._node_next_left = None
            item_node._node_next_right = None
            #
            # Add a new child node to item_node's left side
            # Build a triplet consisting of:
            # -The child node
            # -A list of the nodes to the left of it
            # -A list of the nodes to the right of it
            #
            # The triplet can also be empty
            #
            item_triplet_left = self._get_triplet_node_middle_node_list_left_and_node_list( arg_node = item_node,
                                                                                            arg_list_of_nodes = item_list_of_nodes_left,
                                                                                            arg_bool_is_left = True, )
            #
            # Prep the next iteration only if the triplet holds any values
            #
            if item_triplet_left :

                _deque_of_triplets_node_node_parent_list_left_and_list_right_to_process.append( item_triplet_left )
            #
            # Add a new child node to item_node's right side
            # Build a triplet consisting of:
            # -The child node
            # -A list of the nodes to the left of it
            # -A list of the nodes to the right of it
            #
            item_triplet_right = self._get_triplet_node_middle_node_list_left_and_node_list( arg_node = item_node,
                                                                                             arg_list_of_nodes = item_list_of_nodes_right,
                                                                                             arg_bool_is_left = False, )
            #
            # Prep the next iteration only if the triplet holds any values
            #
            if item_triplet_right :

                _deque_of_triplets_node_node_parent_list_left_and_list_right_to_process.append( item_triplet_right )
        #
        # Return the new root node after the re-balance
        #
        return _node_root_new

    def _get_triplet_node_middle_node_list_left_and_node_list( self, arg_node, arg_list_of_nodes, arg_bool_is_left ):
        """
        This method gets the middle node in arg_list_of_nodes by finding its middle index. This method attaches the
        new child node to arg_node.

        It is a support method for _balance_tree_via_list() and handles both left and right sides.

        The algorithm returns a triplet if relevant. Consisting of the following:

        -The new child node attached to arg_node

        -A sub list of nodes to the left of the new child node

        -A sub list of nodes to the right of the new child node

        Alternate return value:

        If there are no more nodes to process, this method returns an empty list.


        Tests and results:

        -Splits arg_list_of_nodes successfully, regardless of size - passed
        """
        #
        # If arg_list_of_nodes has values, process it, and return the results as
        # a triplet.
        #
        if arg_list_of_nodes :

            _index_mid = len( arg_list_of_nodes ) // 2

            _node_next = arg_list_of_nodes[ _index_mid ]

            if arg_bool_is_left :

                arg_node._node_next_left = _node_next

            else :

                arg_node._node_next_right = _node_next

            return [ _node_next,
                     arg_list_of_nodes[ : _index_mid ],
                     arg_list_of_nodes[ _index_mid + 1 : ], ]
        #
        # If arg_list_of_nodes, return an empty triplet.
        #
        else :

            return []
    #
    # Public - get
    #
    #
    # Public - get - int
    #
    def get_int_count_for_nodes( self ):
        """
        This method counts the number of nodes in the tree and returns the value.
        """
        _int_count = 0
        #
        # Iterate over tree
        #
        _deque_to_process_nodes = deque( [ self ] )

        while _deque_to_process_nodes :

            item_node = _deque_to_process_nodes.pop()
            #
            # Increment count
            #
            _int_count += 1
            #
            # Prep next iteration
            #
            _deque_to_process_nodes.extend( item_node._get_list_of_nodes_next_adjacent() )

        return _int_count

    def get_int_height( self ):
        """
        Returned the longest possible distance between the root node and any leaf node.

        Tests and results:

        -No infinite loop - passed
        -Returns an accurate count - passed
        """
        #
        # This tracks the number of layers where at least one node exists
        #
        _count_height = 0

        _deque_to_process_nodes = deque( [ self ] )

        while True :
            #
            # If the count is zero, return the height
            #
            if not _deque_to_process_nodes :

                return _count_height
            #
            # Increment height count per layer
            #
            _count_height += 1
            #
            # Set item_count_for_nodes equal to length of deque
            # This tracks the number of nodes at the current layer
            #
            item_count_for_nodes = len( _deque_to_process_nodes )
            #
            # While the count for nodes at current layer is greater than zero...
            # process the node and decrement the count
            #
            while item_count_for_nodes > 0 :
                #
                # Left pop ensures the node is from the current layer
                #
                item_node = _deque_to_process_nodes.popleft()
                #
                # Prep for next iteration
                # When we hit zero, we are out of nodes at this layer
                #
                item_count_for_nodes -= 1
                #
                # Append the nodes for the next layer
                #
                _deque_to_process_nodes.extend( item_node._get_list_of_nodes_next_adjacent() )
    #
    # Public - get - list
    #
    def get_list_of_keys( self, **kwargs ):
        """
        Returns a list of all _key_unique attribute values for all nodes in tree.

        Tests and status:

        -All keys accounted for - passed
        -No infinite loop - passed
        """
        #
        # Prep return value
        #
        _list_to_return = []
        #
        # Iterate over tree
        #
        item_node = kwargs.get( "arg_node_root", self, )

        _deque_to_process = deque( [ item_node ] )

        while _deque_to_process :

            item_node = _deque_to_process.popleft()
            #
            # Append key to list
            #
            _list_to_return.append( item_node._key_unique )
            #
            # Prep next iteration
            #
            if item_node._node_next_left :

                _deque_to_process.append( item_node._node_next_left )

            if item_node._node_next_right :

                _deque_to_process.append( item_node._node_next_right )
        #
        # Return list
        #
        return _list_to_return

    def get_list_of_nodes_traversal_level_order( self, arg_node_root = None ):
        """
        Returns a list of nodes in order.

        Order:

        -Top down, layer-by-layer

        -Each layer is covered completely, left to right


        Strategic considerations:

        -Starts with the root node

        -Adds each subsequent layer, left to right


        Visual example:

            0
           / \
          1   2
         / \   \
        3   4   5

        Order: 0 1 2 3 4 5


        Tests and status:

        -List in correct order - passed
        -No infinite loop - passed
        """
        _list_to_return = []

        _node_root = arg_node_root if arg_node_root else self

        _deque_to_process_nodes = deque( [ _node_root ] )

        while _deque_to_process_nodes :

            item_node = _deque_to_process_nodes.popleft()

            _list_to_return.append( item_node )

            _deque_to_process_nodes.extend( item_node._get_list_of_nodes_next_adjacent() )

        return _list_to_return

    def get_list_of_nodes_traversal_level_order_reversed( self, arg_node_root = None ):
        """
        Returns a list of nodes in the tree, going right, then up.

        Order:

        -Goes bottom-up, right to left.

            0
           / \
          1   2
         / \   \
        3   4   5

        Order: 5 4 3 2 1 0


        Tests and status:

        -List in correct order - passed
        -No infinite loop - passed
        """
        _list_to_return = []

        _node_start = self if arg_node_root == None else arg_node_root

        item_list_layer_of_nodes = [ _node_start ]

        _deque_to_process = deque( [ [ item_list_layer_of_nodes,
                                       -1, # item_index_current
                                       ] ] )

        while _deque_to_process :
            #
            # Get the current layer and current index
            #
            item_list_layer_of_nodes, item_index_current = _deque_to_process.pop()
            #
            # If True, re-add deque. Then add the node's children as another deque.
            #
            # Note about indexes: we can't actually disassemble the layer or else its nodes
            # have to be included too early. Instead, we go backwards, and let the garbage collector
            # dump the list from memory once we're done.
            #
            if abs( item_index_current ) <= len( item_list_layer_of_nodes ) :

                _deque_to_process.append( [ item_list_layer_of_nodes,
                                            #
                                            # Mark this as False, so we can disassemble the dequen on the subsequent pass.
                                            #
                                            item_index_current - 1, # item_bool_check_nodes_next
                                            ] )

                item_node = item_list_layer_of_nodes[ item_index_current ]
                #
                # If item_node is not a leaf node, add its layer
                #
                if item_node.logic_nodes_next_exist() :

                    _deque_to_process.append( [ item_node._get_list_of_nodes_next_adjacent(),
                                                -1, # item_bool_check_nodes_next
                                                ] )

            else :

                _list_to_return.extend( reversed( item_list_layer_of_nodes ) )

        return _list_to_return

    def get_list_of_nodes_traversal_in_order( self, arg_node_root = None ) :
        """
        This method returns a list of nodes.

        The order generally follows these rules:

        -Starts with left-most leaf

        -left child -> parent -> right child


        Strategic considerations:

        -Lower sub-trees tend to appear towards the list's beginning

        -Root node is likely to be somewhere in the middle

        -Right half sub-trees appear to the end of the list

        -Last node is going to be right-most leaf


        Visual example ( source: https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/ ):

            1
           / \
          2   3
         / \   \
        4   5   6

        Order: 4 2 5 1 3 6


        Tests and status:

        -List in correct order - passed
        -No infinite loop - passed
        """
        _list_to_return = [ ]

        _node_root = arg_node_root if arg_node_root else self

        _deque_to_process_nodes = deque( [ [ _node_root,
                                             True, # item_bool_need_to_traverse_left
                                             True, # item_bool_need_to_traverse_right
                                             True, # item_bool_need_to_append_output
                                             ] ] )

        while _deque_to_process_nodes :

            item_node, item_bool_need_to_traverse_left, item_bool_need_to_traverse_right, item_bool_need_to_append_output = _deque_to_process_nodes.pop()

            if item_bool_need_to_traverse_left :

                if item_node._node_next_left :

                    item_bool_need_to_traverse_left = False
                    #
                    # Prep next iteration
                    #
                    _deque_to_process_nodes.append( [ item_node,
                                                      item_bool_need_to_traverse_left,
                                                      item_bool_need_to_traverse_right,
                                                      item_bool_need_to_append_output,
                                                      ] )

                    _deque_to_process_nodes.append( [ item_node._node_next_left,
                                                      True, # item_bool_need_to_traverse_left
                                                      True, # item_bool_need_to_traverse_right
                                                      True, # item_bool_need_to_append_output
                                                      ] )

                    # Skip past storing the node and the right check for now
                    continue

            if item_bool_need_to_append_output :

                item_bool_need_to_append_output = False

                _list_to_return.append( item_node )

            if item_bool_need_to_traverse_right :

                if item_node._node_next_right :

                    item_bool_need_to_traverse_right = False
                    #
                    # Prep next iteration
                    #
                    _deque_to_process_nodes.append( [ item_node,
                                                      item_bool_need_to_traverse_left,
                                                      item_bool_need_to_traverse_right,
                                                      item_bool_need_to_append_output,
                                                      ] )

                    _deque_to_process_nodes.append( [ item_node._node_next_right,
                                                      True, # item_bool_need_to_traverse_left
                                                      True, # item_bool_need_to_traverse_right
                                                      True, # item_bool_need_to_append_output
                                                      ] )

            # Reminder: When we get here, we're done with this node and its children

        return _list_to_return

    def get_list_of_nodes_traversal_post_order( self, arg_node_root = None ):
        """
        Returns a list of nodes.

        Order:

        -Starts with left-most leaf node

        -Left child -> right child -> parent node


        Strategic considerations:

        -Favors children towards the beginning, and parents comes up after them

        -The last item will be the root node


        Visual example ( source: https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/ ):

            1
           / \
          2   3
         / \   \
        4   5   6

        Order: 4 5 2 6 3 1


        Tests and status:

        -List in correct order - passed
        -No infinite loop - passed
        """
        _list_to_return = [ ]

        _node_root = arg_node_root if arg_node_root else self

        _deque_to_process_nodes = deque( [ [ _node_root,
                                             True, # item_bool_need_to_traverse_left
                                             True, # item_bool_need_to_traverse_right
                                             True, # item_bool_need_to_append_output
                                             ] ] )

        while _deque_to_process_nodes :

            item_node, item_bool_need_to_traverse_left, item_bool_need_to_traverse_right, item_bool_need_to_append_output = _deque_to_process_nodes.pop()

            if item_bool_need_to_traverse_left :

                if item_node._node_next_left :

                    item_bool_need_to_traverse_left = False
                    #
                    # Prep next iteration
                    #
                    _deque_to_process_nodes.append( [ item_node,
                                                      item_bool_need_to_traverse_left,
                                                      item_bool_need_to_traverse_right,
                                                      item_bool_need_to_append_output,
                                                      ] )

                    _deque_to_process_nodes.append( [ item_node._node_next_left,
                                                      True, # item_bool_need_to_traverse_left
                                                      True, # item_bool_need_to_traverse_right
                                                      True, # item_bool_need_to_append_output
                                                      ] )

                    # Skip past storing the node and the right check for now
                    continue

            if item_bool_need_to_traverse_right :

                if item_node._node_next_right :

                    item_bool_need_to_traverse_right = False
                    #
                    # Prep next iteration
                    #
                    _deque_to_process_nodes.append( [ item_node,
                                                      item_bool_need_to_traverse_left,
                                                      item_bool_need_to_traverse_right,
                                                      item_bool_need_to_append_output,
                                                      ] )

                    _deque_to_process_nodes.append( [ item_node._node_next_right,
                                                      True, # item_bool_need_to_traverse_left
                                                      True, # item_bool_need_to_traverse_right
                                                      True, # item_bool_need_to_append_output
                                                      ] )

                    continue

            _list_to_return.append( item_node )

            # Reminder: When we get here, we're done with this node and its children

        return _list_to_return

    def get_list_of_nodes_traversal_pre_order( self, arg_node_root = None ):
        """
        This method returns a list of nodes.


        Order:

        -Starts with root

        -Then the left most path from root to the left most leaf

        -Makes its way to the right

        -Node parent -> left child -> left grand child


        Strategic considerations:

        -Starts with root

        -Left most leaves will end up in the middle left

        -Right most leaves will end up in the middle right

        -Right-most leaves will end up further towards the end


        Visual example ( source: https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/ ):

            1
           / \
          2   3
         / \   \
        4   5   6

        Order: 1 2 4 5 3 6


        Tests and status:

        -List in correct order - passed
        -No infinite loop - passed
        """
        _list_to_return = [ ]

        _node_root = arg_node_root if arg_node_root else self

        _deque_to_process_nodes = deque( [ [ _node_root,
                                             True, # item_bool_need_to_traverse_left
                                             True, # item_bool_need_to_traverse_right
                                             True, # item_bool_need_to_append_output
                                             ] ] )

        while _deque_to_process_nodes :

            item_node, item_bool_need_to_traverse_left, item_bool_need_to_traverse_right, item_bool_need_to_append_output = _deque_to_process_nodes.pop()

            if item_bool_need_to_append_output :

                item_bool_need_to_append_output = False

                _list_to_return.append( item_node )

            if item_bool_need_to_traverse_left :

                if item_node._node_next_left :

                    item_bool_need_to_traverse_left = False
                    #
                    # Prep next iteration
                    #
                    _deque_to_process_nodes.append( [ item_node,
                                                      item_bool_need_to_traverse_left,
                                                      item_bool_need_to_traverse_right,
                                                      item_bool_need_to_append_output, ] )

                    _deque_to_process_nodes.append( [ item_node._node_next_left,
                                                      True, # item_bool_need_to_traverse_left
                                                      True, # item_bool_need_to_traverse_right
                                                      True, # item_bool_need_to_append_output
                                                      ] )

                    # Skip past storing the node and the right check for now
                    continue

            if item_bool_need_to_traverse_right :

                if item_node._node_next_right :

                    item_bool_need_to_traverse_right = False
                    #
                    # Prep next iteration
                    #
                    _deque_to_process_nodes.append( [ item_node,
                                                      item_bool_need_to_traverse_left,
                                                      item_bool_need_to_traverse_right,
                                                      item_bool_need_to_append_output, ] )

                    _deque_to_process_nodes.append( [ item_node._node_next_right,
                                                      True, # item_bool_need_to_traverse_left
                                                      True, # item_bool_need_to_traverse_right
                                                      True, # item_bool_need_to_append_output
                                                      ] )

            # Reminder: When we get here, we're done with this node and its children

        return _list_to_return
    #
    # Public - get - node
    #
    def get_node_at_key( self, arg_key, **kwargs ):
        """
        Returns the node located at arg_key via binary search.
        """
        #
        # Setup initial values
        #
        _bool_raise_error_if_node_not_found = kwargs.get( "arg_bool_raise_error_if_node_not_found", True, )

        _value_to_return_if_node_not_found = kwargs.get( "arg_value_to_return_if_node_not_found", None, )

        _node_start = kwargs.get( "arg_node_root", self, )
        #
        # Iterate over tree
        #
        item_node = _node_start

        while True :

            if item_node :

                item_key = item_node._key_unique
                #
                # If key match found, return item_node
                #
                if arg_key == item_key :

                    return item_node
                #
                # Prep next iteration
                #
                elif arg_key > item_key :

                    item_node = item_node._node_next_right

                elif arg_key < item_key :

                    item_node = item_node._node_next_left
            #
            # If item_node is None, either...
            # -Raise error
            # -Return default value
            #
            else :

                if _bool_raise_error_if_node_not_found :

                    self._raise_error_because_key_not_found( arg_key = arg_key,
                                                             arg_node = _node_start, )

                else :

                    return _value_to_return_if_node_not_found
    #
    # Public - insert
    #
    def insert_node( self, arg_node, arg_node_root = None ):
        """
        Inserts node via the value stored in its _key_unique attribute.
        """
        _target_key = arg_node._key_unique

        _node_start = self if arg_node_root == None else arg_node_root
        #
        # Iterate over tree
        # arg_node should insert in all cases, and the loop will exit when that happens
        #
        item_node = _node_start

        while True :

            item_key = item_node._key_unique

            if item_key > _target_key :

                item_node_next = item_node._node_next_left

                if item_node_next :

                    item_node = item_node_next

                else :

                    item_node._node_next_left = arg_node

                    break
            #
            # Check the right node if
            #
            elif item_key < _target_key :

                item_node_next = item_node._node_next_right

                if item_node_next :

                    item_node = item_node_next

                else :

                    item_node._node_next_right = arg_node

                    break
            #
            # If keys match...
            # The general best practice is to append a duplicate key to the right of a node
            #
            else :

                item_node_next = item_node._node_next_right

                if item_node_next :

                    item_node = item_node_next

                else :

                    item_node._node_next_right = arg_node

                    break
    #
    # Public - logic
    #
    def logic_circular_reference_exists( self, arg_node_root = None ):
        """
        Returns True if the algorithm detects a repeated node within the tree.
        """
        _node_start = self if arg_node_root == None else arg_node_root
        #
        # Traverse over tree
        #
        _set_of_nodes_traversed = set()

        _deque_to_process = deque( [ [ _node_start,
                                       None, # item_node_previous
                                       None, # item_key_previous
                                     ] ] )

        while _deque_to_process :

            item_node, item_node_previous, item_key_previous = _deque_to_process.pop()

            if item_node in _set_of_nodes_traversed :

                return True

            else :

                _set_of_nodes_traversed.add( item_node )
            #
            # Prep next iteration
            #
            if item_node._node_next_left :

                _deque_to_process.append( [ item_node._node_next_left,
                                            item_node,
                                            item_node._key_unique, ] )

            if item_node._node_next_right :

                _deque_to_process.append( [ item_node._node_next_right,
                                            item_node,
                                            item_node._key_unique, ] )

    def logic_key_exists( self, arg_key, **kwargs ):
        #
        # Setup initial values
        #
        _node_start = kwargs.get( "arg_node_root", self, )
        #
        # Iterate over tree
        #
        item_node = _node_start

        while True :
            #
            # If item_node is a node, then process its unique key
            #
            if item_node :

                item_key = item_node._key_unique
                #
                # If key match found, return True
                #
                if item_key == arg_key :

                    return True
                #
                # Prep next iteration
                #
                # If item_key is less than arg_key, go right
                #
                elif item_key < arg_key :

                    item_node = item_node._node_next_right
                #
                # If item_key is more than arg_key, go left
                #
                elif item_key > arg_key :

                    item_node = item_node._node_next_left
            #
            # In the case item_node is not viable ( ie None ), return False
            #
            else :

                return False

    def logic_nodes_next_exist( self ):

        return self._node_next_left or self._node_next_right

    def logic_tree_is_balanced( self, arg_node_root = None ) :
        """
        This approach starts from the bottom up in the tree.

        This way initial checks are faster, and fewer node references exist in-memory at
        any given moment.
        """
        _node_start = self if arg_node_root == None else arg_node_root
        #
        # Iterate over tree
        #
        _deque_to_process = deque( [ [ [ _node_start ],
                                       0, # item_index
                                       ] ] )

        while _deque_to_process :

            item_list_of_nodes_at_layer, item_index = _deque_to_process.pop()

            #print( "item_index =", item_index, "\n", )

            #print( "item_index =", item_index, "\n", )
            #print( "item_list_of_nodes_at_layer =", [ item_node._key_unique for item_node in item_list_of_nodes_at_layer ], "\n", )

            if item_index < len( item_list_of_nodes_at_layer ) :
                #
                # Re-append the list at this layer, and increment its index by one
                #
                _deque_to_process.append( [ item_list_of_nodes_at_layer,
                                            item_index + 1,
                                            ] )

                item_node = item_list_of_nodes_at_layer[ item_index ]

                _deque_to_process.append( [ item_node._get_list_of_nodes_next_adjacent(),
                                            0,
                                            ] )

                continue

            else :

                for item_node in item_list_of_nodes_at_layer :

                    if not item_node._logic_is_locally_balanced() :

                        return False

        return True
    #
    # Public - pop
    #
    def pop_node( self, arg_bool_is_left_node_next ):

        if arg_bool_is_left_node_next :

            _node_popped = self._node_next_left

            self._node_next_left = None

        else :

            _node_popped = self._node_next_right

            self._node_next_right = None

        return _node_popped
    #
    # Public - print
    #
    def print_view_left( self, arg_node_root = None ) :
        
        _node_root = arg_node_root if arg_node_root else self

        print( self._get_list_of_nodes_in_view( arg_node_root = _node_root,
                                                arg_bool_is_left_view = True, ) )

    def print_view_right( self, arg_node_root = None ) :
        
        _node_root = arg_node_root if arg_node_root else self

        print( self._get_list_of_nodes_in_view( arg_node_root = _node_root,
                                                arg_bool_is_left_view = False, ) )

    def print_tree( self, arg_names_for_attributes_to_print = None, arg_node_root = None ):
        """
        Prints output for the data tree.

        Example code and output…

        Code:

        _dict_tree = Dict_tree_node()

        _dict_tree.append_path( [ 1, 2, 3, ] )

        _dict_tree.print_tree()

        Output:

        ---PRINTING TREE---

        --- PATH: (root) ---

        --- PATH: 1 ---

        --- PATH: 1.2 ---

        --- PATH: 1.2.3 —

        Code:

        _dict_tree = Dict_tree_node()

        _node = _dict_tree.append_path( [ 1, 2, 3, ] )

        _node.set_object_stored_in_node( "EXAMPLE" )

        _dict_tree.print_tree( arg_names_for_attributes_to_print = "_object_stored_in_node" )

        Output:

        ---PRINTING TREE---

        --- PATH: (root) ---

        _object_stored_in_node = None

        --- PATH: 1 ---

        _object_stored_in_node = None

        --- PATH: 1.2 ---

        _object_stored_in_node = None

        --- PATH: 1.2.3 ---

        _object_stored_in_node = EXAMPLE

        Arguments:

        arg_bool_search_entire_tree - Searches entire tree if True, and only the sub-tree if False.

        arg_names_for_attributes_to_print can be a single string, or a list of strings. This will include the attributes in the print output.

        arg_bool_path_is_absolute - If True, starts from the entire tree's root node. If False, the method focuses on the children in
        the sub tree.
        """
        _list_of_names_for_attributes_to_print = sorted( self._get_list_converted_from_object( arg_names_for_attributes_to_print ) )

        print( "---PRINTING TREE---\n" )

        _stack_to_process_pairs_paths_and_nodes = deque( [ [ [],
                                                             arg_node_root if arg_node_root else self,
                                                             ] ] )

        while _stack_to_process_pairs_paths_and_nodes :

            item_path, item_node = _stack_to_process_pairs_paths_and_nodes.pop()

            if _list_of_names_for_attributes_to_print == None :

                self._print_node( arg_path = item_path,
                                  arg_node = item_node, )

            else :

                self._print_node( arg_path = item_path,
                                  arg_node = item_node,
                                  arg_list_of_names_for_attributes_to_print = _list_of_names_for_attributes_to_print, )

            if item_node._node_next_left :

                _stack_to_process_pairs_paths_and_nodes.append( [ [ *item_path, "left", ],
                                                                  item_node._node_next_left, ] )

            if item_node._node_next_right :

                _stack_to_process_pairs_paths_and_nodes.append( [ [ *item_path, "right", ],
                                                                  item_node._node_next_right, ] )
    #
    # Public - raise
    #
    def raise_error_if_circular_reference_detected( self, arg_node_root, arg_node_previous, arg_node_repeated, arg_key_to_node_repeat ):
        """
        Raises an error with comprehensive information if the tree has a repeated node.
        """
        if self.logic_circular_reference_exists( arg_node_root ) :

            print( "Error: circular reference detected.\n" )

            print( "arg_node_previous =", arg_node_previous, "\n", )

            print( "arg_node_previous._key_unique =", arg_node_previous._key_unique, "\n", )

            print( "arg_node_repeated =", arg_node_repeated, "\n", )

            print( "arg_node_repeated._key_unique =", arg_node_repeated._key_unique, "\n", )

            print( "arg_key_to_node_repeat =", arg_key_to_node_repeat, "\n", )

            print( "\n\n" )

            _set_of_nodes_checked = set()

            _deque_to_process = deque( [ arg_node_root ] )

            while _deque_to_process :

                item_node = _deque_to_process.pop()

                _set_of_nodes_checked.add( item_node )

                print( "item_key =", item_node._key_unique, "\n", )

                if item_node._node_next_left :

                    print( "item_key_left =", item_node._node_next_left._key_unique, "\n", )

                    if not item_node._node_next_left in _set_of_nodes_checked :

                        _deque_to_process.append( item_node._node_next_left )

                    else :

                        print( "error: node already checked =", item_node._node_next_left._key_unique, "\n", )

                else :

                    print( "item_key_left =", None, "\n", )

                if item_node._node_next_right :

                    print( "item_key_right =", item_node._node_next_right._key_unique, "\n", )

                    if not item_node._node_next_right in _set_of_nodes_checked :

                        _deque_to_process.append( item_node._node_next_right )

                    else :

                        print( "error: node already checked =", item_node._node_next_right._key_unique, "\n", )

                else :

                    print( "item_key_right =", None, "\n", )

                print( "\n\n\n" )

            self._raise_error()
    #
    # Private
    #
    #
    # Private - get
    #
    def _get_list_of_nodes_in_view( self, arg_node_root, arg_bool_is_left_view ):
        """
        Returns list of nodes on either the left or right side of arg_node_root in the tree.
        """
        _list_to_return = []
        #
        # Iterate over tree
        #
        item_node = arg_node_root

        while item_node :

            _list_to_return.append( item_node._object_stored_in_node )
            #
            # Prep next iteration
            #
            if arg_bool_is_left_view :

                item_node = item_node._node_next_left

            else :

                item_node = item_node._node_next_right
        #
        # Return list
        #
        return _list_to_return

    def _get_list_of_nodes_next( self, **kwargs ) :
        """
        Returns list of child nodes

        Unlike the traversal methods, this supports distinguishing between the sub-tree and immediate children.
        """
        #
        # If arg_bool_search_entire_sub_tree is True, then get list of nodes in subtree.
        #
        if kwargs.get( "arg_bool_search_entire_sub_tree", False, ) :

            _list_to_return = []

            _deque_to_process_nodes = [ self ] \
                                      if kwargs.get( "arg_bool_include_node_current", True, ) \
                                      else [ self._node_next_left,
                                             self._node_next_right, ]

            while _deque_to_process_nodes :

                item_node = _deque_to_process_nodes.pop()
                #
                # Append node to return list
                #
                _list_to_return.append( item_node )
                #
                # Prep next iteration
                #
                _deque_to_process_nodes.extend( item_node._get_list_of_nodes_next_adjacent() )
            #
            # Return list after all nodes traversed.
            #
            return _list_to_return
        #
        # If arg_bool_search_entire_sub_tree is False, only return the immediate nodes.
        #
        else :

            return self._get_list_of_nodes_next_adjacent()

    def _get_list_of_nodes_next_adjacent( self ):
        """
        This method gets a list of only the node's immediate children.

        Note:

        Time tests gives this approach a slight advantage over creating an empty list
        and adding nodes if they exist.
        """
        if self._node_next_left and self._node_next_right :

            return [ self._node_next_left,
                     self._node_next_right, ]

        else :

            if self._node_next_left :

                return [ self._node_next_left ]

            elif self._node_next_right :

                return [ self._node_next_right ]

            else :

                return [ ]
    #
    # Private - logic
    #
    def _logic_is_locally_balanced( self ):
        """
        Returns True if heights for both left and right sides have difference counts equal to or
        less than one.
        """
        #
        # If both nodes are None, then this node is balanced. Return True.
        #
        if not self._node_next_left and not self._node_next_right :

            return True

        else :
            #
            # If both node children exist, compare their heights.
            # The threshold for allowing differences is 1. If their difference exceeds this number
            # then return False. Otherwise, return True.
            #
            if self._node_next_left and self._node_next_right :

                return abs( self._node_next_left.get_int_height() - self._node_next_right.get_int_height() ) <= 1
            #
            # By this stage, either one child or the other exists.
            #
            else :
                #
                # Identify which child exists.
                #
                _node = self._node_next_left if self._node_next_left else self._node_next_right
                #
                # Once its confirmed this child exists, check its height. This height needs to be
                # equal or less than one.
                #
                # Reminder: get_int_height() includes the root node for the count.
                #
                return _node.get_int_height() <= 1
    #
    # Private - raise
    #
    def _raise_error_because_key_not_found( self, arg_key, arg_node ):
        """
        Raise an error if the key doesn't exist in tree.
        """
        print( "Error: arg_key not found in tree.\n" )

        print( "arg_key =", arg_key, "\n", )

        _bool_key_exists = self.logic_key_exists( arg_key = arg_key,
                                                  arg_node_root = arg_node, )

        print( "Is key in tree?", _bool_key_exists, "\n", )

        _list_of_keys = self.get_list_of_keys()

        self.print_object( arg_object = _list_of_keys,
                           arg_name_for_object = "_list_of_keys", )

        self._raise_error()
    #
    # Private - setup
    #
    def __init__(self, **kwargs):

        super().__init__( **kwargs )
        #
        # This key is meant to be unique, but it won't crash the tree outright if used. The general practice
        # is the tree puts duplicates to the right of duplicate keys.
        #
        # Reminders ( 07/08/19 ): The library does not account for these duplicates in its searches, and continues
        # to return the first key with the searched value.
        #
        self._key_unique = kwargs[ "arg_key_unique" ] if "arg_key_unique" in kwargs.keys() else id( self )
        #
        # This links to the left and right children, respectively.
        # In most cases, the left child's key should always be lower than the parent nodes, and the right child's key,
        # higher than the parent.
        #
        # Reminder: append_node() allows for brute forcing child nodes onto its parent, which can lead to situations where
        # the tree won't be properly organized.
        #
        self._node_next_left = None

        self._node_next_right = None
    #
    # Specialized internal methods for debugging
    #
    def _debug_get_tree_mimicking_visual_example( self, **kwargs ):
        """
        This is a debugging tree meant to provide different test cases.

        if arg_bool_needs_to_be_simple :

            0
           / \
          1   2
         /
        3


        if arg_bool_tree_needs_to_be_balanced == True...

        Visual example:

            0
           / \
          1   2
         / \   \
        3   4   5

        else...

        Create a really unbalanced tree.

        Visual example:

            0
           / \
          1   2
         / \   \
        3   4   5
                 \
                  6
                   \
                    7
                     \
                      8
                       \
                        9

        Note about the above tree setup:

        The right side is longer since in most traversals, right-most nodes tend to be traversed later
        than the left. In test cases, I don't want the library potentially benefiting from an earlier technical
        issue, versus a later one, which can also corrupt the left side.

        Reminder:

        The key order at every level goes from left to right.
        """
        #
        # All test trees have at least these first nodes
        #
        # Reminder: In all cases, every tree has same three keys in the same three positions
        #
        # Node zero
        #
        _node_zero = Data_tree_binary_search_node( arg_key_unique = 0 )
        #
        # Node one
        #
        _node_one = Data_tree_binary_search_node( arg_key_unique = 1 )
        _node_zero.append_node( arg_node_next = _node_one,
                                arg_bool_is_left_side = True, )
        #
        # Node two
        #
        _node_two = Data_tree_binary_search_node( arg_key_unique = 2 )
        _node_zero.append_node( arg_node_next = _node_two,
                                arg_bool_is_left_side = False, )
        #
        # Assess boolean arguments
        #
        _bool_needs_to_be_simple = kwargs.get( "arg_bool_needs_to_be_simple", False, )

        _bool_tree_needs_to_be_unbalanced = kwargs.get( "arg_bool_tree_needs_to_be_unbalanced", False, )
        #
        # Adjust tree
        #
        if _bool_needs_to_be_simple :
            #
            # _bool_needs_to_be_simple - yes, _bool_tree_needs_to_be_balanced - yes
            #
            if _bool_tree_needs_to_be_unbalanced :
                #
                # Node three
                #
                # This this creates an additional node on the left for challenging any "is balanced" algorithm.
                #
                # Reminder: This moves node 3 to the right side, and appends 4 to it, to guarantee the tree is unbalanced,
                # while keeping complexity to a minimum
                #
                _node_three = Data_tree_binary_search_node( arg_key_unique = 3 )
                _node_two.append_node( arg_node_next = _node_three,
                                       arg_bool_is_left_side = False, )
                #
                # Node four
                #
                _node_four = Data_tree_binary_search_node( arg_key_unique = 4 )
                _node_three.append_node( arg_node_next = _node_four,
                                         arg_bool_is_left_side = False, )
            #
            # _bool_needs_to_be_simple - yes, _bool_tree_needs_to_be_balanced - no
            #
            else :
                #
                # Node three
                #
                # This this creates an additional node on the left for challenging any "is balanced" algorithm.
                #
                # Reminder: This goes on the left, instead of right, to support quick checks on left side
                #
                _node_three = Data_tree_binary_search_node( arg_key_unique = 3 )
                _node_one.append_node( arg_node_next = _node_three,
                                       arg_bool_is_left_side = True, )

        else :
            #
            # _bool_needs_to_be_simple - no, _bool_tree_needs_to_be_balanced - yes
            #
            # Reminder: happens in all events where _bool_needs_to_be_simple is False
            #
            # Node three
            #
            # This this creates an additional node on the left for challenging any "is balanced" algorithm.
            #
            _node_three = Data_tree_binary_search_node( arg_key_unique = 3 )
            _node_one.append_node( arg_node_next = _node_three,
                                   arg_bool_is_left_side = True, )
            #
            # Node four
            #
            _node_four = Data_tree_binary_search_node( arg_key_unique = 4 )
            _node_one.append_node( arg_node_next = _node_four,
                                   arg_bool_is_left_side = False, )
            #
            # Node five
            #
            _node_five = Data_tree_binary_search_node( arg_key_unique = 5 )
            _node_two.append_node( arg_node_next = _node_five,
                                   arg_bool_is_left_side = False, )
            #
            # _bool_needs_to_be_simple - no, _bool_tree_needs_to_be_balanced - no
            #
            # Reminders:
            # -Unbalances complex tree
            # -Intentionally nested within the if statement above
            #
            if _bool_tree_needs_to_be_unbalanced :
                #
                # Node six
                #
                _node_six = Data_tree_binary_search_node( arg_key_unique = 6 )
                _node_five.append_node( arg_node_next = _node_six,
                                        arg_bool_is_left_side = False, )
                #
                # Node seven
                #
                _node_seven = Data_tree_binary_search_node( arg_key_unique = 7 )
                _node_six.append_node( arg_node_next = _node_seven,
                                       arg_bool_is_left_side = False, )
                #
                # Node eight
                #
                _node_eight = Data_tree_binary_search_node( arg_key_unique = 8 )
                _node_seven.append_node( arg_node_next = _node_eight,
                                         arg_bool_is_left_side = False, )
                #
                # Node nine
                #
                _node_nine = Data_tree_binary_search_node( arg_key_unique = 9 )
                _node_eight.append_node( arg_node_next = _node_nine,
                                         arg_bool_is_left_side = False, )
        #
        # Return root node
        #
        return _node_zero
#
# Test area
#
if __name__ == "__main__" :

    _node_root = Data_tree_binary_search_node( arg_key_unique = "root" )

    _node_root_test_tree = _node_root._debug_get_tree_mimicking_visual_example( arg_bool_needs_to_be_simple = False,
                                                                                arg_bool_tree_needs_to_be_unbalanced = True, )
    #
    # Re-balance the tree
    #
    _node_root = _node_root_test_tree.balance_tree()

    _node_root.logic_circular_reference_exists()

    _node_root.print_tree( arg_names_for_attributes_to_print = [ "_key_unique" ], )



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





















































''''''
#
# Libraries - native
#
import warnings
#
# Libraries - custom
#
# This suppresses a deprecation warning:
# DeprecationWarning: Deprecated since Python 3.4. Use importlib.util.find_spec() instead.
# This warning is related to setuptools, and its a known python issue.
with warnings.catch_warnings() :

    warnings.simplefilter( "ignore",
                           category = DeprecationWarning, )
    #
    # Here for general support
    #
    from .src.base_data_node import Base_data_node

    from .src.data_tree_binary_search_node import Data_tree_node_binary



-----EXPERIMENTAL-----
-----EXPERIMENTAL-----
-----EXPERIMENTAL-----
-----EXPERIMENTAL-----
James Hazlett
james.hazlett.python@gmail.com

Welcome to the "data structure experimental" repository.

This repository exists as an experimental counterpart to the main package: https://github.com/jrhazlett/data-tree

Due to popular demand, I've adapted multiple algorithms to the stack recursion approach, as opposed to method recursion.
As mentioned in the other package, I found this approach to be significantly faster (by almost 3x) than the conventional
method-based approaches.


Data structures covered:

-Binary search tree
-Graph


TABLE OF CONTENTS

CONTACT INFORMATION
DISCLAIMERS
INSTALLATION
CLASS SUMMARIES
PERFORMANCE NOTES
LICENSE (MIT)


CONTACT INFORMATION

James Hazlett
james.hazlett.python@gmail.com


Feel free to reach out via email with library-related questions, suggestions, feature requests, cool ideas,
stories about how it helped you, something I might find interesting (wildly subjective, I know), etc.

Also, once I get this up on github, I want it open to community input.

Fair warning (only because its necessary): Any emails with easily Google-able questions about the Python language
will be ignored outright.


DISCLAIMERS

The objects and their methods are nowhere near tested as extensively as the main library, and exists in a purely
experimental state.

For this reason, its not included as part of the main package, nor does it have its own package on pypi.

Since the code does not exist in a steady state for this repository, there are no plans to add extensive documentation
here. The code itself remains extensively commented though.


INSTALLATION

The only supported approach is to download the source from github.


CLASS SUMMARIES

Binary search tree

This structure sets up a binary search tree with much of the expected functionality, but I still don't consider it
"production ready."

Overall functionality covered so far:

-Balancing

-Binary search

-Insert

-Traversals
--Level order
--Level order reversed
--In order
--Post-order
--Pre-order


Graph

-Count edges

-Count vertices

-Get list of nodes

-Get node at path

-Setup graph based on data structure
--Support for matrices
--Other graphs


PERFORMANCE NOTES


Overall

-All classes dump method recursion for stack recursion, granting about a 3x speed boost (even compiled)


Binary search tree

-Speed tests across large volumes tend to favor the "\\" operator for rounding down, over int().

-Methods dependent on height comparisons take a "bottom-up" approach.

This approach has the algorithm check the nodes with the smallest heights to analyze first. As the checks
get longer, the approach becomes more likely to report the tree is balanced. This way, an unbalance tree
is likely to confirm its status quickly.

In cases where both approaches would report a balanced tree, there's no time difference.


Graph

-Graph traversals use sets for rapidly checking if a node was already covered earlier. This uses CPython's
default instance ids.


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
























































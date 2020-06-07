This is a pure python3 implementation of a classic (non left-leaning)
red-black tree, based upon [Stanislav
Kozlovski's](https://github.com/stanislavkozlovski/Red-Black-Tree) well
documented and tested implementation. I kept those comments, but made the code
more "production ready". Not saying that it is, though. Some quick tests
indicate a 30% speedup over the original code, but it is still far from
optimized. My changes are merely the result of me trying to understand and
clean up the code in order to use it in a personal project. My changes
include:

* Made most of the code PEP8 and pylint comformal.
* Added type hints and asserts.
* Matched interface to Python's built-in containers,
    particularly by making use of "underscore" functions.
* Fixed some bad code smells:
    - A node's color is now a bool instead of a string.
    - There is no NIL node anymore. Leafs just have None as children.
    - Replaced recursion with iteration.
    - Many smaller local improvements.
* Added a few more functions, such as:
    - Reverse iteration
    - Get neighbor nodes
    - To string method
* Opened up the interface a bit to aid extension and quicker access to
    stored information. For example, the insert method returns the
    constructed tree node.
* Merged some internal methods to simplify the code. The methods for each
    of the rebalancing cases for example were separate for easier to
    understand documentation, but I found it actually harder to understand
    the code that way, because code lines that should be together were far
    apart.
* Added a tree dictionary subclass.

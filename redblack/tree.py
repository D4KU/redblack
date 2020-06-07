from __future__ import annotations

from itertools import takewhile
from typing import (
    Callable,
    ClassVar,
    Collection,
    Generic,
    Iterable,
    Iterator,
    List,
    NewType,
    Optional,
    Reversible,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
    )


K = TypeVar('K')  # Key Type


class Node(Generic[K]):
    """
    Node forming a red-black tree.
    """
    __slots__ = ('key', 'red', 'parent', 'left', 'right')

    def __init__(
            self,
            key: K,
            red: bool = False,
            parent: Optional[Node] = None,
            left: Optional[Node] = None,
            right: Optional[Node] = None,
            ):
        """
        :param key: Value after which nodes in the tree are sorted.
            Key's type must be comparable.
        :param red: True if node is initialized as red, False if black
        :param parent: Parent node
        :param left: left child
        :param right: right child
        """
        self.key = key
        self.red = red
        self.parent = parent
        self.left = left
        self.right = right

    def __str__(self) -> str:
        """
        Print own key with color as suffix (R = red)
        """
        color = "R" if self.red else "B"
        return f"{self.key}{color}"

    def __iter__(self) -> Iterator[Node]:
        stack: List[Node] = []
        cur: Optional[Node] = self
        while stack or cur:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            yield cur
            cur = cur.right

    def __reversed__(self) -> Iterator[Node]:
        stack: List[Node] = []
        cur: Optional[Node] = self
        while stack or cur:
            while cur:
                stack.append(cur)
                cur = cur.right
            cur = stack.pop()
            yield cur
            cur = cur.left

    def __eq__(self, other: object) -> bool: return self.key == other
    def __ne__(self, other: object) -> bool: return self.key != other
    def __lt__(self, other: object) -> bool: return self.key < other
    def __gt__(self, other: object) -> bool: return self.key > other
    def __le__(self, other: object) -> bool: return self.key <= other
    def __ge__(self, other: object) -> bool: return self.key >= other

    @property
    def has_children(self) -> bool:
        """
        Returns True if the node has any children.
        """
        return bool(self.child_count)

    @property
    def child_count(self) -> int:
        """
        Returns the number of children the node has.
        """
        return int(bool(self.left)) + int(bool(self.right))


# Node = TypeVar('N', bound=Node)  # Node Type
ON = Optional[Node]  # Node or None
Side = NewType("Side", str)  # string 'R' for right, 'L' for left


class Tree(Collection, Reversible):
    """
    Not-left-leaning Red-black tree implementation supporting
    insertion, removal, (reverse) iteration, and neighbor search.
    Can be used a self-sorting containers that only allow unique items.
    """
    # Type of nodes to construct. Can be overridden in child classes.
    nodetype: ClassVar[Type[Node]] = Node

    def __init__(self, root: ON = None, keys: Iterable[K] = []):
        """
        :param root: Initialize the tree from an already existing one.
            Passing a root node make this tree contain all that nodes'
            children.
        :param keys: Initialize the tree with a node for each passed
            key. If a root was also passed, these nodes will be added
            to 'root' and its children, if they don't already contain
            keys from the list. Note that the tree rebalances after
            each added node, so the passed root node may not end up as
            such in the end.
        """
        self.root = root
        self._len = 0
        if root:
            for n in root:
                self._len += 1
        for k in keys:
            self.insert(k)

    def __len__(self) -> int:
        return self._len

    def __str__(self) -> str:
        return ' '.join(map(str, self))

    def __iter__(self) -> Iterator[Node]:
        if self.root:
            yield from iter(self.root)

    def __reversed__(self) -> Iterator[Node]:
        if self.root:
            yield from reversed(self.root)

    @property
    def first(self) -> Optional[Node]:
        """
        Return the lowest-key tree node, or None if tree is empty.
        """
        n: Optional[Node] = self.root
        if not n:
            return None
        while n.left:
            n = n.left
        return n

    @property
    def last(self) -> Optional[Node]:
        """
        Return the highest-key tree node, or None if tree is empty.
        """
        n: Optional[Node] = self.root
        if not n:
            return None
        while n.right:
            n = n.right
        return n

    @overload
    def __getitem__(self, key: slice) -> List[Node]:
        pass

    @overload
    def __getitem__(self, key: K) -> Node:
        pass

    def __getitem__(self, key: Union[K, slice]) -> Union[Node, List[Node]]:
        if isinstance(key, slice):
            if key.step is not None:
                raise NotImplementedError(
                    "Slice steps are not implemented"
                    )
            begin = None
            if key.start is not None:
                _, begin = self.floor_and_ceil(key.start)
                if begin is None:
                    # Given key is bigger than any in tree.
                    return []
            end = None if key.stop is None else \
                self.floor_and_ceil(key.stop)[1]
            return [n for n in self._iter_slice(begin, end)]
        else:
            node = self.root
            while node:
                if key < node.key:
                    node = node.left
                elif key > node.key:
                    node = node.right
                else:
                    return node
            raise KeyError(key)

    def __delitem__(self, key: K) -> Node:
        return self.remove(self[key])

    def __contains__(self, key: K) -> bool:
        try:
            self[key]
        except KeyError:
            return False
        return True

    def keys(self) -> Iterator[K]:
        """
        Yield an iterator over all the tree's keys
        """
        if self.root:
            for node in self.root:
                yield node.key

    def _iter_slice(
            self,
            start: ON = None,
            stop: ON = None,
            ) -> Iterator[Node]:
        """
        Iterate over the tree's nodes in-order, starting from the given
        node until the end or the passed stop node is hit. The stop node
        is not yielded in this case.

        If None is passed for 'start', iteration begins at the
        lowest-key node in the tree. If None is passed for 'stop',
        iteration continues until the highest-key node was yielded.
        """
        if start is None:
            # search for lowest-key node
            start = self.first
        # test again if there is actually a minimal node
        if start is not None:
            if stop is None:
                yield from self.iter_from(start)
            else:
                yield from takewhile(
                    lambda x: x is not stop,
                    self.iter_from(start),
                    )

    def iter_from(self, start: Node) -> Iterator[Node]:
        """
        Iterate over the tree's nodes in-order, starting from the given
        node.
        """
        n: ON = start
        while n:
            if n >= start:
                yield n
                if n.right:
                    try:
                        yield from iter(n.right)
                    except StopIteration:
                        pass
            n = n.parent

    def reverse_from(self, start: Node) -> Iterator[Node]:
        """
        Iterate over the tree's nodes in reverse order, starting from
        the given node.
        """
        n: ON = start
        while n:
            if n <= start:
                yield n
                if n.left:
                    try:
                        yield from reversed(n.left)
                    except StopIteration:
                        pass
            n = n.parent

    def insert(self, key: K) -> Tuple[Node, bool]:
        """
        Add a new node to the tree. If the key is already present in
        the tree, return a tuple of the already existent node and False.
        Otherwise, return the newly added node and True.
        :return: (node, bool)
        """
        if not self.root:
            self.root = self.nodetype(key=key)
            self._len += 1
            return self.root, True

        parent, side = self._find_parent(key)
        if not side:
            # Key is already in the tree
            return parent, False

        new_node = self.nodetype(
            key=key,
            red=True,
            parent=parent,
        )

        if side == 'L':
            parent.left = new_node
        else:
            parent.right = new_node

        self._try_rebalance(new_node)
        self._len += 1
        return new_node, True

    def remove(self, node: Node) -> Node:
        """
        Remove the given node from the tree.
        """
        if node.child_count > 1:
            # remove the in-order successor instead
            succ = node.right
            assert succ

            while succ.left:
                succ = succ.left

            # but keep its key
            self._copy_node_attr(succ, node)
            node = succ

        self._remove(node)
        self._len -= 1
        return node

    def _copy_node_attr(self, source: Node, target: Node) -> None:
        """
        Copy over all "cargo" attributes from source to target. Those
        are attributes that actually store information and are not just
        for creating a tree structure.
        """
        target.key = source.key

    def _remove(self, node: Node) -> None:
        """
        Remove a node with one child or less from the tree.
        """
        if not node.red:
            child = node.left if node.left else node.right
            if node is self.root:
                if child:
                    # If the root gets removed and it has one valid
                    # child, simply make that child the root.
                    self.root = child
                    self.root.parent = None
                    self.root.red = False
                else:
                    self.root = None
                return
            if child and child.red:
                # Swap the keys with the red child. Since we're at a
                # node with one child only, it's ensured that there
                # are no nodes below the red child.
                self._copy_node_attr(child, node)
                node.left = child.left
                node.right = child.right
                return
            else:
                # Loop through each case until we're left with a leaf
                # node removable without consequences.
                self._prepare_removal(node)
        # Remove leaf node
        assert node.parent
        if node is node.parent.right:
            node.parent.right = None
        else:
            assert node is node.parent.left
            node.parent.left = None

    def floor_and_ceil(self, key: K) -> Tuple[ON, ON]:
        """
        For a given key, return its floor and ceil nodes in the tree.
        Floor is a node with a key less equal the given key.
        Ceil is a node with a key greater equal the given key.
        Both nodes are the same if the tree contains a key matching
        the given one.
        None is returned for the respective node, if it wasn't found.
        For example, when a key greater than any contained in the tree
        is given or the tree is empty, there is no ceil node.
        :return (floor node, ceil node):
        """
        i, floor, ceil = self.root, None, None
        while i:
            if key > i.key:
                floor = i
                i = i.right
            elif key < i.key:
                ceil = i
                i = i.left
            else:
                return i, i
        return floor, ceil

    def get_neighbors(self, key: K) -> Tuple[ON, ON]:
        """
        For a given key, return its predecessor and successor node in
        the tree. This functions differs from floor_and_ceil() only
        when a key equal to the passed one already exists in the tree.
        In this case, this function does not return the same node two
        times.
        None is returned for the respective node if it wasn't found. For
        example, when a key greater than any contained in the tree is
        given or the tree is empty, there is no successor node.
        :return (predecessor node, successor node):
        """
        i, prev, succ = self.root, None, None
        while i:
            if key > i.key:
                prev = i
                i = i.right
            elif key < i.key:
                succ = i
                i = i.left
            else:
                prev = i.left
                while prev:
                    prev = prev.right
                succ = i.right
                while succ:
                    succ = succ.left
                break
        return prev, succ

    def _find_parent(self, key: K) -> Tuple[Node, Optional[Side]]:
        """
        Find the right parent for a given key as well as
        the side the new node should be on.
        If a node with the given key already exists, then
        'node' points to this node and 'side' is None.
        Otherwise, 'node' points to a suitable parent and
        'side' equals 'L' or 'R'.
        Raises AssertError if tree is empty.
        :return: (node, side)
        """
        assert self.root is not None
        node = self.root
        side = None
        while node:
            if key < node.key:
                if node.left:
                    node = node.left
                else:
                    return node, Side('L')
            elif key > node.key:
                if node.right:
                    node = node.right
                else:
                    return node, Side('R')
            else:
                break
        return node, side

    def _get_sibling(self, node: Node) -> Tuple[ON, Side]:
        r"""
        Returns the sibling of the node, as well as the side it is on.
        Raises AssertError if root is passed.

            20(A)
           /    \
        15(B)   25(C)

        _get_sibling(25(C)) => 15(B), 'R'
        """
        parent = node.parent
        assert parent
        if node is parent.left:
            return parent.right, Side('R')
        else:
            assert node is parent.right
            return parent.left, Side('L')

    def _prepare_removal(self, node: Node) -> None:
        if node is self.root:
            # CASE 1
            return

        parent = node.parent
        sibling, side = self._get_sibling(node)
        assert parent and sibling

        if parent.red:
            # CASE 4
            if (not sibling.red
                    and _not_red(sibling.left)
                    and _not_red(sibling.right)
                    ):
                # switch colors
                parent.red, sibling.red = sibling.red, parent.red
                return
        else:
            # CASE 2
            if _not_red(sibling.left) and _not_red(sibling.right):
                if sibling.red:
                    self._side_to_rot(side)(sibling, parent)
                    parent.red = True
                    sibling.red = False
                    self._prepare_removal(node)
                    return
                # CASE 3
                # Color the sibling red and forward the double black
                # node upwards (call the cases again for the parent)
                sibling.red = True
                self._prepare_removal(parent)
                return

        # CASE 5
        if side == 'L':
            inner = sibling.right
            outer = sibling.left
        else:
            inner = sibling.left
            outer = sibling.right

        if (inner
                and inner.red
                and _not_red(outer)
                and not sibling.red
                ):
            if side == 'L':
                self._rotate_left(inner, sibling)
            else:
                self._rotate_right(inner, sibling)
            inner.red = False
            sibling.red = True

        # CASE 6
        sibling, side = self._get_sibling(node)
        assert sibling
        nephew = sibling.left if side == 'L' else sibling.right
        assert not sibling.red
        assert nephew
        assert nephew.red
        assert sibling.parent

        parent_red = sibling.parent.red
        self._side_to_rot(side)(sibling, sibling.parent)
        assert sibling.left
        assert sibling.right

        # new parent is sibling
        sibling.red = parent_red
        sibling.right.red = False
        sibling.left.red = False

    def _try_rebalance(self, node: Node) -> None:
        """
        Given a red child node, determine if there is a need to
        rebalance (if the parent is red). If there is, rebalance it.
        """
        parent = node.parent
        if (_not_red(node)
                or _not_red(parent)
                or parent is self.root
                ):
            # no need to rebalance
            return

        assert parent
        grampa = parent.parent
        assert grampa

        if grampa > parent:
            parent_side = 'L'
            uncle = grampa.right
        else:
            parent_side = 'R'
            uncle = grampa.left

        node_side = 'L' if parent > node else 'R'
        side = node_side + parent_side

        if uncle and uncle.red:
            grampa.red = grampa is not self.root
            assert grampa.left
            assert grampa.right
            grampa.right.red = False
            grampa.left.red = False
            self._try_rebalance(grampa)
        else:
            if side == 'LL':
                self._rotate_right(parent, grampa)
                node.red = True
                parent.red = False
            elif side == 'RR':
                self._rotate_left(parent, grampa)
                node.red = True
                parent.red = False
            elif side == 'LR':
                self._rotate_right(node, parent)
                # Node is now the parent.
                self._rotate_left(node, grampa)
                parent.red = True
                node.red = False
            else:
                assert side == 'RL'
                self._rotate_left(node, parent)
                # Node is now the parent.
                self._rotate_right(node, grampa)
                parent.red = True
                node.red = False
            grampa.red = True

    def _rotate_right(self, a: Node, b: Node) -> None:
        self._set_parent(child=a, parent=b.parent)
        tmp = a.right
        a.right = b
        b.parent = a
        b.left = tmp
        if tmp:
            tmp.parent = b

    def _rotate_left(self, a: Node, b: Node) -> None:
        self._set_parent(child=a, parent=b.parent)
        tmp = a.left
        a.left = b
        b.parent = a
        b.right = tmp
        if tmp:
            tmp.parent = b

    def _set_parent(self, child: Node, parent: Optional[Node]) -> None:
        """
        Assigns a new parent to 'child' and links 'child' in 'parent'
        correctly.
        If 'parent' is None, 'child' becomes the tree's root.
        """
        child.parent = parent
        if parent:
            if parent > child:
                parent.left = child
            else:
                assert parent != child
                parent.right = child
        else:
            self.root = child

    def _side_to_rot(self, side: Side) -> Callable[[Node, Node], None]:
        """Translates a side into a rotation function"""
        return self._rotate_right if side == 'L' else self._rotate_left


def _not_red(node: Optional[Node]) -> bool:
    """Returns True if node is None or black"""
    return not (node and node.red)


r"""
Case 1 applies when there's a double black node at the root.
Because it's the root, we can simply remove it and reduce
the black height of the whole tree.

    __|10B|__                  __10B__
   /         \      ==>       /       \
  9B         20B            9B        20B



Case 2 applies when
    the parent is black
    the sibling is red
    the sibling's children are black or NIL
It takes the sibling and rotates it

                     40B
                    /   \       --CASE 2 ROTATE-->
                |20B|   60R       LEFT ROTATE
DBL BLACK IS 20----^   /   \      SIBLING 60R
                     50B    80B

       60B
      /   \
    40R   80B
   /   \
|20B|  50B

(If the sibling's side was left of it's parent,
we would right rotate it)

Now the original node's parent is red and we can apply case
4 or case 6.



Case 3 deletion is when:
    the parent is black
    the sibling is black
    the sibling's children are black
Then, we make the sibling red and
pass the double black node upwards

                    Parent is black
       ___50B___    Sibling is black
      /         \   Sibling's children are black
   30B          80B        CASE 3
  /   \        /   \        ==>
20B   35R    70B   |90B|<---remove
      /  \
    34B   37B

      ___50B___
     /         \
   30B        |80B|
  /  \        /  \
20B  35R     70R  x
    /   \
  34B   37B



If the parent is red and the sibling is black with no red
children, simply swap their colors

DB-Double Black
        __10R__                   __10B__
       /       \                 /       \
     DB        15B      ===>    X        15R
              /   \                     /   \
            12B   17B                 12B   17B

The black height of the left subtree has been incremented and
the one below stays the same. No consequences, we're done!



Case 5 is a rotation that changes the circumstances so that we
can do a case 6. If the closer node is red and the outer black
or NIL, we do a left/right rotation, depending on the
orientation. This will showcase when the closer node's
side is right.

      ___50B___
     /         \
   30B        |80B|  <-- Double black
  /  \        /   \      Closer node is red (35R)
20B  35R     70R   X     Outer is black (20B)
    /   \                So we do a LEFT ROTATION
  34B  37B               on 35R (closer node)

           __50B__
          /       \
        35B      |80B|   Case 6 is now
       /   \      /      applicable here,
    30R    37B  70R      so we redirect the node
   /   \                 to it
20B   34B



Case 6 requires sibling to be black, outer node to be red.
Then, does a right/left rotation on the sibling.
This will showcase when the sibling's side is left.

                        Double Black
                __50B__       |
               /       \      |
  SIBLING--> 35B      |80B| <-
            /   \      /
         30R    37B  70R
        /   \
     20B   34B

Outer node is red, closer node doesn't matter, parent doesn't
matter. So we do a right rotation on 35B!

          __35B__
         /       \
       30R       50R
      /   \     /   \
    20B   34B 37B    80
                     /
                   70R
"""

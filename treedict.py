from typing import (
    Callable,
    ClassVar,
    Generic,
    Iterator,
    Mapping,
    MutableMapping,
    Optional,
    Tuple,
    Type,
    TypeVar,
    )

from .tree import K, Node, Tree

V = TypeVar('V')  # Value Type


class DictNode(Node, Generic[V]):
    """
    Node forming a dictionary based on a red-black tree. It stores a key
    for sorting and a value for arbitrary cargo information.
    """
    __slots__ = 'val'

    def __init__(self, val: V = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.val = val

    def __str__(self) -> str:
        color = "red" if self.red else "black"
        return f"({self.key}, {self.val}, {color})"


class TreeDict(Tree, MutableMapping[K, V]):
    """
    Dictionary based on a red-black tree. That means its self-sorting
    and only allowing unique items. Note that Python's own OrderedDict
    remembers the order of inserted values, but does not automatically
    sort them.
    """
    nodetype: ClassVar[Type[Node]] = DictNode

    def __init__(
            self,
            root: Optional[DictNode] = None,
            items: Mapping[K, V] = {},
            acc: Callable[[V, V], V] = lambda _, x: x,
    ):
        """
        :param root: Initialize the tree from an already existing one.
            Passing a root node make this tree contain all that nodes'
            children.
        :param items: Initialize the tree with a node for each passed
            key, value pair in the mapping. If a root was also passed,
            these nodes will be added to 'root' and its children, if
            they don't already contain keys from the list. Note that
            the tree rebalances after each added node, so the passed
            root node may not end up as such in the end.
        :param acc: This function handles cases before an already
            contained key is inserted again into the dictionary. It
            takes the old, already contained value as first and the new,
            passed value as second parameter, returning the value to be
            definitively stored for the key.
            By default, the old value mapped to the key is simply
            overridden by the new one.
            Calling this function to handle key clashes is cheaper than
            using the child class DefaultTreeDict with an += assignment,
            because no additional call to __getitem__(), and thus no
            additional tree traversal, is necessary.
        """
        super().__init__(root)
        for i in items.items():
            self.__setitem__(*i)
        self.acc = acc

    def __setitem__(self, key: K, val: V) -> Tuple[DictNode, bool]:
        node, success = super().insert(key)
        node.val = val if success else self.acc(node.val, val)
        return node, success

    insert = __setitem__

    def values(self) -> Iterator[V]:
        if self.root:
            for node in self.root:
                yield node.val

    def items(self) -> Iterator[Tuple[K, V]]:
        if self.root:
            for node in self.root:
                yield (node.key, node.val)

    def _copy_node_attr(
            self,
            source: DictNode,
            target: DictNode,
            ) -> None:
        super()._copy_node_attr(source, target)
        target.val = source.val


class DefaultTreeDict(TreeDict):
    """
    Dictionary based on a red-black tree. That means its self-sorting
    and only allowing unique items. Like Python's defaultdict, this
    container returns a default type when a key is accessed that is not
    present in the dictionary.
    """
    def __init__(
            self,
            default_factory: Optional[Type] = None,
            *args,
            **kwargs,
    ):
        """
        :param default_factory: Default type returned when accessed
            key is not in the map. If None, this class behaves
            exactly like a TreeDict.
        """
        super().__init__(*args, **kwargs)
        self.default_factory = default_factory

    def __getitem__(self, key: K) -> DictNode:
        try:
            return super().__getitem__(key)
        except KeyError:
            if self.default_factory:
                return self.default_factory()
            else:
                raise KeyError(key) from None

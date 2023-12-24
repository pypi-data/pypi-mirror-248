from typing import Hashable, Iterator, Sequence
import attr


E = Hashable

UNSET = object()


@attr.s(slots=True, eq=False)
class Node:
    """
    Do *not* instantiate this class by hand! Let :meth:`Tree._make_node` do it for you. Use
    :meth:`Tree.get` or :meth:`Tree.force` instead.

    You must subclass this to customize the information stored in a Node. Avoid using the prefix
    "node_" for methods or attributes in your subclass.

    Don't forget to use ``@attr.s(slots=True, eq=False)``
    """

    node_parent: "Node | None" = attr.ib(init=False, default=None, repr=False)
    node_prefix: tuple[E, ...] = attr.ib(converter=tuple)
    node_children: "dict[E, Node]" = attr.ib(factory=dict, repr=False)

    def node_reparent(self, parent: "Node | None") -> None:
        old = self.node_parent
        if old is parent:
            return

        key = self.node_prefix[0]

        if old is not None:
            child = old.node_children.pop(key)
            assert child is self

        self.node_parent = None

        if parent is not None:
            assert key not in parent.node_children
            parent.node_children[key] = self
            self.node_parent = parent

    @property
    def node_has_data(self) -> bool:
        raise NotImplementedError

    def node_debug_string(self, indent="  ", initial_indent="") -> str:
        r = []

        def _rec(node, i):
            nonlocal r
            r.append(initial_indent)
            r += (indent for _ in range(i))
            r += node.node_debug_string_prefix()
            this_string = node.node_debug_string_data()
            if this_string:
                r.append(" ")
                r += this_string
            r.append("\n")
            for key, child in sorted(node.node_children.items()):
                assert key == child.node_prefix[0]
                _rec(child, i + 1)

        _rec(self, 0)
        r.pop()  # discard last newline
        return "".join(r)

    def node_debug_string_prefix(self):
        return (repr(list(self.node_prefix)),)

    def node_debug_string_data(self):
        return ()


@attr.s(slots=True, eq=False)
class RawDataNode(Node):
    raw_data = attr.ib(default=None)

    @property
    def node_has_data(self) -> bool:
        return bool(self.raw_data)

    def node_debug_string_data(self):
        return (repr(self.raw_data),) if self.node_has_data else ()


@attr.s(slots=True, eq=False)
class SetNode(RawDataNode):
    """
    Node which holds a set in :attr:`data`. This attribute is initialized lazily.
    """

    @property
    def data(self):
        raw_data = self.raw_data
        if raw_data is None:
            self.raw_data = raw_data = set()
        return raw_data

    def add(self, x):
        self.data.add(x)

    def update(self, xs):
        self.data.update(xs)

    def discard(self, x):
        if self.raw_data:
            self.data.discard(x)

    def remove(self, x):
        self.data.remove(x)

    def clear(self):
        self.data.clear()

    def __iter__(self):
        return iter(self.raw_data or ())

    def __contains__(self, x):
        return x in (self.raw_data or ())


@attr.s(slots=True)
class TraverseResult:
    """
    Attributes
    ----------
    sequence_index: int | None
        Number of matching sequence elements. None if it's the whole sequence.
    node: Node
        Node.
    node_prefix_index: int | None
        Number of matching elements in the :attr:`Node.node_prefix`. None if the entire prefix
        matched.
    """

    sequence_index: "int | None" = attr.ib()
    node: Node = attr.ib()
    node_prefix_index: "int | None" = attr.ib()


@attr.s(slots=True)
class _Frame:
    node: Node = attr.ib()
    children_left: list = attr.ib(default=None, init=False)
    keep: bool = attr.ib(default=None, init=False)
    has_data: bool = attr.ib(default=None, init=False)

    def __attrs_post_init__(self):
        node = self.node
        self.children_left = list(node.node_children.values())
        self.has_data = self.keep = node.node_has_data


@attr.s
class Tree:
    """
    Radix tree with lazy pruning.
    """

    node_class: type = attr.ib()
    root: Node = attr.ib(default=None, init=False)

    def __attrs_post_init__(self):
        self.root = self._make_node(parent=None, prefix=())

    @staticmethod
    def _match_prefix(key, child_prefix, key_start: int = 0) -> int:
        i = 0
        n_prefix = len(child_prefix)
        n_key = max(len(key) - key_start, 0)
        n = min(n_prefix, n_key)
        if not n:
            return 0
        for i in range(n):
            if key[i + key_start] != child_prefix[i]:
                return i
        return n

    def traverse(
        self, node: Node, sequence: Sequence[E], sequence_start_index: int = 0
    ) -> TraverseResult:
        """
        Mostly internal method. Starting at *node*, follow the path of *sequence* by looking
        at children and their children's children and so on.
        """
        _match_prefix = self._match_prefix
        n = len(sequence)
        i = sequence_start_index
        while i < n:
            key_i = sequence[i]
            child = node.node_children.get(key_i)
            if child is None:
                return TraverseResult(sequence_index=i, node_prefix_index=None, node=node)
            else:
                prefix = child.node_prefix
                matching = _match_prefix(sequence, prefix, key_start=i)
                i += matching
                if matching == len(prefix):
                    # full match
                    node = child
                else:
                    # key does not match prefix and prefix is longer than the matching part
                    return TraverseResult(
                        sequence_index=i if i < n else None,
                        node_prefix_index=matching,
                        node=child,
                    )

        return TraverseResult(sequence_index=None, node_prefix_index=None, node=node)

    def force(self, sequence) -> Node:
        """
        Alias for :meth:`get` with ``create=True``.
        """
        return self.get(sequence, create=True)

    def get(self, sequence, *, create: bool = False, node: Node = UNSET) -> Node:
        if node is UNSET:
            node = self.root

        r = self.traverse(node, sequence)

        seq_index = r.sequence_index
        prefix_index = r.node_prefix_index

        if seq_index is None and prefix_index is None:
            return r.node  # full exact match
        elif not create:
            return None

        if prefix_index is None:
            # need to create a new node
            return self._make_node(parent=r.node, prefix=sequence[seq_index:])
        else:
            # we cut the node in two
            # "node -> child" becomes "node -> mid -> child"
            child = r.node
            node = child.node_parent
            child.node_reparent(None)
            prefix = child.node_prefix
            mid = self._make_node(parent=node, prefix=prefix[:prefix_index])
            if seq_index is None:
                result = mid
            else:
                result = self._make_node(parent=mid, prefix=sequence[seq_index:])
            child.node_prefix = prefix[prefix_index:]
            child.node_reparent(mid)
            return result

    def _make_node(self, parent: "Node | None", prefix: tuple[E, ...]) -> Node:
        node = self.node_class(node_prefix=prefix)
        node.node_reparent(parent)
        return node

    def prune(self, node=UNSET) -> None:
        """
        Recursively traverse and remove unnecessary nodes.
        """
        if node is UNSET:
            node = self.root

        Frame = _Frame

        # depth-first traversal without using the Python stack
        path = [Frame(node)]
        while path:
            current = path[-1]
            children = current.children_left
            if children:
                # traverse children first
                path.append(Frame(children.pop()))
            else:
                path.pop()

                if not path:
                    # there is no parent, we are at the search root
                    continue

                parent = path[-1]
                node = current.node

                # no more children left
                if current.keep:
                    # if we are supposed to keep the child, then we must also keep the parent
                    parent.keep = True

                    # unnecessary intermediate node with exactly 1 child
                    if not current.has_data and len(node.node_children) == 1:
                        node.node_reparent(None)
                        [child] = node.node_children.values()
                        child.node_reparent(None)
                        child.node_prefix = node.node_prefix + child.node_prefix
                        child.node_reparent(parent.node)
                else:
                    # remove child from parent
                    node.node_reparent(None)

    def find(self, node: Node = UNSET, has_data: bool = True) -> Iterator[Node]:
        """
        Recursively iterate through every child node. By default, only yield nodes that have
        data (where :attr:`Node.node_has_data` is true).
        """
        if node is UNSET:
            node = self.root
        active = [node]
        while active:
            node = active.pop()
            active.extend(node.node_children.values())
            if not has_data or node.node_has_data:
                yield node

    def find_closest_nodes(self, sequence, node=UNSET) -> Iterator[tuple[int, Node]]:
        """
        Yield pairs (longest_common_prefix, node) in descending order.
        """
        if node is UNSET:
            node = self.root

        root = node  # save search root for later
        r = self.traverse(node, sequence)
        i = r.sequence_index
        j = r.node_prefix_index

        if i is None:
            i = len(sequence)
        if j is None:
            j = len(r.node.node_prefix)

        # enumerate everything under the node that was returned
        yield i, r.node

        # now enumerate all the "uncle" nodes
        node = r.node
        i -= j
        while True:
            child = node
            node = child.node_parent

            if child is root:
                break

            for sibling in node.node_children.values():
                if sibling is not child:
                    yield i, sibling

            i -= len(node.node_prefix)

import sys
from collections import defaultdict
import numpy
import random
from operator import itemgetter
import networkx as nx

##############################################################################
# Private Functions ##########################################################
##############################################################################

def _basic_stats(l):
    a=numpy.array(l,dtype=numpy.double)
    return a.mean(),a.min(),a.max(),a.std(),len(a)

##############################################################################
# Classes ####################################################################
##############################################################################

class HierarchicalPartition:
    """This class implements the hierarchical partition data structure.
    It is able to contain any kind of element that can be contained in a set.

    Parameters
    ----------
    elements : <list>
        The list of elements that are going to be contained by the HierarchicalPartition.
    checks : <bool>
        If True, different (slow) checks run througth the creation of the object, plus in some other methods. This is True by default.

    Returns
    -------
    : HierarchicalPartition
        A list of nodes that are adjacent to n.

    Example
    -------
    >>> from hierpart import HierarchicalPartition
    >>> hp=HierarchicalPartition(['a','b','c','d','e','f']) # This is the line that creates the HierarchicalPartition object.
    >>> # All the following lines of code are here for the doctest.
    >>> # However, these extra lines of code are also useful for learning purposes.
    >>> root=hp.root()
    >>> print root
    0
    >>> print hp.node_elements(root)
    ['a', 'b', 'c', 'd', 'e', 'f']
    >>> n1=hp.add_child(root,['a','b','c'])
    >>> n2=hp.add_child(root,['d','e','f'])
    >>> print n1
    1
    >>> print n2
    2
    >>> print hp.node_elements(n1)
    ['a', 'b', 'c']
    >>> print hp.node_elements(n2)
    ['d', 'e', 'f']
    >>> hp.add_child(n1,['a'])
    3
    >>> n3=hp.add_child(n1,['b','c'])
    >>> hp.add_child(n3,['b'])
    5
    >>> hp.add_child(n3,['c'])
    6
    >>> tree=hp.tree()
    >>> print tree.edges()
    [(0, 1), (0, 2), (1, 3), (1, 4), (4, 5), (4, 6)]
    >>> for node in hp.nodes():
    ...     print node, hp.node_elements(node)
    ...     
    0 ['a', 'b', 'c', 'd', 'e', 'f']
    1 ['a', 'b', 'c']
    2 ['d', 'e', 'f']
    3 ['a']
    4 ['b', 'c']
    5 ['b']
    6 ['c']
    """
    def __init__(self,elements,checks=True):
        self._checks=bool(checks)
        self._elements=list(elements)
        self._tree=nx.DiGraph()
        self._N=1
        self._root=self._N-1
        self._tree.add_node(self._root)
        self._node_elements={}
        self._node_elements[self._root]=elements
        self._node_depth={}
        self._node_depth[self._root]=0

    def tree(self):
        """The returned tree describes the topology of the hierarchical partition.

        Returns
        -------
        : <networkx.DiGraph>
            A list of nodes that are adjacent to n.

        Examples
        --------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy=hp.add_child(n3,['b'])
        >>> dummy=hp.add_child(n3,['c'])
        >>> tree=hp.tree()
        >>> print tree.edges()
        [(0, 1), (0, 2), (1, 3), (1, 4), (4, 5), (4, 6)]
        """
        return self._tree

    def checks(self):
        """
        Returns
        -------
        : <bool>
            True or False, depending on how it was defined at the object creation."""
        return self._checks

    def num_nodes(self):
        """
        Returns
        ------- 
        : <int>
            The number of nodes (not elements) in the tree of the hierarchical partition."""
        assert self._N==self._tree.number_of_nodes()
        return self._N

    def num_edges(self):
        """
        Returns
        -------
        : <int>
            The number of edges, or links, in the tree of the hierarchical partition."""
        assert self.num_nodes()-1==self._tree.number_of_edges()
        return self.num_nodes()-1

    def node_elements(self,node):
        """The elements contained in node "node".

        Parameters
        ----------
        node : "node"
            A node of the tree.

        Returns
        -------
        : <list>
            A list of elements contained in node "node".

        Examples
        --------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy=hp.add_child(n3,['b'])
        >>> dummy=hp.add_child(n3,['c'])
        >>> print hp.node_elements(root)
        ['a', 'b', 'c', 'd', 'e', 'f']
        >>> print hp.node_elements(n1)
        ['a', 'b', 'c']
        """
        try:
            return self._node_elements[node]
        except:
            print 'CRASH INFO:'
            print 'NODE =',node
            assert False, 'ERROR node_elements(): node NODE is not a member of the HierarchicalPartition.'

    def node_size(self,node):
        """The number of elements of a node of the tree.
        
        Parameters
        ----------
        node : "node"
            A node of the tree.

        Returns
        ------- 
        : <int>
            The number of elements the node **node** contains.

        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy=hp.add_child(n3,['b'])
        >>> dummy=hp.add_child(n3,['c'])
        >>> print hp.node_size(root)
        6
        >>> print hp.node_size(n1)
        3
        >>> print hp.node_size(n2)
        3
        >>> print hp.node_size(n3)
        2
        """
        return len(self.node_elements(node))

    def node_parent(self,node):
        """Return the parent node of **node**.

        Parameters
        ----------
        node : "node"
           A node in the graph

        Returns
        -------
        : "node"
            The parent node of **node** if any. Otherwise, it returns None.

        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy=hp.add_child(n3,['b'])
        >>> dummy=hp.add_child(n3,['c'])
        >>> print hp.node_parent(n3)==n1
        True
        >>> print hp.node_parent(n3)==n2
        False
        >>> print hp.node_parent(root)==None
        True
        """
        _in_edges=self._tree.in_edges(node)
        if len(_in_edges)==0: # The node has no parent, then it should be the root
            assert node==self.root(),'ERROR in node parent(): Node "node" has no parent but it is not the root.'
            return None
        assert len(_in_edges)==1,'ERROR in node_parent(): Node with more than one parent...'
        return _in_edges[0][0]

    def node_children(self,node):
        """It yields the children of the node **node**.

        Parameters
        ----------
        node : "node"
            A node of the tree.
 
        Returns
        -------
        : "node_iterator"
            yields over the children nodes of node **node**, if any.
    
        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy=hp.add_child(n3,['b'])
        >>> dummy=hp.add_child(n3,['c'])
        >>> for child in hp.node_children(root):
        ...     print child
        ...
        1
        2
        """
        for child in self._tree[node]:
            yield child

    def node_depth(self,node):
        """Returns the depth at which a given node is.

        Parameters
        ----------
        node : "node"
            A node of the tree.
        
        Returns
        -------
        : <int>
            The depth at which node **node** is in the tree.

        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy=hp.add_child(n3,['b'])
        >>> dummy=hp.add_child(n3,['c'])
        >>> print hp.node_depth(root)
        0
        >>> print hp.node_depth(n1)
        1
        >>> print hp.node_depth(n3)
        2
        """
        return self._node_depth[node]

    def node_branching_factor(self,node):
        """Returns the number of children a given node has.

        Parameters
        ----------
        node : "node"
            A given node of the tree.

        Returns
        -------
        : <int>
            The number of children the node **node** has.

        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy=hp.add_child(n3,['b'])
        >>> dummy=hp.add_child(n3,['c'])
        >>> print hp.node_branching_factor(root) 
        2
        >>> print hp.node_branching_factor(n1) 
        2
        >>> print hp.node_branching_factor(n2) 
        0
        """
        return self._tree.out_degree(node)

    def node_leaf(self,node):
        """Returns True if the node **node** is a leaf of the tree.

        Parameters
        ----------
        node : "node"
            A node of the tree.

        Returns
        -------
        : <bool>
            True if the node **node** is a leaf; else, returns False.

        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy=hp.add_child(n3,['b'])
        >>> dummy=hp.add_child(n3,['c'])
        >>> print hp.node_leaf(root) 
        False
        >>> print hp.node_leaf(n1) 
        False
        >>> print hp.node_leaf(n2) 
        True
        """
        return self.node_branching_factor(node)==0

    def root(self):
        """Returns the root node of the tree.

        Returns
        -------
        : "node"
            The returned node is the root of the tree.
        """
        return self._root

    def all_elements(self):
        """Returns a list of all elements in the tree.

        Returns
        -------
        : <list>
            A list of all elements contained in the tree.
       
        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c']) # This line is to show that it doesn't count
        >>> print hp.all_elements()
        ['a', 'b', 'c', 'd', 'e', 'f']
        """
        return self.node_elements(self.root())

    def total_num_elements(self):
        """Returns the number of elements contained in the tree.

        Returns
        -------
        : <int>
            The number of elements contained in the tree = size(root).

        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c']) # This line is to show that it doesn't count
        >>> print hp.total_num_elements()
        6
        """      
        return self.node_size(self.root())

    def max_depth(self):
        """Returns the depth of the node with the maximum depth of the tree.

        Returns
        -------
        : <int>
            The largest value of the depth among all nodes in the tree.

        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root() # the root has depth 0
        >>> n1=hp.add_child(root,['a','b','c']) # n1 and n2 have depth 1
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c']) # n3 has depth 2.
        >>> dummy=hp.add_child(n3,['b']) # These children of n3 have depth 3.
        >>> dummy=hp.add_child(n3,['c'])
        >>> print hp.max_depth()
        3
        """
        return max([self.node_depth(node) for node in self.nodes()])

    def depths_basic_stats(self):
        """Return *basic_stats* about the list of depths of the leaves in the tree.

        Returns
        -------
        : (float,float,float,float,int)
            
        The returned tuple contains values that are computed out of the list of all depth values among all leaves in the tree.
        The returned values are:
            1. average depth of the leaves of the tree.
            2. minimum depth of the leaves of the tree.
            3. maximum depth of the leaves of the tree.            
            4. std of the depths of the leaves of the tree.
            5. number of leaves in the tree.
        
        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy=hp.add_child(n3,['b'])
        >>> dummy=hp.add_child(n3,['c'])
        >>> print hp.depths_basic_stats()
        (2.25, 1.0, 3.0, 0.82915619758884995, 4)
        """
        return _basic_stats([self.node_depth(node) for node in self.leaves()])

    def max_size(self):
        """Returns the size of the node with the largest size in the tree, aka, the root.

        Comment:
        This function is created to check internal consistency, and also, for completion as min_size() also exist.

        Returns
        -------
        : <int>
            The size of the largest node in the tree. The size of a node is measured as the number of elements the node contains. It should be the size of the root.
        """
        _max_size=max([self.node_size(node) for node in self.nodes()])
        assert _max_size==self.node_size(self.root()), "ERROR: The root is not the node with the largest size!"
        return _max_size

    def min_size(self):
        """Returns the size of the node with the smallest size in the tree.

        Returns
        -------
        : <int> 
            The size of the smallest node in the tree. The size of a node is measured as the number of elements the node contains.""" 
        _min_size=min([self.node_size(node) for node in self.nodes()])
        assert _min_size>0, "ERROR: There is a node with size<=0."
        return _min_size

    def branching_factors(self,no_leaves=True):
        """Returns a list with all branching factors of the tree; ie., one for each node.

        Parameters
        ----------
        no_leaves : <bool> 
            If True, the leaves of the tree are excluded from the list.

        Returns
        -------
        : <list> 
            A list containing the branching factors of all nodes in the tree. 

        Examples
        --------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy=hp.add_child(n3,['b'])
        >>> dummy=hp.add_child(n3,['c'])
        >>> print hp.branching_factors()
        [2, 2, 2]
        >>> print hp.branching_factors(no_leaves=False)
        [2, 2, 0, 0, 2, 0, 0]
        """
        if no_leaves:
            return [self.node_branching_factor(node) for node in self.nodes() if not self.node_leaf(node)]
        else:
            return [self.node_branching_factor(node) for node in self.nodes()]

    def branching_factors_basic_stats(self,no_leaves=True):
        """Return *basic_stats* about the list of depths in the tree.

        Parameters
        ----------
        no_leaves : <bool>
            If True, the leaves of the tree are excluded of the computation.

        Returns
        -------
        : (float,float,float,float,int)
        The returned tuple contains values that are computed out of the list of all depth values among all leaves in the tree.
        The returned values are:
            1. average branching factor of nodes of the tree.
            2. minimum branching factor of nodes of the tree.
            3. maximum branching factor of nodes of the tree.            
            4. std of the branching factor of the nodes of the tree.
            5. number of nodes of the tree that have beeen considered.
        
        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy=hp.add_child(n3,['b'])
        >>> dummy=hp.add_child(n3,['c'])
        >>> print hp.branching_factors_basic_stats()
        (2.0, 2.0, 2.0, 0.0, 3)
        >>> print hp.branching_factors_basic_stats(no_leaves=False)
        (0.8571428571428571, 0.0, 2.0, 0.9897433186107869, 7)
        """
        return _basic_stats(self.branching_factors(no_leaves=no_leaves))

    def add_child(self,parent,child_elements):
        """To add a child to a given node of the tree.

        Remarks:
        If **checks** is set to True (at the moment of the creation of the HierarchicalPartition object), then, the current method checks that the set of elements in the new child is contained by the set of elements of the parent node.

        Parameters
        ----------
        parent : "node"
            The parent node the new child will have.
        child_elements : <list>
            The elements that will be contained in the new child.

        Returns
        -------
        : "node"
            The new child.

        Examples
        --------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> print hp.node_elements(n1)
        ['a', 'b', 'c']
        """
        self._N+=1
        new_child=self._N-1
        if self.checks():
            assert parent in self._tree.nodes(),'ERROR in add_child: "parent" is not in the "tree".'
        self._tree.add_edge(parent,new_child)
        if self.checks():
            try:
                assert set(child_elements) <= set(self.node_elements(parent)), 'ERROR in add_child: the "elements" in the child is not a subset of the "elements" in the parent.'
            except:
                print '# child_elements',child_elements
                print '# parent_elements',self.node_elements(parent)
                assert False
        self._node_elements[new_child]=child_elements
        self._node_depth[new_child]=self._node_depth[parent]+1
        return new_child

    def consistency(self):
        """Checks the consistency of the tree.

        Returns
        -------
        : <bool>
            It returns True if the consistency is right. Otherwise, it returns False.
        """
        for node in self._tree:
            if self.node_leaf(node):
                continue
            children_union=[]
            for child in self._tree[node]:
                children_union+=self.node_elements(child)
            if not set(children_union)==set(self.node_elements(node)):
                return False
        return True

    def nodes(self):
        """Returns a list of the node, ie., sub-communities, in the tree.

        Returns
        -------
        : <list>
            A list of the nodes in the tree.
        """
        return self._tree.nodes()

    def leaves(self):
        """Returns a list with the leaves in the tree.

        Returns
        -------
        : <list>
            A list of the nodes in the tree that are a leaf.
        """
        return [node for node in self.nodes() if self.node_leaf(node)]

    def __iter__(self):
        """Iterates over the nodes of the tree. The iterator goes from the largest node to the smallest node, where the size of the nodes is measured using the method **node_size()**.


        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy=hp.add_child(n3,['b'])
        >>> dummy=hp.add_child(n3,['c'])
        >>> print [node for node in hp]
        [0, 1, 2, 4, 3, 5, 6]
        """
        for dummy,node in sorted([ (self.node_size(node),node) for node in self._tree ],key=itemgetter(0),reverse=True):
            yield node

    def bfs_traversal(self):
        """It yields over the nodes of the tree, performing a BFS algorithm that starts from the root.

        
        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy=hp.add_child(n3,['b'])
        >>> dummy=hp.add_child(n3,['c'])
        >>> print [node for node in hp.bfs_traversal()]
        [0, 1, 2, 3, 4, 5, 6]
        """
        yield self.root()
        wave=[self.root()]
        while len(wave)>0:
            new_wave=[]
            for node in wave:
                for child in self.node_children(node):
                    new_wave.append(child)
                    yield child
            wave=new_wave

    def dfs_traversal(self):
        """It yields over the nodes of the tree, performing a DFS algorithm that starts from the root.

        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy=hp.add_child(n3,['b'])
        >>> dummy=hp.add_child(n3,['c'])
        >>> print [node for node in hp.dfs_traversal()]
        [0, 2, 1, 4, 6, 5, 3]
        """
        stack=[self.root()]
        while len(stack)>0:
            node=stack.pop()
            yield node
            for child in self.node_children(node):
                stack.append(child)

    def edges(self):
        #"""It yields over the edges of the tree."""
        #yield self.root()
        #for edge in self._tree.edges():
        #    yield edge[0],edge[1]
        """It returns the list of edges of the tree.

        Returns
        -------
        : <list>
            The list of edges of the tree.

        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy=hp.add_child(n3,['b'])
        >>> dummy=hp.add_child(n3,['c'])
        >>> print hp.edges()
        [(0, 1), (0, 2), (1, 3), (1, 4), (4, 5), (4, 6)]
        """
        return self._tree.edges()

    def show(self):
        """Shows in the screen a list of the nodes, and their respective elements."""
        for node in self.bfs_traversal():
            print node,self.node_elements(node)

    def copy(self):
        """Copy the current <HierarchicalPartition> object into a new <HierarchicalPartition> object.

        Returns
        -------
        : HierarchicalPartition
            A copy of the current tree.

        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy=hp.add_child(n3,['b'])
        >>> dummy=hp.add_child(n3,['c'])
        >>> hpc=hp.copy()
        >>> print hpc.nodes()        
        [0, 1, 2, 3, 4, 5, 6]
        >>> print hpc.edges()
        [(0, 1), (0, 2), (1, 3), (1, 4), (4, 5), (4, 6)]
        >>> for node in hpc.nodes(): assert hpc.node_elements(node)==hp.node_elements(node)
        """
        _hp=HierarchicalPartition(self.all_elements())
        wave=[self.root()]
        _wave=[_hp.root()]
        while len(wave)>0:
            new_wave=[]
            _new_wave=[]
            for node,_node in zip(wave,_wave):
                for child in self.node_children(node):
                    new_wave.append(child)
                    _child=_hp.add_child(_node,self.node_elements(child))
                    _new_wave.append(_child)
            wave=new_wave
            _wave=_new_wave
        return _hp

    def replica(self,old_elements_2_new_elements):
        """This method allows to replicate the current tree, into another tree, where the nodes change according to a predefined mapping.

        What is this useful for? One possible usage is that of the randomization of a hierarchy.

        Parameters
        ----------
        old_elements_2_new_elements : <dict>
            It maps old elements, into new elements.

        Returns
        -------
        : HierarchicalPartition
            The new hierarchical partition has elements with "renamed names" according to the specification in **old_elements_2_new_elements**.

        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy=hp.add_child(n3,['b'])
        >>> dummy=hp.add_child(n3,['c'])
        >>> old_elements_2_new_elements={'a':'A', 'b':'B', 'c':'C', 'd':'D', 'e':'E', 'f':'F'}
        >>> hpr=hp.replica(old_elements_2_new_elements)
        >>> print hpr.all_elements()
        ['A', 'B', 'C', 'D', 'E', 'F']
        >>> for node in hpr.nodes():
        ...    print node, hpr.node_elements(node)
        ...
        0 ['A', 'B', 'C', 'D', 'E', 'F']
        1 ['A', 'B', 'C']
        2 ['D', 'E', 'F']
        3 ['A']
        4 ['B', 'C']
        5 ['B']
        6 ['C']
        """
        assert len(old_elements_2_new_elements)==self.total_num_elements(),"ERROR: not len(old_elements_2_new_elements)==self.total_num_elements()"
        assert set(old_elements_2_new_elements.keys())==set(self.all_elements()),'ERROR: not set(old_elements_2_new_elements.keys())==set(self.all_elements())'
        assert len(set(old_elements_2_new_elements.values()))==self.total_num_elements(),"ERROR: not len(set(old_elements_2_new_elements.values()))==self.total_num_elements()"

        _hp=HierarchicalPartition([old_elements_2_new_elements[e] for e in self.all_elements()])
        wave=[self.root()]
        _wave=[_hp.root()]
        while len(wave)>0:
            new_wave=[]
            _new_wave=[]
            for node,_node in zip(wave,_wave):
                for child in self.node_children(node):
                    new_wave.append(child)
                    _child=_hp.add_child(_node,[old_elements_2_new_elements[e] for e in self.node_elements(child)])
                    _new_wave.append(_child)
            wave=new_wave
            _wave=_new_wave
        return _hp

    def nodes_at_depth(self,depth):
        """Returns a list of all the nodes in the tree that have a specified depth.

        Comments:
            The list might be empty.
            The list not necessarily conform a partition of the full set of elements.

        Parameters
        ----------
        depth : <int>
            The depth at which the nodes to be returned should be.

        Returns
        -------
        : <list> 
            A list of the nodes at depth "depth". 

        Examples
        --------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy1=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy2=hp.add_child(n3,['b'])
        >>> dummy3=hp.add_child(n3,['c'])
        >>> print root, n1, n2, n3, dummy1, dummy2, dummy3
        0 1 2 4 3 5 6
        >>> for node in hp.nodes():
        ...     print node, hp.node_depth(node)
        ...
        0 0
        1 1
        2 1
        3 2
        4 2
        5 3
        6 3
        >>> print hp.nodes_at_depth(0)
        [0]
        >>> hp.nodes_at_depth(1)
        [1, 2]
        >>> hp.nodes_at_depth(2)
        [3, 4]
        >>> hp.nodes_at_depth(3)
        [5, 6]
        >>> hp.nodes_at_depth(4)
        []
        """
        return [ node for node in self._tree if self.node_depth(node)==depth ]

    def node_children_avrg_size(self,node,weighted=True):
        """Returns the average size of the children nodes of a given node **node**.

        Parameters
        ----------
        node : "node"
            This is the parent of the set of childern nodes, over which the average size is computed.
        weighted : <bool>
            If True, then, each term of the average is weighted by the weight **float(node_size(child))/node_size(parent)**.

        Returns
        -------
        : <float>
            The average size of the children nodes of **node**.

        Example
        -------
        >>> from hierpart import HierarchicalPartition
        >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
        >>> root=hp.root()
        >>> n1=hp.add_child(root,['a','b','c'])
        >>> n2=hp.add_child(root,['d','e','f'])
        >>> dummy1=hp.add_child(n1,['a'])
        >>> n3=hp.add_child(n1,['b','c'])
        >>> dummy2=hp.add_child(n3,['b'])
        >>> dummy3=hp.add_child(n3,['c'])
        >>> print [hp.node_children_avrg_size(node) for node in hp.nodes()]
        [3.0, 1.6666666666666665, 0.0, 0.0, 1.0, 0.0, 0.0]
        >>> print [hp.node_children_avrg_size(node,weighted=False) for node in hp.nodes()]
        [3.0, 1.5, 0.0, 0.0, 1.0, 0.0, 0.0]
        """
        sum_children_size=0.0
        num_children_size=0.0
        weight=1.0
        parent_size=float(self.node_size(node))
        for child in self.node_children(node):
            child_size=float(self.node_size(child))
            if weighted:
                weight=child_size/parent_size
            sum_children_size+=weight*child_size
            num_children_size+=weight
        if num_children_size==0.0:
            return 0.0
        return sum_children_size/num_children_size

##############################################################################
# Public Functions ###########################################################
##############################################################################

# IO HierarchicalPartitions
###########################

def save_hierarchical_partition(hier_part,fileout=None,fhw=None):
    """It saves a HierarchicalPartition object into a file.

    Parameters
    ----------

    hier_part : HierarchicalPartition
        The tree to be saved.
    fileout : <str>
        The name (and path) of the file where the tree is saved.
    fhw : <file-handler>
        Should be a filehandler with writting privileges. This is optional to the use of **fileout**.
    """
    assert not ( fileout is None and fhw is None ), "ERROR in save_hierarchical_partition : fileout and fhw, cannot be both None."
    assert not ( fileout is not None and fhw is not None ), "ERROR in save_hierarchical_partition : fileout and fhw, cannot be both specified."
    if fileout is not None:
        fhw=open(fileout,'w')
    count_vs_depth=defaultdict(int)
    for node in hier_part.dfs_traversal():
        depth=hier_part.node_depth(node)
        count_vs_depth[depth]+=1
        if hier_part.node_leaf(node):
            path=''
            sep=''
            for d in xrange(depth):
                path+=sep+str(count_vs_depth[d+1]-1)
                sep=','
            print >>fhw,path,
            elements=''
            sep=''
            for element in hier_part.node_elements(node):
                assert '"' not in element,'ERROR: the double quotation mark " cannot be part of an element name for saving.'
                elements+=sep+'"'+str(element)+'"'
                sep=','
            print >>fhw,elements
    if fileout is not None:
        fhw.close()

def load_hierarchical_partition(filein):
    """Load a Hierarchical Partition from file.

    Parameters
    ----------
    filein : <str>
        The filename (and path) to the file where a tree is stored.

    Returns
    -------
    : HierarchicalPartition
        The loaded tree.
    """
    element_2_path=defaultdict(float)
    with open(filein,'r') as fh:
        for line in fh.readlines():
            if '#' in line:
                continue
            cols=line.split()
            path=cols[0].split(',')
            elements=[e.replace('"','') for e in cols[1].split('","')]
            for i,e in enumerate(elements):
                element_2_path[e]=path
    assert len(set(element_2_path.keys()))==len(element_2_path) # Check elements are unique.

    class Node:
        def __init__(self):
            self.elements=[]
            self.children=defaultdict(self._new_child)
        def _new_child(self):
            return Node()
        def add_element(self,element):
            self.elements.append(element)
        def num_elements(self):
            return len(self.elements)
        def __getitem__(self,i):
            return self.children[i]
        def num_children(self):
            return len(self.children)

    root=Node()
    for element,path in element_2_path.items():
        node=root
        node.add_element(element)
        for i in path:
            node=node[i]
            node.add_element(element)

    _hier_part=HierarchicalPartition(root.elements)
    node_2_hp_node={}
    node_2_hp_node[root]=_hier_part.root()
    traverse=[root]
    while True:
        try:
            parent=traverse.pop()
            hp_parent=node_2_hp_node[parent]
        except:
            break
        for child in parent.children.values():
            traverse.append(child)
            hp_child=_hier_part.add_child(hp_parent,child.elements)
            node_2_hp_node[child]=hp_child
    #
    return _hier_part

# Hierarchical mutual information tools
########################################

def _plogp(p):
    """Computes p * ln(p). Uses the convention 0 * ln 0 == 0."""
    p=float(p)
    assert p>=0 and p<=1.0
    if p==0.0:
        return 0.0
    return p*numpy.log(p)

def sub_hierarchical_mutual_information(hierpart_x,hierpart_y,node_x,node_y,depth,show=False):
    """Cumputes the hierarchical mutual information between two sub-trees.
    More specifically, it computes I( T_v ; T'_v' ), where T and T' are <HierarchicalPartitions>, v is a node in T and v' is a node in T'. Also, T_v is the sub-tree obtained from T with v as root. The analogous for T'_v'.
    
    Comments:
        This function is used recursivelly to compute I(T;T').

    Parameters
    ----------
    hierpart_x : HierarchicalPartition
        The hierarchical partition T.
    hierpart_y : HierarchicalPartition
        The hierarchical partition T'.
    node_x : "node" 
        The node v. It should belong to T.
    node_y : "node" 
        The node v'. It should belong to T'.
    depth : <int>
        The depth at which the nodes v and v' are. This variable is used for internal checks.
    show : <bool>
        If True, information is printed on the screen as the computation progress.

    Returns
    -------
    : <float>
        The value I( T_v ; T'_v' ).

    Example
    -------
    >>> from hierpart import HierarchicalPartition
    >>> from hierpart import sub_hierarchical_mutual_information
    >>> # Lets create a HierarchicalPartition called "x"
    >>> hpx=HierarchicalPartition(['a','b','c','d','e','f'])
    >>> rootx=hpx.root()
    >>> n1x=hpx.add_child(rootx,['a','b','c'])
    >>> n2x=hpx.add_child(rootx,['d','e','f'])
    >>> dummy=hpx.add_child(n1x,['a'])
    >>> n3x=hpx.add_child(n1x,['b','c'])
    >>> dummy=hpx.add_child(n3x,['b'])
    >>> dummy=hpx.add_child(n3x,['c'])
    >>> # Lets create another slightly different HierarchicalPartition called "y"
    >>> hpy=HierarchicalPartition(['a','b','c','d','e','f'])
    >>> rooty=hpy.root()
    >>> n1y=hpy.add_child(rooty,['a','b','c'])
    >>> n2y=hpy.add_child(rooty,['d','e','f'])
    >>> dummy=hpy.add_child(n2y,['f'])
    >>> n3y=hpy.add_child(n2y,['d','e'])
    >>> dummy=hpy.add_child(n3y,['d'])
    >>> dummy=hpy.add_child(n3y,['e'])
    >>> # Now lets compare sub-trees.
    >>> print sub_hierarchical_mutual_information(hpx,hpy,rootx,rooty,0)
    0.69314718056
    >>> print sub_hierarchical_mutual_information(hpx,hpy,n1x,n1y,1)
    0.0
    """
    wx=hierpart_x.node_elements(node_x)
    wy=hierpart_y.node_elements(node_y)

    wxy=set(wx)&set(wy)
    denxy=float(len(wxy))
    if denxy==0.0 or hierpart_x.node_leaf(node_x) or hierpart_y.node_leaf(node_y):
        return 0.0

    # Compute Sx
    Sx=0.0
    for child_x in hierpart_x.node_children(node_x):
        w_child_x=hierpart_x.node_elements(child_x)
        w_child_x_wxy=set(w_child_x)&wxy
        num=float(len(w_child_x_wxy))
        frac=num/denxy
        Sx-=_plogp(frac)

    # Compute Sy
    Sy=0.0
    for child_y in hierpart_y.node_children(node_y):
        w_child_y=hierpart_y.node_elements(child_y)
        w_child_y_wxy=set(w_child_y)&wxy
        num=float(len(w_child_y_wxy))
        frac=num/denxy
        Sy-=_plogp(frac)

    # Compute Sxy
    Sxy=0.0
    second_term_xy=0.0
    for child_x in hierpart_x.node_children(node_x):
        w_child_x=hierpart_x.node_elements(child_x)
        for child_y in hierpart_y.node_children(node_y):
            w_child_y=hierpart_y.node_elements(child_y)
            w_child_xy=set(w_child_x)&set(w_child_y)
            num=float(len(w_child_xy))
            frac=num/denxy

            Sxy-=_plogp(frac)
            second_term_xy+=frac*sub_hierarchical_mutual_information(hierpart_x,hierpart_y,child_x,child_y,depth+1)

    one_step=Sx+Sy-Sxy
    #ret_val=Sx+Sy-Sxy+second_term_xy
    ret_val=one_step+second_term_xy

    if show:

        def node_communities(hierpart,node):
            s=''
            for child in hierpart.node_children(node):
                s=s+';'+','.join(hierpart.node_elements(child))
            return s[1:]

        print '# x',node_communities(hierpart_x,node_x)
        print '# y',node_communities(hierpart_y,node_y)
        print '# Sx',Sx
        print '# Sy',Sy
        print '# Sxy',Sxy
        print '# Sx+Sy-Sxy',one_step # Sx+Sy-Sxy
        print '# second_term_xy',second_term_xy
        print '# ret_val',ret_val

    return ret_val

def hierarchical_mutual_information(hierpart_x,hierpart_y,show=False):

    """Cumputes the hierarchical mutual information between two trees.
    More specifically, it computes I(T;T'), where T and T' are two <HierarchicalPartitions>.

    Parameters
    ----------
    hierpart_x : HierarchicalPartition
        The hierarchical partition T.
    hierpart_y : HierarchicalPartition
        The hierarchical partition T'.
    show : <bool>
        If True, information is printed on the screen as the computation progress.

    Returns
    -------
    : <float>
        The value I(T;T').

    Example
    -------
    >>> from hierpart import HierarchicalPartition
    >>> from hierpart import hierarchical_mutual_information
    >>> # Lets create a HierarchicalPartition called "x"
    >>> hpx=HierarchicalPartition(['a','b','c','d','e','f'])
    >>> rootx=hpx.root()
    >>> n1x=hpx.add_child(rootx,['a','b','c'])
    >>> n2x=hpx.add_child(rootx,['d','e','f'])
    >>> dummy=hpx.add_child(n1x,['a'])
    >>> n3x=hpx.add_child(n1x,['b','c'])
    >>> dummy=hpx.add_child(n3x,['b'])
    >>> dummy=hpx.add_child(n3x,['c'])
    >>> # Lets create another slightly different HierarchicalPartition called "y"
    >>> hpy=HierarchicalPartition(['a','b','c','d','e','f'])
    >>> rooty=hpy.root()
    >>> n1y=hpy.add_child(rooty,['a','b','c'])
    >>> n2y=hpy.add_child(rooty,['d','e','f'])
    >>> dummy=hpy.add_child(n2y,['f'])
    >>> n3y=hpy.add_child(n2y,['d','e'])
    >>> dummy=hpy.add_child(n3y,['d'])
    >>> dummy=hpy.add_child(n3y,['e'])
    >>> # Lets see how they look...
    >>> hpx.show()
    0 ['a', 'b', 'c', 'd', 'e', 'f']
    1 ['a', 'b', 'c']
    2 ['d', 'e', 'f']
    3 ['a']
    4 ['b', 'c']
    5 ['b']
    6 ['c']
    >>> hpy.show()
    0 ['a', 'b', 'c', 'd', 'e', 'f']
    1 ['a', 'b', 'c']
    2 ['d', 'e', 'f']
    3 ['f']
    4 ['d', 'e']
    5 ['d']
    6 ['e']
    >>> # Now we compare the hierarchies with themselves, and against each other.
    >>> print hierarchical_mutual_information(hpx,hpx)
    1.24245332489
    >>> print hierarchical_mutual_information(hpy,hpy)
    1.24245332489
    >>> print hierarchical_mutual_information(hpx,hpy)
    0.69314718056
    """
    assert isinstance(hierpart_x,HierarchicalPartition)
    assert isinstance(hierpart_y,HierarchicalPartition)
    root_x=hierpart_x.root()
    root_y=hierpart_y.root()
    return sub_hierarchical_mutual_information(hierpart_x,hierpart_y,root_x,root_y,0,show=show)

def normalized_hierarchical_mutual_information(hierpart_x,hierpart_y,show=False):
    """Computes the normalized hierarchical mutual information between two partitions.
    More specifically, it computes i(T;T') where T and T' are two <HierarchicalPartitions>.

    Parameters
    ----------
    hierpart_x : HierarchicalPartition
        The tree T.
    hierpart_y : HierarchicalPartition
        The tree T'.

    Returns
    -------
    : (<float>,<float>,<float>,<float>)
        It returns i(T;T'), I(T;T'), I(T;T), I(T';T')

    Example
    -------
    >>> from hierpart import HierarchicalPartition
    >>> from hierpart import normalized_hierarchical_mutual_information
    >>> # Lets create a HierarchicalPartition called "x"
    >>> hpx=HierarchicalPartition(['a','b','c','d','e','f'])
    >>> rootx=hpx.root()
    >>> n1x=hpx.add_child(rootx,['a','b','c'])
    >>> n2x=hpx.add_child(rootx,['d','e','f'])
    >>> dummy=hpx.add_child(n1x,['a'])
    >>> n3x=hpx.add_child(n1x,['b','c'])
    >>> dummy=hpx.add_child(n3x,['b'])
    >>> dummy=hpx.add_child(n3x,['c'])
    >>> # Lets create another slightly different HierarchicalPartition called "y"
    >>> hpy=HierarchicalPartition(['a','b','c','d','e','f'])
    >>> rooty=hpy.root()
    >>> n1y=hpy.add_child(rooty,['a','b','c'])
    >>> n2y=hpy.add_child(rooty,['d','e','f'])
    >>> dummy=hpy.add_child(n2y,['f'])
    >>> n3y=hpy.add_child(n2y,['d','e'])
    >>> dummy=hpy.add_child(n3y,['d'])
    >>> dummy=hpy.add_child(n3y,['e'])
    >>> # Lets see how they look...
    >>> hpx.show()
    0 ['a', 'b', 'c', 'd', 'e', 'f']
    1 ['a', 'b', 'c']
    2 ['d', 'e', 'f']
    3 ['a']
    4 ['b', 'c']
    5 ['b']
    6 ['c']
    >>> hpy.show()
    0 ['a', 'b', 'c', 'd', 'e', 'f']
    1 ['a', 'b', 'c']
    2 ['d', 'e', 'f']
    3 ['f']
    4 ['d', 'e']
    5 ['d']
    6 ['e']
    >>> # Now we compare the hierarchies with themselves, and against each other.
    >>> print normalized_hierarchical_mutual_information(hpx,hpx)
    (1.0, 1.242453324894, 1.242453324894, 1.242453324894)
    >>> print normalized_hierarchical_mutual_information(hpy,hpy)
    (1.0, 1.242453324894, 1.242453324894, 1.242453324894)
    >>> print normalized_hierarchical_mutual_information(hpx,hpy)
    (0.55788589130225974, 0.69314718055994529, 1.242453324894, 1.242453324894)
    """
    HMI_xx=hierarchical_mutual_information(hierpart_x,hierpart_x,show=False)    
    HMI_yy=hierarchical_mutual_information(hierpart_y,hierpart_y,show=False)    
    HMI_xy=hierarchical_mutual_information(hierpart_x,hierpart_y,show=show)    
    prod=HMI_xx*HMI_yy
    if prod>0.0:
        return HMI_xy/(prod**0.5),HMI_xy,HMI_xx,HMI_yy
    return 0.0,HMI_xy,HMI_xx,HMI_yy

if __name__=='__main__':
    import doctest
    print 'doctesting hierpart...'
    doctest.testmod()
    print 'hierpart doctest success.'

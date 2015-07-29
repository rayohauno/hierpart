Tutorial
========

The best way to learn to use **HierPart** is through a bunch of examples.

Example 1
+++++++++

..
    but, before continuing, a short comment about the coding style. Here, an underbar "_" is used as a prefix for objects variables. This allows the reader to easily distinguish *temporal* object variables from functions, classes or modules

The first example is about constructing a ``HierarchicalPartition`` object::

    >>> from hierpart import HierarchicalPartition
    >>>
    >>> # A HierarchicalPartition object is created. It contains the elements 'a','b',... 
    >>> # which, in this case are strings. But, they can be numbers, or whatever other 
    >>> # thing that can be stored in a set container.
    >>> hp=HierarchicalPartition(['a','b','c','d','e','f'])
    >>>
    >>> # To build the hierarchy, lets start from the root.
    >>> root=hp.root()
    >>>
    >>> # Lets add two children to the root. The elements the children will contain should 
    >>> # be specified. These elements should belong to the parent vertex, in this case, 
    >>> # the root. Otherwise, an error is raised.
    >>> n1=hp.add_child(root,['a','b','c'])
    >>> n2=hp.add_child(root,['d','e','f'])
    >>>
    >>> # Now we add children to the children, and so on...
    >>> hp.add_child(_n1,['a'])
    3
    >>> n3=hp.add_child(n1,['b','c'])
    >>> hp.add_child(n3,['b'])
    5
    >>> hp.add_child(n3,['c'])
    6

This creates the following hierarchy:

..
   .. image:: ./_images/hierpart_1.png
        :width: 200pt
..
   .. image:: ./_images/toy_hierarchy.jpg

.. image:: ./_images/toy_hierarchy.png
        :width: 200pt


Example 2
+++++++++

Two hierarchical partitions can be created, and compared with the hierarchical mutual information::

    >>> import hierpart as hp
    >>> 
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
    >>> # Now we compare the hierarchies with themselves, and against each other, using the hierarchical mutual information
    >>> print hierarchical_mutual_information(hpx,hpx)
    1.24245332489
    >>> print hierarchical_mutual_information(hpy,hpy)
    1.24245332489
    >>> print hierarchical_mutual_information(hpx,hpy)
    0.69314718056
    >>> # Now we repeat using the normalized hierarchical mutual information
    >>> print normalized_hierarchical_mutual_information(hpx,hpx)
    (1.0, 1.242453324894, 1.242453324894, 1.242453324894)
    >>> print normalized_hierarchical_mutual_information(hpy,hpy)
    (1.0, 1.242453324894, 1.242453324894, 1.242453324894)
    >>> print normalized_hierarchical_mutual_information(hpx,hpy)
    (0.55788589130225974, 0.69314718055994529, 1.242453324894, 1.242453324894)

..
   This tutorial was created using the IPython notebook [1]_.

..
   On how to use the ``HierarchicalPartition`` class
   -------------------------------------------------

.. References
   ----------
   .. [1] http://ipython.org/

.. HierPart documentation master file, created by
   sphinx-quickstart on Sat Jul 25 08:12:49 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

HierPart : a python package implementing the hierarchical partition data structure
==================================================================================

What is **HierPart**?
---------------------

**HierPart** is a python package that implements the *hierarchical partition* data structure [1]_. Furthermore, it can be used to compute the *hierarchical mutual information* between hierarchical partitions.

Hierarchical partitions can be used to represent the *hierarchical community structure* of a complex networks [2]_. Therefore, the hierarchical mutual information can be used to compare *hierarchical community structures*. In other words, the hierarchical mutual information provides a generalization of the traditional approach, where the standard mutual information is used to compare node partitions, ie., community structures. 

Table of Contents:
------------------

.. toctree::
   :maxdepth: 1

   installation
   tutorial
   documentation
   glossary
   references
   todo

..
    Typically, the idea is compare the performance of different community detection algorithms. For example, a bunch of benchmark tests, in the form of reference networks with planted community structures, are feeded to the community detection algorithms. Then, the *normalized* mutual information is used to compare the community structure identified by each algorithm, with the planted one. A normalized mutual information equal to one, indicates a perfect match, and a value close to zero, a bad result.

..
   Indices and tables
   ==================

..
   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`

Usage
=====

To use ``optimizer-model``, first you need to instantiate an
:class:`optimizer.Optimizer`:

.. code-block:: python

    from optimizer import Optimizer

    opt = Optimizer()

You can then add inputs variables to it:

.. code-block:: python

    from optimizer import Types

    i0 = opt.add_input(Types.INT)
    i1 = opt.add_input(Types.INT)

And then you can add operations, adding an operation returns a reference to the
result:

.. code-block:: python

    from optimizer import Operations

    i2 = opt.add_operation(Operations.INT_ADD, [i0, i1])
    opt.add_operation(Operations.FINISH, [i2])

When you're done, you can get a list of the operations that were performed
(after all of the optimizations have been applied):

.. code-block:: python

    ops = opt.build_operations()
    assert len(ops) == 3

Optimizations
-------------

Out of the box, an :class:`optimizer.Optimizer` doesn't actually run any
optimizations, it just records the operations. However, ``optimizer-model``
includes many optimizations which can be plugged in:

.. code-block:: python

    opt = Optimizer([list, of, optimization, classes])

The optimizations included with ``optimizer-model`` are:

.. class:: optimizer.optimizations.IntBounds

    Keeps track of the possible bounds for an integer and propogates that data.

.. class:: optimizer.optimizations.ConstantFold

    Performs constant folding on operations which do not have side-effects and
    which have all-constant arguments.

.. class:: optimizer.optimizations.GuardPropagation

    Promotes values to be constant after they've been guarded against.

.. class:: optimizer.optimizations.Virtualize

    Removes allocations which do not escapes the trace, and removes
    ``GETFIELD`` and ``SETFIELD`` operations on objects whose allocation has
    been removed.

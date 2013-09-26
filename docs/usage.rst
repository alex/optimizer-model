Usage
=====

.. class:: optimizer.Optimizer(optimization_classes=[])

    This is the core of ``optimizer-model``. By default it performs no
    optimizations, but you can easily add them:

    .. code-block:: python

        from optimizer import Optimizer

        opt = Optimizer()
        opt = Optimizer([optimization, classes, here])

    .. method:: add_input(tp)

        This adds input variables to a trace.


        .. code-block:: python

            from optimizer import Types

            i0 = opt.add_input(Types.INT)
            i1 = opt.add_input(Types.INT)

    .. method:: add_operation(op, args, descr=None)

        Adds an operation to the sequence of operations, and runs it through
        all of the optimizations. Returns a representation of the result.

        .. code-block:: python

            from optimizer import Operations

            i2 = opt.add_operation(Operations.INT_ADD, [i0, i1])
            opt.add_operation(Operations.FINISH, [i2])

    .. method:: build_operations()

        Returns a sequence of all of the operations, after optimizations:

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

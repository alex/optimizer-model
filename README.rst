Optimizer Model
===============

.. image:: https://travis-ci.org/alex/optimizer-model.png?branch=master
    :target: https://travis-ci.org/alex/optimizer-model

This is a prototype for a new conceptual model for the RPython JIT's optimizer.
It is designed for online processing of a linear sequence of instructions. It
supports pluggable optimization passes.

Internally it is designed for immutable operations/values, no-copying of data,
and no hash tables.

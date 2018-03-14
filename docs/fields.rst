=================
Fields
=================


.. currentmodule:: typedpy

.. contents:: :local:

The Basics - Usage
==================

Each field is a class. Using it has two variations: the simplified form is just the class names. For example:

.. code-block:: python

    names = Array[String]
    name_and_age = Tuple[String, PositiveFloat]
    age_by_name = Map[Sring, PositiveFloat]
    name = String
    quantity = Number

However, if more restriction are required, they need to be passed to the constructor. For Example:

.. code-block:: python

    name = Number(String(pattern='[A-Za-z]+$', maxLength=20)

Predefined Types
================

.. autoclass:: Field

Numerical
---------

:mod:`typedpy` defines the following basic field types:

.. autoclass:: Number

.. autoclass:: Integer

.. autoclass:: Float

.. autoclass:: Positive

.. autoclass:: PositiveFloat

.. autoclass:: PositiveInt

.. autoclass:: Boolean

String, Enums etc.
------------------

.. autoclass:: String

.. autoclass:: Enum

.. autoclass:: EnumString

.. autoclass:: Sized

.. autoclass:: DateString

.. autoclass:: TimeString

.. autoclass:: IPV4

.. autoclass:: JSONString

.. autoclass:: HostName

.. class:: EmailAddress

            String of an email address



Collections
-----------

**All collections support reference to another :class:`Structure`**. For example, this code is valid and will work the
way you'd expect:

.. code-block:: python

    class Foo(Structure):
          s = String

    class Bar(Structure):
          a = Set[Foo]
          b = Map [Foo, Integer]


.. autoclass:: Array

.. autoclass:: Set

.. autoclass:: Tuple

.. autoclass:: Map


* **Note** - The collections support embedded collections, such as :class:`Array` [ :class:`Tuple` [ :class:`Integer` , :class:`Integer` ]]

Re-use
======

.. autoclass:: AllOf

.. autoclass:: AnyOf

.. autoclass:: OneOf

.. autoclass:: NotField

**All the field types under this category support reference to another :class:`Structure`**. For example, this code is valid and will work the
way you'd expect:

.. code-block:: python

    class Foo(Structure):
          s = String

    class Bar(Structure):
          a = Any[Foo, Integer]

Inheritance and mixins
----------------------
Inheritance works the way you would expect:

.. code-block:: python

    # define a new mixin
    class Even(Field):
        def __set__(self, instance, value):
            if value % 2 > 0:
                raise ValueError('Must be even')
            super().__set__(instance, value)

    class EvenPositiveInt(Integer, Positive, Even): Pass

    # Done! Now we have a new Field type that we can use



.. _structure-as-field:

Using a Structure as a Field
----------------------------
Any Structure type can also be used as a field.

.. code-block:: python

    # Suppose we defined a new structure "Foo":
    class Foo(Structure):
        st = String

    # We can now use it as a Field:
    class Example(Structure):
        a = Foo
        b = Array[Foo]
        c = AnyOf[Foo, Integer]

    #This will raise a TypeError for a
    Example(a = 1, b=[], c=2)

    #This is valid
    Example(a=Foo(st=""), b=[Foo(st="xyz")], c=2))

.. _structure-inlining:

Inlining a Structure as a Field
-------------------------------
.. autoclass:: StructureReference


Immutability
============
To define an immutable Field, you use the mixin **ImmutableField**.
Example:

.. code-block:: python

    class ImmutableString(String, ImmutableField): pass

    class A(Structure):
        x = Number
        y = ImmutableString


    a = A(x=0.5, y="abc")

    # This will raise an ValueError exception, with the message  "y: Field is immutable"
    a.y += "xyz"


It is also possible to define an immutable Structure. See Under the **Structures** section.

Extension and Utilities
=======================


.. py:function::  create_typed_field(classname, cls, validate_func=None)

   Factory that generates a new class for a :class:`Field` as a wrapper of any class.

   Arguments:

        classname(`str`):
            A new name this class can be referenced by

        cls(`type`):
            The class we are wrapping

        validate_func(function): optional
            A validation function. It should raise an exception if the instance is invalid.


   Example:

    Given a class Foo, and a validation function for an instance of Foo, called validate_foo(foo):

    .. code-block:: python

        class Foo(object):
            def __init__(self, x):
                self.x = x


        ValidatedFooField = create_typed_field("FooField",
                                             Foo,
                                             validate_func=validate_foo)

    Generates a new :class:`Field` class that validates the content using validate_foo, and can be
    used just like any :class:`Field` type.

    .. code-block:: python

        class A(Structure):
            foo = ValidatedFooField
            bar = Integer

        # assuming we have an instance of Foo called my_foo, we can create a valid instance of A:
        A(bar=4, foo=my_foo)


from typing import Union
from unittest import TestCase

from checksignature import CheckSignature
from checksignature import checksignature


@checksignature
def function(a: str, b: int, c, **kwargs):
    return a, b, c, kwargs


class CheckSignatureTest(TestCase):

    def test_function_executes_with_compatible_signature(self):
        function('one', 2, 3.0, **{'four': 4})

    def test_TypeError_thrown_on_incompatible_signature(self):
        with self.assertRaises(TypeError):
            function(1, 2, 3.0, **{'four': 4})

    def test_can_handle_signature_with_Union(self):

        @checksignature
        def function(a: Union[int, str]):
            return a

        function(1) == 1

    def test_can_handle_signature_fail_with_Union(self):

        @checksignature
        def function(a: Union[int, str]):
            return a

        with self.assertRaises(TypeError):
            function(1.0)

    def test_function_with_no_type_hints(self):

        @checksignature
        def function(a, b, c):
            return a, b, c

        function('one', 2, 3.0)

    def test_keyword_only_signatures(self):

        @checksignature
        def function(a, b: int, *, key=None):
            return a, b, key

        function('one', 2, key=3)

    def test_can_handle_function_with_no_args(self):

        @checksignature
        def function():
            pass

        function()

    def test_can_handle_varargs(self):

        @checksignature
        def function(*a: int):
            return a

        function(1, 2, 3)  # should not raise

        with self.assertRaises(TypeError):
            function(1, 'two', 3.0)

        with self.assertRaises(TypeError):
            function(1, 2, 3.0)

    def test_can_handle_kw_varargs(self):

        @checksignature
        def function(**a: int):
            return a

        function(**{'one': 1, 'two': 2, 'three': 3})  # should not raise

        with self.assertRaises(TypeError):
            function(**{1: 'one', 'two': 2, 'three': 3})

        with self.assertRaises(TypeError):
            function(**{'one': 1, 2: 'two', 'three': 3})

        with self.assertRaises(TypeError):
            function(**{'one': 1, 'two': 2, 3: 'three'})

    def test_altogether_now(self):

        @checksignature
        def function(a: str, b: int, c, *args: int, **kwargs: Union[int, float]):
            return a, b, c, args, kwargs

        function('one', 2, 3.0, 10, 20, 30, **{'four': 4, 'five': 5})    # should not raise
        function('one', 2, 3.0, 10, 20, 30, **{'four': 4, 'five': 5.0})  # should not raise
        function('one', 2, 'x', 10, 20, 30, **{'four': 4, 'five': 5})    # should not raise

        with self.assertRaises(TypeError):
            function(1, 2, 3.0, 10, 20, 30, **{'four': 4, 'five': 5})

        with self.assertRaises(TypeError):
            function('one', 'x', 3.0, 10, 20, 30, **{'four': 4, 'five': 5})

        with self.assertRaises(TypeError):
            function('one', 2, 3.0, 'x', 20, 30, **{'four': 4, 'five': 5})

        with self.assertRaises(TypeError):
            function('one', 2, 3.0, 10, 20, 30, **{'four': 'x', 'five': 5})

    def test_functionless_CheckSignature_evalutation(self):
        CheckSignature().evaluate() == None

    def test_functionless_CheckSignature__call__(self):
        CheckSignature()() == None

    def test_CheckSignature__str__(self):

        @checksignature
        def function():
            pass

        str(function)         == 'function'
        str(CheckSignature()) == ''

    def test_CheckSignature__repr__(self):

        @checksignature
        def function(a):
            return a

        repr(function)         == '<CheckSignature(function)>'
        repr(CheckSignature()) == '<CheckSignature()>'


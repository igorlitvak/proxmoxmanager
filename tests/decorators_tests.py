from proxmoxmanager.utils import return_default_on_exception, reraise_exception_on_exception
import unittest


class ExceptionA(Exception):
    """
    Some exception
    """
    def __init__(self, *args):
        super().__init__(*args)


class ExceptionB(Exception):
    """
    Some exception
    """
    def __init__(self, *args):
        super().__init__(*args)


class ExceptionWithFields(Exception):
    """
    Some exception with fields
    """
    def __init__(self, foo, bar, *args):
        self.foo = foo
        self.bar = bar
        super().__init__(*args)


class TestDecorators(unittest.TestCase):
    """
    Unittest for decorators from proxmoxmanager.utils
    """

    def test_return_default_on_exception(self):
        @return_default_on_exception()
        def none_on_exception():
            raise Exception

        self.assertIsNone(none_on_exception())

        @return_default_on_exception(default_value="foo")
        def str_on_exception():
            raise Exception

        self.assertEqual(str_on_exception(), "foo")

        @return_default_on_exception(default_value=123)
        def int_on_exception():
            raise Exception

        self.assertEqual(int_on_exception(), 123)

        @return_default_on_exception()
        def catch_any_exception():
            raise ExceptionA

        self.assertIsNone(catch_any_exception())

        @return_default_on_exception(catch_errors=ExceptionA)
        def catch_specific_exception():
            raise ExceptionA

        self.assertIsNone(catch_specific_exception())

        @return_default_on_exception(catch_errors=(ExceptionA, ExceptionB))
        def catch_list_of_exceptions():
            raise ExceptionA

        self.assertIsNone(catch_list_of_exceptions())

        @return_default_on_exception(catch_errors=())
        def catch_no_exceptions():
            raise Exception

        self.assertRaises(Exception, catch_no_exceptions)

        @return_default_on_exception(catch_errors=ExceptionB)
        def catch_wrong_exception():
            raise ExceptionA

        self.assertRaises(ExceptionA, catch_wrong_exception)

        @return_default_on_exception(with_args=["foo", 123])
        def catch_with_args_list():
            raise Exception("foo", 123)

        self.assertIsNone(catch_with_args_list())

        @return_default_on_exception(with_args=("foo", 123))
        def catch_with_args_tuple():
            raise Exception("foo", 123)

        self.assertIsNone(catch_with_args_tuple())

        @return_default_on_exception(with_args=("foo", 123))
        def catch_with_wrong_args():
            raise Exception("foo", 321)

        self.assertRaises(Exception, catch_with_wrong_args)

        @return_default_on_exception(with_fields={"foo": 123, "bar": "baz"})
        def catch_with_fields():
            raise ExceptionWithFields(foo=123, bar="baz")

        self.assertIsNone(catch_with_fields())

        @return_default_on_exception(with_fields={"foo": 123})
        def catch_with_some_fields():
            raise ExceptionWithFields(foo=123, bar="baz")

        self.assertIsNone(catch_with_some_fields())

        @return_default_on_exception(with_fields={"foo": 123, "bar": "baz", "bad_field": 321})
        def catch_with_nonexistent_fields():
            raise ExceptionWithFields(foo=123, bar="baz")

        self.assertRaises(ExceptionWithFields, catch_with_nonexistent_fields)

        @return_default_on_exception(with_fields={"foo": 321, "bar": "baz"})
        def catch_with_wrong_fields():
            raise ExceptionWithFields(foo=123, bar="baz")

        self.assertRaises(ExceptionWithFields, catch_with_wrong_fields)

    def test_reraise_exception_on_exception(self):
        @reraise_exception_on_exception(Exception)
        def exception_on_exception():
            raise Exception

        self.assertRaises(Exception, exception_on_exception)

        @reraise_exception_on_exception(ExceptionA)
        def exception_a_on_exception():
            raise Exception

        self.assertRaises(ExceptionA, exception_a_on_exception)

        @reraise_exception_on_exception(ExceptionB, catch_errors=ExceptionA)
        def catch_specific_exception():
            raise ExceptionA

        self.assertRaises(ExceptionB, catch_specific_exception)

        @reraise_exception_on_exception(ExceptionB)
        def catch_any_exception():
            raise ExceptionA

        self.assertRaises(ExceptionB, catch_any_exception)

        @reraise_exception_on_exception(ExceptionB, catch_errors=(ExceptionA, ExceptionB))
        def catch_list_of_exceptions():
            raise ExceptionA

        self.assertRaises(ExceptionB, catch_list_of_exceptions)

        @reraise_exception_on_exception(ExceptionA, catch_errors=())
        def catch_no_exceptions():
            raise Exception

        self.assertRaises(Exception, catch_no_exceptions)

        @reraise_exception_on_exception(ExceptionB, catch_errors=ExceptionB)
        def catch_wrong_exception():
            raise ExceptionA

        self.assertRaises(ExceptionA, catch_wrong_exception)

        @reraise_exception_on_exception(ExceptionA, with_args=["foo", 123])
        def catch_with_args_list():
            raise Exception("foo", 123)

        self.assertRaises(ExceptionA, catch_with_args_list)

        @reraise_exception_on_exception(ExceptionA, with_args=("foo", 123))
        def catch_with_args_tuple():
            raise Exception("foo", 123)

        self.assertRaises(ExceptionA, catch_with_args_tuple)

        @reraise_exception_on_exception(ExceptionB, with_args=("foo", 123))
        def catch_with_wrong_args():
            raise ExceptionA("foo", 321)

        self.assertRaises(ExceptionA, catch_with_wrong_args)

        @reraise_exception_on_exception(Exception("bar", 777))
        def reraise_with_args():
            raise Exception

        with self.assertRaises(Exception) as assertion:
            reraise_with_args()

        self.assertEqual(assertion.exception.args, ("bar", 777))

        @reraise_exception_on_exception(Exception("bar", 777), with_args=("foo", 123))
        def catch_and_reraise_with_args():
            raise Exception("foo", 123)

        with self.assertRaises(Exception) as assertion:
            reraise_with_args()

        self.assertEqual(assertion.exception.args, ("bar", 777))

        @reraise_exception_on_exception(ExceptionA, with_fields={"foo": 123, "bar": "baz"})
        def catch_with_fields():
            raise ExceptionWithFields(foo=123, bar="baz")

        self.assertRaises(ExceptionA, catch_with_fields)

        @reraise_exception_on_exception(ExceptionA, with_fields={"foo": 123})
        def catch_with_some_fields():
            raise ExceptionWithFields(foo=123, bar="baz")

        self.assertRaises(ExceptionA, catch_with_some_fields)

        @reraise_exception_on_exception(ExceptionA, with_fields={"foo": 123, "bar": "baz", "bad_field": 321})
        def catch_with_nonexistent_fields():
            raise ExceptionWithFields(foo=123, bar="baz")

        self.assertRaises(ExceptionWithFields, catch_with_nonexistent_fields)

        @reraise_exception_on_exception(ExceptionA, with_fields={"foo": 321, "bar": "baz"})
        def catch_with_wrong_fields():
            raise ExceptionWithFields(foo=123, bar="baz")

        self.assertRaises(ExceptionWithFields, catch_with_wrong_fields)


if __name__ == '__main__':
    unittest.main()

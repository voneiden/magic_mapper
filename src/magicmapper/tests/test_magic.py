import unittest

from ..magicmapper import Schema, Value, magic_map, Variable, List


class MagicTestCase(unittest.TestCase):
    def test_default_widget_size(self):
        test_source_data = [
            {"person": {"name": "foo1"}},
            {"person": {"name": "foo2"}},
        ]
        schema = {"names": Schema({"name": Value("person") >> Value("name")})}
        result = magic_map(schema, test_source_data)
        self.assertEqual({"names": [{"name": "foo1"}, {"name": "foo2"}]}, result)

    def test_magic_variables(self):
        test_source_data = {"foo": {"bar": [{"name": "foo1"}, {"name": "foo2"}]}}

        schema = {
            "names": Variable("testvar")
            >> List("bar", min_length=1)
            >> Schema({"name": Value("name")})
        }

        result = magic_map(
            schema, test_source_data, variables={"testvar": Value("foo")}
        )
        self.assertEqual({"names": [{"name": "foo1"}, {"name": "foo2"}]}, result)

    def test_list_cast(self):
        test_source_data = {"devices": {"name": "onlydevice"}}
        schema = {
            "devices": List("devices", cast=True) >> Schema({"name": Value("name")})
        }

        result = magic_map(schema, test_source_data)
        self.assertEqual({"devices": [{"name": "onlydevice"}]}, result)

        test_source_data = {"devices": [{"name": "d1"}, {"name": "d2"}]}
        result = magic_map(schema, test_source_data)
        self.assertEqual({"devices": [{"name": "d1"}, {"name": "d2"}]}, result)

    def test_list_reduce(self):
        test_source_data = {
            "devices": [
                {"name": "notinterested", "data": [{"value": 1}]},
                {"name": "notinterested2", "data": [{"value": 2}]},
            ]
        }

        schema = {
            "values": List(
                "devices",
                reduce=(lambda x, y: x + [v["value"] for v in y["data"]], lambda: []),
            )
        }
        result = magic_map(schema, test_source_data)
        self.assertEqual({"values": [1, 2]}, result)

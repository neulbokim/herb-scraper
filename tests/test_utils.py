import unittest
from crawler.utils import save_json, load_json

class TestUtils(unittest.TestCase):
    def test_json_save_load(self):
        """JSON 데이터를 저장하고 정상적으로 불러올 수 있는지 테스트"""
        sample_data = {"test_key": "test_value"}
        save_json(sample_data, "test.json", folder="data/processed")

        loaded_data = load_json("test.json", folder="data/processed")
        self.assertEqual(loaded_data, sample_data)

if __name__ == "__main__":
    unittest.main()

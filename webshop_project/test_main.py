import unittest
import urllib.request
import json


class TestBackendAPI(unittest.TestCase):
    def test_read_products_endpoint(self):
        url = "http://localhost:8000/products"
        try:
            response = urllib.request.urlopen(url)
            status = response.getcode()
            data = json.loads(response.read().decode('utf-8'))

            self.assertEqual(status, 200)
            self.assertIsInstance(data, list)
        except Exception as e:
            self.fail(f"HTTP Request failed: {e}")

    def test_add_product_endpoint(self):
        url = "http://localhost:8000/add-test-product?name=TestIntegrationToy&price=990.0"
        try:
            req = urllib.request.Request(url, method="POST")
            response = urllib.request.urlopen(req)
            status = response.getcode()
            data = json.loads(response.read().decode('utf-8'))

            self.assertEqual(status, 200)
            self.assertIn("added", data["message"])
        except Exception as e:
            self.fail(f"HTTP Request failed: {e}")


if __name__ == "__main__":
    unittest.main()
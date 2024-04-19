import json
import os
import unittest
import sys

print(sys.path)
from epycocotools.coco import COCO
import json
import unittest


class CocoTestCase(unittest.TestCase):
    TEST_DATA_FILE = "/tmp/test_dataset.json"

    def setUp(self):
        # Set up any necessary test data or configurations
        # Create a temporary test JSON file in COCO dataset format
        test_data = {
            "info": {
                "description": "Test dataset",
                "version": "1.0",
                "year": 2022,
                "contributor": "Your Name",
                "date_created": "2022-01-01",
            },
            "images": [
                {"id": 1, "file_name": "image1.jpg", "width": 800, "height": 600},
                {"id": 2, "file_name": "image2.jpg", "width": 1024, "height": 768},
            ],
            "annotations": [
                {
                    "id": 1,
                    "image_id": 1,
                    "category_id": 1,
                    "bbox": [100, 100, 200, 200],
                    "area": 40000,
                    "iscrowd": 0,
                },
                {
                    "id": 2,
                    "image_id": 2,
                    "category_id": 2,
                    "bbox": [200, 200, 300, 300],
                    "area": 60000,
                    "iscrowd": 0,
                },
            ],
            "categories": [
                {"id": 1, "name": "cat", "supercategory": "animal"},
                {"id": 2, "name": "dog", "supercategory": "animal"},
            ],
        }
        with open(self.TEST_DATA_FILE, "w") as f:
            json.dump(test_data, f)

    def tearDown(self):
        os.remove(self.TEST_DATA_FILE)

    def test_load_annotations(self):
        coco_obj = COCO(self.TEST_DATA_FILE)
        annotations = coco_obj.loadAnns(ids=[1, 2])

        self.assertEqual(len(annotations), 2)
        self.assertEqual(annotations[0]["id"], 1)
        self.assertEqual(annotations[0]["image_id"], 1)
        self.assertEqual(annotations[0]["category_id"], 1)
        self.assertEqual(annotations[0]["bbox"], [100, 100, 200, 200])
        self.assertEqual(annotations[0]["area"], 40000)
        self.assertEqual(annotations[0]["iscrowd"], 0)

        self.assertEqual(annotations[1]["id"], 2)
        self.assertEqual(annotations[1]["image_id"], 2)
        self.assertEqual(annotations[1]["category_id"], 2)
        self.assertEqual(annotations[1]["bbox"], [200, 200, 300, 300])
        self.assertEqual(annotations[1]["area"], 60000)
        self.assertEqual(annotations[1]["iscrowd"], 0)


if __name__ == "__main__":
    unittest.main()

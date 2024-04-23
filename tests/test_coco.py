import json
import os
import unittest

import numpy as np
from src.epycocotools.coco import COCO


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
                {
                    "id": 3,
                    "image_id": 2,
                    "category_id": 2,
                    "bbox": [1, 2, 3, 4],
                    "area": 12,
                    "iscrowd": 1,
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
        # Load the annotations from the test data file
        coco_obj = COCO(self.TEST_DATA_FILE)
        annotations = coco_obj.loadAnns(ids=[1, 2])

        # Assert the expected behavior of the function
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

    def test_create_index(self):
        coco_obj = COCO(self.TEST_DATA_FILE)
        coco_obj.createIndex()
        # Assert that the index has been created successfully
        self.assertIsNotNone(coco_obj.dataset)
        self.assertIsNotNone(coco_obj.anns)
        self.assertIsNotNone(coco_obj.cats)
        self.assertIsNotNone(coco_obj.imgs)

    def test_get_ann_ids(self):
        coco_obj = COCO(self.TEST_DATA_FILE)
        coco_obj.createIndex()
        # Get annotation ids for specific image and category
        ann_ids = coco_obj.getAnnIds(imgIds=[1], catIds=[1])
        # Assert that the correct annotation ids are returned
        self.assertEqual(ann_ids, [1])

    def test_get_cat_ids(self):
        coco_obj = COCO(self.TEST_DATA_FILE)
        coco_obj.createIndex()
        # Get category ids for specific category names
        cat_ids = coco_obj.getCatIds(catNms=["cat"])
        # Assert that the correct category ids are returned
        self.assertEqual(cat_ids, [1])

    def test_get_img_ids(self):
        coco_obj = COCO(self.TEST_DATA_FILE)
        coco_obj.createIndex()
        # Get image ids for specific image and category
        img_ids = coco_obj.getImgIds(imgIds=[1], catIds=[1])
        # Assert that the correct image ids are returned
        self.assertEqual(img_ids, [1])

    def test_load_anns(self):
        coco_obj = COCO(self.TEST_DATA_FILE)
        coco_obj.createIndex()
        # Load specific annotations by their ids
        annotations = coco_obj.loadAnns(ids=[1])
        # Assert that the correct annotations are loaded
        self.assertEqual(len(annotations), 1)
        self.assertEqual(annotations[0]["id"], 1)

    def test_load_cats(self):
        coco_obj = COCO(self.TEST_DATA_FILE)
        coco_obj.createIndex()
        # Load specific categories by their ids
        categories = coco_obj.loadCats(ids=[1])
        # Assert that the correct categories are loaded
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0]["id"], 1)

    def test_load_imgs(self):
        coco_obj = COCO(self.TEST_DATA_FILE)
        coco_obj.createIndex()
        # Load specific images by their ids
        images = coco_obj.loadImgs(ids=[1])
        # Assert that the correct images are loaded
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0]["id"], 1)

    def test_load_numpy_annotations(self):
        coco = COCO()
        data = np.array([[1, 100, 200, 50, 50, 0.9, 1], [2, 150, 250, 70, 60, 0.8, 2]])
        annotations = coco._loadNumpyAnnotations(data)
        self.assertEqual(len(annotations), 2)
        self.assertEqual(annotations[0]["image_id"], 1)
        self.assertEqual(annotations[0]["bbox"], [100, 200, 50, 50])
        self.assertEqual(annotations[0]["score"], 0.9)
        self.assertEqual(annotations[0]["category_id"], 1)
        self.assertEqual(annotations[1]["image_id"], 2)
        self.assertEqual(annotations[1]["bbox"], [150, 250, 70, 60])
        self.assertEqual(annotations[1]["score"], 0.8)
        self.assertEqual(annotations[1]["category_id"], 2)

    def test_getAnnIds_with_areaRange(self):
        coco_obj = COCO(self.TEST_DATA_FILE)
        areaRange = {"min": 0, "max": 40001}
        ann_ids = coco_obj.getAnnIds(areaRng=areaRange)
        # Assert that the correct annotation ids are returned based on area range
        self.assertEqual(ann_ids, [1, 3])

    def test_getAnnIds_with_iscrowd(self):
        coco_obj = COCO(self.TEST_DATA_FILE)
        iscrowd = True
        ann_ids = coco_obj.getAnnIds(iscrowd=iscrowd)
        # Assert that the correct annotation ids are returned based on iscrowd flag
        self.assertEqual(ann_ids, [3])

    def test_getAnnIds_with_is_not_crowd(self):
        coco_obj = COCO(self.TEST_DATA_FILE)
        iscrowd = False
        ann_ids = coco_obj.getAnnIds(iscrowd=iscrowd)
        # Assert that the correct annotation ids are returned based on iscrowd flag
        self.assertEqual(ann_ids, [1, 2])


if __name__ == "__main__":
    unittest.main()

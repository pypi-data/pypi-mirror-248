import unittest
import os
import shutil
from psmanager.project_structure_manager import ProjectStructureManager

class TestProjectStructureManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = "temp_test_dir"
        self.manager = ProjectStructureManager(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_structure(self):
        self.manager.create_structure()
        # Let's check that the directories and files have been created
        self.assertTrue(os.path.exists(self.temp_dir))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "mypackage")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "mypackage", "__init__.py")))

    def test_load_structure_from_json(self):
        # Let's create the structure and then load from the standard file
        self.manager.create_structure()
        self.manager.load_structure_from_json()
        # Let's check that the directories and files have been created
        self.assertTrue(os.path.exists(self.temp_dir))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "mypackage")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "mypackage", "__init__.py")))

    def test_create_structure_with_content(self):
        self.manager.create_structure_with_content()
        # Let's check that the directories and files have been created
        self.assertTrue(os.path.exists(self.temp_dir))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "mypackage")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "mypackage", "__init__.py")))
        # Let's check that the files contain the expected content.
        expected_content = self.manager.structure_data["mypackage"]["__init__.py"] if "mypackage" in self.manager.structure_data and "__init__.py" in self.manager.structure_data["mypackage"] else ""
        file_content = self.manager.get_file_content(os.path.join(self.temp_dir, "mypackage", "__init__.py"))
        self.assertEqual(file_content, expected_content)

if __name__ == '__main__':
    unittest.main()

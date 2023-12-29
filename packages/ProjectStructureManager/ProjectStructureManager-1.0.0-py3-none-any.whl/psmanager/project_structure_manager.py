# project_structure_manager.py

import os
import json

class ProjectStructureManager:
    def __init__(self, base_path, structure_file="structure.json"):
        self.base_path = base_path
        self.structure_file = structure_file
        self.structure_data = self.load_structure_from_json()

    def load_structure_from_json(self):
        with open(self.structure_file, 'r') as file:
            structure_data = json.load(file)
        return structure_data

    def create_structure(self):
        self._create_item(self.base_path, "", self.structure_data)

    def create_structure_with_content(self):
        self._create_item_with_content(self.base_path, "", self.structure_data)

    def _create_item(self, base_path, current_path, item):
        current_path = os.path.join(base_path, current_path)

        if isinstance(item, dict):
            os.makedirs(current_path, exist_ok=True)
            for key, value in item.items():
                self._create_item(current_path, key, value)
        elif isinstance(item, str):
            self._create_file_with_content(current_path, item)

    def _create_item_with_content(self, base_path, current_path, item):
        current_path = os.path.join(base_path, current_path)

        if isinstance(item, dict):
            os.makedirs(current_path, exist_ok=True)
            for key, value in item.items():
                self._create_item_with_content(current_path, key, value)
        elif isinstance(item, str):
            self._create_file_with_content(current_path, item)

    def _create_file_with_content(self, file_path, content):
        with open(file_path, 'w') as file:
            file.write(content)

    def get_file_content(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()


if __name__ == "__main__":
    manager = ProjectStructureManager("./", "structure.json")
    # manager.create_structure()
    manager.create_structure_with_content()

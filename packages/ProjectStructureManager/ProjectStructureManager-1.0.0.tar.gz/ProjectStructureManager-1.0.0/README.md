
[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=PROJECT+STRUCTURE+MANAGER)](https://github.com/komanch7/projectstructuremanager)
---

### 🔥 My Stats:
[![GitHub Streak](https://github-readme-streak-stats.herokuapp.com/?user=komanch7&theme=dark&background=0d1117)](https://github.com/komanch7/projectstructuremanager/pulse)

- Information is presented in several languages:
    
    | [German](https://github.com/komanch7/projectstructuremanager/blob/main/docs/README_DE.md) |
    [Russian](https://github.com/komanch7/projectstructuremanager/blob/main/docs/README_RU.md) |
    [Ukrainian](https://github.com/komanch7/projectstructuremanager/blob/main/docs/README_UA.md) |


# projectstructuremanager
ProjectStructureManager is a Python project for creating folder and file structures exactly as the developer modeled the project.

## ProjectStructureManager Structure
The project has the following structure:
```
|--docs/
||--__init__.py
||--README_DE.md
||--README_RU.md
||--README_UA.md
|--psmanager/
||--__init__.py
||--project_structure_manager.py
|--tests/
||--__init__.py
||--test_psmanager.py
||--test_structure.json
|--LICENSE
|--main.py
|--README.md
|--requirements.txt
|--structure.json
```
## Tech Stack

**Server:** Python 3.9^

---

# Clone this repository

```sh
gh repo clone komanch7/projectstructuremanager psm-pro

cd psm-cli

  or

git clone https://github.com/komanch7/projectstructuremanager psm-pro

cd psm-pro
```
## Create and activate a virtual environment
```python
python -m venv venv

venv\Scripts\activate

python -m pip install --upgrade pip
  or
python3 -m pip install --upgrade pip
```
## Usage
```python
# main.py

from psmanager.project_structure_manager import ProjectStructureManager

if __name__ == "__main__":
    path = "."
    file_struct = "structure.json"
    manager = ProjectStructureManager(path, file_struct)
    manager.create_structure()
```
### Installing modules from requirements.txt
- If the requirements.txt file contains models, then enter the following command in the terminal
```
pip install -r requirements.txt
```
## Command to run tests
```
python -m unittest discover -s tests 
```
## Response
```bash
>> test_create_structure (test_psmanager.TestProjectStructureManager) ... ok
>> test_create_structure_with_content (test_psmanager.TestProjectStructureManager) ... ok
>> test_load_structure_from_json (test_psmanager.TestProjectStructureManager) ... ok
>> 
>> ----------------------------------------------------------------------
>> Ran 3 tests in 0.425s
>> 
>> OK
```

# Create the structure
```python
python main.py
  or
python3 main.py
```
## Deactivate environment
- Command to deactivate the virtual environment upon completion of work
```
deactivate
```
### JSON test project model
```json
{
    "mypackage": {
        "mypackage": {
            "controllers": {
                "__init__.py": "",
                "control_one.py": "",
                "control_two.py": "",
                "control_three.py": "",
                "control_four.py": ""
            },
            "__init__.py": "",
            "models": {
                "__init__.py": "",
                "model_one.py": "",
                "model_two.py": "",
                "model_three.py": "",
                "model_four.py": ""
            }
        },
        "__init__.py": "# None",
        "tests": {
            "__init__.py": "",
            "test_one.py": "",
            "test_two.py": "",
            "test_three.py": "",
            "test_four.py": ""
        },
        "docs": {
            "__init__.py": "",
            "README.md": ""
        },
        "main.py": "# main()",
        "requirements.txt": "# requirements.txt"
    }
}
```
## Test Structure
Folder and file structure for the future project:
```
|--mypackage/
||--mypackage/
|||--__init__.py
|||--controllers/
||||--__init__.py
||||--control_one.py
||||--control_two.py
||||--control_three.py
||||--control_four.py
|||--models/
||||--__init__.py
||||--model_one.py
||||--model_two.py
||||--model_three.py
||||--model_four.py
||--tests/
||||--__init__.py
||||--test_one.py
||||--test_two.py
||||--test_three.py
||||--test_four.py
||--__init__.py
||--docs/
||||--__init__.py
||||--README.md
||--main.py
||--requirements.txt
||--LICENSE
```
## 🚀 About Me
- I'm a beginner in Python development. Thank you for your understanding and support.

## License
[MIT](https://github.com/komanch7/projectstructuremanager/LICENSE)

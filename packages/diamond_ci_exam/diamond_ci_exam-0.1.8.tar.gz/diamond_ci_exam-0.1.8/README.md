# Exam Continuous Integration EPSI DevOps 3A
## Authors :
    - Thibault Scorielle 
    - Antoine Letailleur
    - Dimitri Perreaux

[package on pypi.org](https://pypi.org/project/diamond_ci_exam/)


## Purpose :
The objective of this project is to generate a diamond pattern using letters. The script takes a letter as a parameter and displays a diamond, starting with 'A', where the provided letter marks the widest point of the diamond.
### Exemple :
diamond('A')
```
A
```

diamond('B')
```
 A
B B
 A
```

diamond('C')
```
  A
 B B
C   C
 B B
  A
```

### Want to use this project?
1. FORK / CLONE

#### run the project 
```shell
$ cd diamond_ci_exam
$ py diamond_ci_exam.py '<your_letter>'
#ex : $ py diamond_ci_exam.py 'J'
```
(default parameter : 'F')


2. CREATE and ACTIVATE a VIRTUAL ENVIRONMENT **to use poetry**
#### Install venv
```shell
$ py -m pip install --user virtualenv
```
#### Create virtual env
```shell
$ py venv env
```
#### Activate virtual env
```shell
$ .\env\Scripts\activate
```
#### Install pipx
```shell
$ python -m pip install pipx
$ python -m pipx ensurepath
```

[README.md repo pipx](https://github.com/pypa/pipx/blob/main/README.md)
#### Install poetry
```shell
$ pipx install poetry
```
[POETRY documentation](https://python-poetry.org/docs/)
#### Install poetry dependencies
```shell
$ poetry install
```

### Run Linters locally with poetry
```shell
$ poetry run flake8 ./diamond_ci_exam/diamond_ci_exam.py
$ poetry run isort ./diamond_ci_exam/diamond_ci_exam.py
$ poetry run bandit ./diamond_ci_exam/diamond_ci_exam.py
```
[FLAKE8](https://flake8.pycqa.org/en/latest/) : check PEP8\
[ISORT](https://github.com/gforcada/flake8-isort) : check imports\
[BANDIT](https://github.com/tylerwince/flake8-bandit) : find common security issues in Python code

3. TESTS
### Unit Tests locally 
- witout poetry
```shell
$ python -m unittest discover -s test 
```
- with poetry 
```shell
$ poetry run python -m unittest discover -s test 
```

[unittest discover arguments](https://docs.python.org/3/library/unittest.html#unittest-test-discovery)

4. PUBLISH PACKAGE
```shell
$ poetry publish --build --username __token__ --password <pypi API token>
```
[poetry publish arguments](https://python-poetry.org/docs/cli/#publish)

/!\ Don't forget to change the version of the package in pyproject.toml when you want to push and to update the package /!\


** Project is written with python 3.11 and tested on 3.9, 3.10, 3.11 **
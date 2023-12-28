# Exam Continuous Integration EPSI DevOps 3A
## Authors :
    - Thibault Scorielle 
    - Antoine Letailleur
    - Dimitri Perreaux
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
$ .\env\Scripts\ativate
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
### Units Tests locally
```shell
$ python -m unittest discover -s test 
```
[unittest discover arguments](https://docs.python.org/3/library/unittest.html#unittest-test-discovery)

[package on pypi.org](https://pypi.org/project/diamond_ci_exam/)
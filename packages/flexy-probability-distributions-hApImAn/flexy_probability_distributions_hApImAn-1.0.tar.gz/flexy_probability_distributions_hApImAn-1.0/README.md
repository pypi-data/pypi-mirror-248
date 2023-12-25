# Python Package
## Installing a Python Package using Modularized Code
You can put your code into the python_package folder in your local computer or a virtual environment (see bottom page for more info in virtual env). Inside the python_package folder, you'll need to create a few folders and files:
* a setup.py file, which is required in order to use pip install
* a folder called 'distributions', which is the name of the Python package
* inside the 'distributions' folder, you'll need the Gaussiandistribution.py file, Generaldistribution.py and an __init__.py file.

Once everything is set up, you'll need to open a new terminal and do the following command:
- switch to the python package directory
- run command `pip install .`
  If everything is set up correctly, pip will install the distributions package into the workspace. You can then start the python interpreter from the terminal typing:
`python`
- then within the interpreter,  you can use the distributions package:  
    ```python
    from distributions import Gaussian
    Test using: 
    gaussian_one = Gaussian(25, 2)
    gaussian_one.mean
    gaussian_one + gaussian_one
    ```
## How to use venv and pip, the commands look something like this:
```python
python3 -m venv environmentname
source environmentname/bin/activate
pip install numpy
```
It is advisable to switch to a virtual environment when installing packages that are not directly available on python. 

## You can install this package from the test.pypi.org repository using the following command
`pip install -i https://test.pypi.org/simple/ flexy-probability-distributions`

Thank you for checking this awesome distributions project out. Feel free to reach out if you have any question. 

Happy Coding! :)
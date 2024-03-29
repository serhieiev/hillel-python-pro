# lesson_01: Unix CLI utils

## Home assignment

1. Написати команду, що порахує кількість символів у N рядку файлу. Число N повинно бути задано за допомогою environment variable.
2. Встановити python 3.9+
3. Встановити pipenv
4. Створити своє середовище за допомогою pipenv

Як результат скинути скріншот консолі з командами. Можна викласти на github.

## Solution

### Command to count characters of a given line

```bash
export COUNT_CHARS=5
sed -n "${COUNT_CHARS}p" filename | wc -c
```

The `sed -n "${COUNT_CHARS}p" filename` command prints only the specified line of the file named `filename` and `wc -c` counts the number of characters in that line. Replace filename with the actual name of your file.

<img width="580" alt="count_chars_output" src="https://github.com/serhieiev/hillel-python-pro/assets/12089303/bf7be1a7-33be-4792-81ae-2cecdb6365c3">

### Installing Python with pyenv

pyenv is a robust Python version manager, allowing developers to easily switch between multiple versions of Python. It is simple, unobtrusive, and follows the UNIX tradition of single-purpose tools that do one thing well. For an in-depth introduction to `pyenv`, follow this Real Python [tutorial](https://realpython.com/intro-to-pyenv/).

This guide will help you to install `pyenv` and setup specific versions of Python.

To install `pyenv` on MacOS using Homebrew, follow the steps below:

Update Homebrew:

```bash
brew update
brew install pyenv
```

You can confirm the installation and check your `pyenv` version with:

```bash
pyenv -v
```

Before installing a specific version of Python, it's helpful to check its availability. For example, if we want to install Python 3.9:

```bash
pyenv install --list | grep "3.9.*"
```

This command will display all available versions starting with 3.9

To install Python `3.9.16`, use the following command:

```bash
pyenv install -v 3.9.16
```

Let's also install Python 3.10.11:

```bash
pyenv install -v 3.10.11
```

After installation, you can set a global Python version. For instance, to set `3.10.11` as the default Python version, use:

```bash
pyenv global 3.10.11
```

At this point, you should have a functioning pyenv setup with your desired Python versions installed. You can check the installation by invoking the Python version with:

```bash
pyenv versions
python -V
```

You should see installed versions and your global Python version.

<img width="500" alt="pyenv_output" src="https://github.com/serhieiev/hillel-python-pro/assets/12089303/376551ca-1699-4ccf-9260-bb9fc0d47733">

### Installing pipenv

Install pipenv using pip:

```bash
pip install pipenv
```

<img width="544" alt="install_pipenv_output" src="https://github.com/serhieiev/hillel-python-pro/assets/12089303/f2117936-2430-48ea-aaff-75158161793f">

### Creating a virtual environment with pipenv

Navigate to your desired project directory and initialize a new pipenv project:

```bash
mkdir my_project
cd my_project
pipenv --python 3.10
```

To activate the virtual environment, you use the shell command:

```bash
pipenv shell
```

You can now install packages using pipenv. For example, to install the `requests` library:

```bash
pipenv install requests
```

This command not only installs the library, but also adds it to your `Pipfile` as a project dependency. You can see the `Pipfile` and `Pipfile.lock` in your project directory. These files keep track of your project's dependencies and the exact versions used, making it easy for others to replicate your environment.

<img width="585" alt="create_env_output" src="https://github.com/serhieiev/hillel-python-pro/assets/12089303/76b12b29-6934-4c8d-a148-29ce542ac2e1">

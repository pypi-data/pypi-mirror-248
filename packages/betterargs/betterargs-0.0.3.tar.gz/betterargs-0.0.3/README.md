# betterargs

A tool to create a command-line interface for your app using python

## Installation

- **Requirements**
    - python3.10
    - pip3

```bash
pip install betterargs
```

## Releases

Packaging and releases are handled in the [packaging branch](https://github.com/danielmuringe/betterargs/tree/packaging).

MAIN BRANCH IS RESERVED FOR MAINTAINING CODE ONLY!!!

- [version 0.0.3](https://github.com/danielmuringe/betterargs/releases/tag/v0.0.3)

- [version 0.0.2](https://github.com/danielmuringe/betterargs/releases/tag/v.0.0.2)


## Usage

- Create a command string in YAML format in a:
    1. YAML file
    2. Python dictionary
    3. Python string

- Convert the yaml file to command line namespace using appropriate function

### 1. Using a [YAML file](https://github.com/danielmuringe/betterargs/tree/dev/testing/command_tree.yaml)
```yaml
# Create command tree in a yaml file

git:
    args:
        path:
            atype: flag
            help: Path of the repo
    subparsers:
        parsers:
            clone:
                args:
                    quiet-clone:
                        atype: flag
                        help: Operate quietly. Progress is not reported to the standard error stream.
                    no-checkout:
                        help: No checkout of HEAD is performed after the clone is complete
            init:
                args:
                    quiet-init:
                        atype: flag
                        help: Operate quietly. Progress is not reported to the standard error stream.
```


```python
# Import betterargs
import betterargs


# Create command line namespace and get arguments
command_tree_PATH = 'command_tree.yaml'

args = betterargs.format_path_tree(command_tree_PATH)
```

### 2. Using [Python Dictionary in YAML Format](https://github.com/danielmuringe/betterargs/blob/dev/testing/format_dict_tree_test.py)

```python
# Import betterargs
import betterargs


# Define command tree in a dictionary in YAML format
command_tree_DICT = {
    "git": {
        "args": {
            "path": {
                "atype": "flag",
                "help": "Path of the repo",
            },
        },
        "subparsers": {
            "parsers": {
                "clone": {
                    "args": {
                        "quiet-clone": {
                            "atype": "flag",
                            "help": "Operate quietly. Progress is not reported to the standard error stream.",
                        },
                        "no-checkout": {
                            "help": "No checkout of HEAD is performed after the clone is complete"
                        },
                    },
                },
                "init": {
                    "args": {
                        "quiet-init": {
                            "atype": "flag",
                            "help": "Operate quietly. Progress is not reported to the standard error stream.",
                        },
                    },
                },
            },
        },
    },
}


# Create command line namespace and get arguments
args = betterargs.format_dict_tree(command_tree_DICT)
```

### 3. Using [string in YAML Format](https://github.com/danielmuringe/betterargs/blob/dev/testing/format_str_tree_test.py)


```python
# Import betterargs
import betterargs


# Define command tree in a string in YAML format
command_tree_STR = """
git:
    args:
        path:
            atype: flag
            help: Path of the repo
    subparsers:
        parsers:
            clone:
                args:
                    quiet-clone:
                        atype: flag
                        help: Operate quietly. Progress is not reported to the standard error stream.
                    no-checkout:
                        help: No checkout of HEAD is performed after the clone is complete
            init:
                args:
                    quiet-init:
                        atype: flag
                        help: Operate quietly. Progress is not reported to the standard error stream.
"""


# Create command line namespace and get arguments
args = betterargs.format_str_tree(command_tree_STR)

```


## Contributors
- Author: [Daniel Muringe](https://danielmuringe.github.io/)


## Contribution

You are more than welcome to contribute 😊


### Process

It's simple!!!

- Fork the github repo

- Clone the github repo

```bash
git clone https://github.com/danielmuringe/betterargs
```

- Make your modifications in the [dev branch](https://github.com/danielmuringe/betterargs/tree/dev)

- Merge into main branch respecting the .gitignore of the main branch. **KEEP IT CLEAN PLEASE !!!**

- Create pull request

- Wait for confirmation

### Rules
1. Active changes must take place in the [dev branch](https://github.com/danielmuringe/betterargs/tree/dev). Active changes include:

    - Changes to [betterargs module](https://github.com/danielmuringe/betterargs/tree/dev/betterargs)

    - Modification of development notes [betterargs module](https://github.com/danielmuringe/betterargs/tree/dev/betterargs/notes.md)

    - Changes to the [project tests](https://github.com/danielmuringe/betterargs/tree/dev/betterargs/testing)

2. Tests must be put in the [testing directory of dev branch](https://github.com/danielmuringe/betterargs/tree/dev/testing)

3. All packaging must be done in the [packaging branch](https://github.com/danielmuringe/betterargs/tree/packaging)

Other rules will be added at my discretion


## Tests
- Tests can be found in the [testing directory of dev branch](https://github.com/danielmuringe/betterargs/tree/dev/testing)


## Documentation
Coming Soon 😊

***

[![Pylint](https://github.com/davidprush/keycollator/actions/workflows/pylint.yml/badge.svg)](https://github.com/davidprush/keycollator/actions/workflows/pylint.yml)
[![Makefile CI](https://github.com/davidprush/keycollator/actions/workflows/makefile.yml/badge.svg)](https://github.com/davidprush/keycollator/actions/workflows/makefile.yml)
[![Python Version](https://img.shields.io/pypi/pyversions/keycollator.svg)](https://pypi.org/project/keycollator/)
[![License](https://img.shields.io/github/license/davidprush/keycollator)](https://github.com/davidprush/keycollator/blob/master/LICENSE)

#

```bash
┬┌─┌─┐┬ ┬┌─┐┌─┐┬  ┬  ┌─┐┌┬┐┌─┐┬─┐
├┴┐├┤ └┬┘│  │ ││  │  ├─┤ │ │ │├┬┘
┴ ┴└─┘ ┴ └─┘└─┘┴─┘┴─┘┴ ┴ ┴ └─┘┴└─
```
#

Compares text in a file to reference/glossary/key-items/dictionary.[[1]](#citation1)[[2]](#citation2)

🧱 Built by [David Rush](https://github.com/davidprush) fueled by ☕️ ℹ️ [info](#additional-information)

[keycollator #.#.# Pypi Project Description](https://pypi.org/project/keycollator)

***

# 👇 Table of Contents

1. [Structure](#structure)
2. [Features](#features)
3. [Installation](#installation)
    1. [Install from **Pypi** using pip3](#install-from-pypi-using-pip3)
4. [Documentation](#documentation)
5. [Supported File Formats](#supported-file-formats)
6. [Usage](#usage)
    1. [Import _keycollator_ into Python Projects](#import-keycollator-into-python-projects)
    2. [Requirements](#requirements)
    3. [CLI](#cli)
    4. [Turn on _verbose_ output](#turn-on-verbose-output)
    5. [Apply _fuzzy matching_](#apply-fuzzy-matching)
    6. [Set the _key file_](#set-the-key-file)
    7. [Set the _text file_](#set-the-text-file)
    8. [Specify the _output file_](#specify-the-output-file)
    9. [Set _limit results_ for console and _output file_](#set-limit-results-for-console-and-output-file)
    10. [Set _upper bound limit_](#set-the-upper-bound-limit)
    11. [Turn on _logging_:](#turn-on-logging)
    12. [Create a _log file_](#create-a-log-file)
7. [Example Output](#example-output)
8. [Todo](#todo)
9. [Project Resource Acknowledgements](#project-resource-acknowledgements)
10. [Deployment Features](#deployment-features)
11. [Releases](#releases)
    1. [Pypi Versions](#pypi-versions)
12. [License](#license)
13. [Citation](#citation)
14. [Additional Information](#additional-information)

<a name="structure"></a>
## 🗂️ Structure

```bash
.
│
├── assets
│   └── images
│       └── coverage.svg
│
├── docs
│   ├── cli.md
│   └── index.md
│
├── src
│   ├── __init__.py
│   ├── cli.py
│   ├── keycollator.py
│   ├── extractfile.py
│   ├── threadanalysis.py
│   ├── extractonator.py
│   ├── requirements.txt
│   └──data
│       ├── (placeholder)
│       └── (placeholder)
│
├── tests
│   └── test_keycollator
│       ├── __init__.py
│       └── test_keycollator.py
│
├── COD_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── make-venv.sh
├── Makefile
├── pyproject.toml
├── README.README
├── README.rst
├── setup.cfg
└── setup.py
```

<a name="features"></a>
## 🚀 Features

```bash
──> Extract text from file to dictionary
    └──> Extract keys from file to dictionary
          └──> Find matches of keys in text file
                └──> Apply fuzzy matching
```

<a name="installation"></a>
## 🧰 Installation

<a name="install-from-pypi-using-pip3"></a>
### 🖥️ Install from **Pypi** using pip3

📦 <https://pypi.org/project/keycollator/>

```bash
python3 -m pip install --upgrade keycollator
```

<a name="documentation"></a>
## 📄 Documentation

Official documentation can be found here:

<https://github.com/davidprush/keycollator/tree/main/docs>

<a name="supported-file-formats"></a>
## 💪 Supported File Formats

- TXT/CSV files (Mac/Linux/Win)
- Plans to add PDF and JSON

<a name="usage"></a>
## 📐 Usage

<a name="import-keycollator-into-python-project"></a>
### 🖥️ Import _keycollator_ into Python Projects

```
from keycollator.customlogger import CustomLogger as cl
from keycollator.proceduretimer import ProcedureTimer as pt
```

<a name="requirements"></a>
### 🖥️ Requirements

```
click >= 8.0.2
datetime >= 4.7
fuzzywuzzy >= 0.18.0
halo >= 0.0.31
nltk >= 3.7
pytest >= 7.1.3
python-Levenshtein >= 0.12.2
termtables >= 0.2.4
joblib >= 1.2.0
```

<a name="cli"></a>
### 🖥️ CLI

keycollator uses the `CLI` to change default parameters and functions

```bash
Usage: keycollator.py [OPTIONS] COMMAND [ARGS]...

  keycollator is an app that finds keys in a text file.

Options:
  -t, --text-file PATH          Path/file name of the text to be searched for
                                against items in the key file
  -k, --key-file PATH           Path/file name of the key file containing a
                                dictionary, key items, glossary, or reference
                                list used to search the text file
  -r, --result-file PATH        Path/file name of the output file that
                                will contain the results (CSV or TXT)
  --limit-result TEXT           Limit the number of results
  --abreviate INTEGER           Limit the text length of the results
                                (default=32)
  --fuzz-ratio INTEGER RANGE    Set the level of fuzzy matching (default=99)
                                to validate matches using approximations/edit
                                distances, uses acceptance ratios with integer
                                values from 0 to 99, where 99 is nearly
                                identical and 0 is not similar  [0<=x<=99]
  --ubound-limit INTEGER RANGE  Ignores items from the results with matches
                                greater than the upper boundary (upper-limit);
                                reduce eroneous matches  [1<=x<=99999]
  --lbound-limit INTEGER RANGE  Ignores items from the results with matches
                                less than the lower boundary (lower-limit);
                                reduce eroneous matches  [0<=x<=99999]
  -v, --verbose                 Turn on verbose
  -l, --logging                 Turn on logging
  -L, --log-file PATH           Path/file name to be used for the log file
  --help                        Show this message and exit.
```

<a name="turn-on-verbose-output"></a>
#### 🖥️ Turn on _verbose_ output

  >currently provides only one level for verbose, future versions will implement multiple levels (DEBUG, INFO, WARN, etc.)

```bash
keycollator --verbose
```

<a name="apply-fuzzy-matching"></a>
#### 🖥️ Apply _fuzzy matching_

  >_fuzzy matching_ uses approximate matches (edit distances) whereby 0 is the least strict and accepts nearly anything as a match and more strictly 99 accepts only nearly identical matches; by default the app uses level 99 only if regular matching finds no matches

```bash
keycollator --fuzzy-matching=[0-99]
```

<a name="set-the-key-file"></a>
#### 🖥️ Set the _key file_

  >each line of text represents a key which will be used to match with items in the _text file_

```bash
keycollator --key-file="/path/to/key/file/keys.txt"
```

<a name="set-the-text-file"></a>
#### 🖥️ Set the _text file_

  >text file whereby each line represents an item that will be compared with the items in the _keys file_

```bash
keycollator --text-file="/path/to/key/file/text.txt"
```

<a name="specify-the-output-file"></a>
#### 🖥️ Specify the _output file_

  >currently uses CSV but will add additional file formats in future releases (PDF/JSON/DOCX)

```bash
keycollator --output-file="/path/to/results/result.csv"
```

<a name="set-limit-results-for-console-and-output-file"></a>
#### 🖥️ Set _limit results_ for console and _output file_

  >Limit the number of results

```bash
keycollator --limit-results=30
```

<a name="set-upper-bound-limit"></a>
#### 🖥️ Set _upper bound limit_

  >rejects items with matches over the integer value set, helps with eroneous matches when using fuzzy matching

```bash
keycollator --ubound-limit
```

<a name="turn-on-loggin"></a>
#### 🖥️ Turn on _logging_:

  >turn on _logging_ whereby if no _log file_ is supplied by user it will create one using the default _log.log_

```bash
keycollator --set-logging
```

<a name="create-a-log-file"></a>
#### 🖥️ Create a _log file_

  >set the name of the _log file_ to be used by _logging_

```bash
keycollator --log-file="/path/to/log/file/log.log"
```

<a name="example-output"></a>
## Example Output

```bash
python3 src/keycollator.py
Analyzing text for keys...
100%|██████████████████████████████████████████████████████████████| 679/679 [00:51<00:00, 13.31it/s]
1.r              [536]   51.conduct        [7]   101.connect       [3]   151.assist develo*[1]
2.manage          [73]   52.establish      [7]   102.determine     [3]   152.assist tracki*[1]
3.develop         [62]   53.execute        [7]   103.facilitate    [3]   153.capture speci*[1]
4.report          [58]   54.follow         [7]   104.foster        [3]   154.conduct code *[1]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
47.finance        [8]    97.business admin*[3]   147.advise sponso*[1]   197.flexible      [1]
48.powerpoint     [8]    98.attention deta*[3]   148.advocate      [1]   198.creative      [1]
49.build          [7]    99.python         [3]   149.align documen*[1]   199.selfmotivated [1]
50.complete       [7]    100.collaborate   [3]   150.analyze under*[1]   200.difference la*[1]
[0.00]seconds
 ```

<a name="todo"></a>
## 🎯 Todo 📌

```bash
    ❌ Fix pylint errors
    ❌ Add command line option to add a stopwords file
    ❌ Fix all cli options
    ❌ Add comments
    ❌ Refactor code and remove redunancies
    ❌ Fix pylint errors
    ❌ Add proper error handling
    ❌ Add CHANGELOG.md
    ❌ Create method to KeyKrawler to select and _create missing files_
    ❌ Update CODE_OF_CONDUCT.md
    ❌ Update CONTRIBUTING.md
    ❌ Github: issue and pr templates
    ❌ Workflow Automation
    ❌ Makefile Usage
    ❌ Dockerfile
    ❌ @dependabot configuration
    ❌ Release Drafter (release-drafter.yml)
```

<a name="project-resource-acknowledgements"></a>
## 👔 Project Resource Acknowledgements

  1. [Creating a Python Package](https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/#creating-a-python-package)
  1. [javiertejero](https://gist.github.com/javiertejero/4585196)

<a name="deployment-features"></a>
## 💼 Deployment Features (Not yet implemented)

  | Feature | Notes |
  | ------- | ----- |
  | Github | issue and pr templates |
  | Workflows | [Automate your workflow from idea to production](https://github.com/features/actions?&ef_id=Cj0KCQjwj7CZBhDHARIsAPPWv3cJBfbABq5nd5kGwDIiJ5Ax-TFF_8CbqlKvQ92R7L1EuyjMgr2FacgaAnUiEALw_wcB:G:s&OCID=AID2202669_SEM_Cj0KCQjwj7CZBhDHARIsAPPWv3cJBfbABq5nd5kGwDIiJ5Ax-TFF_8CbqlKvQ92R7L1EuyjMgr2FacgaAnUiEALw_wcB:G:s&gclid=Cj0KCQjwj7CZBhDHARIsAPPWv3cJBfbABq5nd5kGwDIiJ5Ax-TFF_8CbqlKvQ92R7L1EuyjMgr2FacgaAnUiEALw_wcB) |
  | Makefile-usage | [Makefile Usage](https://github.com/TezRomacH/python-package-template/blob/master/README.md#makefile-usage) |
  | Dockerfile | [Docker Library: Python](https://github.com/docker-library/python) |
  | @dependabot | [Configuring Dependabot version updates](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuring-dependabot-version-updates#enabling-github-dependabot-version-updates) |
  | Release Drafter | release-drafter.yml |

<a name="releases"></a>
## 📈 Releases

  | Release | Version | Status |
  | ------- | ------- | ------- |
  | **Current:** | [0.0.5](https://pypi.org/project/keycollator/0.0.5/) | Working |

<a name="pypi-versions"></a>
### 📦 Pypi Versions

  | Version | Notes |
  | ------- | ----- |
  | [0.0.1](https://pypi.org/project/keycollator/0.0.1/) | Initial prototype |
  | [0.0.2](https://pypi.org/project/keycollator/0.0.2/) | Bug fixes |
  | [0.0.4](https://pypi.org/project/keycollator/0.0.4/) | Fixed functions/methods |
  | [0.0.5](https://pypi.org/project/keycollator/0.0.5/) | Fixed functions/methods |

<a name="license"></a>
## 🛡 License

[![License](https://img.shields.io/github/license/davidprush/keycollator)](https://github.com/davidprush/keycollator/blob/master/LICENSE)

This project is licensed under the terms of the **MIT** license. See [LICENSE](https://github.com/davidprush/keycollator/blob/master/LICENSE) for more details.

<a name="citation"></a>
## 📄 Citation

```bibtex
@misc{keycollator,
  author = {David Rush},
  title = {Compares text in a file to reference/glossary/key-items/dictionary file.},
  year = {2022},
  publisher = {Rush Solutions, LLC},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/davidprush/keycollator}}
}
```

***

<a name="additional-information"></a>
#### Additional Information

<a name="citation1"></a>
1. _The latest version of this document can be found [here](https://github.com/davidprush/keycollator/blob/main/README.md); if you are viewing it there (via HTTPS), you can download the Markdown/reStructuredText source [here](https://github.com/davidprush/keycollator)._ 
<a name="citation2"></a>
2. _You can contact the author via [e-mail](davidprush@gmail.com)._

***

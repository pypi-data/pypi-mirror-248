# nlpia2

<!-- [![PyPI version](https://img.shields.io/pypi/pyversions/nlpia2.svg)](https://pypi.org/project/nlpia2/)
 [![License](https://img.shields.io/pypi/l/qary.svg)](https://pypi.python.org/pypi/qary/)
 -->
<!-- https://gitlab.com/username/userproject/badges/master/coverage.svg
 -->
[![codecov](https://codecov.io/gl/tangibleai/nlpia2/branch/master/graph/badge.svg)](https://codecov.io/gl/tangibleai/nlpia2)
[![GitLab CI](https://gitlab.com/tangibleai/nlpia2/badges/master/pipeline.svg)](https://gitlab.com/tangibleai/nlpia2/badges/master/pipeline.svg)

Official [code repository](https://gitlab.com/tangibleai/nlpia2/) for the book [_Natural Language Processing in Action, 2nd Edition_](https://proai.org/nlpia2e) by Maria Dyshel and Hobson Lane at [Tangible AI](https://tangibleai.com) for [Manning Publications](https://manning.com). It would not have happened without the generous work of [contributing authors](AUTHORS.md).

## Quickstart

### Windows

If you are using Windows you will have to first install `git-bash` so you can have the same environment used within more than 99% of all production NLP pipelines: [docs/README-windows-install.md](./docs/README-windows-install.md)

### Within `bash`

Launch your terminal (`git-bash` application on Windows) and then install the nlpia2 package from source:

```bash
git clone git@gitlab.com:tangbileai/nlpia2
cd nlpia2
pip install --upgrade pip virtualenv
python -m virtualenv .venv
source .venv/bin/activate | source .venv/Scripts/activate
pip install -e .
```

Then you can check to see if everything is working by importing the Chapter 3 FAQ chatbot example.

```python
from nlpia2.ch03.faqbot import run_bot
run_bot()
```

## Install

To get the most of this repository, you need to do three things.

1. **Clone the repository** to your local machine if you want to execute the code locally or want local access to the data (recommended).
2. **Create a virtual environment** to hold the `nlpia2` package and it's dependences.
3. **Install nlpia2** as an `--editable` package so you can contribute to it if you find bugs or things you'd like to add.


### Clone the Repository

If you're currently viewing this file on GitLab, and you'd rather access the data and code local to your machine, you may clone this repository to your local machine. Navigate to your preferred directory to house the local clone (for example, you local _git_ directory) and execute:

`git clone git@gitlab.com:tangbileai/nlpia2`



### Create a Virtual Environment

To use the various packages in vogue with today's advanced NLP referenced in the NLPIA 2nd Edition book, such as PyTorch and SpaCy, you need to install them in a conda environment.  To avoid potential conflics of such packages and their dependencies with your other python projects, it is a good practice to create and activate a _new_ conda environment.

Here's how we did that for this book.

1. **Make sure you have Anaconda3 installed.** Make sure you can run conda from within a bash shell (terminal). The `conda --version` command should say something like '`4.10.3`.

2. **Update conda itself**. Keep current the `conda` package, which manages all other packages. Your base environment is most likely called _base_ so you can execute `conda update -n base -c defaults conda` to bring that package up to date.  Even if _base_ is not the activated environment at the moment, this command as presented will update the conda package in the _base_ environment. This way, next time you use the `conda` command, in any environment, the system will use the updated _conda_ package.

3. **Create a new environment and install the variety of modules needed in NLPIA 2nd Edition.**

There are two ways to do that.  

### Use the script already provided in the repository (_`nlpia2/src/nlpia2/scripts/conda_install.sh`_)

If you have cloned the repository, as instructed above, you already have a script that will do this work. From the directory housing the repository, run
`cd nlpia2/src/nlpia2/scripts/` and from there run `bash conda_install.sh` 

### Or manually execute portions of the script as follows

First, create a new environment (or activate it if it exists)

```bash
# create a new environment named "nlpia2" if one doesn't already exist:
conda activate nlpia2 \
    || conda create -n nlpia2 -y 'python==3.9.7' \
    && conda activate nlpia2
```

Once that completes, install all of `nlpia2`'s conda dependences if they aren't already installed:

``` bash
conda install -c defaults -c huggingface -c pytorch -c conda-forge -y \
    emoji \
    ffmpeg \
    glcontext \
    graphviz \
    huggingface_hub \
    jupyter \
    lxml \
    manimpango \
    nltk \
    pyglet \
    pylatex \
    pyrr \
    pyopengl \
    pytest \
    pytorch \
    regex \
    seaborn \
    scipy \
    scikit-learn \
    sentence-transformers \
    statsmodels \
    spacy \
    torchtext \
    transformers \
    wikipedia \
    xmltodict
```

Finally, install via pip any packages not available through conda channels.  In such scenarios it is generally a better practice to apply all pip installs after _all_ conda installs.  Furthermore, to ensure the pip installation is properly configured for the python version used in the conda environment, rather than use `pip` or `pip3`, activate the environment and invoke pip by using `python -m pip`.

``` bash
conda activate nlpia2
python -m pip install manim manimgl
```

## Ready, Set, Go!

Congratulations! You now have the nlpia2 repository cloned which gives you local access to all the data and scripts need in the NLPIA Second Edition book, and you have created a powerful environment to use.  When you're ready to type or execute code, check if this environment is activated. If not, activate by executing:

`conda activate nlpia2`

And off you go tackle some serious Natural Language Processing, in order to make the world a better place for all.

Run a jupyter notebook server within docker:
`jupyter-repo2docker --editable .`

### TODO

- [ ] dictionary of .nlpia2 filepaths and their corresponding remote URLs and proai.org shorturls
- [ ] download if necessary to cache all required datasets in .nlpia2-data
- [ ] collect_data.py using 

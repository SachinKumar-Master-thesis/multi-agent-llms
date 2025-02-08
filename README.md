# multi-agent-llms
The repo implements an Elastic Search(ES) agent using llama-index workflows.
The current implmentations uses multi-agent archietecture with actor-critic model to develop ES agent.
Following are the components developed
- Schema selector: select set of schemas to answer user query
- Query generator(actor): Generate ES queries which are to be run downstream by opensearch_py
- Query validator(critic): semantic validation of the es and user query
- Query runner(actor): runner es query against opensearch instance
- Query corrector(critic): incorporate errors from es run and correct the query
- Response synthesizer: generate inferences


## Developer Guide

The pkg is developed using nbdev to incorporate the development via Jupyter notebook. The development should always be restricted to the nbs folder. It is assumed that all the env variables related to ES, LLM and others are present in a .env file, which is to be read at run time and instantiated

### Install multi_agent_llms in Development mode
``` sh
# clean notebooks of its output
$ nbdev_clean

# compile to have changes apply to multi_agent_llms
$ nbdev_prepare

# export pkg for local installation
$ nbdev_export

# make sure multi_agent_llms package is installed in development mode
$ pip install -e .

# make changes under nbs/ directory
# ...

# doc preview
$ pip install quarto
$ nbdev_preview

```

### Precommit
Precommit is used to regulate the git precommit hooks to ensure the notebook cleaning and execution of nbdev commands to ensure latest code being commited and no notebook meta-data is commited to git
``` sh
# install pre-commit
$ pip install pre-commit

# cp pre-commit-config to the below location
$ cp pre-commit-config.yaml .pre-commit-config.yaml

# install pkks
$ pre-commit install

```
### Docker


## Usage

### Installation

Install latest from the GitHub
[repository](https://github.com/SachinKumar-Master-thesis/multi-agent-llms):

``` sh
$ pip install git+https://github.com/SachinKumar-Master-thesis/multi-agent-llms.git
```

or from
[conda](https://anaconda.org/SachinKumar-Master-thesis/multi-agent-llms)

``` sh
$ conda install -c SachinKumar-Master-thesis multi_agent_llms
```

or from [pypi](https://pypi.org/project/multi-agent-llms/)

``` sh
$ pip install multi_agent_llms
```

### Documentation

Documentation can be found hosted on this GitHub
[repository](https://github.com/SachinKumar-Master-thesis/multi-agent-llms)’s
[pages](https://SachinKumar-Master-thesis.github.io/multi-agent-llms/).
Additionally you can find package manager specific guidelines on
[conda](https://anaconda.org/SachinKumar-Master-thesis/multi-agent-llms)
and [pypi](https://pypi.org/project/multi-agent-llms/) respectively.

## How to use

Fill me in please! Don’t forget code examples:

``` python

```

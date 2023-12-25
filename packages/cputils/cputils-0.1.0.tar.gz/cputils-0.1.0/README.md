# cputils

[![license MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.txt)

Utilities for Competitive Programming. 

Currently supports downloading of samples, and running local tests with samples.

## Installation
Assuming you have a [Python3](https://www.python.org/) distribution with [pip](https://pip.pypa.io/en/stable/installing/), install the package running:

```bash
pip3 install cputils
```

## Usage
### cpconfig
To create a config file, run
```bash
cpconfig
```

### cpsamples
To download the samples of a problem run
```bash
cpsamples <problem>
```

### cptest
To test a solution or set of solutions run
```bash
cptest <problem>/<solution(s)>
```
Pro-tip: use glob patterns like ```problem/code*``` or ```problem/*.py```.
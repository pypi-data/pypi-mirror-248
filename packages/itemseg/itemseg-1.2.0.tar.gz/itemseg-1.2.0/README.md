# itemseg

10-K Item Segmentation with Line-based Attention (ISLA) is a tool to process
EDGAR 10-K reports and extract item-specific text. 


[![PyPI - Version](https://img.shields.io/pypi/v/itemseg.svg)](https://pypi.org/project/itemseg)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/itemseg.svg)](https://pypi.org/project/itemseg)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip3 install itemseg
```

### Download resource file
```console
python3 -m itemseg --get_resource
```

### Download nltk data

Launch python3 console
```console
>>> import nltk
>>> nltk.download('punkt')
```

### Obtain 10-K file and segment items
Use Apple 10-K (2023) as an example
```console
python3 -m itemseg --input https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/0000320193-23-000106.txt
```

See the results in ./segout01/

## License

`itemseg` is distributed under the terms of the [CC BY-NC](https://creativecommons.org/licenses/by-nc/4.0/) license.

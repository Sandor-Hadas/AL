# AL

Prerequirements:
- python 2.7.15+
- pip
- packages: xmltodict, pprint, csv, json

Example uses:
$ python al.py --in input.xml --out out.html
$ python al.py --in input.csv --out out.xml --print txt
$ python al.py --in input.json --out out.csv --print html
$ python al.py --in input.json --out out.json --print txt

Print help:
$ python py   (no parameters or invalid parameters)

Tests:
- Test data is in the TestData directory. Please see test details in test_samply.py.  Run 'pytest' for tests.


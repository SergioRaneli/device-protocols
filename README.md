Device Protocols
================

[![Build Status](https://travis-ci.org/nspyke/device-protocols.svg?branch=master)](https://travis-ci.org/nspyke/device-protocols)

Simple Python library to parse data from devices using various protocols.

Only GPS103 currently is included.
Others may be added in the future.
 
To use the library, just import it and call the functions.
```
from protocols import gps103
```

To test, run
```
nosetests
```
You'll need to have installed [nose](https://nose.readthedocs.io/en/latest/index.html) to run the tests

If you find bugs, pull requests are welcome.
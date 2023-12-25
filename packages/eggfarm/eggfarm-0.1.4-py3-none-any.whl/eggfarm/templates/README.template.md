# create Linux offline package
* install all dependencies
    * `make install` 
* run all tests
    * `make test`
* generate a Linux offline package
    * `make package`
* if `No matching distribution happened`, please delete the package in requirements.txt, download the source distribution into ./source folder. 
    * `make source_package`
* upload dist/\*_table_func_\*.tar.gz to yanhuang platform and register it
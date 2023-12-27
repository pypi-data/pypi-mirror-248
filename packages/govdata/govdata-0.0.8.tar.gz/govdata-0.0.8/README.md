# govdata
Client-library to fetch data from GovData/OpenData-sources via DKAN-REST-API. 
Take a look at [https://www.govdata.de/](https://www.govdata.de/) to determine if your city of interest provides some data.

## install 
```bash
python -m pip install govdata
```

## example usage
```py
from govdata import DKANPortalClient 
import requests
# get opendata-city-client
cityclient = DKANPortalClient(city="braunschweig", apiversion=3)

# get all available packages (topics)
packagelist = cityclient.get_packages()

# request data for package from packagelist
first_package_id_from_list = packagelist[0]
package_meta = cityclient.get_package_metadata(package_id=first_package_id_from_list)
resources_for_package = package_meta["resources"]
```

## run tests
```bash
pytest --cov=govdata tests
```

## testcoverage
```
collecting ... 
 tests/test_govdata.py ✓✓✓✓✓✓✓✓                                                                                                                                          100% ██████████

---------- coverage: platform ###, python 3.8.10-final-0 -----------
Name                                                          Stmts   Miss  Cover
---------------------------------------------------------------------------------
/###/.local/lib/python3.8/site-packages/govdata.py     106     56    47%
---------------------------------------------------------------------------------
TOTAL                                                           106     56    47%
```


from govdata import DKANPortalClient 
import requests
# get opendata-city-client
cityclient = DKANPortalClient(city="braunschweig", apiversion=3)

# get all available packages (topics)
packagelist = cityclient.get_packages()

# request data for package from packagelist
first_package_id_from_list = packagelist[0]
package_meta = cityclient.get_package_metadata(package_name=first_package_id_from_list)
resources_for_package = package_meta["resources"]

# fetch informations from choosen resource by id
index_of_choosen_resource = 1
resource_id = resources_for_package[index_of_choosen_resource]["id"]
resource_metadata = cityclient.get_resource_metadata(resource_id=resource_id)

# get all tags of cityclient
cityclient.get_unique_tags()


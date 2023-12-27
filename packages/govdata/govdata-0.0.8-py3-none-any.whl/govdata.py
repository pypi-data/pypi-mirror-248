import pretty_errors
import requests
import pandas as pd

from typing import Type, Dict, List, Any

class DKANPortalClient:
    """
    A client for interacting with the DKAN API.

    Attributes:
        base_url (str): The base URL of the DKAN API for a specific city.

    Methods:
        get_resource_metadata(resource_id: str) -> Dict: Get metadata for a specific resource.
        get_package_metadata(package_name: str) -> Dict: Get metadata for a specific package.
        get_packages() -> List[Dict]: Get a list of all packages.
        get_contributors() -> List[str]: Get a list of contributors (groups).
        get_total_packages_with_resources() -> List[Dict]: Get a list of all packages with resources.
        test_connection() -> bool: Test the connection to the DKAN API.
    """
    def __init__(self, city: str, apiversion: int = 3):
        """
        Initialize the DKANClient with the base URL for a specific city.

        Args:
            city (str): The city for which the DKANClient is initialized.
            apiverion (int): The apiversion for which the DKANClient is initialized. Default: 3.
        """
        self.city: str = city
        self.apiversion: int = apiversion
        self.base_url: str = f"https://opendata.{city}.de/api/{apiversion}"


    def connectiontest(self) -> bool:
        """
        Test the connection to the DKAN API.

        Returns:
            bool: True if the API is reachable, False otherwise.

        Raises:
            requests.exceptions.RequestException: If the HTTP request encounters an error.
            ValueError: If the response JSON lacks expected keys.
        """
        # Build the URL for the site_read API endpoint
        url = f"{self.base_url}/action/site_read"

        try:
            # Send an HTTP GET request to the API endpoint
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            # Check if the API is reachable based on the response
            return response.json().get("result", False)

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that might occur during the request
            raise e

        except (ValueError, KeyError) as e:
            # Handle JSON parsing errors or missing keys
            raise ValueError("Unable to parse response JSON or missing expected keys") from e


    
    def get_total_packages_with_resources(self) -> List[Dict[str, Any]]:
        """
        Get a list of all packages (datasets) with their resources available in the DKAN API.

        Returns:
            list: A list of dictionaries, each containing metadata for a package and its resources.

        Raises:
            requests.exceptions.RequestException: If the HTTP request encounters an error.
            ValueError: If the response JSON cannot be parsed or lacks expected keys.
        """
        # Build the URL for the current_package_list_with_resources API endpoint
        url = f"{self.base_url}/action/current_package_list_with_resources"

        try:
            # Send an HTTP GET request to the API endpoint
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            # Check if the response indicates success
            if response.json().get("success", False):
                # Extract the list of packages with resources from the response
                packages_with_resources = [element for element in response.json()["result"][0]]
                return packages_with_resources

            raise ValueError("API request was not successful")

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that might occur during the request
            raise e

        except (ValueError, KeyError) as e:
            # Handle JSON parsing errors or missing keys
            raise ValueError("Unable to parse response JSON or missing expected keys") from e

    def get_tags(self) -> List[str]:
        """
        Get a list of tags/short-descriptions available in the Dataset of your choince.

        Returns:
            list: A list of strings, each representing a tag.

        Raises:
            requests.exceptions.RequestException: If the HTTP request encounters an error.
            ValueError: If the response JSON cannot be parsed or lacks expected keys.
        """

        packages_with_resources = self.get_total_packages_with_resources()                

        # if packages available, create dataframe
        if packages_with_resources:
            df = pd.DataFrame(packages_with_resources)  

            # create empty list for tags
            taglist = []

            # filter dataframe for unique tags
            for entry in df.tags:
                for tag in entry:
                    if tag["name"] not in taglist:
                        taglist.append(tag["name"])
            return taglist
        
    def get_contributors(self) -> List[str]:
        """
        Get a list of contributors (groups) available in the DKAN API.

        Returns:
            list: A list of strings, each representing a contributor (group).

        Raises:
            requests.exceptions.RequestException: If the HTTP request encounters an error.
            ValueError: If the response JSON cannot be parsed or lacks expected keys.
        """
        # Build the URL for the group list API endpoint
        url = f"{self.base_url}/action/group_list"

        try:
            # Send an HTTP GET request to the API endpoint
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            # Parse the JSON response and return the list of contributors
            contributors = response.json().get("result", [])
            return contributors

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that might occur during the request
            raise e

        except (ValueError, KeyError) as e:
            # Handle JSON parsing errors or missing keys
            raise ValueError("Unable to parse response JSON or missing expected keys") from e


    def get_packages_with_resources_by_contributor(self, contributor_id: str) -> List:
        """
        Get a list of packages with their resources associated with a specific contributor (group).

        Args:
            contributor_id (str): The ID of the contributor for which to retrieve packages.

        Returns:
            list: A list of dictionaries, each containing metadata for a package and its resources.

        Raises:
            requests.exceptions.RequestException: If the HTTP request encounters an error.
            ValueError: If the response JSON cannot be parsed or lacks expected keys.
        """
        # Build the URL for the group_package_show API endpoint with the specified contributor ID
        url = f"{self.base_url}action/group_package_show?id={contributor_id}"

        try:
            # Send an HTTP GET request to the API endpoint
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            # Check if the response indicates success
            if response.json().get("success", False):
                # Extract the list of packages with resources from the response
                packages_with_resources = response.json().get("result", [])

                # Transform the data structure to a list of dictionaries
                # Assuming the response structure is a list with a single dictionary at index 0
                l = [element for element in packages_with_resources[0]] if packages_with_resources else []
                return l

            raise ValueError("API request was not successful")

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that might occur during the request
            raise e

        except (ValueError, KeyError) as e:
            # Handle JSON parsing errors or missing keys
            raise ValueError("Unable to parse response JSON or missing expected keys") from e


    def get_packages(self) -> List[Dict[str, Any]]:
        """
        Get a list of all packages (datasets) available in the DKAN API.

        Returns:
            list: A list of dictionaries, each containing metadata for a package.

        Raises:
            requests.exceptions.RequestException: If the HTTP request encounters an error.
            ValueError: If the response JSON cannot be parsed or lacks expected keys.
        """
        # Build the URL for the package list API endpoint
        url = f"{self.base_url}/action/package_list"

        try:
            # Send an HTTP GET request to the API endpoint
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            # Check if the response indicates success
            if response.json()["success"]:
                # Extract the list of packages from the response
                packages = response.json().get("result")
                return packages
            else:
                raise ValueError("API request was not successful")

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that might occur during the request
            raise e

        except (ValueError, KeyError) as e:
            # Handle JSON parsing errors or missing keys
            raise ValueError("Unable to parse response JSON or missing expected keys") from e


    def get_package_metadata(self, package_name: str) -> Dict[str, Any]:
        """
        Get metadata for a specific package (dataset) by its ID.

        Args:
            package_name (str): The ID of the package.

        Returns:
            dict: Metadata for the specified package in the form of a dictionary.

        Raises:
            requests.exceptions.RequestException: If the HTTP request encounters an error.
            ValueError: If the response JSON cannot be parsed.
        """
        # Build the URL for the package show API endpoint
        url = f"{self.base_url}/action/package_show?id={package_name}"

        try:
            # Send an HTTP GET request to the API endpoint
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            # Parse the JSON response and return the result
            if response.json()["success"]:
                # Extract the list of packages from the response
                packages = response.json().get("result")
                if type(packages) == list:
                    if len(packages) > 0:
                        return packages[0]

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that might occur during the request
            raise e

        except ValueError as e:
            # Handle JSON parsing errors
            raise ValueError("Unable to parse response JSON") from e


    
    def get_resource_metadata(self, resource_id: str) -> Dict[str, Any]:
        """
        Get metadata for a specific resource by its ID.

        Args:
            resource_id (str): The ID of the resource.

        Returns:
            dict: Metadata for the specified resource in the form of a dictionary.

        Raises:
            requests.exceptions.RequestException: If the HTTP request encounters an error.
            ValueError: If the response JSON cannot be parsed.
        """
        # Build the URL for the resource show API endpoint
        url = f"{self.base_url}/action/resource_show?id={resource_id}"

        try:
            # Send an HTTP GET request to the API endpoint
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            
            # Parse the JSON response and return the result
            if response.json()["success"]:
                # Extract the list of resources from the response
                resource = response.json().get("result")
                return resource

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that might occur during the request
            raise e

        except ValueError as e:
            # Handle JSON parsing errors
            raise ValueError("Unable to parse response JSON") from e
        

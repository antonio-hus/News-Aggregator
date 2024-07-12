###################
# IMPORTS SECTION #
###################
import requests
import os


#######################
# DATABASE OPERATIONS #
#######################

# Periodic Update of Articles in DataBase
# To be called every 12 hours ( at usual down-times )
def periodicUpdate():
    """
    Main Functionality:
    - add in database new articles
    - update in database modified articles
    - delete articles older than 7 days
    """
    pass


####################
# MEDIA OPERATIONS #
####################


def checkMediaURL(url: str) -> bool:
    """
    Checks if a Media's URL is still valid
    Returns True if it is valid
    Returns False if it is invalid
    """
    try:
        # Getting the response of the URL
        response = requests.head(url, allow_redirects=True)

        # Check if the status code is in the range of 200-399 ( Valid URL )
        if 200 <= response.status_code < 400:
            return True
        else:
            return False

    # Invalid Request => Invalid Media
    except requests.RequestException:
        return False


def getMediaURL(url: str) -> str:
    """
    Returns the URL of the Media Item if URL valid
    Returns the URL of a placeholder if URL not valid
    """
    placeholder_url = "https://example.com/placeholder.jpg"

    # Valid Media URL
    if checkMediaURL(url):
        return url

    # PlaceHolder URL
    return placeholder_url


def downloadFile(url: str, dest_folder: str):
    """
    Downloads a file from a URL and saves it to a destination folder
    Returns the file path of the downloaded file
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Extract file name from URL and create full path
        filename = os.path.join(dest_folder, os.path.basename(url))

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return filename
    except requests.RequestException:
        return None


def getMediaFile(url: str):
    """
    Returns the File of the Media Item if URL valid
    Returns the File of a placeholder if URL not valid
    """
    placeholder_file = "../media/media_placeholder.png"

    # Valid Media URL
    if checkMediaURL(url):
        file_path = downloadFile(url, "../media")
        if file_path:
            return file_path

    # PlaceHolder File
    return placeholder_file

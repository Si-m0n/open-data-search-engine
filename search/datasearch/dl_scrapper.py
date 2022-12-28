# Download zip files, create directories accordingly and unzip the files

import zipfile
import os
import requests as re
from bs4 import BeautifulSoup as bs

base_url = "https://opendata.justice-administrative.fr/"

ce_url = "https://opendata.justice-administrative.fr/DCE/"

caa_url = "https://opendata.justice-administrative.fr/DCA/"

ta_url = "https://opendata.justice-administrative.fr/DTA/"

download_dir = "Projets/Scrapping/download/"


def unzip(path_to_zip_file, directory_to_extract_to):

    with zipfile.ZipFile(path_to_zip_file, "r") as zip_ref:
        zip_ref.extractall(directory_to_extract_to)


def dl_files(url_taget):
    """
    Download all files from the url_target and save them in download_dir.
    url_target must be either ce_url, caa_url or ta_url
    """
    # Get the HTTP request and make the BeautifulSoup to parse
    r = re.get(url_taget, allow_redirects=True)
    soup = bs(r.content, "html.parser")

    # Find all files to download
    links = soup.find_all("a")
    files_links = []
    files_name = []
    # Process the link format
    for link in links:
        if not ".csv" in link.get("href"):
            files_links.append(base_url.rstrip("/") + link.get("href"))
            files_name.append(link.text)
    # Download each file
    for i in range(len(files_links)):
        print(files_name[i])
        path_dir = download_dir + files_name[i].rstrip(".zip") + "/"
        path_file = path_dir + files_name[i]
        os.mkdir(path_dir)
        with open(path_file, "wb") as file:
            response = re.get(files_links[i])
            file.write(response.content)
        unzip(path_file, path_dir)
        os.remove(path_file)

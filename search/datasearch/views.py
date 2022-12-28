from django.shortcuts import render, redirect
from datasearch.models import Decision, LegalBody
from bs4 import BeautifulSoup as bs
from django.forms.models import model_to_dict
from datasearch.forms import DecisionForm, SearchForm

import os, zipfile, shutil
import requests as re


# Create your views here.
def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            # Implémenter la recherche
            return render("search-result")
    else:
        form = SearchForm()
    return render(
        request,
        "datasearch/index.html",
        {"form": form},
    )


def search_result(request):
    return render(
        request,
        "datasearch/search_result.html",
    )


def decision(request, id):
    decision = DecisionForm(data=model_to_dict(Decision.objects.get(id=id)))
    return render(
        request,
        "datasearch/decision.html",
        {"decision": decision},
    )


def xml_to_decision(path_xml_file):
    # Load the xml file with BeautifulSoup
    with open(path_xml_file, "r", encoding="utf-8") as xml_file:
        content = xml_file.readlines()
        content = "".join(content)
        # Le paramètre "html.parser" renvoie un avertissement que l'on peut ignorer
        bs_content = bs(content, "html.parser")

        # Extract data from the xml file
        file_number = int(bs_content.find("numero_dossier").text)
        last_update = bs_content.find("date_mise_jour").text
        lecture_date = bs_content.find("date_lecture").text
        if bs_content.find_all("avocat_requerant"):
            lawyer = bs_content.find("avocat_requerant").text
        else:
            lawyer = ""
        decision_type = bs_content.find("type_decision").text
        if bs_content.find_all("type_recours"):
            appeal_type = bs_content.find("type_recours").text
        else:
            appeal_type = ""
        publication_code = bs_content.find("code_publication").text
        if bs_content.find_all("solution"):
            solution = bs_content.find("solution").text
        else:
            solution = ""
        if bs_content.find_all("numero_role"):
            role_number = int(bs_content.find("numero_role").text)
        else:
            role_number = None
        if bs_content.find_all("date_audience"):
            hearing_date = bs_content.find("date_audience").text
        else:
            hearing_date = None
        if bs_content.find_all("formation_jugement"):
            jugement_format = bs_content.find("formation_jugement").text
        else:
            jugement_format = ""
        text = bs_content.find("decision").get_text()

        legal_code = bs_content.find("code_juridiction").text
        legal_name = bs_content.find("nom_juridiction").text
        # Enlève les chiffres du code de juridiction pour obtenir le type de juridiction
        legal_type = "".join(char for char in legal_code if char.isalpha())

        try:
            legal_body = LegalBody.objects.get(legal_code=legal_code)
        except:
            legal_body = LegalBody.objects.create(
                legal_type=legal_type, legal_name=legal_name, legal_code=legal_code
            )

        return Decision(
            file_number=file_number,
            last_update=last_update,
            lecture_date=lecture_date,
            lawyer=lawyer,
            decision_type=decision_type,
            appeal_type=appeal_type,
            publication_code=publication_code,
            solution=solution,
            role_number=role_number,
            text=text,
            hearing_date=hearing_date,
            jugement_format=jugement_format,
            legal_body=legal_body,
        )


def update_db(path_file):
    dir_list = os.listdir(path_file)
    for dir in dir_list:
        path_dir = path_file + "/" + dir
        file_list = os.listdir(path_dir)
        for file in file_list:
            path_file2 = path_dir + "/" + file
            decision = xml_to_decision(path_file2)
            try:
                decision_in_db = Decision.objects.get(file_number=decision.file_number)
            except:
                decision.save()


base_url = "https://opendata.justice-administrative.fr/"

ce_url = "https://opendata.justice-administrative.fr/DCE/"

caa_url = "https://opendata.justice-administrative.fr/DCA/"

ta_url = "https://opendata.justice-administrative.fr/DTA/"

download_dir = "C:/Users/Simon/Documents/Python/open-data-search-engine/search/datasearch/download/datasearch/"


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
        print("Downloading : " + files_name[i])
        path_dir = download_dir + files_name[i].rstrip(".zip") + "/"
        path_file = path_dir + files_name[i]
        os.mkdir(path_dir)
        with open(path_file, "wb") as file:
            response = re.get(files_links[i])
            file.write(response.content)
        print("Unzipping : " + files_name[i])
        unzip(path_file, path_dir)
        os.remove(path_file)
        update_db(path_dir)
        shutil.rmtree(path_dir)

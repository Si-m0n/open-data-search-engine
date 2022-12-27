from django.shortcuts import render
from datasearch.models import Decision, LegalBody
from bs4 import BeautifulSoup as bs

# Create your views here.
def index(request):
    return render(
        request,
        "datasearch/index.html",
    )


def xml_to_decision(xml_file):
    # Load the xml file with BeautifulSoup
    content = xml_file.readlines()
    content = "".join(content)
    # Enlever le paramètre lxml si erreur
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
    role_number = int(bs_content.find("numero_role").text)
    hearing_date = bs_content.find("date_audience").text
    jugement_format = bs_content.find("formation_jugement").text
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

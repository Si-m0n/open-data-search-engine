from django.db import models

# Create your models here.
class LegalBody(models.Model):
    class LegalType(models.TextChoices):
        COURS_ADMINISTRATIVE_APPEL = "CAA"
        CONSEIL_ETAT = "CE"
        TRIBUNAL_ADMINISTRATIF = "TA"

    legal_type = models.CharField(
        "Type de juridiction", null=True, choices=LegalType.choices, max_length=20
    )
    legal_name = models.CharField("Nom de la juridiction", max_length=100)
    legal_code = models.CharField("Code de la juridiction", max_length=20)

    def __str__(self):
        return self.legal_code


class Decision(models.Model):
    file_number = models.IntegerField("Numéro de dossier")
    last_update = models.DateField("Date de mise à jour")
    lecture_date = models.DateField("Date de lecture")
    lawyer = models.CharField("Avocat requérant", max_length=30)
    decision_type = models.CharField("Type de décision", max_length=100)
    appeal_type = models.CharField("Type de recours", max_length=100)
    publication_code = models.CharField("Code publication", max_length=20)
    solution = models.CharField("Solution", default="", blank=True, max_length=100)
    text = models.CharField("Texte intégral", max_length=100000)

    legal_body = models.ForeignKey(
        LegalBody,
        verbose_name="Instance judiciaire",
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.file_number)

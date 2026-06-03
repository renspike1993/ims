from django.db import models


# ======================================================
# TEMPLATE MODEL
# ======================================================
from django.db import models


class Template(models.Model):

    academic_year = models.CharField(max_length=20)

    front_template = models.ImageField(
        upload_to="id_templates/front/",
        blank=True,
        null=True,
        help_text="Upload the front design of the ID card."
    )

    back_template = models.ImageField(
        upload_to="id_templates/back/",
        blank=True,
        null=True,
        help_text="Upload the back design of the ID card."
    )

    date_started = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.academic_year

    class Meta:
        verbose_name = "Template"
        verbose_name_plural = "ID Templates"
        ordering = ["-id"]

# ======================================================
# STUDENT IDENTIFICATION CARD
# ======================================================
class StudentIdentificationCard(models.Model):

    PROGRAM_OPTIONS = [
        ("BSIT", "BSIT"),
        ("BSED", "BSED"),
        ("BEED", "BEED"),
        ("BSCRIM", "BSCRIM"),
        ("BSHM", "BSHM"),
        ("DHST", "DHST"),
        ("BST", "BST"),
        ("BSBA", "BSBA"),
    ]

    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
        related_name="students"
    )

    id_number = models.CharField(max_length=50, unique=True)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    program = models.CharField(
        max_length=50,
        choices=PROGRAM_OPTIONS,
        default="BSIT",
    )

    mobile_number = models.CharField(max_length=20, blank=True, null=True)

    guardian = models.CharField(max_length=255, blank=True, null=True)
    guardian_mobile_number = models.CharField(max_length=20, blank=True, null=True)

    profile_picture = models.ImageField(
        upload_to="student_profiles/",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.id_number} - {self.last_name}, {self.first_name}"

    def full_name(self):
        return f"{self.last_name}, {self.first_name}"

    class Meta:
        verbose_name = "Identification Card"
        verbose_name_plural = "Identification Cards"
        ordering = ["-id"]
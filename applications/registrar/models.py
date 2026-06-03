from django.db import models


class Folder(models.Model):

    FLOOR_OPTIONS = [
        ("1st_floor", "1st Floor"),
        ("2nd_floor", "2nd Floor"),
    ]

    folder_name = models.CharField(max_length=20)

    floor = models.CharField(
        max_length=255,
        choices=FLOOR_OPTIONS,
        default="1st_floor",
    )

    capacity = models.PositiveIntegerField(null=True, blank=True, default=50)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.folder_name


# ======================================================
# STUDENT DOCUMENT (CSV IMPORT TARGET)
# ======================================================
class StudentDocument(models.Model):

    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    class Meta:
        verbose_name = "Student Document"
        verbose_name_plural = "Student Documents"
        ordering = ["folder"]

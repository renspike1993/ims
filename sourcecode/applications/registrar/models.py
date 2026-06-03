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
    capacity = models.PositiveIntegerField(null=True, blank=True,default=50)
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.folder_name}"
    
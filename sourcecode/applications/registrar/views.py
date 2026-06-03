import csv
from django.shortcuts import render
from django.db import transaction
from .models import Folder, StudentDocument


def read_csv(request):

    data = []
    csv_file_path = "media/student_folders.csv"

    try:
        with open(csv_file_path, newline='', encoding='utf-8') as file:

            reader = csv.DictReader(file)

            # ✅ START TRANSACTION (ALL OR NOTHING)
            with transaction.atomic():

                for row in reader:

                    folder_name = row.get("folder_name")
                    first_name = row.get("first_name")
                    last_name = row.get("last_name")
                    middle_name = row.get("middle_name")

                    # normalize NULL values
                    if middle_name == "NULL":
                        middle_name = None

                    # -------------------------------------------------
                    # 1. GET OR CREATE FOLDER
                    # -------------------------------------------------
                    folder, _ = Folder.objects.get_or_create(
                        folder_name=folder_name
                    )

                    # -------------------------------------------------
                    # 2. PREVENT DUPLICATE STUDENTS
                    # -------------------------------------------------
                    exists = StudentDocument.objects.filter(
                        folder=folder,
                        first_name=first_name,
                        last_name=last_name,
                        middle_name=middle_name
                    ).exists()

                    if not exists:
                        StudentDocument.objects.create(
                            folder=folder,
                            first_name=first_name,
                            last_name=last_name,
                            middle_name=middle_name
                        )

                    data.append(row)

    except FileNotFoundError:
        return render(
            request,
            "portal/csv_view.html",
            {"error": "CSV file not found."}
        )

    return render(
        request,
        "portal/csv_view.html",
        {
            "data": data,
            "message": "CSV imported successfully (no duplicates allowed)."
        }
    )
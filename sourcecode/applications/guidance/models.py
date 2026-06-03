from django.db import models
from django.utils import timezone

# Create your models here.


class Exam(models.Model):
    exam_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True) 
    duration = models.PositiveIntegerField(null=True, blank=True,default=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.exam_name

    class Meta:
        verbose_name = "Entrance Exam"
        verbose_name_plural = "Entrance Exams"
        ordering = ["-created_at"]



class ExamCategory(models.Model):



    category_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "Exam Category"
        verbose_name_plural = "Exam Categories"
        ordering = ["-created_at"]



class ExamQuestion(models.Model):

    OPTIONS = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("E", "E"),
    ]

    exam_name = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="exam_question",
        blank=True,
        null = True,

    )

    category_name = models.ForeignKey(
        ExamCategory,
        on_delete=models.CASCADE,
        related_name="exam_question",
        blank=True,
        null = True,
    )


    question = models.TextField(null=True, blank=True)


    option_a = models.CharField(max_length=255,null=True)
    option_b = models.CharField(max_length=255,null=True)
    option_c = models.CharField(max_length=255,null=True)
    option_d = models.CharField(max_length=255,null=True)
    option_e = models.CharField(max_length=255,default="None of the above")



    correct_option = models.CharField(
        max_length=50,
        choices=OPTIONS,
        default="entrance_exam",
    )


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question



    class Meta:
        verbose_name = "Exam Question"
        verbose_name_plural = "Exam Questions"
        ordering = ["-created_at"]



class Examinee(models.Model):

    exam_taken = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="examinee",
        blank=True,
        null = True,

    )

    PROGRAM_OPTIONS = [
        ("BSIT", "Bachelor of Science in Information Technology"),
        ("BSED", "Bachelor of Secondary Education"),
        ("BEED", "Bachelor of Elementary Education"),
        ("BSCRIM", "Bachelor of Science in Criminology"),
        ("BSHM", "Bachelor of Science Hospitality Management"),
        ("DHST", "DHST (TVET)"),
        ("BST", "Bachelor of Science in Tourism"),
        ("BSBA", "Bachelor of Science in Business Administration"),
    ]


    or_number = models.CharField(max_length=11,blank=False,default="")

    first_name = models.CharField(max_length=255,blank=False,default="")
    middle_name = models.CharField(max_length=1,blank=True,default="")
    last_name = models.CharField(max_length=255,blank=False,default="")
    is_submitted = models.BooleanField(default=False)


    program = models.CharField(
        max_length=255,
        choices=PROGRAM_OPTIONS,
        default="BSIT",
    )



    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


    def full_name(self):
        return f"{self.last_name}, {self.first_name}"

    def masked_full_name(self):
        if not self.first_name or not self.last_name:
            return ""

        return f"{self.last_name[0]}****, {self.first_name[0]}****"

    class Meta:
        verbose_name = "Examinee"
        verbose_name_plural = "Examinees"
        ordering = ["-created_at"]

class ExamResponse(models.Model):

    examinee_question = models.ForeignKey(
        ExamQuestion,
        on_delete=models.CASCADE,
        related_name="exam_response",
        blank=False,
        null=True,
    )

    examinee = models.ForeignKey(
        Examinee,
        on_delete=models.CASCADE,
        related_name="exam_response",
        blank=False,
        null=True,
    )

    RESPONSE_OPTIONS = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("E", "E"),
    ]

    examinee_response = models.CharField(
        max_length=255,
        choices=RESPONSE_OPTIONS,
        default="E",
    )

    is_correct = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.examinee_question:
            self.is_correct = (
                self.examinee_response ==
                self.examinee_question.correct_option
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.examinee}"



    class Meta:
        verbose_name = "Examinee Answer"
        verbose_name_plural = "Examinees Answer"
        ordering = ["-created_at"]
        unique_together = ["examinee_question", "examinee"]
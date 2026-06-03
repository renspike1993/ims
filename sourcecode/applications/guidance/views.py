from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib import messages
from applications.guidance.models import ExamQuestion, ExamResponse, Examinee
import time

def login_view(request):
    if request.method == "POST":
        or_number = request.POST.get("or_number")

        try:
            examinee = Examinee.objects.get(or_number=or_number)

            # store session
            request.session["examinee_id"] = examinee.id

            # return redirect("dashboard")
            return redirect("dashboard")
        except Examinee.DoesNotExist:
            messages.error(request, "Invalid OR Number.")

    return render(request, "portal/login.html")


from collections import defaultdict

def dashboard(request):
    examinee_id = request.session.get("examinee_id")

    if not examinee_id:
        return redirect("login")

    examinee = Examinee.objects.get(id=examinee_id)

    questions = (
        ExamQuestion.objects
        .filter(exam_name=examinee.exam_taken)
        .select_related("category_name")
        .order_by("category_name__category_name", "id")
    )

    categories = defaultdict(list)

    for question in questions:
        categories[question.category_name].append(question)

    context = {
        "examinee": examinee,
        "categories": dict(categories),
        "start_time": request.session.get("exam_start_time"),
    }

    return render(
        request,
        "portal/dashboard.html",
        context
    )

def submit_answers(request):
    if request.method == "POST":

        examinee_id = request.session.get("examinee_id")
        examinee = Examinee.objects.get(id=examinee_id)

        questions = ExamQuestion.objects.filter(
            exam_name=examinee.exam_taken
        )

        for q in questions:
            answer = request.POST.get(f"answer_{q.id}")

            if answer:
                ExamResponse.objects.update_or_create(
                    examinee=examinee,
                    examinee_question=q,
                    defaults={
                        "examinee_response": answer
                    }
                )
        return redirect("exam_result")
        # return redirect("dashboard")
    



def exam_result(request):
    examinee_id = request.session.get("examinee_id")

    if not examinee_id:
        return redirect("login")

    examinee = Examinee.objects.get(id=examinee_id)

    responses = ExamResponse.objects.filter(examinee=examinee)

    total_questions = responses.count()
    correct_answers = responses.filter(is_correct=True).count()
    wrong_answers = total_questions - correct_answers

    score = correct_answers
    percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0

    return render(request, "portal/result.html", {
        "examinee": examinee,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "score": score,
        "percentage": round(percentage, 2)
    })

from django.shortcuts import render, get_object_or_404

def print_exam_result(request, examinee_id):
    examinee = get_object_or_404(
        Examinee,
        pk=examinee_id
    )

    responses = (
        ExamResponse.objects
        .filter(examinee=examinee)
        .select_related(
            "examinee_question",
            "examinee_question__category_name"
        )
    )

    total = responses.count()
    correct = responses.filter(is_correct=True).count()
    wrong = total - correct

    percentage = (
        (correct / total) * 100
        if total else 0
    )

    # Category breakdown
    category_scores = {}

    for response in responses:
        category = (
            response.examinee_question.category_name.category_name
            if response.examinee_question.category_name
            else "Uncategorized"
        )

        if category not in category_scores:
            category_scores[category] = {
                "total": 0,
                "correct": 0,
            }

        category_scores[category]["total"] += 1

        if response.is_correct:
            category_scores[category]["correct"] += 1

    context = {
        "examinee": examinee,
        "total": total,
        "correct": correct,
        "wrong": wrong,
        "percentage": round(percentage, 2),
        "category_scores": category_scores,
    }

    return render(
        request,
        "portal/print_result.html",
        context
    )
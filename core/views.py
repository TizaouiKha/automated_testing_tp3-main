from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.utils.text import slugify
from .models import Form, FormResponse, Answer, Question


@login_required
def create_form(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            slug = slugify(title)
            base_slug, counter = slug, 1
            while Form.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            is_private = request.POST.get("is_private") == "on"
            access_token = request.POST.get("access_token", "").strip()
            form = Form.objects.create(
                title=title,
                slug=slug,
                is_active=True,
                is_private=is_private,
                access_token=access_token,
            )

            # Questions are submitted as parallel lists: question_label[], question_type[]
            labels = request.POST.getlist("question_label")
            types = request.POST.getlist("question_type")
            for order, (label, question_type) in enumerate(zip(labels, types)):
                label = label.strip()
                if label:
                    Question.objects.create(
                        form=form,
                        label=label,
                        question_type=question_type,
                        order=order,
                    )

            return redirect("form_detail", slug=form.slug)

    return render(request, "core/create_form.html")


def form_detail(request, slug):
    form = get_object_or_404(Form, slug=slug, is_active=True)

    if form.is_private:
        token = request.GET.get("token", "")
        if token != form.access_token:
            return render(request, "core/form_detail.html", {"access_denied": True})

    questions = form.questions.all()

    if request.method == "POST":
        form_response = FormResponse.objects.create(form=form)
        errors = {}

        for question in questions:
            value = request.POST.get(f"question_{question.id}", "").strip()
            if question.is_required and not value:
                errors[question.id] = "Mandatory field"
            else:
                Answer.objects.create(
                    response=form_response,
                    question=question,
                    value=value,
                )

        if errors:
            form_response.delete()
            return render(request, "core/form_detail.html", {
                "form": form,
                "questions": questions,
                "errors": errors,
                "submitted_data": request.POST,
            })

        return redirect("form_success", slug=slug)

    return render(request, "core/form_detail.html", {
        "form": form,
        "questions": questions,
        "errors": {},
        "submitted_data": {},
    })


def form_success(request, slug):
    form = get_object_or_404(Form, slug=slug)
    return render(request, "core/form_success.html", {"form": form})

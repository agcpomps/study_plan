from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User


class Subject(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class Course(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(
        Subject, related_name="courses", on_delete=models.CASCADE
    )
    description = models.TextField()
    duration = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class StudyPlan(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self) -> str:
        return f"{self.course} - {self.user}"

    def calculate_progres(self):
        total_goals = self.goals.count()
        if total_goals == 0:
            return 0
        completed_goals = self.goals.filter(completed=True).count()
        return (completed_goals / total_goals) * 100


class Goal(models.Model):
    description = models.CharField(max_length=200)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    study_plan = models.ForeignKey(
        StudyPlan, on_delete=models.CASCADE, related_name="goals"
    )

    def mark_as_complete(self):
        self.completed = True
        self.save()

        study_plan = self.study_plan
        study_plan.completed = study_plan.calculate_progres() == 100
        study_plan.save()

    def __str__(self) -> str:
        return self.description


class ItemBase(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = (models.CharField(max_length=250),)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to="files")


class Video(ItemBase):
    url = models.URLField()


class Content(models.Model):
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": ("text", "video", "file")},
    )
    object_id = models.PositiveBigIntegerField()
    item = GenericForeignKey("content_type", "object_id")

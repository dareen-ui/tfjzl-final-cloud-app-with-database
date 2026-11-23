# Adds a sample course with lessons and exam questions (run with: python manage.py shell < ci/seed.py)
import os
from django.contrib.auth.models import User
from onlinecourse.models import Course, Lesson, Instructor, Question, Choice

admin_pw = os.environ["ADMIN_PW"]
learner_pw = os.environ["LEARNER_PW"]
User.objects.create_superuser("admin", "admin@example.com", admin_pw)
learner = User.objects.create_user("dareen", password=learner_pw, first_name="Dareen", last_name="Alalyani")
inst_user = User.objects.create_user("instructor", password=admin_pw, first_name="Yan")
instructor = Instructor.objects.create(user=inst_user, full_time=True, total_learners=100)

course = Course.objects.create(name="Learning Django", description="Build web applications with Django.", pub_date="2026-11-23")
course.instructors.add(instructor)
Lesson.objects.create(title="Django Overview", order=0, course=course, content="Django is a high-level Python web framework.")
Lesson.objects.create(title="Django Models", order=1, course=course, content="Models define the structure of your data.")

q1 = Question.objects.create(course=course, content="Which language is Django written in?", grade=50)
Choice.objects.create(question=q1, content="Python", is_correct=True)
Choice.objects.create(question=q1, content="Java", is_correct=False)
Choice.objects.create(question=q1, content="C#", is_correct=False)

q2 = Question.objects.create(course=course, content="Which of these are Django model field types?", grade=50)
Choice.objects.create(question=q2, content="CharField", is_correct=True)
Choice.objects.create(question=q2, content="ForeignKey", is_correct=True)
Choice.objects.create(question=q2, content="TextBox", is_correct=False)
print("seeded")

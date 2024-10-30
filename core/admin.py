from django.contrib import admin
from .models import Academic,Skill,User,Cv,Experience,Referee,Profile,Cv

model_list = [User, Skill, Cv, Academic, Experience, Referee, Profile]
admin.site.register(model_list)
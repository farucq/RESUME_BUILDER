
from django.contrib import admin
from django.urls import path
from . import views
from .views import generate_pdf

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('createcv/', views.createCv, name="createcv"),
    path('skill-save/', views.saveSkill, name="skill-save"),
    path('edu-save/', views.saveEducation, name="edu-save"),
    path('exp-save/', views.saveExperience, name="exp-save"),
    path('ref-save/', views.saveReferee, name="ref-save"),
    path('profile-save/', views.uploadProfile, name="profile-save"),
    path('register/', views.registerView, name="reg-form"),
    path('cv-detail/<id>', views.viewPDF, name="cv-detail"),
   # path('cv-download/<id>', views.generate_PDF, name="cv-download"),
   path('cv-download/<id>', views.generate_pdf, name="cv-download"),

    path('cv-edit/', views.editCv, name="cv-edit"),
    path('cv-edit/fetchprofile/', views.fetchProfile, name="fetchprofile"),
    path('cv-edit/updateprofile/', views.updateProfile, name="profile-update"),
    path('cv-edit/deleteprofile/', views.deleteProfile, name="profile-delete"),
    path('cv-edit/eduview/', views.educationView, name="edu-view"),
    path('cv-edit/eduview/academic/', views.fetchAcademic, name="fetchacademic"),
    path('cv-edit/eduview/update_academic/', views.updateAcademic, name="update_academic"),
    path('cv-edit/eduview/delete_academic/', views.deleteAcademic, name="delete_academic"),
    path('cv-edit/skillview/', views.skillView, name="skill-view"),
    path('cv-edit/skillview/skill/', views.fetchSkill, name="fetchskill"),
    path('cv-edit/skillview/update_skill/', views.updateSkill, name="update_skill"),
    path('cv-edit/skillview/delete_skill/', views.deleteSkill, name="delete_skill"),
    path('cv-edit/expview/', views.experienceView, name="exp-view"),
    path('cv-edit/expview/experience/', views.fetchExperience, name="fetchexperience"),
    path('cv-edit/expview/update_experience/', views.updateExperience, name="update_experience"),
    path('cv-edit/expview/delete_experience/', views.deleteExperience, name="delete_experience"),
    path('cv-edit/refview/', views.refereeView, name="ref-view"),
    path('cv-edit/refview/referee/', views.fetchReferee, name="fetchreferee"),
    path('cv-edit/refview/update_referee/', views.updateReferee, name="update_referee"),
    path('cv-edit/refview/delete_referee/', views.deleteReferee, name="delete_referee"),
     path('addash', views.addash, name="addash"),
     path('feedback/submit/', views.submit_feedback, name='submit_feedback'),
    path('feedback/view/', views.view_feedback, name='view_feedback'),
    path('feedback/success/', views.FeedbackSuccessView, name='feedback_success'),
    path('download-pdf/', generate_pdf, name='download_pdf'),
    path('template-switcher/', views.template_switcher, name='template_switcher'),

    path('manage_users/', views.manage_users, name='manage_users'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),      
    path('view_resumes/', views.view_resumes, name='view_resumes'),  # New URL for viewing all resumes
    path('resume/<int:user_id>/', views.resume_detail, name='resume_detail'),

    
]

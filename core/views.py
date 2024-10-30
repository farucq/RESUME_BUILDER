from fileinput import filename
from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import render, redirect,reverse
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout
from django.template import context
from .models import Skill,Academic,Experience,Referee,Profile,User,Cv
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
import pdfkit
from .models import Profile

#from reportlab.lib.pagesizes import letter
#from reportlab.pdfgen import canvas
#from .models import Profile, Skill, Referee, Experience, Academic



def index(request):
    return render(request, 'core/index.html')

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_superuser:
                return redirect('addash')  # Redirect superuser to admin
            else:
                return redirect('dashboard')
            
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('login')
    return render(request, 'core/login.html')


@login_required
def addash(request):
    return render(request,'core/admin home.html')


@login_required
def dashboard(request):
    user_id = request.user.id

    try:
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]
        print('Cv ID is',cv_id)
        print('Data type',type(cv_id))
        if isinstance(cv_id, int):
            context = {'status':'there_is_cv'}
            return render(request, 'core/dashboard.html', context)
    except Exception as e:
        context = {'status':'no_cv'}
        return render(request, 'core/dashboard.html', context)

def createCv(request):
    user_id = request.user.id

    try:
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]

        profile_id = Profile.objects.filter(cv_id=cv_id).values_list('id', flat=True)
        profile_id = list(profile_id)
        profile_id = profile_id[0]

        if isinstance(profile_id, int):
            context = {'status':'there_is_profile'}
            return render(request, 'core/create_cv.html', context)
    except Exception as e:
        context = {'status':'no_profile'}
        return render(request, 'core/create_cv.html', context)

def saveSkill(request):
    if request.method == 'POST':
        user_id = request.user.id
        
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]

        s_name = request.POST.getlist('s_name[]')
        s_level = request.POST.getlist('s_level[]')

        if(len(s_name) == 1):
            a = Skill(s_name = s_name[0], s_level = s_level[0], cv_id = cv_id)
            a.save()
            return JsonResponse({'status':1})   
        else:
            for x,y in zip(s_level,s_name):
                a = Skill(s_level=x, s_name=y, cv_id=cv_id)
                a.save()
            return JsonResponse({'status':1})
    return JsonResponse({'status':0})

def saveEducation(request):
    if request.method == 'POST':
        name = request.POST.getlist('name[]')
        year = request.POST.getlist('year[]')
        award = request.POST.getlist('award[]')

        user_id = request.user.id
        
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]

        if(len(name) == 1):
            a = Academic(a_institution = name[0], a_year = year[0], a_award = award[0], cv_id = cv_id)
            a.save()
            return JsonResponse({'status':1})   
        else:
            for x,y,z in zip(name,year,award):
                a = Academic(a_institution=x, a_year=y, a_award=z, cv_id=cv_id)
                a.save()
            return JsonResponse({'status':1})
    return JsonResponse({'status':0})

def saveExperience(request):
    if request.method == 'POST':
        c_name = request.POST.getlist('c_name[]')
        role = request.POST.getlist('role[]')
        duration = request.POST.getlist('duration[]')

        user_id = request.user.id
        
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]

        if(len(c_name) == 1):
            a = Experience(e_name = c_name[0], e_role = role[0], e_duration = duration[0], cv_id = cv_id)
            a.save()
            return JsonResponse({'status':1})   
        else:
            for x,y,z in zip(c_name,role,duration):
                a = Experience(e_name=x, e_role=y, e_duration=z, cv_id=cv_id)
                a.save()
            return JsonResponse({'status':1})
    return JsonResponse({'status':0})


def saveReferee(request):
    if request.method == 'POST':
        r_name = request.POST.getlist('r_name[]')
        phno = request.POST.getlist('phno[]')
        email = request.POST.getlist('email[]')

        user_id = request.user.id
        
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]

        if(len(r_name) == 1):
            a = Referee(re_name = r_name[0], re_email=email[0], re_phone=phno[0], cv_id= cv_id)
            a.save()
            return JsonResponse({'status':1})
        else:
            for x,y,z in zip(r_name,phno,email):
                a = Referee(re_name=x, re_phone=y, re_email=z, cv_id= cv_id)
                a.save()
            return JsonResponse({'status':1})
    return JsonResponse({'status':0})

def uploadProfile(request):
    fname = request.POST.get('fname')
    mname = request.POST.get('mname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    gender = request.POST.get('gender')
    bio = request.POST.get('bio')
    dob = request.POST.get('dob')
    occupation = request.POST.get('occupation')
    country = request.POST.get('country')
    region = request.POST.get('region')
    file = request.FILES.get('file')
    user_id = request.user.id

    Cv.objects.create(user_id=user_id)

    cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
    cv_id = list(cv_id)
    cv_id = cv_id[0]
    print('Cv ID is',cv_id)


    p = Profile(fname=fname, mname=mname, lname=lname, email=email, bio=bio, dob=dob, gender=gender, occupation=occupation, country=country, region=region, avator=file,phone=phone,cv_id=cv_id)
    p.save()

    return JsonResponse({'status':1})

def updateProfile(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        fname = request.POST.get('fname')
        mname = request.POST.get('mname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        bio = request.POST.get('bio')
        dob = request.POST.get('dob')
        occupation = request.POST.get('occupation')
        country = request.POST.get('country')
        region = request.POST.get('region')
        file = request.FILES.get('file')

        user_id = request.user.id
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True).first()

        # Fetch the current profile to check existing avatar
        profile = get_object_or_404(Profile, cv_id=id)

        # Use the existing avatar if no new file is uploaded
        avatar = file if file else profile.avator

        # Update the profile with the new data
        profile.fname = fname
        profile.mname = mname
        profile.lname = lname
        profile.email = email
        profile.bio = bio
        profile.dob = dob
        profile.gender = gender
        profile.occupation = occupation
        profile.country = country
        profile.region = region
        profile.avator = avatar  # Retain existing avatar if no new file
        profile.phone = phone
        profile.cv_id = cv_id
        profile.save()

        return JsonResponse({'status': 'success', 'message': 'Profile Updated Successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def registerView(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password = make_password(password)

        check_user = User.objects.filter(username=username).count()
        check_email = User.objects.filter(email=email).count()

        if(check_user > 0):
            messages.error(request, 'Username is already taken')
            return redirect('reg-form')
        elif(check_email > 0):
            messages.error(request, 'Email is already taken')
            return redirect('reg-form')
        else:
            User.objects.create(username=username, email=email, password=password)
            messages.success(request, 'Account created successfully, Please Sign In')
            return redirect('reg-form')
    else:
        return render(request, 'core/register.html')        


def logoutView(request):
    logout(request)
    return redirect('index')



def editCv(request):
    return render(request, 'core/edit_cv.html')

def fetchProfile(request):
    id = request.POST.get('id')
    print('Cv ID is',id)
    
    user_profile = Profile.objects.get(cv_id=id)


    user_profile = {'fname':user_profile.fname, 
    'mname':user_profile.mname,
    'lname':user_profile.lname,
    'email':user_profile.email,
    'phone':user_profile.phone,
    'bio':user_profile.bio,
    'dob':user_profile.dob,
    'gender':user_profile.gender,
    'country':user_profile.country,
    'region':user_profile.region,
    'occupation':user_profile.occupation
    }
    return JsonResponse(user_profile)

def deleteProfile(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print('Cv ID is',id)
        
        user_profile = Profile.objects.get(cv_id=id)
        user_profile.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})

def educationView(request):
    id = request.user.cv.id
    print('Cv ID is',id)
    user_education = Academic.objects.filter(cv_id=id).all()
    context = {'user_education':user_education}
    return render(request, 'core/education_view.html', context)

def fetchAcademic(request):
    id = request.POST.get('id')
    print('Cv ID is',id)
    
    user_education = Academic.objects.get(id=id)

    user_education = {'institution':user_education.a_institution, 
    'year':user_education.a_year,
    'award':user_education.a_award
    }
    return JsonResponse(user_education)

def updateAcademic(request):
    id = request.POST.get('id')
    institution = request.POST.get('institution')
    year = request.POST.get('year')
    award = request.POST.get('award')


    Academic.objects.filter(id=id).update(a_institution=institution, a_year=year, a_award=award)

    return JsonResponse({'status':1})

def deleteAcademic(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print('Cv ID is',id)
        
        user_education = Academic.objects.get(id=id)
        user_education.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})

def experienceView(request):
    id = request.user.cv.id
    print('Cv ID is',id)
    user_experience = Experience.objects.filter(cv_id=id).all()
    context = {'user_experience':user_experience}
    return render(request, 'core/experience_view.html', context)

def fetchExperience(request):
    id = request.POST.get('id')
    print('Cv ID is',id)
    
    user_experience = Experience.objects.get(id=id)

    user_experience = {'name':user_experience.e_name, 
    'role':user_experience.e_role,
    'duration':user_experience.e_duration
    }
    return JsonResponse(user_experience)

def updateExperience(request):
    id = request.POST.get('id')
    name = request.POST.get('name')
    role = request.POST.get('role')
    duration = request.POST.get('duration')


    Experience.objects.filter(id=id).update(e_name=name, e_role=role, e_duration=duration)

    return JsonResponse({'status':1})

def deleteExperience(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print('Cv ID is',id)
        
        user_experience = Experience.objects.get(id=id)
        user_experience.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})

def refereeView(request):
    id = request.user.cv.id
    print('Cv ID is',id)
    user_referee = Referee.objects.filter(cv_id=id).all()
    context = {'user_referee':user_referee}
    return render(request, 'core/referee_view.html', context)

def fetchReferee(request):
    id = request.POST.get('id')
    print('Cv ID is',id)
    
    user_referee = Referee.objects.get(id=id)

    user_referee = {'name':user_referee.re_name, 
    'email':user_referee.re_email,
    'phone':user_referee.re_phone
    }
    return JsonResponse(user_referee)

def updateReferee(request):
    id = request.POST.get('id')
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')


    Referee.objects.filter(id=id).update(re_name=name, re_email=email, re_phone=phone)

    return JsonResponse({'status':1})

def deleteReferee(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print('Cv ID is',id)
        
        user_referee = Referee.objects.get(id=id)
        user_referee.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})


def skillView(request):
    id = request.user.cv.id
    print('Cv ID is',id)
    user_skill = Skill.objects.filter(cv_id=id).all()
    context = {'user_skill':user_skill}
    return render(request, 'core/skill_view.html', context)

def fetchSkill(request):
    id = request.POST.get('id')
    print('Cv ID is',id)
    
    user_skill = Skill.objects.get(id=id)

    user_skill = {'name':user_skill.s_name, 
    'level':user_skill.s_level
    }
    return JsonResponse(user_skill)

def updateSkill(request):
    id = request.POST.get('id')
    name = request.POST.get('name')
    level = request.POST.get('level')


    Skill.objects.filter(id=id).update(s_name=name, s_level=level)

    return JsonResponse({'status':1})

def deleteSkill(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print('Cv ID is',id)
        
        user_skill = Skill.objects.get(id=id)
        user_skill.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})




from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from weasyprint import HTML
from .models import Profile, Skill

from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML
from io import BytesIO
from .models import Profile, Skill, Academic, Experience, Referee, Feedback  # Ensure correct imports
from django.contrib.auth.decorators import login_required


from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML
from io import BytesIO
from .models import Profile, Skill, Academic, Experience, Referee
from django.contrib.auth.decorators import login_required

@login_required
def generate_pdf(request):
    # Fetch the user's CV details based on their login
    user = request.user
    try:
        user_profile = Profile.objects.filter(cv__user=user)
        user_skill = Skill.objects.filter(cv__user=user)
        user_education = Academic.objects.filter(cv__user=user)
        user_experience = Experience.objects.filter(cv__user=user)
        user_referee = Referee.objects.filter(cv__user=user)
    except Profile.DoesNotExist:
        return HttpResponse("Profile not found", status=404)

    # Load your HTML template
    template = get_template('core/new2_template.html')
    context = {
        'user_profile': user_profile,
        'user_skill': user_skill,
        'user_education': user_education,
        'user_experience': user_experience,
        'user_referee': user_referee,
    }

    # Render the HTML with context data
    html_content = template.render(context)

    # Create a PDF
    pdf_file = HTML(string=html_content).write_pdf()

    # Prepare the response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="resume.pdf"'

    return response



from .models import Feedback
from .forms import FeedbackForm

# View for user feedback submission
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback_success')  # Redirect to a success page
    else:
        form = FeedbackForm()
    return render(request, 'core/submit_feedback.html', {'form': form})

# View for admin to see feedback
def view_feedback(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'core/view_feedback.html', {'feedbacks': feedbacks})

def FeedbackSuccessView(request):
    template_name = 'feedback_success.html'
    return render(request, 'core/dashboard.html')

# def viewPDF(request, id=None):
#     user_profile = Profile.objects.filter(cv_id=id)
#     user_skill = Skill.objects.filter(cv_id=id).values()
#     user_referee = Referee.objects.filter(cv_id=id).values()
#     user_experience = Experience.objects.filter(cv_id=id).values()
#     user_education = Academic.objects.filter(cv_id=id).values()


#     context = {'user_profile':user_profile,'user_skill':user_skill,'user_experience':user_experience,'user_referee':user_referee,'user_education':user_education,'cv_id': id}
#     return render(request, 'core/new2_template.html', context)

        

from django.shortcuts import render

from django.shortcuts import render, get_object_or_404



def viewPDF(request, id=None):
    # Check if ID is valid
    if id is None:
        return render(request, 'core/error_template.html', context={'error_message': 'CV ID not provided.'})

    user_profile = get_object_or_404(Profile, cv_id=id)  # This will raise a 404 if not found
    user_skill = Skill.objects.filter(cv_id=id).values()
    user_referee = Referee.objects.filter(cv_id=id).values()
    user_experience = Experience.objects.filter(cv_id=id).values()
    user_education = Academic.objects.filter(cv_id=id).values()

    context = {
        'user_profile': user_profile,
        'user_skill': user_skill,
        'user_experience': user_experience,
        'user_referee': user_referee,
        'user_education': user_education,
        'cv_id': id,
    }
    
    return render(request, 'core/new2_template.html', context)

def template_switcher(request):
    template = request.GET.get('template', 'template1')  # Default to 'template1' if not specified
    cv_id = request.GET.get('id')  # Get the cv_id from the request
    print(f"Received cv_id: {cv_id}")

    # Validate cv_id
    if not cv_id or not cv_id.isdigit():
        return render(request, 'core/error_template.html', context={'error_message': 'Invalid CV ID provided.'})

    user_profile = get_object_or_404(Profile, cv_id=cv_id)  # Raises 404 if not found

    # Fetch related data
    user_skill = Skill.objects.filter(cv_id=cv_id).values()
    user_referee = Referee.objects.filter(cv_id=cv_id).values()
    user_experience = Experience.objects.filter(cv_id=cv_id).values()
    user_education = Academic.objects.filter(cv_id=cv_id).values()

    # Prepare context with fetched data
    context = {
        'user_profile': user_profile,  # Now a single object
        'user_skill': user_skill,
        'user_experience': user_experience,
        'user_referee': user_referee,
        'user_education': user_education,
        'cv_id': cv_id,
    }

    # Render the selected template with the context data
    template_mapping = {
        'template1': 'core/new4_template.html',
        'template2': 'core/new3_template.html',
        'template3': 'core/new_template.html',
        'template4': 'core/new5_template.html',
        'template5': 'core/new2_template.html',


    }

    template_to_render = template_mapping.get(template, 'core/new3_template.html')
    return render(request, template_to_render, context)

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import User  # Import your custom User model

def manage_users(request):
    # Get all users from the custom User model
    users = User.objects.filter(is_admin=False)
    
    return render(request, 'core/manage_users.html', {'users': users})

def delete_user(request, user_id):
    try:
        # Fetch the user by id
        user = User.objects.get(id=user_id)
        user.delete()  # Delete the user
        messages.success(request, f'User {user.username} has been deleted successfully.')
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
    return redirect(reverse('manage_users'))

def view_resumes(request):
    users = User.objects.filter(is_admin=False)  # Fetch all non-admin users
    return render(request, 'core/view_resumes.html', {'users': users})

# views.py
from django.shortcuts import render, get_object_or_404
from .models import User, Cv, Skill, Academic, Experience, Referee, Profile

def resume_detail(request, user_id):
    # Get the user object or return 404 if not found
    user = get_object_or_404(User, id=user_id)
    
    # Get the CV associated with the user
    cv = get_object_or_404(Cv, user=user)
    
    # Fetch the user's profile details
    user_profile = get_object_or_404(Profile, cv=cv)
    
    # Fetch skills, education, experience, and referees
    user_skill = Skill.objects.filter(cv=cv)
    user_education = Academic.objects.filter(cv=cv)
    user_experience = Experience.objects.filter(cv=cv)
    user_referee = Referee.objects.filter(cv=cv)

    # Render the template with the context
    return render(request, 'core/admin_rs_temp.html', {
        'user_profile': user_profile,
        'user_skill': user_skill,
        'user_education': user_education,
        'user_experience': user_experience,
        'user_referee': user_referee,
    })

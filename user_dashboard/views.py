import json
from django.shortcuts import render, redirect, HttpResponseRedirect,HttpResponse
from django.views.generic import TemplateView, ListView
from . models import Api, Project, Configs
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from homepage.views import index
import uuid
from django.conf import settings
from django.contrib import messages
import requests
from user_dashboard.models import Project
from django.contrib.auth.views import logout_then_login
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import urllib.parse
from user_dashboard.models import Project, Api
from django.shortcuts import get_object_or_404
#

# HEADERS = {
#     "Authorization": "Bearer %s" % (settings.AUTH_ADMIN_TOKEN)
# }

# BASE_URL = settings.AUTH_API_URL


@login_required(login_url='/accounts/signin')
def dash_rdrct(request):
    user = request.user
    proj_name = Project.objects.filter(user=user).get(last_project=True)
    
    if proj_name is not None:
        proj_name = proj_name.name
    else:
        proj_name = Project.objects.create(
        name="Default_Project", user=user, token=uuid.uuid4().hex, last_project=True)
        proj_name.save()
        proj_name.name = user.last_project
        user.save()
    return redirect('/dashboard/main/' + '{}'.format(proj_name))
    # return redirect('/dashboard/')

#new Dashboard
@login_required(login_url='/accounts/signin')
def dash(request):
    user = request.user
    projects = Project.objects.filter(user=user)
    context = {
        'projects' : projects
    }
    return render(request, 'user_dashboard/dashboard.html', context)

#ProjPage
@login_required(login_url='/accounts/signin')
def oneproj(request, name):
    try:
        user= request.user
        projects = Project.objects.filter(user=user)
        user_proj = Project.objects.filter(user=user).filter(name=name)
        spef_proj = Project.objects.filter(user=user).get(name=name)
        api_list = Api.objects.all()
        spef_proj.last_project = True
        spef_proj.save()
        pe = Configs.objects.filter(project=spef_proj)
    except Project.DoesNotExist:
        messages.info(request, f"Project {name} does not exist..Add a new project")
        return redirect('user_dashboard:settings')


    context = {
        'projects' : projects,
        'user_proj': user_proj,
        'api_list': api_list,
        'spef_proj':spef_proj,
        'pe':pe,
    }

    return render(request, 'user_dashboard/project.html', context)



@login_required(login_url='/accounts/signin')
def api_list(request, project_name):
    print(request)
    # proj = Project.objects.get(name=project_name)
    path = request.path
    get_id = str([i for i in str(path).split('/') if i][-1])
    projet = request.user.projects.get(name=get_id)
    print(projet)
    all_apis = Api.objects.order_by('title')
    print(all_apis)
    return render(request, 'user_dashboard/dashboard.html', {'all_apis':all_apis, 'projet':projet})

def adding_api(request, proj_id, id):
    add_to_api = Api.objects.get(id=id)
    print(add_to_api)
    project = Project.objects.get(id=proj_id)
    print(project)
    Project.add_api(api=add_to_api, projet=project)
    #all_apis = objects.order_by('title')
    pro_id = project.name
    print(pro_id)
    return redirect('/dashboard/main/' + '{}'.format(pro_id))
    #return render(request, 'user_dashboard/dashboard.html', {'all_apis':all_apis})

def activate_api(request, proj_id, id):
        print(request.POST)
        pj = Project.objects.get(id=proj_id)
        api = pj.project_api.get(id=id)
        pe = Configs.objects.filter(project=pj).get(konfigd_api=api)
        #api = ApiList.objects.get(id=id)
        print(pj)

        if request.POST.get('active') == 'true':
            pe.is_active = True
            pe.save()
            print(pe.is_active)
            return JsonResponse({'status':'Active'})
        pe.is_active = False
        pe.save()
        print(pe.is_active)
        return JsonResponse({'status':'De-Activated'})

@login_required(login_url='/accounts/signin')
def configure_api(request, proj_id, api_id):
    projects = Project.objects.filter(user=request.user)
    pro_name = Project.objects.filter(user=request.user).get(id=proj_id)
    api_to_conf = pro_name.project_api.get(id=api_id)
    name = api_to_conf.title
    inst = Configs.objects.filter(project=pro_name).get(konfigd_api=api_to_conf)
    
    edit_settings = dict()
    try:
        docs = get_object_or_404(Api, id=api_id)
        api_docs = docs.docs_url
        response = requests.get(api_docs)
        documentation = response.json()
        servers = documentation['data']['servers']
        paths = documentation['data']['paths']
        server_url = servers[0]['url']
        if request.method == 'POST':
            dicto = request.POST
            user_settings = dicto.dict()
            del user_settings['csrfmiddlewaretoken']
            print(user_settings)

            # configs = Configs.objects.filter(konfigs=None, project=pro_name).get(konfigd_api=api_to_conf)
            # print(configs)
            
            # save = request.POST.get('save')
            # print(save)
            # update = request.POST.get('update')
            # create = request.POST.get('create')

            print(name, "line 147")
            if name.upper() == 'SMS MICROAPI':
                print('something')
                sender = user_settings['sender']
                service_name = user_settings['service_name'] 
                token = user_settings['token'] 
                sid = user_settings['sid'] 
                verified_no = user_settings['verified_no'] 
                default = user_settings['default'] 
                
                headers = {}
                payload = {
                    "sender": f'{sender}',
                    "service_name": f'{service_name}',
                    "token": f'{token}',
                    "sid": f'{sid}',
                    "verified_no": f'{verified_no}',
                    "default": f'{default}'
                }

                payload2 = {
                    "senderID": f'{sender}'
                }
                
                if 'save_btn' in request.POST:
                    url = api_to_conf.post_settings
                    del user_settings['save_btn']
                    register = requests.request('POST', 'https://sms-microapi.herokuapp.com/v2/sms/user_register', headers=headers, data=payload2)
                    reg = register.json()
                    print(reg)
                    response = requests.request('POST', url, headers=headers, data=payload)
                    print(response)
                    response = response.json()
                    msg = response['details']
                    print(msg)
                    if response['status'] == 201:
                        print('something')
                        specf_set = dict()    
                        inst.konfigs = user_settings
                        inst.save()
                        messages.success(request, "you've successfully configured {}|{}".format(name, msg))
                        return redirect('/dashboard/main/' + '{}'.format(pro_name.name), {'paths' : paths,'url' : server_url})
                    else:
                        messages.success(request, f"{msg}")
                        return redirect('/dashboard/main/' + '{}'.format(pro_name.name), {'paths' : paths,'url' : server_url})
                
                elif 'update_btn' in request.POST:
                    print('yes')
                    url = 'https://sms-microapi.herokuapp.com/v2/sms/config/update_config'
                    del user_settings['update_btn']
                    response = requests.request('PUT', url, headers=headers, data=payload)
                    response = response.json()
                    msg = response['details']
                    # print(response)
                    if response['status'] == 202:
                        # specf_set = dict()    
                        print('yessss')
                        first_time = True
                        edit_settings = dict()
                        print(edit_settings)
                        print(inst.konfigs)
                        print(user_settings)

                        inst.konfigs = user_settings
                        inst.save()
                        messages.success(request, "you've successfully updated {}|{}".format(name, msg))
                        return redirect('/dashboard/main/' + '{}'.format(pro_name.name), {'paths' : paths,'url' : server_url})
                    else:
                        messages.success(request, f"{msg}")
                        return redirect('/dashboard/main/' + '{}'.format(pro_name.name), {'paths' : paths,'url' : server_url})
                
                elif 'create_btn' in request.POST:

                    url = api_to_conf.post_settings
                    del user_settings['create_btn']
                    response = requests.request('POST', url, headers=headers, data=payload)
                    print(response)
                    response = response.json()
                    msg = response['details']
                    print(msg)
                    if response['status'] == 201:
                        print('something')
                        specf_set = dict()    
                        inst.konfigs = user_settings
                        inst.save()
                        messages.success(request, "you've successfully configured {}|{}".format(name, msg))
                        return redirect('/dashboard/main/' + '{}'.format(pro_name.name), {'paths' : paths,'url' : server_url})
                    else:
                        messages.success(request, f"{msg}")
                        return redirect('/dashboard/main/' + '{}'.format(pro_name.name), {'paths' : paths,'url' : server_url})


            messages.success(request, "you've successfully configured {}".format(name))
            return redirect('/dashboard/main/' + '{}'.format(pro_name.name), {'paths' : paths,'url' : server_url})
        else:

            first_time = True
            edit_settings = dict()
            url = api_to_conf.get_settings
            if inst.konfigs is not None:
                first_time = False
                edit_settings = inst.konfigs
                print(edit_settings)
            response = requests.get(url,headers=HEADERS)
            response = response.json()
            # print(response)
            settings = response['data']
            oauth = ['Facebook Credentials', 'Twitter Credentials','Github Credentials', 'Google Credentials','SendGrid Credentials','Aws Settings Credentials']

            return render(request, 'user_dashboard/configure_api.html', {'settings':settings, 'first_time':first_time, 'ap_name':name, 'oauth':oauth, 'api_id':api_to_conf.id, 'edit_settings':edit_settings,'paths' : paths,'url' : server_url})
    except Exception as e:
        messages.info(request, 'Sorry, Documentation Format is Invalid')
        return redirect('/dashboard/main/' + '{}'.format(pro_name.name))

# @login_required(login_url='/accounts/signin')
# def configure_api(request):
#     user = request.user
#     projects = Project.objects.filter(user=user)
#     context = {
#         'projects' : projects
#     }
#     return render(request, 'user_dashboard/configure_api.html', context)


def logout(request):
    auth.logout(request)
    return redirect('index')


# def settings(request):
#     user = request.user
#     projects = Project.objects.filter(user=user)
#     context = {
#         'projects':projects
#     }
#     return render(request, 'user_dashboard/acct_settings.html', context)


@login_required(login_url='/accounts/signin')
def addProject(request):  # function to add a project to a user
    if request.method == "POST":

        project_name = request.POST['project_name']
        print(f'project name {project_name}')
        
        if len(project_name.strip()) >= 3:
            user = request.user
            addproject = Project.objects.filter(user=user.id).filter(name=project_name)  # user.id or user.user_id??
            print(addProject)
            if addproject.exists():
                messages.warning(request, f'Project with name {project_name} already exists')
                return redirect("user_dashboard:dash_main")
            else:
                proj = Project.objects.create(
                    name=project_name,
                    user=user,
                    token=uuid.uuid4().hex,
                    last_project= True
                )
                proj.save()
                print(proj)
                print("done creating")
                return redirect("user_dashboard:dash_proj", name=proj.name)
        else:
            messages.warning(request, f'Project Name cant be left empty or be less than 3 characters')
            return redirect("user_dashboard:dash_main")          
    else:
        return redirect('/dashboard', {'error': 'Project name already taken'})




# @login_required(login_url='/accounts/signin')
# def switch(request, project_name):
#     user = request.user
#     switch_proj = Project.objects.get(id=id)
#     return redirect('/dashboard')
#     # return render(request, 'user_dashboard/dashboard.html')


@login_required(login_url='/accounts/signin')
def home_page(request, name):
    user = request.user
    projID = Project.objects.filter(user_id=user).filter(name=name).first()
    return redirect("dashboard:dashboard", id=(projID))


def upload_avatar(request):
    pass


class ConfigureApiView(LoginRequiredMixin, TemplateView):
    template_name = 'user_dashboard/configure_api.html'


HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmMmE5NzkwYTYxNDNhMDAwNDBkN2M4OSIsImVtYWlsIjoiaG5naTdtaWNyb2FwaUBnbWFpbC5jb20iLCJEQlVSSSI6Im1vbmdvZGIrc3J2Oi8vbWljcm9hcGk6c2VjcmV0MTIzQGNsdXN0ZXIwLmphcGl3Lm1vbmdvZGIubmV0L21pY3JvYXBpP3JldHJ5V3JpdGVzPXRydWUmdz1tYWpvcml0eSIsImlhdCI6MTU5NjYyNjg4NH0.NFFT4s08h-IYE_PzvxBwXsua7KFl_Z5_2iNqDc4OEXs"
}

def change_password(request):
    if request.method == "POST":
        print("here")
        old_pass = request.POST.get("old_password")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")
        print("here2s")
        # get old pass from auth api

        if pass1 == pass2:
            # url = settings.AUTH_API_URL + "/api/user/password/change-password"
            url = "https://authentication-microapi.herokuapp.com/api/user/password/change-password"
            payload = {
                "email":request.user.email,
                "oldPassword": old_pass,
                "newPassword": pass1
            }
            print("here3s")

            response = requests.post(url=url, data=payload, headers=HEADERS)
            response = response.json()  
            print(response)
            try:
                if response["success"] == True:
                    # if response is success
                    messages.info(request, "Password has been changed")
                else:
                    messages.info(request, response["data"]["message"])
            except:
                messages.info(request, "Authentication is not available right now")
            finally:
                return redirect("dashboard:settings")
        else:
            messages.warning(request, "Password are not alike")
            return redirect("dashboard:settings")


def create_api_page(request):
    return render(request, 'user_dashboard/create_api.html')
    
def create_api(request):
    if request.method == 'POST':
        api = Api()
        url = request.POST['info_url']
        response = requests.request('get', url)
        info = response.json()
        try:
            if info['success'] == True:
                print(info)
                api.title = info['data']['title']
                api.description = info['data']['description']
                api.icon = info['data']['icon']
                print(api)
                api.save()
        except KeyError:
            return redirect('dashboard:create_api_page')

        api.get_settings = request.POST['settings_url']
        api.docs_url = request.POST['docs_url']
        api.post_settings = request.POST['post_settings']
        api.save()
        return redirect('dashboard:create_api_page')
    else:
        return redirect('dashboard:create_api_page')


############################
# ACCOUNT SETTINGS
##########################

# List all projects for a user
def get_projects(request):
    user_id = user.id
    project = Project.objects.filter(user=user_id)
    if project.exists():
        return project
    else:
        raise Http404('No project found for this user')

@login_required
def update_project(request, id):
    project = get_object_or_404(Project, id=id)
    user = request.user
    if project is not None:
        # check if the current user has project Id similar to the passed ID
        if request.method == 'POST':
            project_name = request.POST['project_name']
            # project_check = Project.objects.filter(Q(user_id=user.id) & Q(name=project_name))
            project_check = Project.objects.filter(user_id=user.id).filter(name=project_name)
            # Project.objects.filter(user_id=user.id).update(**{name: project_name}, {token: uuid.uuid4().hex})
            print (project_check)
            if not project_check:
                project.name = project_name
                # project.user_id = user,
                project.token = uuid.uuid4().hex
                project.save()
                messages.info(request, "Your project name has successfully being updated")
            else:
                messages.warning(request, "You already have a project with this project name.")
        else:
            return render(request, "accounts/project_update.html")
    return render(request, "accounts/project_update.html", context)

# edit profile
@login_required   
def settings(request):
    user = request.user
    projects = Project.objects.filter(user=user)
    context = {
        'projects' : projects
    }
    error = []
    if request.method == 'POST':
        username = request.POST.get("username").replace(" ", "")
        email = request.POST.get("email").replace(" ", "")
        if username == "":
            username = user.username
        if email == "":
            email = user.email
        try:
            username_exists = User.objects.get(username=username)
            if username_exists and user != username_exists:
                error.append("error1")
                messages.warning(request, "Username already exists. Please select another")
        except ObjectDoesNotExist:
            user.username = username
        try:
            email_exists = User.objects.get(email=email)
            if email_exists and user != email_exists:
                error.append("error2")
                messages.warning(request, "Email already exists. Please select another")
        except ObjectDoesNotExist:
            user.email = email

        if not error:
            user.save()
            messages.success(request, "Details successfully updated!", extra_tags='alert')
    return render(request, 'user_dashboard/acct_settings.html', context) 

@login_required  
def delete_project(request, id):
    context = {}
    # project=""
    users = request.user
    if request.method == "GET":
        try:
            project = Project.objects.get(id=id)
            if project.user.id == users.id:
                # project.is_active = false This is a better option
                print("Project successfully deleteed")
                project.delete()
                # project.save()
                messages.success(request, "Project successfully deleted!")
            else:
                messages.success(request, "Project does not exists!")
            return render(request, 'user_dashboard/acct_settings.html')
        except ObjectDoesNotExist:
            messages.warning(request, "Project does not exists")
        # except Exception as e:
        #     # context['message'] = e.message
        #     messages.warning(request, e.message)
        # return render(request, 'user_dashboard/acct_settings.html', context)
    return render(request, 'user_dashboard/acct_settings.html')
    


############################
# END ACCOUNT SETTINGS
##########################


############################
# DOCUMENTATION VIEWING ON CONFIGURATION PAGE
##########################
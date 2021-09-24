from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
import re
from django.contrib import messages
import math
# Create your views here.

from .models import ExtendedUsers, Branch, Attendence, Department, Institute, Semester


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'index.html')


def login(request):
    if request.user.is_authenticated:
        return redirect(dashboard)

    if request.method == "POST":
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid Login Credential'})

    else:
        return render(request, 'login.html')


@login_required(login_url='login')
def dashboard(request):
    total_users = User.objects.count()
    # messages.success(request,'hello world testing')
    return render(request, 'dashboard.html', {'total_user': total_users})


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect(index)


@login_required(login_url='login')
def registerUsers(request):
    if ExtendedUsers.objects.filter(user=request.user)[0].user_role == 'admin':
        branch_data = Branch.objects.all()
        sem = Semester.objects.all()
        if request.method == 'POST':
            errors = {}
            if 'firstname' not in request.POST.keys():
                errors['firstname'] = "First Name is required"

            if 'disp' not in request.POST.keys():
                errors['disp'] = "Display Name is required"

            if 'lastname' not in request.POST.keys():
                errors['lastname'] = "Last Name is required"

            if 'role' not in request.POST.keys():
                errors['role'] = "Role is required"
            else:
                if request.POST['role'] not in ['student', 'faculty', 'admin']:
                    errors['role'] = "Valid User Role is Required"

            if 'username' not in request.POST.keys():
                errors['username'] = "Username is Required"
            else:
                if not request.POST['username'].isalnum():
                    errors['username'] = "AlphaNumeric is required only"

                    if len(request.POST['username']) > 10:
                        errors['username'] = "Username Should be between 10 chars"

            if 'email' not in request.POST.keys():
                errors['email'] = "Email is Required"
            else:
                match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                                 request.POST['email'])
                if match == None:
                    errors['email'] = "Valid Emails is Required"

            if 'branch' not in request.POST.keys():
                errors['branch'] = "Branch is Required"

            if 'phone' not in request.POST.keys():
                errors['phone'] = "Phone number is Required"

            if 'password' not in request.POST.keys():
                errors['password'] = "Password is Required"
            else:
                if len(request.POST['password']) < 5:
                    errors['password'] = "Minimum Password Should be 5 character"

            if errors:

                branch = Branch.objects.all()
                return render(request, 'register_user.html', {'branch': branch_data, 'sem': sem, 'formerrors': errors})

            else:
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                role = request.POST['role']
                username = request.POST['username']
                email = request.POST['email']
                branch = request.POST['branch']
                phone = request.POST['phone']
                password = request.POST['password']

                errors = {}

                if User.objects.filter(username=username):
                    errors['username'] = 'User is Alerady Exist'

                if User.objects.filter(email=email):
                    errors['email'] = 'Email is Alerady Exist'

                if not errors:
                    newUser = User.objects.create_user(username, email, password)
                    newUser.first_name = firstname
                    newUser.last_name = lastname
                    newUser.save()

                    etu = ExtendedUsers(user=newUser)
                    etu.branch = Branch.objects.get(id=branch)
                    etu.sem_id = Semester.objects.get(id=request.POST['sem'])
                    etu.mobile = phone
                    etu.disp = request.POST['disp']
                    etu.org_password = password
                    etu.user_role = role
                    etu.save()

                    messages.success(request, 'New User Successfully Created')
                    return redirect('dashboard')
                else:
                    print(errors)
                    return render(request, 'register_user.html',
                                  {'formerrors': errors, 'branch': branch_data, 'sem': sem})

        else:

            return render(request, 'register_user.html', {'branch': branch_data, 'sem': sem})

    else:
        return redirect('not_found')


def notfound404(request):
    return render(request, 'not_found.html')


@login_required(login_url='login')
def user_info(request):
    limit = 10
    if 'page' in request.GET.keys():
        page = int(request.GET['page'])
    else:
        page = 1

    start_from = (page - 1) * limit
    if start_from < 0:
        start_from = 0

    total_records = User.objects.count()

    total_pages = math.ceil(total_records / limit)

    profiles = User.objects.all()[start_from:start_from + limit]
    return render(request, 'user_list.html',
                  {'profiles': profiles, 'total_pages': range(1, total_pages + 1), 'one': 1, 'zero': 0})


@login_required(login_url='login')
def disable_user(request):
    if 'action' in request.GET.keys():
        if request.GET['action'] == "1":
            action = 1
        else:
            action = 0
    if 'username' in request.GET.keys():
        u = ExtendedUsers.objects.get(user_id=int(request.GET['username']))
        u.user_status = action
        u.save()
        # print('MSG',u.mobile)

        return redirect('user_info')


@login_required(login_url='login')
def view_user(request, id):
    profile = User.objects.get(id=id)

    return render(request, 'view_profile.html', {'profile': profile})


@login_required(login_url='login')
def edit_profile(request, id):
    profile_id = id
    roles = {'student', 'admin', 'faculty'}
    allsem = Semester.objects.all()
    if request.user.info.user_role == "admin":
        if request.method == "POST":
            errors = {}
            if 'firstname' not in request.POST.keys():
                errors['firstname'] = "First Name is required"

            if 'lastname' not in request.POST.keys():
                errors['lastname'] = "Last Name is required"

            if 'role' not in request.POST.keys():
                errors['role'] = "Role is required"
            else:
                if request.POST['role'] not in ['student', 'faculty', 'admin']:
                    errors['role'] = "Valid User Role is Required"

            if 'email' not in request.POST.keys():
                errors['email'] = "Email is Required"
            else:
                match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                                 request.POST['email'])
                if match == None:
                    errors['email'] = "Valid Emails is Required"

            if 'branch' not in request.POST.keys():
                errors['branch'] = "Branch is Required"
            else:
                if not Branch.objects.filter(id=request.POST['branch']):
                    errors['branch'] = "Valid Branch is Required"

            if 'phone' not in request.POST.keys():
                errors['phone'] = "Phone number is Required"

            if 'password' not in request.POST.keys():
                errors['password'] = "Password is Required"
            else:
                if len(request.POST['password']) < 5:
                    errors['password'] = "Minimum Password Should be 5 character"

            if errors:
                branch = Branch.objects.all()
                return render(request, 'edit_profile.html', {'roles': roles, 'branch': branch, 'sem': allsem,
                                                             'profile': User.objects.get(id=profile_id),
                                                             'formerrors': errors})

            else:
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                role = request.POST['role']
                email = request.POST['email']
                branch = request.POST['branch']
                phone = request.POST['phone']
                password = request.POST['password']

                flashError = {}

                if not flashError:
                    newUser = User.objects.get(id=profile_id)
                    newUser.first_name = firstname
                    newUser.last_name = lastname
                    newUser.email = email
                    newUser.save()

                    etu = ExtendedUsers.objects.get(user=newUser)
                    etu.branch = Branch.objects.get(id=branch)
                    etu.mobile = phone
                    etu.disp = request.POST['disp']
                    etu.sem_id = Semester.objects.get(sem_in_number=request.POST['sem'])
                    etu.org_password = password
                    etu.user_role = role
                    etu.save()

                    messages.success(request, 'Successfully Updated')
                    return redirect('dashboard')
                else:
                    branch = Branch.objects.all()
                    print(flashError)
                    return render(request, 'edit_profile.html',
                                  {'roles': roles, 'profile': User.objects.get(id=profile_id), 'branch': branch,
                                   'flashError': flashError, 'sem': allsem})
        else:
            profile = User.objects.get(id=str(profile_id))
            branch = Branch.objects.all()
            return render(request, 'edit_profile.html',
                          {'roles': roles, 'profile': profile, 'sem': allsem, 'branch': branch})
    else:
        return redirect('not_found')


def attendence_list(request):
    # attendence=Attendence()
    # attendence.user_id=request.user
    # print(request.user.id)
    # attendence.save()

    atn = Attendence.objects.filter(user_id=request.user)
    return render(request, 'attendence_list.html', {'attendence': atn})


@login_required(login_url='login')
def add_institute(request):
    if request.user.info.user_role == "admin":
        if request.method == "POST":
            errors = {}
            if 'inst' not in request.POST.keys():
                errors['inst'] = "Institute name is required"
            else:
                if len(request.POST['inst']) > 100 or len(request.POST['inst']) < 1:
                    errors['inst'] = "Department name should be less than 100 chars"

            if 'alias' not in request.POST.keys():
                errors['alias'] = 'Alias is Required'
            else:
                if len(request.POST['alias']) > 100 or len(request.POST['alias']) < 1:
                    errors['alias'] = "Department name should be less than 100 chars"

            if errors:
                return render(request, 'add_institute.html', {'errors': errors})
            else:
                errors = {}

                if Institute.objects.filter(name=request.POST['inst']):
                    errors['inst'] = 'Institute is Alerady Exist'

                if Institute.objects.filter(alias=request.POST['alias']):
                    errors['alias'] = 'Institute alias is Alerady Exist'

                if errors:
                    return render(request, 'add_institute.html', {'errors': errors})
                else:
                    inst = Institute()
                    inst.name = request.POST['inst']
                    inst.alias = request.POST['alias']
                    inst.save()
                    return redirect('institute')

        return render(request, 'add_institute.html')

    else:
        return redirect('not_found')


@login_required(login_url='login')
def institute(request):
    d = Institute.objects.all()
    return render(request, 'institute.html', {'inst': d})


@login_required(login_url='login')
def edit_institute(request):
    if request.user.info.user_role == "admin":
        if request.method == "POST":
            errors = {}
            if 'inst' not in request.POST.keys():
                errors['inst'] = "Institute name is required"
            else:
                if len(request.POST['inst']) > 100 or len(request.POST['inst']) < 1:
                    errors['inst'] = "Institute name should be less than 100 chars"

            if 'alias' not in request.POST.keys():
                errors['alias'] = 'Alias is Required'
            else:
                if len(request.POST['alias']) > 100 or len(request.POST['alias']) < 1:
                    errors['alias'] = "Institute name should be less than 100 chars"

            if errors:
                return render(request, 'edit_institute.html', {'errors': errors})
            else:

                data = Institute.objects.get(id=request.POST['id'])
                data.name = request.POST['inst']
                data.alias = request.POST['alias']
                data.save()
                messages.success(request, 'Successfully Updated')
                return redirect(dashboard)
        else:
            inst = Institute.objects.get(id=request.GET['id'])
            return render(request, 'edit_institute.html', {'inst': inst})
    else:
        return redirect('not_found')


@login_required(login_url='login')
def add_department(request):
    if request.user.info.user_role == "admin":
        inst = Institute.objects.all()
        if request.method == "POST":
            errors = {}
            if 'dept' not in request.POST.keys():
                errors['dept'] = "Department name is required"
            else:
                if len(request.POST['dept']) > 100 or len(request.POST['dept']) < 1:
                    errors['dept'] = "Department name should be less than 100 chars"

            if 'alias' not in request.POST.keys():
                errors['alias'] = 'Alias is Required'
            else:
                if len(request.POST['alias']) > 100 or len(request.POST['alias']) < 1:
                    errors['alias'] = "Department alias should be less than 100 chars"

            if errors:
                return render(request, 'add_department.html', {'errors': errors, 'inst': inst})
            else:
                errors = {}
                if Department.objects.filter(name=request.POST['dept']):
                    errors['dept'] = "This Department Alerady Exist"
                if Department.objects.filter(alias=request.POST['alias']):
                    errors['alias'] = "This Department Alias Alerady Exist"

                if errors:
                    return render(request, 'add_department.html', {'errors': errors, 'inst': inst})
                else:
                    d = Department()
                    d.institute_id = Institute.objects.get(id=request.POST['inst_id'])
                    d.name = request.POST['dept']
                    d.alias = request.POST['alias']
                    d.save()
                    messages.success(request, 'Department Successfully Created')
                    return redirect('dashboard')
        else:
            return render(request, 'add_department.html', {'inst': inst})
    else:
        return redirect('not_found')


@login_required(login_url="login")
def department(request):
    dept = Department.objects.all()
    return render(request, 'department.html', {'dept': dept})


def edit_department(request, id):
    if request.user.info.user_role == "admin":
        dept = Department.objects.get(id=id)
        inst = Institute.objects.all()

        if request.method == "POST":
            errors = {}
            if 'dept' not in request.POST.keys():
                errors['dept'] = "Department name is required"
            else:
                if len(request.POST['dept']) > 100 or len(request.POST['dept']) < 1:
                    errors['dept'] = "Department name should be less than 100 chars"

            if 'alias' not in request.POST.keys():
                errors['alias'] = 'Alias is Required'
            else:
                if len(request.POST['alias']) > 100 or len(request.POST['alias']) < 1:
                    errors['alias'] = "Department alias should be less than 100 chars"

            if errors:
                return render(request, 'add_department.html', {'errors': errors, 'inst': inst})
            else:
                errors = {}
                if Department.objects.filter(name=request.POST['dept']):
                    errors['dept'] = "This Department Alerady Exist"
                if Department.objects.filter(alias=request.POST['alias']):
                    errors['alias'] = "This Department Alias Alerady Exist"

                if errors:
                    return render(request, 'add_department.html', {'errors': errors, 'inst': inst})
                else:
                    d = Department.objects.get(id=request.POST['dept_id'])
                    d.name = request.POST['dept']
                    d.alias = request.POST['alias']
                    d.save()
                    messages.success(request, 'Department Successfully Updated')
                    return redirect('dashboard')

        else:

            return render(request, 'edit_department.html', {'dept': dept, 'inst': inst})
    else:
        return redirect('not_found')


@login_required(login_url='login')
def add_branch(request):
    if request.user.info.user_role == "admin":
        dept = Department.objects.all()
        if request.method == "POST":
            errors = {}
            if 'branch' not in request.POST.keys():
                errors['branch'] = "Branch name is required"
            else:
                if len(request.POST['branch']) > 100 or len(request.POST['branch']) < 1:
                    errors['branch'] = "Branch name should be less than 100 chars"

            if 'alias' not in request.POST.keys():
                errors['alias'] = 'Alias is Required'
            else:
                if len(request.POST['alias']) > 100 or len(request.POST['alias']) < 1:
                    errors['alias'] = "Department alias should be less than 100 chars"

            if errors:
                return render(request, 'add_branch.html', {'errors': errors, 'dept': dept})
            else:
                errors = {}
                if Branch.objects.filter(name=request.POST['branch']):
                    errors['branch'] = "This Branch Alerady Exist"
                if Branch.objects.filter(alias=request.POST['alias']):
                    errors['alias'] = "This Branch Alias Alerady Exist"

                if errors:
                    return render(request, 'add_branch.html', {'errors': errors, 'dept': dept})
                else:
                    b = Branch()
                    b.name = request.POST['branch']
                    b.alias = request.POST['alias']
                    b.dept_id = Department.objects.get(id=request.POST['dept'])
                    b.save()
                    messages.success(request, 'Branch Successfully Created')
                    return redirect('dashboard')
        else:
            return render(request, 'add_branch.html', {'dept': dept})
    else:
        return redirect('not_found')


@login_required(login_url='login')
def branch(request):
    return render(request, 'branch.html', {'branch': Branch.objects.all()})


def edit_branch(request, id):
    b = Branch.objects.get(id=id)
    dept = Department.objects.all()

    if request.user.info.user_role == "admin":
        if request.method == "POST":
            errors = {}
            if 'branch' not in request.POST.keys():
                errors['branch'] = "Branch name is required"
            else:
                if len(request.POST['branch']) > 100 or len(request.POST['branch']) < 1:
                    errors['branch'] = "Branch name should be less than 100 chars"

            if 'alias' not in request.POST.keys():
                errors['alias'] = 'Alias is Required'
            else:
                if len(request.POST['alias']) > 100 or len(request.POST['alias']) < 1:
                    errors['alias'] = "Department alias should be less than 100 chars"

            if errors:
                return render(request, 'edit_branch.html', {'errors': errors, 'branch': b, 'dept': dept})
            else:
                errors = {}
                if Branch.objects.filter(name=request.POST['branch']):
                    errors['branch'] = "This Branch Alerady Exist"
                if Branch.objects.filter(alias=request.POST['alias']):
                    errors['alias'] = "This Branch Alias Alerady Exist"

                if errors:
                    return render(request, 'edit_branch.html', {'errors': errors, 'branch': b, 'dept': dept})
                else:
                    b = Branch()
                    b.name = request.POST['branch']
                    b.alias = request.POST['alias']
                    b.dept_id = Department.objects.get(id=request.POST['dept'])
                    b.save()
                    messages.success(request, 'Branch Successfully Created')
                    return redirect('dashboard')
        else:
            return render(request, 'edit_branch.html', {'branch': b, 'dept': dept})

    else:
        return redirect('not_found')


@login_required(login_url='login')
def add_semester(request):
    if request.user.info.user_role == "admin":
        if request.method == "POST":
            errors = {}
            if 'num' not in request.POST.keys():
                errors['num'] = "Semester Number is required"
            else:
                if len(request.POST['num']) > 12 or len(request.POST['num']) <= 1:
                    errors['num'] = "Semester Number name should be less than 1 chars"

            if 'alias' not in request.POST.keys():
                errors['alias'] = 'Alias is Required'
            else:
                if len(request.POST['alias']) > 100 or len(request.POST['alias']) < 1:
                    errors['alias'] = "Department alias should be less than 100 chars"

        else:
            return render(request, 'add_semester.html')
    else:
        return redirect('not_found')

from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('login',views.login,name="login"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('logout',views.logout,name="logout"),
    path('register',views.registerUsers,name="register"),
    path('404_not_found',views.notfound404,name="not_found"),
    path('user_info',views.user_info,name="user_info"),

    path('user_info/disable',views.disable_user,name="disable_user"),
    path('user_info/view/<int:id>',views.view_user,name="user_view"),
    path('user_info/edit/<int:id>',views.edit_profile,name="edit_profile"),

    path('attendence_list',views.attendence_list,name="attendence_list"),
    path('add_institute',views.add_institute,name="add_institute"),
    path('institute',views.institute,name="institute"),
    path('edit_institute',views.edit_institute,name="edit_institute"),
    path('add_department',views.add_department,name="add_department"),
    path('department',views.department,name="department"),
    path('edit_department/<int:id>',views.edit_department,name="edit_department"),

    path('add_branch',views.add_branch,name="add_branch"),
    path('branch',views.branch,name="branch"),
    path('edit_branch/<int:id>',views.edit_branch,name="edit_branch"),

    path('add_semester',views.add_semester,name="add_semester"),


]
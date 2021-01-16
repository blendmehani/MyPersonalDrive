from django.shortcuts import render, redirect, get_object_or_404, Http404
from .forms import UpdateUserForm, UploadFile
from accounts.models import User
from .models import Directory, File
from django.http import HttpResponse, JsonResponse
from itertools import chain
import os


def main(request, username):
    user = request.user
    context = {}
    if not user.is_authenticated:
        return redirect('dashboard')

    directories = Directory.objects.filter(parent_dir_id__isnull=True, user=user)
    files = File.objects.filter(parent_dir_id__isnull=True, user=user)
    directories_files = list(chain(directories, files))
    directories_files.sort(key=lambda x: x.date_created)
    if not directories_files:
        context['empty'] = 'No directories or files found in your account.'

    if request.GET.get('file_name'):
        file_name = request.GET.get('file_name')
        searched_files = File.objects.filter(user=user, file_name__icontains=file_name)
        directories_files = searched_files
        if not searched_files:
            context['empty'] = f'There were no results matching your search: "{file_name}".'

    context['files'] = directories_files
    context['user_url'] = request.build_absolute_uri()
    context['all_directories'] = Directory.objects.filter(user=user).values('parent_dir_id')
    context['all_files'] = File.objects.filter(user=user).values('parent_dir_id')
    return render(request, 'content/main_logic.html', context)


def nested(request, dir_name, username):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('dashboard')
    url = request.build_absolute_uri()
    url_list = url.split('/')
    final_url = url_list[-2]
    final_url = final_url.replace('%20', ' ')
    parent_id = get_object_or_404(Directory, dir_name=final_url, user=user)
    directories = Directory.objects.filter(parent_dir_id=parent_id.id).filter(user=user.id)
    files = File.objects.filter(parent_dir_id=parent_id).filter(user=user.id)
    directories_files = list(chain(directories, files))
    directories_files.sort(key=lambda x: x.date_created)
    context['files'] = directories_files
    return render(request, 'content/main_logic.html', context)


def user_settings(request, username):
    context = {}
    if request.POST:
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            update = form.save(commit=False)
            update.first_name = first_name.capitalize()
            update.last_name = last_name.capitalize()
            form.initial = {
                "first_name": request.POST['first_name'].capitalize(),
                "last_name": request.POST['last_name'].capitalize(),
                "email": request.POST['email'],
                "phone_number": request.POST['phone_number']
            }
            update.save()
            context['success_message'] = 'Data updated successfully.'
    else:
        form = UpdateUserForm(
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
                "phone_number": request.user.phone_number
            }
        )
    context['update_user_form'] = form
    return render(request, 'user_settings.html', context)


def delete_user(request, username):
    user = User.objects.get(username=username)
    if request.POST:
        user.delete()
        return redirect('dashboard')
    context = {}
    return render(request, 'delete_user.html', context)


def deactivate_user(request, username):
    user = User.objects.get(username=username)
    if request.POST:
        user.is_active = 0
        user.save()
        return redirect('dashboard')
    context = {}
    return render(request, 'deactivate_user.html', context)


def create_directory(request, username):
    import re
    response_data = {}
    user = User.objects.get(username=username)
    if request.is_ajax and request.POST:
        dir_name = request.POST['dir_name']
        dir_path = request.POST['url']
        if 'file' in dir_path:
            dir_list = dir_path.split('/')
            dir_parent = dir_list[-2]
            if '%20' in dir_parent:
                dir_parent_final = dir_parent.replace('%20', ' ')
            else:
                dir_parent_final = dir_parent
            dir_parent_id = get_object_or_404(Directory, dir_name=dir_parent_final, user=request.user.id).id
        else:
            dir_parent_id = None
        regex = "^[ A-Za-z0-9_-]*$"
        if re.match(regex, dir_name) and not Directory.objects.filter(dir_name=dir_name, user=request.user.id).exists():
            response_data['title'] = 'Congratulations!'
            response_data['is_success'] = True
            response_data['message'] = f'Directory "{dir_name}" has been successfully created.'
            Directory.objects.create(
                parent_dir_id=dir_parent_id,
                dir_name=dir_name,
                user=user
            )
        else:
            response_data['is_success'] = False
            response_data['title'] = 'We are sorry!'
            response_data['message'] = f'Directory "{dir_name}" has not been created. ' \
                                       f'Please use a correct and unique name.'
        return JsonResponse(response_data)


def upload_file(request, username):
    context = {}
    user = request.user
    if request.POST:
        form = UploadFile(request.POST, request.FILES)
        print(request.FILES['file'])
        if form.is_valid():
            save_file = form.save(commit=False)
            file = request.FILES['file']
            url = request.POST['url']
            file_name = os.path.splitext(file.name)[0]
            i = 1
            final_file_name = file_name
            while File.objects.filter(file_name=final_file_name, user=user).exists():
                final_file_name = file_name + '(' + str(i) + ')'
                i = i + 1
            save_file.file_name = final_file_name
            save_file.user = user
            if 'file' in url:
                url_list = url.split('/')
                dir_parent = url_list[-2]
                if '%20' in dir_parent:
                    dir_parent_final = dir_parent.replace('%20', ' ')
                else:
                    dir_parent_final = dir_parent
                dir_parent_id = get_object_or_404(Directory, dir_name=dir_parent_final, user=user.id)
                save_file.parent_dir_id = dir_parent_id
                save_file.save()
                return redirect('nested', username, dir_parent_final)
            else:
                save_file.save()
                context['title'] = "Congratulations!"
                context['message'] = f"File {final_file_name} has been uploaded successfully"
                context['is_success'] = 1
                return redirect('main', username)

        else:
            form = UploadFile()
            return HttpResponse('spo bon')


def change_name(request, username):
    user = request.user
    if request.POST:
        directories = Directory.objects.filter(user=user)
        files = File.objects.filter(user=user)
        for directory in directories:
            if request.POST.get('d' + str(directory.id)):
                if request.POST.get('d' + str(directory.id)) != directory.dir_name:
                    if not Directory.objects.filter(dir_name=request.POST.get('d' + str(directory.id)), user=user):
                        directory.dir_name = request.POST.get('d' + str(directory.id))
                        directory.save()
        for file in files:
            if request.POST.get('f' + str(file.id)):
                if request.POST.get('f' + str(file.id)) != file.file_name:
                    file_name = request.POST.get('f' + str(file.id))
                    final_file_name = file_name
                    i = 1
                    while File.objects.filter(file_name=final_file_name, user=user).exists():
                        final_file_name = file_name + '(' + str(i) + ')'
                        i = i + 1
                    file.file_name = final_file_name
                    file.save()
        return redirect('main', username)
    return redirect('main', username)

from django.shortcuts import render, redirect, get_object_or_404, Http404
from .forms import UpdateUserForm, UploadFile
from accounts.models import User
from .models import Directory, File, SharedFile
from django.http import HttpResponse, JsonResponse, FileResponse
from itertools import chain
import os
from django.db.models import Q, Value, IntegerField
from django.conf import settings
from urllib import parse

regex = "^[^\s/\:\"&<>|.]+(\s[^\s/\:\"&<>|.]+)*$"


def main(request, username):
    user = request.user
    context = {}
    if not user.is_authenticated or not username == user.username:
        raise Http404

    directories = Directory.objects.filter(parent_dir_id__isnull=True, user=user, is_deleted=False, is_active=True)
    files = File.objects.filter(parent_dir_id__isnull=True, user=user, is_deleted=False, is_active=True)
    directories_files = list(chain(directories, files))
    directories_files.sort(key=lambda x: x.date_created)

    if not directories_files:
        context['empty'] = 'No directories or files found in your account.'

    if request.GET.get('file_name'):
        file_name = request.GET.get('file_name')
        searched_files = File.objects.filter(user=user, file_name__icontains=file_name, is_deleted=False,
                                             is_active=True).order_by(
            'date_created')
        directories_files = searched_files
        if not searched_files:
            context['empty'] = f'There were no results matching your search: "{file_name}".'

    context['files'] = directories_files
    context['user_url'] = request.build_absolute_uri()
    context['all_directories'] = Directory.objects.filter(user=user, is_deleted=False, is_active=True).values('parent_dir_id')
    context['directories'] = Directory.objects.filter(user=user, is_deleted=False, is_active=True).values('dir_name')
    context['all_files'] = File.objects.filter(user=user).values('parent_dir_id')

    return render(request, 'content/main_logic.html', context)


def nested(request, dir_name, username):
    context = {}
    user = request.user
    if not user.is_authenticated or not username == user.username:
        raise Http404

    parent_id = get_object_or_404(Directory, dir_name=dir_name, user=user, is_deleted=False, is_active=True)
    directories = Directory.objects.filter(parent_dir_id=parent_id.id, user=user, is_deleted=False, is_active=True)
    files = File.objects.filter(parent_dir_id=parent_id, user=user, is_deleted=False, is_active=True)
    directories_files = list(chain(directories, files))
    directories_files.sort(key=lambda x: x.date_created)

    if request.GET.get('file_name'):
        file_name = request.GET.get('file_name')
        searched_files = File.objects.filter(user=user, file_name__icontains=file_name, is_deleted=False, is_active=True).order_by(
            'date_created')
        directories_files = searched_files
        if not searched_files:
            context['empty'] = f'There were no results matching your search: "{file_name}".'

    context['files'] = directories_files
    context['directories'] = Directory.objects.filter(user=user, is_deleted=False, is_active=True).exclude(id=parent_id.id)
    context['all_directories'] = Directory.objects.filter(user=user, is_deleted=False, is_active=True).values('parent_dir_id')
    context['nested'] = '1'

    return render(request, 'content/main_logic.html', context)


def user_settings(request, username):
    context = {}
    user = request.user
    if not user.is_authenticated or not username == user.username:
        raise Http404

    if request.POST:
        form = UpdateUserForm(request.POST, instance=user)

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
    user = request.user
    if not user.is_authenticated or not username == user.username:
        raise Http404

    if request.POST:
        user.delete()
        return redirect('dashboard')

    return render(request, 'delete_user.html')


def deactivate_user(request, username):
    user = request.user
    if not user.is_authenticated or not username == user.username:
        raise Http404

    if request.POST:
        user.is_active = 0
        user.save()
        return redirect('dashboard')

    return render(request, 'deactivate_user.html')


def create_directory(request, username):
    context = {}
    user = request.user
    if not user.is_authenticated or not username == user.username:
        raise Http404

    if request.is_ajax and request.POST:
        dir_name = request.POST['dir_name']
        dir_path = parse.unquote(request.POST['url'])

        if 'file' in dir_path:
            dir_list = dir_path.split('/')
            dir_parent = dir_list[-2]
            dir_parent_id = get_object_or_404(Directory, dir_name=dir_parent, user=user)
        else:
            dir_parent_id = None

        if re.match(regex, dir_name):
            static_dir_name = dir_name
            i = 1
            while Directory.objects.filter(dir_name=dir_name, user=user):
                dir_name = static_dir_name + '(' + str(i) + ')'
                i = i + 1

            context['title'] = 'Congratulations!'
            context['is_success'] = True
            context['message'] = f'Directory " {dir_name} " has been successfully created.'

            Directory.objects.create(
                parent_dir_id=dir_parent_id,
                dir_name=dir_name,
                user=user
            )
        else:
            context['is_success'] = False
            context['title'] = 'We are sorry!'
            context['message'] = f'Directory " {dir_name} " has not been created. ' \
                                 f'Please use a correct and unique name.'

        return JsonResponse(context)
    raise Http404


def upload_file(request, username):
    user = request.user
    if not user.is_authenticated or not username == user.username:
        raise Http404

    if request.POST:
        form = UploadFile(request.POST, request.FILES)
        url = parse.unquote(request.POST['url'])

        if form.is_valid():
            save_file = form.save(commit=False)
            file = request.FILES['file']

            file_name = os.path.splitext(file.name)[0]
            file_type = os.path.splitext(file.name)[1]
            file_type = file_type.replace('.', '')

            if "'" in file_name:
                file_name = file_name.replace("'", "")

            if not re.match(regex, file_name):
                file_name = 'Please Change File Name'

            final_file_name = file_name
            i = 1
            while File.objects.filter(file_name=final_file_name, type=file_type, user=user):
                final_file_name = file_name + '(' + str(i) + ')'
                i = i + 1

            save_file.file_name = final_file_name
            save_file.user = user

            if 'file' in url:
                url_list = url.split('/')
                dir_parent = url_list[-2]
                dir_parent_object = get_object_or_404(Directory, dir_name=dir_parent, user=user, is_deleted=False, is_active=True)
                save_file.parent_dir_id = dir_parent_object
                save_file.save()
                return redirect('nested', username, dir_parent)
            else:
                save_file.save()
                return redirect('main', username)

        else:
            form = UploadFile()

        if 'file' in url:
            return redirect('nested', username)

        return redirect('main', username)
    raise Http404


def change_name(request, username):
    user = request.user
    if not user.is_authenticated or not username == user.username:
        raise Http404

    if request.POST:
        directories = Directory.objects.filter(user=user, is_deleted=False, is_active=True)
        files = File.objects.filter(user=user, is_deleted=False, is_active=True)

        for directory in directories:
            posted_directory_name = request.POST.get('d' + str(directory.id))
            print(posted_directory_name)
            if posted_directory_name:

                if posted_directory_name != directory.dir_name:
                    if re.match(regex, posted_directory_name):
                        i = 1
                        while Directory.objects.filter(dir_name=posted_directory_name, user=user):
                            posted_directory_name = request.POST.get('d' + str(directory.id)) + '(' + str(i) + ')'
                            i = i + 1
                        directory.dir_name = posted_directory_name
                        directory.save()

        for file in files:
            posted_file_name = request.POST.get('f' + str(file.id))

            if posted_file_name:

                if posted_file_name != file.file_name:
                    if re.match(regex, posted_file_name):
                        i = 1
                        while File.objects.filter(file_name=posted_file_name, user=user):
                            posted_file_name = request.POST.get('f' + str(file.id)) + '(' + str(i) + ')'
                            i = i + 1
                        file.file_name = posted_file_name
                        file.save()

        url = parse.unquote(request.POST.get('url'))
        if 'file' in url:
            url_list = url.split('/')
            dir_parent = url_list[-2]
            return redirect('nested', username, dir_parent)

        return redirect('main', username)
    raise Http404


def delete_file(request, username):
    user = request.user
    if not user.is_authenticated or not username == user.username:
        raise Http404

    if request.POST:
        directories = Directory.objects.filter(user=user, is_deleted=False)
        files = File.objects.filter(user=user, is_deleted=False)
        for directory in directories:
            if request.POST.get('dc' + str(directory.id)):
                if request.POST.get('dc' + str(directory.id)) == 'checked':
                    directory.is_deleted = True
                    children = directory.get_all_children()
                    for child in children:
                        child.is_active = False
                        child.save()
                    directory.save()
        for file in files:
            if request.POST.get('fc' + str(file.id)):
                if request.POST.get('fc' + str(file.id)) == 'checked':
                    file.is_deleted = True
                    file.is_active = False
                    file.save()

        url = parse.unquote(request.POST.get('url'))
        if 'file' in url:
            url_list = url.split('/')
            dir_parent = url_list[-2]
            return redirect('nested', username, dir_parent)

        return redirect('main', username)
    raise Http404


def recycle_bin(request, username):
    context = {}
    user = request.user
    if not user.is_authenticated or not username == user.username:
        raise Http404

    directories = Directory.objects.filter(user=user, is_deleted=True)
    files = File.objects.filter(user=user, is_deleted=True)
    directories = directories.annotate(count_files=Value(0, IntegerField()))
    directories = directories.annotate(count_directories=Value(0, IntegerField()))

    for directory in directories:
        children = directory.get_all_children()
        directories_num = 0
        files_num = 0
        for child in children:
            if child.type == 'directory':
                directories_num += 1
            else:
                files_num += 1
        directory.count_directories = directories_num - 1
        directory.count_files = files_num

    directories_files = list(chain(directories, files))
    directories_files.sort(key=lambda x: x.date_updated)
    all_directories = Directory.objects.filter(user=user, is_deleted=True).count()
    all_files = File.objects.filter(user=user, is_deleted=True).count()

    context['all_deleted_directories'] = all_directories
    context['all_deleted_files'] = all_files
    context['files'] = directories_files
    return render(request, 'recycle_bin/recycle_bin.html', context)


def empty_recycle_bin(request, username):
    user = request.user
    if not user.is_authenticated or not username == user.username:
        raise Http404

    Directory.objects.filter(is_deleted=True, user=user).delete()
    File.objects.filter(is_deleted=True, user=user).delete()

    return redirect('recycle_bin', username)


def restore_all(request, username):
    user = request.user
    if not user.is_authenticated or user.username != username:
        raise Http404

    Directory.objects.filter(Q(user=user) & (Q(is_deleted=True) | Q(is_active=False))).update(is_deleted=False,
                                                                                              is_active=True)

    File.objects.filter(Q(user=user) & (Q(is_deleted=True) | Q(is_active=False))).update(is_deleted=False,
                                                                                         is_active=True)

    return redirect('recycle_bin', username)


def restore_selected(request, username):
    user = request.user
    if not user.is_authenticated or user.username != username:
        raise Http404

    if request.POST:
        directories = Directory.objects.filter(user=user, is_deleted=True)
        files = File.objects.filter(user=user, is_deleted=True)
        for directory in directories:
            if request.POST.get('dc' + str(directory.id)):
                if request.POST.get('dc' + str(directory.id)) == 'checked':
                    directory.is_deleted = False
                    children = directory.get_all_children()
                    for child in children:
                        child.is_active = True
                        child.save()
                    directory.save()
        for file in files:
            if request.POST.get('fc' + str(file.id)):
                if request.POST.get('fc' + str(file.id)) == 'checked':
                    file.is_deleted = False
                    file.is_active = True
                    file.save()
    return redirect('recycle_bin', username)


def permanently_delete_selected(request, username):
    user = request.user
    if not user.is_authenticated or user.username != username:
        raise Http404

    if request.POST:
        directories = Directory.objects.filter(user=user, is_deleted=True)
        files = File.objects.filter(user=user, is_deleted=True)
        for directory in directories:
            if request.POST.get('dc' + str(directory.id)):
                if request.POST.get('dc' + str(directory.id)) == 'checked':
                    directory.delete()
        for file in files:
            if request.POST.get('fc' + str(file.id)):
                if request.POST.get('fc' + str(file.id)) == 'checked':
                    file.delete()
    return redirect('recycle_bin', username)


def share_file(request, username):
    context = {}
    user = request.user
    if not user.is_authenticated or user.username != username:
        raise Http404

    if request.is_ajax and request.POST:
        file_name = request.POST['file_name']
        share_with = request.POST['share_with']
        shared_from = user

        if File.objects.filter(user=user, is_deleted=False, is_active=True, file_name=file_name):
            file = File.objects.get(user=user, is_deleted=False, is_active=True, file_name=file_name)

            if User.objects.filter(email=share_with):
                if not user.email == share_with:
                    shared_to = get_object_or_404(User, email=share_with)
                    if not SharedFile.objects.filter(shared_file=file, shared_to=shared_to):
                        SharedFile.objects.create(
                            shared_file=file,
                            shared_from=shared_from,
                            shared_to=shared_to
                        )
                        context['title'] = 'Congratulations!'
                        context['is_success'] = True
                        context['message'] = f'File "{file_name}" has been shared with "{share_with}"'
                    else:
                        context['title'] = 'We are sorry!'
                        context['is_success'] = False
                        context['message'] = f'File "{file_name}" has already been shared with "{share_with}".'
                else:
                    context['title'] = 'We are sorry!'
                    context['is_success'] = False
                    context['message'] = f'File "{file_name}" can not be shared with yourself.'
            else:
                context['title'] = 'We are sorry!'
                context['is_success'] = False
                context['message'] = f'User "{share_with}" does not exist.'

        else:
            context['title'] = 'We are sorry!'
            context['is_success'] = False
            context['message'] = f'File "{file_name}" does not exist.'
        return JsonResponse(context)


def shared_files(request, username):
    context = {}
    user = request.user
    if not user.is_authenticated or user.username != username:
        raise Http404

    shared_to = SharedFile.objects.filter(shared_to=user).order_by('date_created')
    shared_from = SharedFile.objects.filter(shared_from=user).order_by('date_created')

    if request.GET.get('file_name'):
        file_name = request.GET.get('file_name')
        searched_files_to = SharedFile.objects.filter(shared_to=user,
                                                      shared_file__file_name__icontains=file_name).order_by('date_created')
        searched_files_from = SharedFile.objects.filter(shared_from=user,
                                                        shared_file__file_name__icontains=file_name).order_by('date_created')
        shared_to = searched_files_to
        shared_from = searched_files_from
        if not searched_files_to:
            context['empty_to'] = f'There were no results matching your search: "{file_name}".'
        if not searched_files_from:
            context['empty_from'] = f'There were no results matching your search: "{file_name}".'

    context['shared_to'] = shared_to
    context['shared_from'] = shared_from
    return render(request, 'share_file/share_file.html', context)


def move_to(request, username):
    user = request.user
    if not user.is_authenticated or user.username != username:
        raise Http404

    if request.POST:
        directories = Directory.objects.filter(user=user, is_deleted=False, is_active=True)
        files = File.objects.filter(user=user, is_deleted=False, is_active=True)
        parent_dir = request.POST.get('move_to_select')
        if parent_dir == '!none':
            parent_dir = None
        else:
            parent_dir = Directory.objects.get(user=user, dir_name=parent_dir)

        for directory in directories:
            if request.POST.get('dc' + str(directory.id)):

                if request.POST.get('dc' + str(directory.id)) == 'checked':
                    children = directory.get_all_children()
                    children_list = []
                    for child in children:
                        if child.type == 'directory':
                            children_list.append(child.dir_name)

                    if request.POST.get('move_to_select') not in children_list:
                        directory.parent_dir_id = parent_dir
                        directory.save()

        for file in files:
            if request.POST.get('fc' + str(file.id)):

                if request.POST.get('fc' + str(file.id)) == 'checked':
                    file.parent_dir_id = parent_dir
                    file.save()

        url = parse.unquote(request.POST.get('url'))
        if 'file' in url:
            url_list = url.split('/')
            dir_parent = url_list[-2]
            return redirect('nested', username, dir_parent)

    return redirect('main', username)


def unshare_selected(request, username):
    user = request.user
    if not user.is_authenticated or user.username != username:
        raise Http404

    if request.POST:
        shared_to = SharedFile.objects.filter(shared_to=user)
        shared_from = SharedFile.objects.filter(shared_from=user)
        for file in shared_to:
            if request.POST.get('tfc' + str(file.id)):

                if request.POST.get('tfc' + str(file.id)) == 'checked':
                    file.delete()

        for file in shared_from:
            if request.POST.get('ffc' + str(file.id)):

                if request.POST.get('ffc' + str(file.id)) == 'checked':
                    file.delete()

    return redirect('shared_files', username)


def unshare_to(request, username):
    user = request.user
    if not user.is_authenticated or user.username != username:
        raise Http404

    SharedFile.objects.filter(shared_to=user).delete()

    return redirect('shared_files', username)


def unshare_from(request, username):
    user = request.user
    if not user.is_authenticated or user.username != username:
        raise Http404

    SharedFile.objects.filter(shared_from=user).delete()

    return redirect('shared_files', username)


def unshare_all(request, username):
    user = request.user
    if not user.is_authenticated or user.username != username:
        raise Http404

    SharedFile.objects.filter(shared_to=user).delete()
    SharedFile.objects.filter(shared_from=user).delete()

    return redirect('shared_files', username)


def download(request, file_path):
    user = request.user
    if not user.is_authenticated:
        raise Http404

    file = get_object_or_404(File, file=file_path, is_deleted=False, is_active=True)
    shared_to = SharedFile.objects.filter(shared_file=file, shared_to=user)

    if file.user != request.user and not shared_to:
        raise Http404

    absolute_path = '{}/{}'.format(settings.MEDIA_ROOT, file_path)
    response = FileResponse(open(absolute_path, 'rb'), as_attachment=True)
    return response


def view(request, file_path):
    context = {}
    user = request.user
    if not user.is_authenticated:
        raise Http404

    file = get_object_or_404(File, file=file_path, is_deleted=False, is_active=True)
    shared_to = SharedFile.objects.filter(shared_file=file, shared_to=user)

    if file.user != request.user and not shared_to:
        raise Http404

    if file.type == 'word':
        context['file'] = file
        context['absolute_path'] = '{}/{}'.format(settings.MEDIA_ROOT, file_path)
        return render(request, 'content/snippets/word.html', context)

    absolute_path = '{}/{}'.format(settings.MEDIA_ROOT, file_path)
    response = FileResponse(open(absolute_path, 'rb'))
    return response

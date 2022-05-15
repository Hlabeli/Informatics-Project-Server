from datetime import datetime
import json
from re import T
from django.shortcuts import HttpResponse


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Project, Comment, Category
from .forms import CommentForm, ProjectForm, ProjectCoverImageForm

from django.core.paginator import Paginator
from django.contrib.auth.models import User


'''
Method to retrieves all projects and categories from the db and 
sends it to the template i.e. index.html
'''

def index(request):

    try:
        projects = Project.objects.all().order_by('-created_at', )
        categories = Category.objects.all()

        paginator = Paginator(projects, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Get the number of projects per category
        categories_list = []
        for cat in categories:
            a = Project.objects.filter(category=cat)
            categories_list.append({
                "category":cat,
                "number": len(a)
            })

        data = {
            "projects": page_obj,  # projects,
            "page_obj": page_obj,
            "category_list": {
                "data": categories_list,
                "all": len(projects)
            },
            "featured": projects.first
        }

        return render(request, 'projects/index.html', data)
    except Exception as exc:
        print(exc)
        messages.error(request, "Error fetching list of projects.")
        return render(request, 'projects/index.html', {})


'''
Method to retrieves all projects (by category) and categories from the db and 
sends it to the template i.e. index.html
'''

def get_projects_by_category(request, category):

    try:
        # Get the category
        category = Category.objects.get(category=category)
        # get projects matching the category

        projects = Project.objects.filter(category=category).order_by('-created_at', )
        categories = Category.objects.all()

        #Get all Project and retrieve only the latest to be used as featured Project in template
        all_projects = Project.objects.all().order_by('-created_at', )

        # Get the number of projects per category
        categories_list = []
        for cat in categories:
            a = Project.objects.filter(category=cat)
            categories_list.append({
                "category": cat,
                "number": len(a)
            })

        if projects:
            paginator = Paginator(projects, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            data = {
                "projects": page_obj,  # projects,
                "page_obj": page_obj,
                "category_list": {
                    "data": categories_list,
                    "all": len(Project.objects.all())
                },
                "featured": all_projects.first

            }

            return render(request, 'projects/index.html', data)
        else:

            data = {
                "category_list": {
                    "data": categories_list,
                    "all": len(all_projects)
                },
                "error": True,
                "featured": all_projects.first
            }

            messages.info(request, "No projects found for the selected categories")
            return render(request, 'projects/index.html', data)


    except Exception as exc:
        print(exc)
        messages.error(request, "projects not found for the selected category")
        return render(request, 'projects/index.html', {"error": True})


'''
Method to retrieves all projects (for logged user) 
sends it to the template i.e. index.html
'''

def get_user_projects(request, username):

    try:
        # Get the category
        user = User.objects.get(username=username)
        # get projects matching the category

        projects = Project.objects.filter(created_by=user).order_by('-created_at', )
        # Get all Project and retrieve only the latest to be used as featured Project in template
        all_projects = Project.objects.all().order_by('-created_at', )

        categories = Category.objects.all()

        # Get the number of projects per category
        categories_list = []
        for cat in categories:
            a = Project.objects.filter(category=cat)
            categories_list.append({
                "category": cat,
                "number": len(a)
            })

        if projects:
            paginator = Paginator(projects, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            data = {
                "projects": page_obj,  # projects,
                "page_obj": page_obj,
                "category_list": {
                    "data": categories_list,
                    "all": len(Project.objects.all())
                },
                "featured": all_projects.first

            }

            return render(request, 'projects/index.html', data)
        else:
            data = {
                "category_list": {
                    "data": categories_list,
                    "all": len(all_projects)
                },
                "error": True,
                "featured": all_projects.first
            }

            messages.info(request, "User has not published any Project!")
            return render(request, 'projects/index.html', data)


    except Exception as exc:
        messages.error(request, "Error fetching your created projects")
        return render(request, 'projects/index.html', {"error": True})


'''
1) This methods retrieves an project with slug matching the 'projects_slug' argument. 
2) The method also retrieves the list of comments for an Project.
3) Sends comment forms to template
'''

def get_project(request, project_slug):
    try:
        # Create comment form
        add_comment_form = CommentForm()

        project_cover_image_form = ProjectCoverImageForm()

        selected_project = Project.objects.get(slug=project_slug)
        comments = Comment.objects.filter(project=selected_project).order_by('-created_at',)

        paginator = Paginator(comments, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, 'projects/project.html', {
            "title": selected_project.title,
            "subtitle": selected_project.subtitle,
            "content": selected_project.content,
            "slug": selected_project.slug,
            "created_by": selected_project.created_by,
            "created_at": selected_project.created_at,
            "updated_at": selected_project.updated_at,
            "project_found" : True,
            "cover_image" : selected_project.cover_image,
            "comments" : comments,
            "page_obj": page_obj,
            "category" : selected_project.category,
            "add_comment_form": add_comment_form,
            "categories": Category.objects.all(),
            "form": project_cover_image_form
        })

    except Exception as exc:
        print(exc)
        return render(request, 'projects/project.html', {
            "project_found" : False
        })


'''
Method to display add Project form i.e. GET
Save Project => POST
'''

@login_required(login_url='signin')
def add_project(request):

    if request.method == 'GET':
        # Create Project form
        project_form = ProjectForm(initial={'category': '1'})
        return render(request, 'projects/add.html', {"form": project_form, 'is_error': False})

    elif request.method == 'POST':
        try:
            project_form = ProjectForm(request.POST, request.FILES)
            if project_form.is_valid():
                project = project_form.save(commit=False)
                project.created_by = request.user
                project.slug = slugify(project.title)
                project.save()

                # Be nice - sent a flash message :)
                messages.success(request, 'Your project is now Live!')
                return redirect('get-project', project_slug=project.slug)

            else:
                # Create Project form
                project_form = ProjectForm(initial={'category': '1'})
                return render(request, 'projects/add.html', {"form": project_form, 'is_error': True})

        except Exception as exc:
            print("printing...")
            print(exc)
            # Create Project form
            project_form = ProjectForm(initial={'category': '1'})
            return render(request, 'projects/add.html', {"form": project_form, 'is_error': True})
    else:
        print("Unknown")


'''
Edit Project method. 
Check if user is authenticated
'''

@login_required(login_url='signin')
def edit_project(request, project_slug):
    if request.user.is_authenticated:
        # ajax PUT request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "PUT":
            # Get the comment from request.body
            title = json.loads(request.body)["title"]
            subtitle = json.loads(request.body)["subtitle"]
            content = json.loads(request.body)["content"]
            category_id = json.loads(request.body)["category"]

            try:
                # Get Project
                project = Project.objects.get(slug=project_slug)
                category = Category.objects.get(pk=category_id)
                project.title = title
                project.subtitle = subtitle
                project.content = content
                project.category = category
                project.save()

                # send to client side.
                return JsonResponse({"updated_at": project.updated_at}, status=200)

            except Exception as exc:
                return JsonResponse({"error": "Unable to update project. Please try again later"}, status=400)

        elif request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "GET":
            try:
                # Get Project and comment
                project = Project.objects.get(slug=project_slug)
                # send to client side.
                return JsonResponse({"title": project.title, "subtitle": project.subtitle, "content" : project.content}, status=200)

            except Exception as exc:
                return JsonResponse({"error": "Unable to cancel edit project. Please try again later"}, status=400)
        else:
            # some error occured
            return JsonResponse({"error": "Unknown request error!"}, status=400)
    else:
        messages.info(request, 'You are not signed in. Please Sign in to continue!')
        return redirect('signin')

@login_required(login_url='signin')
def update_project_image(request, project_slug):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
            try:
                project = Project.objects.get(slug=project_slug)
                form = ProjectCoverImageForm(request.POST, request.FILES, instance=project)
                if form.is_valid():
                    form.save()
                    #ser_instance = serializers.serialize('json', [project, ])
                    return JsonResponse({"photo": project.cover_image.url}, status=200)
                else:
                    return JsonResponse({"error": "Unable to update image. Please try again later."}, status=400)
            except Exception as exc:
                print(exc)
                return JsonResponse({"error": "Unable to update image. Please try again later."}, status=400)
        else:
            return JsonResponse({"error": "Unknown request error!"}, status=400)

    else:
        messages.info(request, 'You are not signed in. Please Sign in to continue!')
        return redirect('signin')



'''
This method will add comment into the database and send out list of comments (Http response) for updating the Project view.
It will use an ajax request as I do not want to reload the page each time a user adds comment
'''

@login_required(login_url='signin')
def add_comment(request, project_slug, username):
    if request.accepts and request.method == "POST":
        if request.user.is_authenticated:
            # Get form data
            comment_form = CommentForm(request.POST)

            # get Project object from slug
            project = Project.objects.get(slug=project_slug)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)

                user = User.objects.get(username=username)
                comment.created_by = user
                comment.project = project
                comment.save()

                # serialize in new comment object in json
                ser_instance = serializers.serialize('json', [comment, ])
                full_name = comment.created_by.first_name + " " + comment.created_by.last_name
                username = comment.created_by.username

                data = {
                    "name": full_name,
                    "username": username,
                }

                # send to client side.
                return JsonResponse({"comment": ser_instance, "id": comment.comment_id, "user": json.dumps(data)},
                                    status=200)
            else:
                # Form is invalid.
                print("Form is Invalid")
                return JsonResponse({"error": comment_form.errors}, status=400)
        else:
            messages.info(request, 'You are not signed in. Please Sign in to continue!')
            return redirect('signin')
    else:
        return JsonResponse({"error": "Unknown request"}, status=400)

'''
Function to Edit comment
'''
@login_required(login_url='signin')
def edit_comment(request, comment_id):
    # ajax PUT request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "PUT":
        # Get the comment from request.body
        comment_from_ajax = json.loads(request.body)["comment"]

        try:
            # Get Project and comment
            comment = Comment.objects.get(pk=comment_id)
            comment.comment = comment_from_ajax
            comment.save()

            # send to client side.
            return JsonResponse({"updated_at": comment.updated_at}, status=200)

        except Exception as exc:
            return JsonResponse({"error": "Unable to update comment. Please try again later"}, status=400)

    elif request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "GET":
        try:
            # Get Project and comment
            comment = Comment.objects.get(pk=comment_id)
            # send to client side.
            return JsonResponse({"comment": comment.comment}, status=200)

        except Exception as exc:
            return JsonResponse({"error": "Unable to cancel edit comment. Please try again later"}, status=400)
    else:
        # some error occured
        return JsonResponse({"error": "Unknown request"}, status=400)


@login_required(login_url='signin')
def delete_comment(request, comment_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "DELETE":
        print("comment id is: " + str(comment_id))
        try:
            # Get Project and comment
            comment = Comment.objects.get(pk=comment_id)
            comment.delete()
            return JsonResponse({"message": "deleted"}, status=200)
        except Exception as exc:
            print(exc)
            return JsonResponse({"error": "Could not remove comment. Please try again later!"}, status=400)
    else:
        return JsonResponse({"error": "Unknown request"}, status=400)

from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.index, name='all-projects'), # e.g. localhost:8000/projects
    path('projects/add/', views.add_project, name='add-project'),
    path('projects/<category>/', views.get_projects_by_category, name="get-projects-by-cat"),
    path('projects/user/<username>/', views.get_user_projects, name="get-user-projects"),
    path('projects/get/<slug:project_slug>/', views.get_project, name='get-project'),

    path('ajax/update/image/<slug:project_slug>', views.update_project_image, name='update-project-image'),
    path('ajax/edit/project/<slug:project_slug>/', views.edit_project, name='edit-project'),
    path('ajax/edit/comment/edit/<int:comment_id>/', views.edit_comment, name='edit-comment'),
    path('ajax/add/comment/<slug:project_slug>/<username>', views.add_comment, name="add-comment"),
    path('ajax/delete/comment/<int:comment_id>/', views.delete_comment, name='delete-comment'),
]
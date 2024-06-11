from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import (send_mail, EmailMultiAlternatives)
from django.template.loader import get_template
from django.contrib.auth.models import Group, User
from django.http import Http404

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response


from .forms import UserRegisterForm
from .permissions import (
    IsAuthor, 
    IsCustomer, 
    IsManager, 
    IsModerator, 
    get_user, 
    has_group,
)

# Create your views here.
group_url_to_group = {
    'manager': Group.objects.get(name="Manager"),
    'author': Group.objects.get(name="Author"),
    'moderator': Group.objects.get(name="Moderator")
}
def index_view(request):
    return render(request, 'user/index.html', {'title': 'index'})

def register_view(request):
    if request.method == 'POST':
        title = "Register"
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # mail system
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            htmly = get_template('user/email.html')
            d = { 'username': username}

            subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, f'Your account has been created! You are now able to log in')

            # password setting
            user = form.save(commit=False)
            password = form.cleaned_data.get['password']
            user.set_password(password)
            user.save()

            new_user = authenticate(username=user.username, password=password)

            login(request, new_user)

    else:
        form = UserRegisterForm()        
    
    return render(request, 'user/register.html', {'title': "Register", 'form': form})

def login_view(request):
    title = "Login"
    form = AuthenticationForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get['username']
        password = form.cleaned_data.get['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f'Welcome {username}!!')
            return redirect('index')
        else:
            messages.info(request, f'account does not exist, Sign in')

    context = {
        'title': title,
        'form': form
    }
    return render(request, 'user/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('api/')

class UserGroupView(ViewSet):
    permission_classes = [IsManager]

    def get_group(self, group: str) -> Group:
        group_result = group_url_to_group.get(group)
        if group_result is None:
            raise Http404(f"invalid group name: {group}")
        return group_result
    
    def create(self, request: Request, group: str) -> Response:
        try:
            username = request.data['username']
        except KeyError:
            return Response({'error': 'must provide a username'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, username=username)
        group_obj = self.get_group(group)
        group_obj.user_set.add(user)

        return Response({'success': f'{username} assigned to group {group_obj.name}'}, status=status.HTTP_201_CREATED)

    def remove(self, request: Request, group: str, pk: int) -> Response:
        user = get_object_or_404(User, pk=pk)
        group_obj = self.get_group(group)
        if not has_group(user, group_obj.name):
            return Response(
                {'errors': f'{user.username} does not belong to the {group_obj.name} group'},
                status=status.HTTP_400_BAD_REQUEST
            )
        group_obj.user_set.remove(user)
        return Response(
            {'success': f'{user.username} does not belong to the {group_obj.name} group'},
            status=status.HTTP_400_BAD_REQUEST
        )

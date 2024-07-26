# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, ProfileForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status



@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            return Response({'status':'Registration Successful'}, status=status.HTTP_201_CREATED)  # Redirect to a success page

    # else:
    #     user_form = UserRegistrationForm()
    #     profile_form = ProfileForm()

    # return render(request, 'user/templates/register.html', {
    #     'user_form': user_form,
    #     'profile_form': profile_form,
    # })

    return Response({
        'user_form_errors': user_form.errors,
        'profile_form_errors': profile_form.errors
    }, status=status.HTTP_400_BAD_REQUEST)

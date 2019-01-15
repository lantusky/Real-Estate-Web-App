from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

def register(request):
  if request.method == 'POST':
    # get form values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # check password match
    if password == password2:
      print('in')
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return redirect('register')
      if User.objects.filter(email=email).exists():
        messages.error(request, 'That email is taken')
        return redirect('register')
      
      # create account
      user = User.objects.create_user(username=username, email=email, password=password, 
      first_name=first_name, last_name=last_name)
      # auto login after register
      # auth.login(request, user)
      # messages.success(request, 'You are now logged in')
      # redirect('index')

      # manual login required
      user.save()
      messages.success(request, 'You are now registered and you can log in!')
      return redirect('login')

    else:
      messages.error(request, 'Password do not match')
      return redirect('register')
  else:
    return render(request, 'accounts/register.html')

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user:
      auth.login(request, user)
      messages.success(request, 'You are now logged in!')
      return redirect('dashboard')
    else:
      messages.error(request, 'invalid credentials')
      return redirect('login')
  else:
    return render(request, 'accounts/login.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('index')

def dashboard(request):
  user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

  context = {
    'contacts': user_contacts
  }
  return render(request, 'accounts/dashboard.html', context)

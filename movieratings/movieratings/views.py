from django.shortcuts import render, redirect

from movieratings.forms import UserForm

def index(request):
    return render(request, 'index.html')

def registration(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user.form.save()
            password = user.password

            user.set_password(password)
            user.save()


            user = authenticate(username=user.username, password=password)

            login(request, user)
            return redirect('ratings:rater-detail', rater_id=user.rater.id)

    else:
        form = UserForm()

    return render(request, 'registration/register.html', {'form': form})

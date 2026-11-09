from .models import Referee
from django import forms

class RefereeForm(forms.ModelForm):
    class Meta:
        model = Referee
        fields = ['full_name', 'phone_number', 'level', 'bio', 'profile_photo']


@login_required
def become_referee(request):
    if hasattr(request.user, 'referee'):
        return redirect('home')

    if request.method == 'POST':
        form = RefereeForm(request.POST, request.FILES)
        if form.is_valid():
            referee = form.save(commit=False)
            referee.user = request.user
            referee.save()
            return redirect('home')
    else:
        form = RefereeForm()

    return render(request, 'players/become_referee.html', {'form': form})


def referee_list(request):
    referees = Referee.objects.all().order_by('full_name')
    return render(request, 'players/referee_list.html', {'referees': referees})
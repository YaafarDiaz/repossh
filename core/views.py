from django.shortcuts import render
def home(request):
    title = "Home"
    context = {
        'title': title,
    }
    return render(request, 'core/index.html', context)
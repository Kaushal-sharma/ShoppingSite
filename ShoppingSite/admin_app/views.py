from django.shortcuts import render

# Create your views here.
def dashboard(request):
    text = 'Hello Admin App'
    return render(request, 'admin_app/dashboard.html', {'data': text})

from django.shortcuts import render, redirect, get_list_or_404

# Create your views here.
def home(request):
    context = { 'username': 'Mike Zeno'}
    return render(request, 'trader/home.html', context)
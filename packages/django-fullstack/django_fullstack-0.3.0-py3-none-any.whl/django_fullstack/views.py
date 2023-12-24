from inertia import render

def welcome_page(request):
    packages = ["Django"]
    return render(request, "index", {"packages": packages})

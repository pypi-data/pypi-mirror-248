from inertia import render

def welcome_page(request):
    packages = ["Django", "Inertia.js", "Vite.js"]
    return render(request, "index", {"packages": packages})

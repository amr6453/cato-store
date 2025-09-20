from django.shortcuts import render


def index(request):
    """Static index page — no database access."""
    context = {
        'title': 'Cato Store',
        'message': 'Welcome to the placeholder Cato Store home page.',
        'links': [
            {'url': '/', 'label': 'Home'},
            {'url': '/about/', 'label': 'About'},
            {'url': '/contact/', 'label': 'Contact'},
        ]
    }
    return render(request, 'store/index.html', context)


def about(request):
    """Simple about page."""
    return render(request, 'store/about.html', {'title': 'About Cato Store', 'message': 'This is a simple about page.'})


def contact(request):
    """Simple contact page."""
    return render(request, 'store/contact.html', {'title': 'Contact Cato Store', 'message': 'Contact us at contact@example.com'})

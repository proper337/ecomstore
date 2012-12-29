from  django.shortcuts import render_to_response

def home(request):
    """
    
    Arguments:
    - `request`:
    """
    return render_to_response("index.html")

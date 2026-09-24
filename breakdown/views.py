from django.shortcuts import redirect

def breakdown_redirect(request):
    return redirect('emergency:request_help')

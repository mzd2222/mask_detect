from django.shortcuts import render


# Create your views here.
def v_name(request, v_name):
    return render(request, 'video/video.html', {
        'v_name': v_name
    })

from django.shortcuts import render, redirect, get_object_or_404
from .models import Story
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.conf import settings

## from .forms import ContactForm

# Create your views heredef story(request):.
def story(request):

    print("Data : ", request , "-- End --")

    if request.method == "POST":
        if request.POST['recType'] == 'text':
            try:

                print("Text")

                subscriber_id = request.POST['subscriber_id']
                title = request.POST['title']
                content = request.POST['content']
                category = request.POST['category']
                is_anonymous_raw = request.POST.get('is_anonymous')
                is_anonymous = is_anonymous_raw == 'on'
                file_path = ''

                print(subscriber_id)
                print(title)
                print(content)
                print(category)
                print(is_anonymous)

                print("Before Insert Text Story")
                story = Story(user_id=subscriber_id, title=title, 
                                content=content, category=category, is_anonymous=is_anonymous,  
                                speech_url=file_path, is_published = False, creation_date=timezone.now() )

                story.save()
                print("After Insert Text Story")

                stories = Story.objects.order_by('-creation_date').filter(is_published=True)
                context = {"stories": stories}

                print (context['stories']);

                return render(request, "stories/story.html", context)

            except Exception as e:
                stories = Story.objects.order_by('-creation_date').filter(is_published=True)
                context = {"stories": stories}

                print (context['stories']);

                return render(request, "stories/story.html", context)
        else:
            try:

                print("Voice")

                subscriber_id = request.POST['subscriber_id']
                audio_file = request.FILES['audio_file']

                # Save file directly inside your media root directory
                file_path = default_storage.save(f'stories/{audio_file.name}', ContentFile(audio_file.read()))
                
                # If you use a Django model, you can alternatively do:
                # AudioModel.objects.create(file=audio_file)

                print("Before Insert Voice Story")
                story = Story(user_id=subscriber_id, speech_url=file_path, 
                            is_published = False, creation_date=timezone.now() )
                
                story.save()
                print("After Insert Voice Story")
                
                # # send mail - configure gmail
                ''' # send_mail(
                    "Clinic Inquiry",
                    "There has been an inquiry for " + listing + ". Sign into the admin panel for more info",
                    "hellowai2012@gmail.com",
                    [doctor_email],
                    fail_silently=False
                ) '''
                messages.success(request, "Your request hasb been submitted, a representative will get back to you soon")

                return JsonResponse({
                    'message': 'Upload success',
                    'file_path': file_path
                }, status=200)
                
            except Exception as e :
                print(e)
                return JsonResponse({'error': 'Invalid request handler method'}, status=400)

    #Handle non-Post method
    stories = Story.objects.order_by('-creation_date').filter(is_published=True)
    context = {"stories": stories}

    print (context['stories']);

    return render(request, "stories/story.html", context)

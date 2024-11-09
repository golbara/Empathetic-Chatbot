from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.http import require_POST

def index(request):
    template = loader.get_template("bot/index.html")
    # return HttpResponse(template)
    return render(request, "bot/index.html")

# def get_input(request):
#     if request.method == "POST":
#         user_message = request.POST.get("message")
#         # Process the message here (e.g., call your chatbot response function)
#         bot_response = "You said: " + user_message  # Placeholder for actual bot response logic
#         return JsonResponse({"response": bot_response})
#     return JsonResponse({"error": "Invalid request"}, status=400)

message_param = openapi.Parameter(
    'message', openapi.IN_FORM, description="User message", type=openapi.TYPE_STRING
)

# @swagger_auto_schema(method='post', manual_parameters=[message_param])
# @require_POST
@api_view(['POST'])
def get_input(request):
    print("Hiiiiiiiiiiii$$$$")
    if request.method == "POST":
        user_message = request.POST.get("message")
        # Process the message here (e.g., call your chatbot response function)
        bot_response = "You said: " + user_message  # Placeholder for actual bot response logic
        print("*******************************************")
        return JsonResponse({"response": bot_response})
    return JsonResponse({"error": "Invalid request"}, status=400)

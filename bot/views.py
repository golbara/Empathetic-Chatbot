from django.template import loader
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.http import require_POST
from openai import OpenAI
import streamlit as st    
import subprocess
from django.http import HttpResponse
from django.shortcuts import redirect
import os
def streamlit_view(request):
    # Get the current directory of this script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Path to the Streamlit script in the current directory
    streamlit_file = os.path.join(current_directory, "streamlit.py")
    # Start the Streamlit app as a subprocess
    subprocess.Popen(["streamlit", "run", streamlit_file])

    # Redirect to the default Streamlit URL
    return redirect("http://localhost:8501")


def index(request):
    # template = loader.get_template("bot/index.html")
    # # return HttpResponse(template)
    # return render(request, "bot/index.html")
    st.title("ChatGPT-like clone")

    #client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"],base_url="https://api.metisai.ir/api/v1/wrapper/{provider}")
    client = OpenAI(
        api_key="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")
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

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

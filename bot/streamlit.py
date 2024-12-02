from openai import OpenAI
import streamlit as st
import pandas as pd
from scipy.spatial.distance import cosine
import os
import json  # For serializing lists to a string
from datasets import load_from_disk

# st.title("Welcome! 😄")
# CSS for RTL and Persian font
st.markdown(
    """
    <style>
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazir-font/dist/font-face.css');
    .rtl-text {
        text-align: right;
        direction: rtl;
        font-family: 'Vazir', sans-serif;
        font-size: 1.1em;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
with st.container():
    # Display the message with RTL alignment
    st.markdown(
        f"""
        <div class="rtl-text">
            <h1> خوش آمدید !😄</h1> <br>

        </div>
        """,
        unsafe_allow_html=True,
    )

# Use the cached dataset
# Load dataset
@st.cache_data
def load_dataset():
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Path to the Streamlit script in the current directory
    data_path = os.path.join(current_directory, "data")
    # Load the dataset from the saved location
    return load_from_disk(data_path)


dataset = load_dataset()

def precision():
    return st.session_state.cliked/st.session_state.nreturned



def save_to_dataset(query, selected_messages, sorted_indices, filename="feedback_dataset.json"):
    # Get the current directory and file path
    current_directory = os.path.dirname(os.path.abspath(__file__))
    print(current_directory)
    file_path = os.path.join(current_directory, 'data',filename) 
    disliked_list = []
    liked_list = []
    if(len(st.session_state.liked) != 0):
        liked_list = [st.session_state.nearests[i]["Persian Messages"] for i in range(st.session_state.nreturned) if f"like_{i}"  in st.session_state.liked]
    if(len(st.session_state.disliked) == 0):
        disliked_list = [st.session_state.nearests[i]["Persian Messages"] for i in range(st.session_state.nreturned) if f"like_{i}" not in st.session_state.liked]
    else:
        disliked_list = [(st.session_state.nearests[int(key.split('_')[1])]["Persian Messages"]) for key in st.session_state.disliked]

    # Create a dictionary of data to save
    data = {
        "prompt": query,
        "liked": liked_list,  # Keep as list; JSON handles serialization
        "disliked": disliked_list,
        "MRR": st.session_state.mrr, 
        "precision": precision()
    }
    
    # Check if the file exists and save appropriately
    if not os.path.exists(file_path):
        # If the file doesn't exist, create a new JSON file and write the data
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump([data], file, ensure_ascii=False, indent=4)  # Create a list with the first entry
    else:
        # If the file exists, append the new data
        with open(file_path, "r+", encoding="utf-8") as file:
            existing_data = json.load(file)  # Load the existing JSON data
            existing_data.append(data)  # Append the new entry
            file.seek(0)  # Reset file pointer to the beginning
            json.dump(existing_data, file, ensure_ascii=False, indent=4)  # Write updated data




client = OpenAI(
    api_key="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")

if "nreturned" not in st.session_state:
    st.session_state.nreturned = 10


if "prompt" not in st.session_state:
    st.session_state.prompt = ""
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "embedding_model" not in st.session_state:
    st.session_state["embedding_model"] = "text-embedding-3-small"

if "cliked" not in st.session_state:
    st.session_state.cliked = 0

if "cdisliked" not in st.session_state:
    st.session_state.cdisliked = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

if "nearests" not in st.session_state:
    st.session_state.nearests = []

if "selected_messages" not in st.session_state:
    st.session_state.selected_messages = []

# if "sorted_indices" not in st.session_state:
#     st.session_state.sorted_indices = []
if "liked" not in st.session_state:
    st.session_state.liked = set()
if "disliked" not in st.session_state:
    st.session_state.disliked = set()

if "mrr" not in st.session_state:
    st.session_state.mrr = 0



def click_button(key_name, entry,rank):
    st.session_state.key_name = True
    st.session_state.cliked += 1
    if f"dislike_{rank}" in st.session_state.disliked:
        st.session_state.disliked.remove(f"dislike_{rank}")  # Remove from disliked
        st.session_state.cdisliked -= 1
    st.session_state.liked.add(key_name)
    st.session_state.selected_messages.append(entry["Persian Messages"])
    st.session_state.mrr += 1/(rank+1)
    print("**************************  ",st.session_state.mrr)

def click_disButton(key_name, entry,rank):
    st.session_state.key_name = True
    st.session_state.cdisliked += 1
    if f"like_{rank}" in st.session_state.liked:
        # Remove from liked
        st.session_state.liked.remove(f"like_{rank}")
        st.session_state.cliked -= 1
        st.session_state.selected_messages.remove(entry["Persian Messages"])
        # add to disliked
    st.session_state.disliked.add(key_name)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

################################################################################################## User prompt input ################################################################# 
if prompt := st.chat_input("چه خبر؟"):
    st.session_state.prompt = prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get embedding of the prompt
    query_embedding = client.embeddings.create(input=prompt, model=st.session_state.embedding_model).data[0].embedding

    # Find similarity distances
    # Compute cosine distances and store them in a separate list
    distances = [cosine(query_embedding, embedding) for embedding in dataset["embedding"]]

    # Pair each distance with its corresponding dataset row index
    distance_with_indices = list(enumerate(distances))

    # Sort the dataset indices based on cosine distances
    sorted_indices = sorted(distance_with_indices, key=lambda x: x[1])
    # st.session_state.sorted_indices = sorted_indices

    with st.container():
        # Display the message with RTL alignment
        st.markdown(
            f"""
            <div class="rtl-text">
                <strong> از بین موارد زیر،متن‌(های) مرتبط را لایک کنید.</strong> <br>
            </div>
            """,
            unsafe_allow_html=True,
        )
    # Display the top 5 sorted Persian messages
    for rank, (index, distance) in enumerate(sorted_indices[:st.session_state.nreturned]):
        # st.session_state.rank = rank
        print(f"rank: {rank}      index: {index}")
        entry = dataset[index]  # Access the dataset row using the index
        st.session_state.nearests.append(entry)
        with st.container():
            # Display the message with RTL alignment
            st.markdown(
                f"""
                <div class="rtl-text">
                    <strong>رتبه {rank + 1}:</strong> {entry['Persian Messages']} <br>
                    <em>فاصله:</em> {distance:.4f}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Create columns for Like/Dislike buttons
            col1, col2 = st.columns([1, 1])
            with col1:
                key_name = f"like_{rank}"
                st.button("👍", key=key_name,on_click=click_button,args=[key_name,entry,rank])

            with col2:
                key_name = f"dislike_{rank}"
                st.button("👎", key=key_name,on_click=click_disButton,args=[key_name,entry,rank])

    st.button("انتخاب کردم",key="done!")    
elif st.session_state.prompt!="" and st.session_state["done!"]: #################################################################### selecting is done ################################################################
    # generating
    ## Combine selected messages with user prompt
    with st.spinner("در حال تولید پاسخ..."):
        assistant_input = {
            "selected_messages": st.session_state.selected_messages,
            "prompt": st.session_state.prompt
        }

        # Pass selected messages and prompt to the assistant
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": "system", "content": f"Use the following selected messages to inform your response: {assistant_input['selected_messages']}"},
                    {"role": "user", "content": assistant_input["prompt"]}
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
        # Delete a single key-value pair
    # for message in st.session_state.selected_messages:
    #     print("***********************",message)
            # Save query, selected messages, and sorted messages
    save_to_dataset(
        st.session_state.prompt,
        st.session_state.selected_messages,
        # st.session_state.sorted_indices
        st.session_state.nearests
    )
    print("@@@@@@@@@@@@@@@@@@@@@@@  ",st.session_state.mrr,"@@@@@@@@@@@@@@@@@@@@@@@  ")
    print("@@@@@@@@@@@@@@@@@@@@@@@  ",st.session_state.cliked/st.session_state.nreturned,"@@@@@@@@@@@@@@@@@@@@@@@  ")

    del st.session_state.liked
    del st.session_state.disliked
    del st.session_state.cliked
    del st.session_state.cdisliked
    del st.session_state.selected_messages
    # del st.session_state.sorted_indices
    del st.session_state.mrr
    del st.session_state.nearests

elif st.session_state.prompt != "":##############################################################################################    selecting    ################################################################
   # Display the top 5 sorted Persian messages
    with st.container():
        # Display the message with RTL alignment
        st.markdown(
            f"""
            <div class="rtl-text">
                <strong> از بین موارد زیر،متن‌(های) مرتبط را لایک کنید.</strong> <br>
            </div>
            """,
            unsafe_allow_html=True,
        )
    for rank, entry in enumerate(st.session_state.nearests):
        # entry = dataset[index]  # Access the dataset row using the index
        with st.container():
            # Display the message with RTL alignment
            st.markdown(
                f"""
                <div class="rtl-text">
                    <strong>رتبه {rank + 1}:</strong> {entry['Persian Messages']} <br>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Create columns for Like/Dislike buttons
            col1, col2 = st.columns([1, 1])
            with col1:
                key_name = f"like_{rank}"
                # Allow users to select messages by clicking Like
                st.button("👍", key=key_name,on_click=click_button,args=[key_name,entry,rank],disabled= key_name in st.session_state.liked)

            with col2:
                key_name = f"dislike_{rank}"
                # Allow users to unselect messages by clicking Dislike
                st.button("👎", key=key_name,on_click=click_disButton,args=[key_name,entry,rank],disabled= key_name in st.session_state.disliked)         
    st.button("انتخاب کردم",key="done!")    

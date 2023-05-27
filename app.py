import streamlit as st
import os

from main import generate_answer, generate_summary, video_info, is_valid_openai_key, is_valid_youtube_url, get_video_duration, calculate_api_cost

st.set_page_config(page_title="GPTube", page_icon='🎥')

MIN_TIME = 4
MAX_TIME = 30


# App UI
def gptube_app():



    st.header("🎥 GPTube")

    st.markdown('#') 

    choice = st.radio("Please choose an option :", ('Generate Summary', 'Generate Answer to a Question'), horizontal=True)

    st.markdown('#') 

    # OPENAI API KEY
    st.markdown('#### 🔑 Step 1 : Enter Your OpenAI API Key') 
    openai_api_key = st.text_input("[Get Yours From the OPENAI Website](https://platform.openai.com/account/api-keys) : ", placeholder="sk-***********************************", type="password")
    
    # Disable YouTube URL field until OpenAI API key is valid
    if openai_api_key:
        st.markdown('#### 📹 Step 2 : Enter the YouTube Video URL')
        youtube_url = st.text_input("URL :", placeholder="https://www.youtube.com/watch?v=************")
    else:
        st.markdown('#### 📹 Step 2 : Enter the YouTube Video URL')
        youtube_url = st.text_input(
            "URL : ",
            placeholder="Please enter a valid OpenAI API key first",
            disabled=True
        )

    if is_valid_youtube_url(youtube_url):
        video_duration = get_video_duration(youtube_url)
        option = 'summary' if choice == 'Generate Summary' else 'answer'
        api_call_cost = calculate_api_cost(video_duration, option)

        if video_duration >= MIN_TIME and video_duration <= MAX_TIME:
            st.info(f"The duration of the video is {video_duration} minutes. This will cost you approximately ${api_call_cost}")
            
            thumbnail_url, video_title = video_info(youtube_url)
            st.markdown(f"#### {video_title}")
            st.image(f"{thumbnail_url}", use_column_width='always')
            
        else:
            st.warning(f"Please enter a youtube video that is {MIN_TIME} minutes long at minimum and {MAX_TIME} minutes at maximum.")
    else:
        st.error("Please enter a valid YouTube video URL.")


    if choice == "Generate Summary":
        if openai_api_key and youtube_url:
            if st.button("Generate Summary"):
                if not is_valid_openai_key(openai_api_key):
                    st.markdown(f"##### ❌ Please enter a valid OpenAI API key. ")
                elif not youtube_url:
                    st.warning("Please enter the YouTube video URL.")
                else:
                    with st.spinner("Generating summary..."):
                            # Call the function with the user inputs
                            summary = generate_summary(openai_api_key, youtube_url)

                    st.markdown(f"#### 🤖 Summary :")
                    st.success(summary)
        else:
            st.warning("Please enter a valid OpenAI API and YouTube URL key first")

    elif choice == "Generate Answer to a Question": 
        if openai_api_key and youtube_url:
            st.markdown('#### 🤔 Step 3 : Enter your question')
            question = st.text_input("What are you looking for ?", placeholder="What does X mean ? How to do X ?")
        else:
            st.markdown('#### 🤔 Step 3 : Enter your question')
            question = st.text_input("What are you looking for ?", placeholder="Please enter a valid OpenAI API and YouTube URL key first", disabled=True)
            
        # Add a button to run the function
        if st.button("Generate Answer"):
            if not is_valid_openai_key(openai_api_key):
                st.markdown(f"##### ❌ Please enter a valid OpenAI API key. ")

            elif not youtube_url:
                st.warning("Please enter the YouTube video URL.")
            elif not question:
                st.warning("Please enter your question.")
            else:
                os.environ["OPENAI_API_KEY"] = openai_api_key

                with st.spinner("Generating answer..."):
                    # Call the function with the user inputs
                    answer = generate_answer(openai_api_key, youtube_url, question)

                st.markdown(f"#### 🤖 {question}")
                st.success(answer)
def main():         
    gptube_app()

    # Hide Left Menu
    st.markdown("""<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>""", unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()




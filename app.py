import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

st.sidebar.title("Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp chat file", type=["txt"])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # Process chat into a DataFrame
    df = preprocessor.preprocess(data)

    # Display DataFrame
    st.dataframe(df)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")  # Insert at start

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        #computing area
        num_messages,words,media,links = helper.fetch_stats(selected_user,df)

        col1, col2, col3, col4= st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header('Total media:')
            st.title(media)

        with col4:
            st.header("Total links:")
            st.title(links)

        #finding busiest persons(more than 2 person)

        if selected_user == 'Overall':
            st.title('most bussy user')

            x,new_df = helper.fetch_most_active_user(df)
            fig , ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color ='#075e54')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)
        
        #WordCloud
        st.title("Explore Word Cloud")
        df_wc = helper.create_Wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        








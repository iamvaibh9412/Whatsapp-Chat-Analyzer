import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyser')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)


    #fetch unique users
    user_list = df['user'].unique().tolist()
    # user_list.remove("NaukriSaksham Data Science - Paid members")
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show Analysis", user_list)

# STATISTICS
    if st.sidebar.button("Show Analysis"):
        st.title("TOP STATISTICS")
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)
        
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_links)  

        #Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df) 
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color = "yellow")
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df) 
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['day_date'], daily_timeline['message'], color = "green")
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        #Activity Map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month= helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'brown')
            st.pyplot(fig)

        #Activity heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


            

        # Finding the Busiest user in group (Group Level)
        if selected_user == 'Overall':
            st.title("Most Busy User")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
           
            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color = 'orange')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #Wordcloud
        st.title("WORDCLOUD")
        df_wc = helper.create_wordcloud(selected_user, df)
        # fig, ax = plt.subplots()
        # ax.imshow(df_wc)
        # st.pyplot(fig)

        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

# Set the style for seaborn
sns.set(style='whitegrid')

# Load the emoji font
emoji_font = FontProperties(fname='NotoColorEmoji.ttf')
st.sidebar.image('assests/images.png')
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    # user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis for User:", user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
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

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green', marker='o', linestyle='-')
        ax.set_title('Monthly Timeline')
        ax.set_xlabel('Time')
        ax.set_ylabel('Messages')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black', marker='o', linestyle='-')
        ax.set_title('Daily Timeline')
        ax.set_xlabel('Date')
        ax.set_ylabel('Messages')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            ax.set_title('Most Busy Day')
            ax.set_xlabel('Day')
            ax.set_ylabel('Messages')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            ax.set_title('Most Busy Month')
            ax.set_xlabel('Month')
            ax.set_ylabel('Messages')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heatmap, ax=ax, cmap='coolwarm', linewidths=.5, annot=True)
        ax.set_title('Weekly Activity Heatmap')
        ax.set_xlabel('Period')
        ax.set_ylabel('Day')
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            
            # Renaming columns
            new_df.columns = ['user', 'percent']
            
            fig, ax = plt.subplots()
            ax.bar(x.index, x.values, color='red')
            ax.set_title('Most Busy Users')
            ax.set_xlabel('User')
            ax.set_ylabel('Messages')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

        # most common words
        st.title('Most Common Words')
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='blue')
        ax.set_title('Most Common Words')
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Words')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        emoji_df.columns = ['Emoji', 'Weight']
        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df['Weight'].head(),autopct="%0.2f")#labels=emoji_df[0].head()
            st.pyplot(fig)

st.sidebar.markdown('<p style="font-size:20px; color:lightgreen;">Made By Arin © 2024</p>', unsafe_allow_html=True)

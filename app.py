import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Personalized Content Feed",
    page_icon="📱",
    layout="wide"
)

st.title("📱 Personalized Content Feed Prioritization System")
st.write("Discover content according to your interests!")

# Sample dataset
posts = [
    {
        "id": 1,
        "title": "Virat Kohli's Latest Cricket News",
        "category": "Cricket",
        "likes": 900,
        "comments": 120,
        "hours_ago": 2,
        "description": "Latest cricket updates and match highlights."
    },
    {
        "id": 2,
        "title": "Introduction to Artificial Intelligence",
        "category": "Technology",
        "likes": 700,
        "comments": 90,
        "hours_ago": 5,
        "description": "Learn the basics of AI and machine learning."
    },
    {
        "id": 3,
        "title": "Healthy Food and Fitness Tips",
        "category": "Fitness",
        "likes": 500,
        "comments": 60,
        "hours_ago": 8,
        "description": "Simple tips for a healthier lifestyle."
    },
    {
        "id": 4,
        "title": "Python Programming for Beginners",
        "category": "Technology",
        "likes": 600,
        "comments": 80,
        "hours_ago": 1,
        "description": "Learn Python with simple examples."
    },
    {
        "id": 5,
        "title": "Travel Guide to Manali",
        "category": "Travel",
        "likes": 400,
        "comments": 40,
        "hours_ago": 12,
        "description": "Explore beautiful places in Manali."
    },
    {
        "id": 6,
        "title": "Latest Football Highlights",
        "category": "Sports",
        "likes": 800,
        "comments": 100,
        "hours_ago": 3,
        "description": "Football news, goals, and match highlights."
    },
    {
        "id": 7,
        "title": "Data Science Career Roadmap",
        "category": "Technology",
        "likes": 750,
        "comments": 110,
        "hours_ago": 4,
        "description": "Skills and tools required for Data Science."
    },
    {
        "id": 8,
        "title": "Easy Indian Cooking Recipes",
        "category": "Cooking",
        "likes": 300,
        "comments": 35,
        "hours_ago": 20,
        "description": "Prepare delicious meals at home."
    }
]

df = pd.DataFrame(posts)

# User interest profiles
user_profiles = {
    "Ritesh": ["Cricket", "Technology"],
    "Aman": ["Sports", "Fitness"],
    "Priya": ["Cooking", "Travel"]
}

st.sidebar.header("User Preferences")

user = st.sidebar.selectbox(
    "Select User",
    list(user_profiles.keys())
)

interests = user_profiles[user]

st.sidebar.write("Your interests:")
st.sidebar.write(", ".join(interests))

category = st.sidebar.selectbox(
    "Filter Category",
    ["All"] + sorted(df["category"].unique().tolist())
)

# Normalize engagement and popularity
max_engagement = (
    df["likes"] + df["comments"]
).max()

max_likes = df["likes"].max()

# Calculate priority score
def calculate_score(post):
    interest_score = (
        100 if post["category"] in interests else 20
    )

    engagement_score = (
        (post["likes"] + post["comments"])
        / max_engagement * 100
    )

    popularity_score = (
        post["likes"] / max_likes * 100
    )

    recency_score = max(
        0, 100 - post["hours_ago"] * 2
    )

    score = (
        0.40 * interest_score
        + 0.25 * engagement_score
        + 0.20 * popularity_score
        + 0.15 * recency_score
    )

    return round(score, 2)

df["Priority Score"] = df.apply(
    calculate_score, axis=1
)

# Sort posts by priority
df = df.sort_values(
    by="Priority Score",
    ascending=False
).reset_index(drop=True)

# Dashboard metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Posts", len(df))
col2.metric("Your Interests", len(interests))
col3.metric("Top Priority Score", df["Priority Score"].max())

st.subheader("🔥 Your Personalized Feed")

st.caption(
    "Posts are ranked using interests, engagement, "
    "popularity, and recency."
)

# Category filter
if category != "All":
    display_df = df[df["category"] == category]
else:
    display_df = df

# Store liked post IDs for this session
if "liked_posts" not in st.session_state:
    st.session_state.liked_posts = set()

# Display ranked posts
for rank, (_, post) in enumerate(
    display_df.iterrows(), start=1
):
    with st.container(border=True):
        left, right = st.columns([4, 1])

        with left:
            st.markdown(
                f"### {rank}. {post['title']}"
            )
            st.write(post["description"])
            st.caption(
                f"Category: {post['category']} | "
                f"Likes: {post['likes']} | "
                f"Comments: {post['comments']}"
            )

        with right:
            st.metric(
                "Priority Score",
                f"{post['Priority Score']:.2f}"
            )

            post_id = int(post["id"])

            if post_id in st.session_state.liked_posts:
                st.button(
                    "❤️ Liked",
                    key=f"liked_{post_id}",
                    disabled=True
                )
            else:
                if st.button(
                    "🤍 Like",
                    key=f"like_{post_id}"
                ):
                    st.session_state.liked_posts.add(post_id)
                    st.rerun()

# Display ranking table
st.subheader("📊 Content Ranking Analysis")

st.dataframe(
    display_df[
        ["title", "category", "likes",
         "comments", "hours_ago", "Priority Score"]
    ],
    use_container_width=True,
    hide_index=True
)

st.success(
    "Personalized content ranking completed successfully!"
)

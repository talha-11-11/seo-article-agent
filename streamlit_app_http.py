import time
import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000/api"

st.set_page_config(
    page_title="SEO Article Generator (API)",
    layout="wide",
)

st.title("SEO Article Generator – FastAPI + Streamlit")
st.caption("This UI calls the FastAPI backend using HTTP")

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("Article Settings")

topic = st.sidebar.text_input(
    "Topic / Primary Keyword",
    value="best productivity tools for remote teams",
)

target_word_count = st.sidebar.slider(
    "Target word count",
    min_value=500,
    max_value=3000,
    value=1500,
    step=100,
)

language = st.sidebar.selectbox(
    "Language",
    options=["en"],
    index=0,
)

generate_btn = st.sidebar.button("Generate Article")

# -----------------------------
# Helper Functions
# -----------------------------
def create_job(topic: str, target_word_count: int, language: str):
    payload = {
        "topic": topic,
        "target_word_count": target_word_count,
        "language": language,
    }

    response = requests.post(f"{API_BASE_URL}/jobs", json=payload)
    response.raise_for_status()
    return response.json()


def get_job(job_id: str):
    response = requests.get(f"{API_BASE_URL}/jobs/{job_id}")
    response.raise_for_status()
    return response.json()


# -----------------------------
# Main Logic
# -----------------------------
if generate_btn:
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        st.info("Sending job to FastAPI backend...")

        try:
            job = create_job(topic, target_word_count, language)
            job_id = job["id"]

            st.success(f"Job created → ID: {job_id}")

            with st.spinner("AI agent is analyzing SERP and generating content..."):
                while True:
                    job_data = get_job(job_id)

                    if job_data["status"] == "completed":
                        break
                    elif job_data["status"] == "failed":
                        st.error(f"Job failed: {job_data.get('error_message')}")
                        st.stop()

                    time.sleep(1.5)  # Poll every 1.5s

            st.success("Article generation completed!")

            article = job_data["article"]
            seo = article["seo"]

            # -----------------------------
            # SEO Metadata
            # -----------------------------
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("SEO Metadata")
                st.write("**Title tag:**")
                st.code(seo["title_tag"])

                st.write("**Meta description:**")
                st.write(seo["meta_description"])

                st.write("**Primary Keyword:**")
                st.code(seo["keyword_analysis"]["primary_keyword"])

                st.write("**Secondary Keywords:**")
                for kw in seo["keyword_analysis"]["secondary_keywords"]:
                    st.write(f"- {kw}")

            with col2:
                st.subheader("Quality Score")
                score = seo["quality_score"]
                st.metric("Overall Score", str(score["overall_score"]))
                st.write(f"✅ Primary in title: {score['has_primary_in_title']}")
                st.write(f"✅ Primary in intro: {score['has_primary_in_intro']}")
                st.write(f"✅ Heading structure OK: {score['heading_structure_ok']}")
                st.write(
                    f"✅ Meets word count: {score['meets_word_count']} (Actual: {article['word_count']})"
                )

            st.markdown("---")

            # -----------------------------
            # Internal & External Links
            # -----------------------------
            col3, col4 = st.columns(2)

            with col3:
                st.subheader("Internal Linking Suggestions")
                for link in seo["internal_links"]:
                    st.write(f"- **{link['anchor_text']}** → `{link['target_slug']}`")

            with col4:
                st.subheader("External References")
                for ref in seo["external_references"]:
                    st.write(
                        f"- [{ref['title']}]({ref['url']}) — _{ref['suggested_position']}_"
                    )

            st.markdown("---")

            # -----------------------------
            # FAQ Section
            # -----------------------------
            st.subheader("FAQ")
            for faq in seo["faq"]:
                with st.expander(faq["question"]):
                    st.write(faq["answer"])

            st.markdown("---")

            # -----------------------------
            # Full Article
            # -----------------------------
            st.subheader("Generated Article")
            st.markdown(f"# {article['h1']}")
            st.markdown(article["body_markdown"])

            # -----------------------------
            # Structured Data Preview
            # -----------------------------
            st.markdown("---")
            st.subheader("Structured Data (JSON-LD)")
            st.json(seo["structured_data"])

        except requests.exceptions.ConnectionError:
            st.error(
                "❌ Could not connect to FastAPI backend.\n\n"
                "Make sure FastAPI is running on:\n"
                "http://localhost:8000"
            )
        except Exception as e:
            st.error(f"Unexpected error: {e}")

else:
    st.info("Enter a topic in the sidebar and click **Generate Article**.")

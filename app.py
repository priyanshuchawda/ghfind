import streamlit as st
from backend import search_contributions

st.set_page_config(page_title="GitHub Contribution Finder", page_icon="🔍")

st.title("GitHub Contribution Finder")
st.markdown("Find relevant issues or PRs for your next open-source contribution using Gemini AI!")

with st.form("contribution_form"):
    st.markdown("### Search")
    repo = st.text_input("Repository", placeholder="facebook/react", help="Enter owner/repo format")
    idea = st.text_area("Contribution Idea", placeholder="Improve documentation around hooks performance")
    submitted = st.form_submit_button("Find Contribution Opportunities")

if submitted:
    if not repo or not idea:
        st.warning("Please provide both a repository and an idea.")
    else:
        with st.spinner("Analyzing idea & fetching from GitHub. Please wait..."):
            result = search_contributions(repo, idea)
            
            if "error" in result:
                st.error(result["error"])
            else:
                data = result["data"]
                res_type = result["type"]
                
                if res_type == "none" or not data:
                    st.info("No relevant issues or pull requests found.")
                else:
                    titles = {"issues": "Issues", "pull requests": "Pull Requests"}
                    display_title = titles.get(res_type, "Items")
                    
                    st.success(f"Found {len(data)} relevant {display_title}:")
                    
                    for item in data:
                        st.markdown(f"**#{item.get('number')} - {item.get('title')}**")
                        st.markdown(f"[{item.get('url')}]({item.get('url')})")
                        st.divider()

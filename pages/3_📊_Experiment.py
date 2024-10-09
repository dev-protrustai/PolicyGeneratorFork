import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Experiment", page_icon="📊")

st.markdown("# Experiment")
st.sidebar.header("Experiment")

num_rows = st.slider("Number of rows", 1, 10000, 500)
np.random.seed(42)
data = []
for i in range(num_rows):
    data.append(
        {
            "Preview": f"https://picsum.photos/400/200?lock={i}",
            "Views": np.random.randint(0, 1000),
            "Active": np.random.choice([True, False]),
            "Category": np.random.choice(["🤖 LLM", "📊 Data", "⚙️ Tool"]),
            "Progress": np.random.randint(1, 100),
        }
    )
data = pd.DataFrame(data)

config = {
    "Preview": st.column_config.ImageColumn(),
    "Progress": st.column_config.ProgressColumn(),
}

if st.toggle("Enable editing"):
    edited_data = st.data_editor(data, column_config=config, use_container_width=True,num_rows="dynamic")
else:
    st.dataframe(data, column_config=config, use_container_width=True)



left, middle, right = st.columns(3, vertical_alignment="bottom")

left.text_input("Write something")
middle.button("Click me", use_container_width=True)
right.checkbox("Check me")



col1, col2, col3 = st.columns(3,vertical_alignment="bottom")

with col1:
    with st.container(height=300):
        st.markdown("new")
    with st.popover("Ask AI"):
        # st.markdown("Hello World 👋")
        name = st.chat_input("What is your question?")
    st.write("Your name:", name)
with col2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")
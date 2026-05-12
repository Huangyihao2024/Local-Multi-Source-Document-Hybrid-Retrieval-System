import streamlit as st
from search import hybrid_search
from file_parser import parse_file

st.title("🔍 本地检索系统")

q = st.text_input("搜索")

# 添加滑块控件，控制返回结果数量（1~50，默认10）
top_k = st.slider("显示结果数", min_value=1, max_value=50, value=10, step=1)

if q:
    res = hybrid_search(q, top_k=top_k)   # 传入用户选择的 top_k

    for r in res:
        st.markdown(f"### {r['path']}")
        st.write(f"score: {r['score']:.4f}")

        try:
            text = parse_file(r["path"])
            st.write(text[:300])
        except:
            st.write("read error")
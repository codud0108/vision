import streamlit as st

st.set_page_config(page_title="To-Do List", page_icon="📝", layout="centered")

st.title("📝 나의 To-Do List")

# 세션 상태 초기화
if "todo_list" not in st.session_state:
    st.session_state.todo_list = []

# 할 일 추가
with st.form("todo_form", clear_on_submit=True):
    new_task = st.text_input("할 일을 입력하세요", "")
    submitted = st.form_submit_button("추가하기")
    if submitted and new_task:
        st.session_state.todo_list.append({"task": new_task, "done": False})

# 할 일 목록 보여주기
st.subheader("📋 오늘의 할 일")

# 체크박스를 통해 완료 처리
for i, item in enumerate(st.session_state.todo_list):
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        checked = st.checkbox("", key=f"check_{i}", value=item["done"])
    with col2:
        st.markdown(
            f"<span style='text-decoration: {'line-through' if checked else 'none'};'>{item['task']}</span>",
            unsafe_allow_html=True,
        )
    # 상태 업데이트
    st.session_state.todo_list[i]["done"] = checked

# 완료된 항목 삭제 버튼
if st.button("✅ 완료된 항목 지우기"):
    st.session_state.todo_list = [item for item in st.session_state.todo_list if not item["done"]]

# 현재 할 일 개수
st.info(f"남은 할 일: {sum(not item['done'] for item in st.session_state.todo_list)}개")

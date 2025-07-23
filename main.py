import streamlit as st
import urllib.parse
import random
from datetime import datetime

# 사용자 이름 입력
st.set_page_config(page_title="🎧 사용자별 플레이리스트", layout="centered")
st.title("🎧 사용자별 플레이리스트")
username = st.text_input("🙋‍♂️ 사용자 이름을 입력하세요", value="guest")

if not username.strip():
    st.warning("사용자 이름을 입력해주세요.")
    st.stop()

# 공유용 플레이리스트 데이터 (전체 사용자 공통)
if "playlist_data" not in st.session_state:
    st.session_state.playlist_data = {
        "운동할 때": ["방탄소년단 - Fire", "BLACKPINK - Pink Venom"],
        "공부할 때": ["Lofi Girl - Study Beats", "윤하 - 사건의 지평선"],
    }

# 사용자별 선택 기록 (개별 사용자에게만 보임)
if "user_selected_data" not in st.session_state:
    st.session_state.user_selected_data = {}

if username not in st.session_state.user_selected_data:
    st.session_state.user_selected_data[username] = {mood: [] for mood in st.session_state.playlist_data}

available_moods = list(st.session_state.playlist_data.keys())
selected_mood = st.selectbox("🎵 상황을 선택하세요", available_moods)

# 추천 받기
if st.button("🎵 추천받기"):
    songs = st.session_state.playlist_data[selected_mood]
    if songs:
        song = random.choice(songs)
        st.success(f"'{selected_mood}' 상황 추천 곡:")
        st.markdown(f"🎶 {song}")
        st.markdown(
            f'<iframe width="100%" height="100" '
            f'src="https://www.youtube.com/embed?listType=search&list={urllib.parse.quote(song)}" '
            f'frameborder="0" allowfullscreen></iframe>',
            unsafe_allow_html=True
        )
        # 사용자 개인 추천 기록 저장
        if song not in st.session_state.user_selected_data[username][selected_mood]:
            st.session_state.user_selected_data[username][selected_mood].append(song)
    else:
        st.warning("해당 상황에 곡이 없습니다.")

# 곡 추가하기
st.divider()
st.subheader("➕ 곡 추가하기")
new_song = st.text_input("🎶 곡 제목 입력 (예: 아이유 - 에잇)")

if st.button("곡 추가"):
    if new_song.strip():
        st.session_state.playlist_data[selected_mood].append(new_song.strip())
        st.success(f"'{new_song}'이(가) 전체 '{selected_mood}'에 추가되었습니다!")
    else:
        st.warning("곡 제목을 입력해주세요.")

# 사용자 개인 플레이리스트
st.divider()
st.subheader(f"📁 '{username}'님의 개인 플레이리스트")
for mood, songs in st.session_state.user_selected_data[username].items():
    if songs:
        with st.expander(f"🎼 {mood} ({len(songs)}곡)"):
            for song in songs:
                st.markdown(f"🔹 {song}")

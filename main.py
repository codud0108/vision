import streamlit as st
import random

st.set_page_config(page_title="나만의 플레이리스트", page_icon="🎶", layout="centered")
st.title("🎶 나만의 플레이리스트 추천 앱")

# 예시 플레이리스트 데이터
playlist_data = {
    "기분이 우울할 때": [
        "백예린 - Square (2017)",
        "IU - Love Poem",
        "정승환 - 눈사람",
        "Coldplay - Fix You",
    ],
    "기분이 신날 때": [
        "방탄소년단 - Dynamite",
        "NewJeans - Super Shy",
        "Bruno Mars - Uptown Funk",
        "ZICO - 아무노래",
    ],
    "공부할 때": [
        "Lofi Girl - Study Beats",
        "카더가든 - 명동콜링",
        "윤하 - 사건의 지평선",
        "John Coltrane - In A Sentimental Mood",
    ],
    "산책할 때": [
        "잔나비 - 주저하는 연인들을 위해",
        "볼빨간사춘기 - 여행",
        "Paul Kim - 모든 날, 모든 순간",
        "IU - 밤편지",
    ],
}

# 사용자 입력 받기
st.subheader("🎧 어떤 상황에 어울리는 노래를 찾고 있나요?")
mood = st.selectbox("상황을 선택하세요", list(playlist_data.keys()))

# 추천 버튼
if st.button("🎵 추천 받기"):
    st.success(f"'{mood}'에 어울리는 노래 추천 리스트 🎶")
    recommended = random.sample(playlist_data[mood], len(playlist_data[mood]))
    for i, song in enumerate(recommended, 1):
        st.markdown(f"**{i}. {song}**")

# 노래 추가 기능
st.divider()
st.subheader("➕ 나만의 노래를 추가해보세요")

new_mood = st.selectbox("추가할 상황 선택", list(playlist_data.keys()), key="add_mood")
new_song = st.text_input("노래 제목을 입력하세요")

if st.button("노래 추가하기"):
    if new_song.strip():
        playlist_data[new_mood].append(new_song.strip())
        st.success(f"'{new_song}'이(가) '{new_mood}' 리스트에 추가되었습니다!")
    else:
        st.warning("노래 제목을 입력해주세요.")

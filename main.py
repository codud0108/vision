import streamlit as st
import urllib.parse
from datetime import datetime

st.set_page_config(page_title="나만의 플레이리스트", page_icon="🎧", layout="centered")
st.title("🎧 나만의 플레이리스트 추천 앱")
st.markdown("상황에 맞는 음악을 추천받고, 새로운 상황과 곡도 자유롭게 추가하세요!")

# 🎯 접속 시간 기반 추천 상황 설정
def recommend_mood_by_time():
    hour = datetime.now().hour
    if 5 <= hour < 10:
        return "산책할 때"
    elif 10 <= hour < 17:
        return "공부할 때"
    elif 17 <= hour < 21:
        return "기분이 신날 때"
    else:
        return "기분이 우울할 때"

# 세션 상태 초기화
if "playlist_data" not in st.session_state:
    st.session_state.playlist_data = {
        "기분이 우울할 때": [
            "백예린 - Square (2017)",
            "밍기뉴 - 오래오래, 우리",
            "밍기뉴 - 나의 모든 이들에게",
            "IU - Love Poem",
            "정승환 - 눈사람",
        ],
        "기분이 신날 때": [
            "방탄소년단 - Dynamite",
            "NewJeans - Super Shy",
            "Bruno Mars - Uptown Funk",
        ],
        "공부할 때": [
            "Lofi Girl - Study Beats",
            "카더가든 - 명동콜링",
            "윤하 - 사건의 지평선",
        ],
        "산책할 때": [
            "잔나비 - 주저하는 연인들을 위해",
            "볼빨간사춘기 - 여행",
            "Paul Kim - 모든 날, 모든 순간",
        ],
    }

# 🕒 시간 기반 추천 상황 출력
recommended_mood = recommend_mood_by_time()
st.info(f"🕒 지금 시간에는 '{recommended_mood}' 분위기의 음악이 잘 어울려요!")

# 🎯 상황 선택
available_moods = list(st.session_state.playlist_data.keys())
selected_mood = st.selectbox("🎵 원하는 상황을 선택하세요", available_moods, index=available_moods.index(recommended_mood) if recommended_mood in available_moods else 0)

# 추천 버튼
if st.button("🎵 추천받기"):
    st.success(f"'{selected_mood}' 상황에 어울리는 곡 목록:")
    for i, song in enumerate(st.session_state.playlist_data[selected_mood], 1):
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song)}"
        st.markdown(f"{i}. 🔗 [**{song}**]({search_url})")

# 🎼 노래 추가
st.divider()
st.subheader("➕ 노래 추가하기")
new_song = st.text_input("🎶 추가할 노래 제목 (예: 아이유 - 에잇)")
target_mood = st.selectbox("🗂 추가할 상황 선택", available_moods, key="add_mood")

if st.button("노래 추가"):
    if new_song.strip():
        st.session_state.playlist_data[target_mood].append(new_song.strip())
        st.success(f"✅ '{new_song}'이(가) '{target_mood}'에 추가되었습니다!")
    else:
        st.warning("노래 제목을 입력해주세요.")

# ➕ 새로운 상황 추가
st.divider()
st.subheader("➕ 새로운 상황 추가하기")
new_mood = st.text_input("💡 새로운 상황 이름 (예: 비 오는 날, 운동할 때)")
if st.button("상황 추가"):
    new_mood = new_mood.strip()
    if new_mood:
        if new_mood not in st.session_state.playlist_data:
            st.session_state.playlist_data[new_mood] = []
            st.success(f"'{new_mood}' 상황이 추가되었습니다!")
        else:
            st.info(f"'{new_mood}' 상황은 이미 존재해요.")
    else:
        st.warning("상황 이름을 입력해주세요.")

# 📂 저장된 플레이리스트 출력
st.divider()
st.subheader("📁 나의 상황별 플레이리스트")

for mood, songs in st.session_state.playlist_data.items():
    with st.expander(f"🎼 {mood} ({len(songs)}곡)"):
        for song in songs:
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song)}"
            st.markdown(f"🔹 [**{song}**]({url})", unsafe_allow_html=True)

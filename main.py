import streamlit as st
import urllib.parse
import random
from datetime import datetime

st.set_page_config(page_title="나만의 플레이리스트", page_icon="🎧", layout="centered")
st.title("🎧 플레이리스트 추천")
st.markdown("상황에 맞는 음악을 추천받고, 새로운 상황과 곡도 자유롭게 추가하세요!")

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

if "playlist_data" not in st.session_state:
    st.session_state.playlist_data = {
        "우울할 때": ["백예린 - Square (2017)", "밍기뉴 - 오래오래, 우리", "밍기뉴 - 나의 모든 이들에게", "IU - Love Poem", "정승환 - 눈사람"],
        "신날 때": ["방탄소년단 - Dynamite", "NewJeans - Super Shy", "Bruno Mars - Uptown Funk"],
        "공부할 때": ["Lofi Girl - Study Beats", "카더가든 - 명동콜링", "윤하 - 사건의 지평선"],
        "산책할 때": ["잔나비 - 주저하는 연인들을 위해", "볼빨간사춘기 - 여행", "Paul Kim - 모든 날, 모든 순간"],
        "샤워할 때": ["LUCY - 아지랑이", "볼빨간사춘기 - 나의 사춘기에게", "안녕 - 너의 번호를 누르고"],
        "운동할 때": ["잔나비 - 주저하는 연인들을 위해", "볼빨간사춘기 - 여행", "Paul Kim - 모든 날, 모든 순간"],
        "독서할 때": ["잔나비 - 주저하는 연인들을 위해", "볼빨간사춘기 - 여행", "Paul Kim - 모든 날, 모든 순간"],
        "잠자기 전": ["잔나비 - 주저하는 연인들을 위해", "볼빨간사춘기 - 여행", "Paul Kim - 모든 날, 모든 순간"],
        "운전하다 피곤할 때": ["잔나비 - 주저하는 연인들을 위해", "볼빨간사춘기 - 여행", "Paul Kim - 모든 날, 모든 순간"],
        "식사할 때": ["잔나비 - 주저하는 연인들을 위해", "볼빨간사춘기 - 여행", "Paul Kim - 모든 날, 모든 순간"],
        "명상할 때": ["잔나비 - 주저하는 연인들을 위해", "볼빨간사춘기 - 여행", "Paul Kim - 모든 날, 모든 순간"],
        "비올 때": ["잔나비 - 주저하는 연인들을 위해", "볼빨간사춘기 - 여행", "아이유 - love wins all", "Paul Kim - 모든 날, 모든 순간"],
        "눈올 때": ["잔나비 - 주저하는 연인들을 위해", "볼빨간사춘기 - 여행", "Paul Kim - 모든 날, 모든 순간"],
        "봄에": ["방탄소년단 - 봄날", "볼빨간사춘기 - 여행", "Paul Kim - 모든 날, 모든 순간"],
        "여름에": ["잔나비 - 주저하는 연인들을 위해", "볼빨간사춘기 - 여행", "Paul Kim - 모든 날, 모든 순간"],
        "가을에": ["잔나비 - 주저하는 연인들을 위해", "볼빨간사춘기 - 여행", "Paul Kim - 모든 날, 모든 순간"],
        "겨울에": ["원위 - 크리스마스는 이래야지", "ARIANA GRANDE - SANTA TELL ME", "Paul Kim - 모든 날, 모든 순간"],
        "버스에서": ["원위 - 크리스마스는 이래야지", "ARIANA GRANDE - SANTA TELL ME", "Paul Kim - 모든 날, 모든 순간"],
    }

recommended_mood = recommend_mood_by_time()
st.info(f"🕒 지금 시간에는 '{recommended_mood}' 분위기의 음악이 잘 어울려요!")

available_moods = list(st.session_state.playlist_data.keys())
selected_mood = st.selectbox("🎵 원하는 상황을 선택하세요", available_moods, index=available_moods.index(recommended_mood) if recommended_mood in available_moods else 0)

if st.button("🎵 추천받기"):
    st.success(f"'{selected_mood}' 상황에 어울리는 곡 목록:")
    for i, song in enumerate(st.session_state.playlist_data[selected_mood], 1):
        st.markdown(f"**{i}. {song}**")
        st.markdown(
            f'<iframe width="100%" height="100" '
            f'src="https://www.youtube.com/embed?listType=search&list={urllib.parse.quote(song)}" '
            f'frameborder="0" allowfullscreen></iframe>',
            unsafe_allow_html=True
        )

# 🎲 랜덤 추천
st.divider()
st.subheader("🎲 무작위 상황 & 곡 추천받기")

if st.button("랜덤 추천 받기"):
    random_mood = random.choice(available_moods)
    if st.session_state.playlist_data[random_mood]:
        random_song = random.choice(st.session_state.playlist_data[random_mood])
        st.info(f"'{random_mood}' 상황에 어울리는 랜덤 추천 곡:")
        st.markdown(
            f'<iframe width="100%" height="100" '
            f'src="https://www.youtube.com/embed?listType=search&list={urllib.parse.quote(random_song)}" '
            f'frameborder="0" allowfullscreen></iframe>',
            unsafe_allow_html=True
        )
    else:
        st.warning(f"'{random_mood}' 상황에는 곡이 없습니다. 추가해주세요!")

# 노래 추가
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

# 새로운 상황 추가
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

# 저장된 플레이리스트
st.divider()
st.subheader("📁 나의 상황별 플레이리스트")

for mood, songs in st.session_state.playlist_data.items():
    with st.expander(f"🎼 {mood} ({len(songs)}곡)"):
        for song in songs:
            st.markdown(f"🔹 {song}")
            st.markdown(
                f'<iframe width="100%" height="100" '
                f'src="https://www.youtube.com/embed?listType=search&list={urllib.parse.quote(song)}" '
                f'frameborder="0" allowfullscreen></iframe>',
                unsafe_allow_html=True
            )

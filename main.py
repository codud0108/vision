import streamlit as st
import urllib.parse
import random
from datetime import datetime

st.set_page_config(page_title="나만의 플레이리스트", page_icon="🎧", layout="centered")
st.title("🎧 플레이리스트 추천")
st.markdown("상황에 맞는 음악을 추천받고, 새로운 상황과 곡도 자유롭게 추가하세요!")

# 사용자 입력
username = st.text_input("🙋‍♀️ 사용자 이름을 입력하세요", value="guest").strip()
if not username:
    st.warning("사용자 이름을 입력해주세요.")
    st.stop()

# 시간 기반 자동 추천 상황
def recommend_mood_by_time():
    hour = datetime.now().hour
    if 5 <= hour < 10:
        return "산책할 때"
    elif 10 <= hour < 17:
        return "공부할 때"
    elif 17 <= hour < 21:
        return "운동할 때"
    else:
        return "잠자기 전"

# 초기 데이터
if "playlist_data" not in st.session_state:
    st.session_state.playlist_data = {
        "우울할 때": ["백예린 - Square (2017)", "밍기뉴 - 오래오래, 우리", "IU - Love Poem", "정승환 - 눈사람"],
        "신날 때": ["방탄소년단 - Dynamite", "NewJeans - Super Shy", "Bruno Mars - Uptown Funk"],
        "공부할 때": ["Lofi Girl - Study Beats", "카더가든 - 명동콜링", "윤하 - 사건의 지평선"],
        "산책할 때": ["잔나비 - 주저하는 연인들을 위해", "볼빨간사춘기 - 여행", "Paul Kim - 모든 날, 모든 순간", "볼빨간사춘기 - 나만 봄", "악동뮤지션 - 시간과 낙엽", "10cm - 쓰담쓰담"],
        "샤워할 때": ["LUCY - 아지랑이", "볼빨간사춘기 - 나의 사춘기에게", "안녕 - 너의 번호를 누르고"],
        "운동할 때": ["Stray Kids - S-Class", "ZICO - 아무노래", "BLACKPINK - Pink Venom", "Eminem - Lose Yourself", "방탄소년단 - Fire", "SEVENTEEN - HOT"],
        "독서할 때": ["잔나비 - 주저하는 연인들을 위해", "볼빨간사춘기 - 여행"],
        "잠자기 전": ["폴킴 - 너를 만나", "백예린 - Bye bye my blue", "정승환 - 이 바보야", "적재 - 나랑 같이 걸을래", "로이킴 - 그때 헤어지면 돼"],
        "비올 때": ["Heize - 비도 오고 그래서", "적재 - 나랑 같이 걸을래", "김광석 - 어느 60대 노부부 이야기", "아이유 - Love wins all", "폴킴 - 모든 날, 모든 순간"],
        "봄에": ["방탄소년단 - 봄날", "볼빨간사춘기 - 여행", "10cm - 봄이 좋냐??"],
        "겨울에": ["원위 - 크리스마스는 이래야지", "ARIANA GRANDE - SANTA TELL ME"],
    }

# 사용자별 추천 기록 초기화
if "user_selected_data" not in st.session_state:
    st.session_state.user_selected_data = {}

if username not in st.session_state.user_selected_data:
    st.session_state.user_selected_data[username] = {
        mood: [] for mood in st.session_state.playlist_data
    }

# 상황 선택
available_moods = list(st.session_state.playlist_data.keys())
recommended_mood = recommend_mood_by_time()
st.info(f"🕒 지금 시간에는 '{recommended_mood}' 분위기의 음악이 잘 어울려요!")
selected_mood = st.selectbox("🎵 원하는 상황을 선택하세요", available_moods, index=available_moods.index(recommended_mood))

# 추천 버튼 → 1곡 무작위 추천 + 사용자별 저장
if st.button("🎵 추천받기"):
    songs = st.session_state.playlist_data[selected_mood]
    if songs:
        song = random.choice(songs)
        st.success(f"'{selected_mood}' 상황에 어울리는 추천 곡:")
        st.markdown(f"🎶 {song}")
        st.markdown(
            f'<iframe width="100%" height="100" '
            f'src="https://www.youtube.com/embed?listType=search&list={urllib.parse.quote(song)}" '
            f'frameborder="0" allowfullscreen></iframe>',
            unsafe_allow_html=True
        )
        # 사용자 추천 기록 저장
        if song not in st.session_state.user_selected_data[username][selected_mood]:
            st.session_state.user_selected_data[username][selected_mood].append(song)
    else:
        st.warning("해당 상황에 곡이 없습니다. 곡을 추가해주세요!")

# 🎲 랜덤 추천
st.divider()
st.subheader("🎲 무작위 상황 & 곡 추천받기")
num_songs = st.slider("추천받을 곡 개수", min_value=1, max_value=5, value=1)

if st.button("랜덤 추천 받기"):
    random_mood = random.choice(available_moods)
    songs = st.session_state.playlist_data[random_mood]
    if songs:
        selected_songs = random.sample(songs, k=min(num_songs, len(songs)))
        st.info(f"'{random_mood}' 상황에서 추천된 곡 {len(selected_songs)}개:")
        for song in selected_songs:
            st.markdown(f"🎶 {song}")
            st.markdown(
                f'<iframe width="100%" height="100" '
                f'src="https://www.youtube.com/embed?listType=search&list={urllib.parse.quote(song)}" '
                f'frameborder="0" allowfullscreen></iframe>',
                unsafe_allow_html=True
            )
            # 사용자 추천 기록 저장
            if song not in st.session_state.user_selected_data[username][random_mood]:
                st.session_state.user_selected_data[username][random_mood].append(song)
    else:
        st.warning(f"'{random_mood}' 상황에는 곡이 없습니다!")

# ➕ 노래 추가
st.divider()
st.subheader("➕ 노래 추가하기")
new_song = st.text_input("🎶 추가할 노래 제목 (예: 아이유 - 에잇)")
target_mood = st.selectbox("🗂 추가할 상황 선택", available_moods, key="add_mood")

if st.button("노래 추가"):
    if new_song.strip():
        if new_song.strip() not in st.session_state.playlist_data[target_mood]:
            st.session_state.playlist_data[target_mood].append(new_song.strip())
            st.success(f"✅ '{new_song}'이(가) '{target_mood}'에 추가되었습니다!")
        else:
            st.info("이미 추가된 곡이에요!")
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
            for user in st.session_state.user_selected_data:
                st.session_state.user_selected_data[user][new_mood] = []
            st.success(f"'{new_mood}' 상황이 추가되었습니다!")
            st.experimental_rerun()
        else:
            st.info(f"'{new_mood}' 상황은 이미 존재해요.")
    else:
        st.warning("상황 이름을 입력해주세요.")

# 📂 사용자 개인 추천 기록 출력
st.divider()
st.subheader(f"👤 '{username}'님의 추천곡 기록")
user_data = st.session_state.user_selected_data[username]
for mood, songs in user_data.items():
    if songs:
        with st.expander(f"⭐ {mood} 추천 기록 ({len(songs)}곡)"):
            for song in songs:
                st.markdown(f"✅ {song}")

import streamlit as st
import urllib.parse
import random
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="🎧 사용자별 플레이리스트", layout="centered")
st.title("🎧 사용자별 플레이리스트 추천")

# 사용자 이름 입력
username = st.text_input("🙋‍♂️ 사용자 이름을 입력하세요", value="guest")

if not username.strip():
    st.warning("사용자 이름을 입력해주세요.")
    st.stop()

# 전체 공유용 플레이리스트 데이터 (모든 사용자 공통)
if "playlist_data" not in st.session_state:
    st.session_state.playlist_data = {
        "운동할 때": [
            "방탄소년단 - Fire", "BLACKPINK - Pink Venom", "ZICO - 아무노래"
        ],
        "공부할 때": [
            "Lofi Girl - Study Beats", "윤하 - 사건의 지평선", "카더가든 - 명동콜링"
        ],
        "비올 때": [
            "Heize - 비도 오고 그래서", "아이유 - Love wins all", "폴킴 - 모든 날, 모든 순간"
        ],
        "잠자기 전": [
            "백예린 - Bye bye my blue", "정승환 - 이 바보야", "로이킴 - 그때 헤어지면 돼"
        ]
    }

# 사용자별 선택 기록 (개인화된 추천 저장용)
if "user_selected_data" not in st.session_state:
    st.session_state.user_selected_data = {}

# 사용자 초기화
if username not in st.session_state.user_selected_data:
    st.session_state.user_selected_data[username] = {
        mood: [] for mood in st.session_state.playlist_data
    }

available_moods = list(st.session_state.playlist_data.keys())

# 현재 시간 추천 상황
def recommend_mood_by_time():
    hour = datetime.now().hour
    if 5 <= hour < 10:
        return "공부할 때"
    elif 10 <= hour < 17:
        return "운동할 때"
    elif 17 <= hour < 21:
        return "비올 때"
    else:
        return "잠자기 전"

recommended = recommend_mood_by_time()
st.info(f"🕒 지금 시간엔 '{recommended}' 분위기의 음악이 잘 어울려요!")

# 상황 선택
selected_mood = st.selectbox("🎵 상황을 선택하세요", available_moods, index=available_moods.index(recommended))

# 추천 버튼 (1곡 무작위 추천)
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
        # 사용자 개인 기록에 추가
        if song not in st.session_state.user_selected_data[username][selected_mood]:
            st.session_state.user_selected_data[username][selected_mood].append(song)
    else:
        st.warning("해당 상황에 곡이 없습니다.")

# 곡 추가 기능
st.divider()
st.subheader("➕ 곡 추가하기")
new_song = st.text_input("🎶 추가할 노래 제목 (예: 아이유 - 에잇)")

if st.button("곡 추가"):
    if new_song.strip():
        st.session_state.playlist_data[selected_mood].append(new_song.strip())
        st.success(f"✅ '{new_song}'이(가) '{selected_mood}' 상황에 추가되었습니다! (모든 사용자 공유)")
    else:
        st.warning("노래 제목을 입력해주세요.")

# 사용자별 플레이리스트 출력
st.divider()
st.subheader(f"📁 '{username}'님의 추천 기록")
user_playlist = st.session_state.user_selected_data[username]

for mood, songs in user_playlist.items():
    if songs:
        with st.expander(f"🎼 {mood} ({len(songs)}곡 추천됨)"):
            for song in songs:
                st.markdown(f"🔹 {song}")
                st.markdown(
                    f'<iframe width="100%" height="100" '
                    f'src="https://www.youtube.com/embed?listType=search&list={urllib.parse.quote(song)}" '
                    f'frameborder="0" allowfullscreen></iframe>',
                    unsafe_allow_html=True
                )

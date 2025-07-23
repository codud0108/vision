import streamlit as st
import random
import urllib.parse
from datetime import datetime
from supabase import create_client, Client

# Supabase 연결
supabase_url = st.secrets["supabase"]["url"]
supabase_key = st.secrets["supabase"]["key"]
supabase: Client = create_client(supabase_url, supabase_key)

# 기본 설정
st.set_page_config(page_title="나만의 플레이리스트", page_icon="🎧")
st.title("🎧 플레이리스트 추천")

username = st.text_input("🙋‍♀️ 사용자 이름을 입력하세요", value="guest").strip()
if not username:
    st.warning("사용자 이름을 입력해주세요.")
    st.stop()

# 시간에 따라 자동 추천되는 분위기
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

# 초기 곡 리스트
playlist_data = {
    "우울할 때": ["백예린 - Square (2017)", "밍기뉴 - 오래오래, 우리", "IU - Love Poem"],
    "신날 때": ["방탄소년단 - Dynamite", "NewJeans - Super Shy", "Bruno Mars - Uptown Funk"],
    "공부할 때": ["Lofi Girl - Study Beats", "카더가든 - 명동콜링", "윤하 - 사건의 지평선"],
    "산책할 때": ["잔나비 - 주저하는 연인들을 위해", "볼빨간사춘기 - 여행", "10cm - 쓰담쓰담"],
    "운동할 때": ["Eminem - Lose Yourself", "BLACKPINK - Pink Venom", "방탄소년단 - Fire"],
    "잠자기 전": ["백예린 - Bye bye my blue", "정승환 - 이 바보야", "적재 - 나랑 같이 걸을래"],
}

available_moods = list(playlist_data.keys())
recommended_mood = recommend_mood_by_time()
st.info(f"🕒 지금 시간에는 '{recommended_mood}' 분위기의 음악이 잘 어울려요!")

# 추천 상황 선택
selected_mood = st.selectbox("🎵 원하는 상황을 선택하세요", available_moods, index=available_moods.index(recommended_mood))

# ▶ Supabase 저장 함수
def save_recommendation(username, mood, song):
    supabase.table("user_recommendations").insert({
        "username": username,
        "mood": mood,
        "song": song
    }).execute()

# ▶ Supabase 불러오기 함수
def load_user_recommendations(username):
    res = supabase.table("user_recommendations").select("*").eq("username", username).execute()
    return res.data if res.data else []

# 🎵 추천받기
if st.button("🎵 추천받기"):
    songs = playlist_data[selected_mood]
    song = random.choice(songs)
    st.success(f"'{selected_mood}' 상황에 어울리는 곡:")
    search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song)}"
    st.markdown(f"🎶 [{song}]({search_url})")
    save_recommendation(username, selected_mood, song)

# 🎲 랜덤 추천
st.divider()
st.subheader("🎲 무작위 상황 & 곡 추천")
num_songs = st.slider("추천받을 곡 수", 1, 5, 1)

if st.button("랜덤 추천 받기"):
    mood = random.choice(available_moods)
    songs = playlist_data[mood]
    selected = random.sample(songs, min(num_songs, len(songs)))
    st.info(f"'{mood}' 분위기의 추천곡 {len(selected)}개:")
    for song in selected:
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song)}"
        st.markdown(f"🎶 [{song}]({search_url})")
        save_recommendation(username, mood, song)

# ➕ 곡 추가
st.divider()
st.subheader("➕ 노래 추가")
new_song = st.text_input("🎶 추가할 노래 제목 (예: 아이유 - 에잇)")
target_mood = st.selectbox("🗂 추가할 상황", available_moods)

if st.button("노래 추가"):
    if new_song.strip():
        if new_song not in playlist_data[target_mood]:
            playlist_data[target_mood].append(new_song)
            st.success(f"'{new_song}' 이(가) '{target_mood}'에 추가되었습니다.")
        else:
            st.info("이미 추가된 곡입니다.")
    else:
        st.warning("노래 제목을 입력해주세요.")

# 🗂 사용자 추천 기록
st.divider()
st.subheader(f"👤 '{username}'님의 추천 기록")
records = load_user_recommendations(username)
if records:
    grouped = {}
    for r in records:
        grouped.setdefault(r["mood"], []).append(r["song"])
    for mood, songs in grouped.items():
        with st.expander(f"⭐ {mood} ({len(songs)}곡)"):
            for song in songs:
                search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song)}"
                st.markdown(f"✅ [{song}]({search_url})")
else:
    st.info("추천 기록이 없습니다.")

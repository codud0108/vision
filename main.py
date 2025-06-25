import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import urllib.parse
from datetime import datetime
import json

# Google 인증 (secrets 사용)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# 시트 불러오기
sheet = client.open("playlist_data").sheet1

# ---------------------
# 📥 데이터 불러오기
# ---------------------
def load_data():
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    if not df.empty and "mood" in df.columns and "song" in df.columns:
        return df
    else:
        return pd.DataFrame(columns=["mood", "song"])

df = load_data()
available_moods = sorted(df["mood"].unique()) if not df.empty else []

# ---------------------
# ⏰ 시간 기반 추천
# ---------------------
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

# ---------------------
# 🎧 Streamlit 앱 시작
# ---------------------
st.set_page_config(page_title="나만의 플레이리스트", page_icon="🎧", layout="centered")
st.title("🎧 나만의 플레이리스트 (Google Sheets 공유)")
recommended_mood = recommend_mood_by_time()
st.info(f"🕒 현재 추천 상황: **{recommended_mood}**")

# ---------------------
# 🎯 분위기 선택 및 추천 곡 표시
# ---------------------
if available_moods:
    selected_mood = st.selectbox("🎵 분위기 선택", available_moods, index=available_moods.index(recommended_mood) if recommended_mood in available_moods else 0)

    st.subheader(f"🎶 '{selected_mood}' 분위기의 추천 곡:")
    mood_songs = df[df["mood"] == selected_mood]["song"].tolist()
    for i, song in enumerate(mood_songs, 1):
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song)}"
        st.markdown(f"{i}. 🔗 [**{song}**]({url})")
else:
    st.warning("아직 등록된 분위기가 없습니다.")

# ---------------------
# ➕ 곡 추가
# ---------------------
st.divider()
st.subheader("➕ 새로운 곡 추가하기")
new_song = st.text_input("🎶 곡 제목 (예: 아이유 - 에잇)")
target_mood = st.selectbox("🗂 곡을 추가할 분위기", available_moods) if available_moods else None

if st.button("노래 추가") and new_song and target_mood:
    sheet.append_row([target_mood, new_song.strip()])
    st.success(f"✅ '{new_song}'이(가) '{target_mood}'에 추가되었습니다!")

# ---------------------
# ➕ 새로운 분위기 추가
# ---------------------
st.subheader("🌈 새로운 분위기 추가하기")
new_mood = st.text_input("새로운 분위기 이름 (예: 비 오는 날)")
if st.button("분위기 추가"):
    if new_mood.strip():
        if new_mood.strip() not in available_moods:
            # 분위기만 추가할 때는 빈 곡으로 넣기
            sheet.append_row([new_mood.strip(), ""])
            st.success(f"✅ '{new_mood}' 분위기가 추가되었습니다!")
        else:
            st.info("이미 있는 분위기입니다.")
    else:
        st.warning("분위기 이름을 입력해주세요.")

# ---------------------
# 📁 전체 플레이리스트 표시
# ---------------------
st.divider()
st.subheader("📁 분위기별 전체 플레이리스트 보기")
for mood in available_moods:
    songs = df[df["mood"] == mood]["song"].dropna().tolist()
    with st.expander(f"🎼 {mood} ({len(songs)}곡)"):
        for song in songs:
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song)}"
            st.markdown(f"🔹 [**{song}**]({url})", unsafe_allow_html=True)

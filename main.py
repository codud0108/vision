import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import urllib.parse
from datetime import datetime

st.set_page_config(page_title="나만의 플레이리스트", page_icon="🎧", layout="centered")
st.title("🎧 나만의 플레이리스트 (Google Sheets 공유)")

# =========================
# 1. Google Sheets 인증 (Secrets에서 불러오기)
# =========================
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Streamlit Cloud의 secrets.toml 에서 gcp_service_account 가져오기
creds_dict = st.secrets["gcp_service_account"]

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# =========================
# 2. Google Sheet 열기
# =========================
# 구글 시트 이름을 실제 시트명으로 바꿔주세요!
sheet = client.open("playlist_data").sheet1

# =========================
# 3. 데이터 불러오기 함수
# =========================
@st.cache_data(ttl=60)
def load_data():
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    if not df.empty and "mood" in df.columns and "song" in df.columns:
        return df
    else:
        return pd.DataFrame(columns=["mood", "song"])

df = load_data()
available_moods = sorted(df["mood"].unique()) if not df.empty else []

# =========================
# 4. 시간대별 추천 상황 함수
# =========================
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

recommended_mood = recommend_mood_by_time()
st.info(f"🕒 현재 추천 상황: **{recommended_mood}**")

# =========================
# 5. 분위기 선택 및 노래 추천
# =========================
if available_moods:
    selected_mood = st.selectbox(
        "🎵 분위기 선택",
        available_moods,
        index=available_moods.index(recommended_mood) if recommended_mood in available_moods else 0,
    )

    st.subheader(f"🎶 '{selected_mood}' 분위기의 추천 곡:")
    mood_songs = df[df["mood"] == selected_mood]["song"].tolist()
    for i, song in enumerate(mood_songs, 1):
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song)}"
        st.markdown(f"{i}. 🔗 [**{song}**]({url})")
else:
    st.warning("아직 등록된 분위기가 없습니다.")

# =========================
# 6. 새로운 곡 추가
# =========================
st.divider()
st.subheader("➕ 새로운 곡 추가하기")
new_song = st.text_input("🎶 곡 제목 (예: 아이유 - 에잇)")
target_mood = st.selectbox("🗂 곡을 추가할 분위기", available_moods) if available_moods else None

if st.button("노래 추가"):
    if new_song and target_mood:
        sheet.append_row([target_mood, new_song.strip()])
        st.success(f"✅ '{new_song}'이(가) '{target_mood}'에 추가되었습니다! 앱을 새로고침 해주세요.")
    else:
        st.warning("노래 제목과 분위기를 모두 입력해주세요.")

# =========================
# 7. 새로운 분위기 추가
# =========================
st.subheader("🌈 새로운 분위기 추가하기")
new_mood = st.text_input("새로운 분위기 이름 (예: 비 오는 날)")

if st.button("분위기 추가"):
    if new_mood:
        if new_mood not in available_moods:
            sheet.append_row([new_mood.strip(), ""])  # 빈 곡과 함께 추가
            st.success(f"✅ '{new_mood}' 분위기가 추가되었습니다! 앱을 새로고침 해주세요.")
        else:
            st.info("이미 존재하는 분위기입니다.")
    else:
        st.warning("분위기 이름을 입력해주세요.")

# =========================
# 8. 전체 플레이리스트 보기
# =========================
st.divider()
st.subheader("📁 분위기별 전체 플레이리스트 보기")

for mood in available_moods:
    songs = df[df["mood"] == mood]["song"].dropna().tolist()
    with st.expander(f"🎼 {mood} ({len(songs)}곡)"):
        for song in songs:
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song)}"
            st.markdown(f"🔹 [**{song}**]({url})", unsafe_allow_html=True)

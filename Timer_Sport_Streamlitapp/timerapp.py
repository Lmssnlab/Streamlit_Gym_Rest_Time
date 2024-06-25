import streamlit as st
import time
import pandas as pd

st.set_page_config(page_title="Gym Rest Timer", layout="wide")

st.write("This application is a Gym Rest Timer. It allows you to track the rest times between your gym sets.")

# Initialisation des variables de session
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0
if 'rest_times' not in st.session_state:
    st.session_state.rest_times = []

def start_stop_timer():
    if st.session_state.timer_running:
        elapsed_time = time.time() - st.session_state.start_time
        st.session_state.rest_times.append(round(elapsed_time, 2))
        st.session_state.timer_running = False
    else:
        st.session_state.start_time = time.time()
        st.session_state.timer_running = True

st.title("Gym Rest Timer")

col1, col2 = st.columns(2)

with col1:
    if st.session_state.timer_running:
        if st.button("Stop Timer"):
            start_stop_timer()
    else:
        if st.button("Start Timer"):
            start_stop_timer()

    # Créer un emplacement pour le timer
    timer_placeholder = st.empty()

with col2:
    if st.session_state.rest_times:
        df = pd.DataFrame({"Rest Times": st.session_state.rest_times})
        st.write("Rest Times:")
        st.dataframe(df)
        st.write(f"Average Rest Time: {df['Rest Times'].mean():.2f} seconds")

if st.button("Reset Session"):
    st.session_state.rest_times = []
    st.session_state.timer_running = False
    st.experimental_rerun()

# Afficher le timer de manière lisible
if st.session_state.timer_running:
    elapsed_time = time.time() - st.session_state.start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    timer_placeholder.write(f"Timer running: {minutes:02d}:{seconds:02d}")
else:
    timer_placeholder.empty()

# Boucle pour mettre à jour le timer
while st.session_state.timer_running:
    elapsed_time = time.time() - st.session_state.start_time
    timer_placeholder.write(f"Timer running: {elapsed_time:.2f} seconds")
    time.sleep(0.1)  # Mise à jour toutes les 0.1 secondes
    if not st.session_state.timer_running:
        timer_placeholder.empty()

# Effacer le timer quand il n'est pas en cours
if not st.session_state.timer_running:
    timer_placeholder.empty()


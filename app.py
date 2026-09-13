import streamlit as st
import random
import os

# Page configuration
st.set_page_config(page_title="Sea of Seas: Command HQ", page_icon="⚓", layout="wide")

# Custom UI Styling for Dark Modern Military Interface
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
        text-align: center;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: bold;
        padding: 10px 16px;
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #475569;
        color: #f8fafc;
    }
    .stButton>button:hover {
        border-color: #38bdf8;
        color: #38bdf8;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to display local images safely
def render_image(image_path, caption=""):
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True, caption=caption)
    else:
        st.info(f"📷 [Artwork: {caption}]")

# Initialize Session States
if "view" not in st.session_state:
    st.session_state.view = "hq"  # Views: hq, mission, combat, dock
if "fleet_hp" not in st.session_state:
    st.session_state.fleet_hp = 100
if "max_hp" not in st.session_state:
    st.session_state.max_hp = 100
if "ammo" not in st.session_state:
    st.session_state.ammo = 60
if "credits" not in st.session_state:
    st.session_state.credits = 150
if "victories" not in st.session_state:
    st.session_state.victories = 0
if "enemy_hp" not in st.session_state:
    st.session_state.enemy_hp = 0
if "enemy_max_hp" not in st.session_state:
    st.session_state.enemy_max_hp = 0
if "enemy_name" not in st.session_state:
    st.session_state.enemy_name = "Feindverband"
if "log" not in st.session_state:
    st.session_state.log = ["Willkommen im Hauptquartier, Kommandant."]

def add_log(msg):
    st.session_state.log.insert(0, msg)

# --- SIDEBAR STATUS ---
st.sidebar.markdown("## ⚓ FLOTTEN-DASHBOARD")
st.sidebar.markdown("---")
st.sidebar.progress(max(0.0, min(1.0, st.session_state.fleet_hp / st.session_state.max_hp)), 
                    text=f"Hülle: {st.session_state.fleet_hp}/{st.session_state.max_hp} HP")
st.sidebar.metric("Munitionsvorrat 💣", f"{st.session_state.ammo} Schuss")
st.sidebar.metric("Ressourcen 🪙", f"{st.session_state.credits} G")
st.sidebar.metric("Siege 🏆", f"{st.session_state.victories}")

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Spiel zurücksetzen"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- TOP HEADER ---
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>⚓ SEA OF SEAS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Tactical Fleet Command & Operation Dashboard</p>", unsafe_allow_html=True)
st.markdown("---")

# Check Game Over
if st.session_state.fleet_hp <= 0:
    st.error("💥 IHRE FLOTTE WURDE ZERSTÖRT! DAS SEEMANDAT IST GESCHEITERT.")
    if st.button("Neuen Verband aufstellen"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- VIEW 1: HAUPTQUARTIER (HQ) ---
elif st.session_state.view == "hq":
    st.subheader("🌐 Befehlslage & Operationen")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        render_image("player_ship.png", "Flaggschiff 'Black Sea'")
    
    with col2:
        st.markdown("### 📋 Status des Flaggschiffs")
        st.write(f"- **Schiffstyp:** Panzerkreuzer Klasse I")
        st.write(f"- **Struktur:** {st.session_state.fleet_hp} / {st.session_state.max_hp} HP")
        st.write(f"- **Hauptgeschütze:** 203mm Dual-Kanone")
        st.write(f"- **Einsatzbereitschaft:** {'Bereit' if st.session_state.fleet_hp > 30 else 'Kritisch'}")
        
        st.markdown("---")
        st.markdown("### 🗺️ Auslaufbefehle")
        
        if st.button("🎯 Patrouillen-Mission starten"):
            st.session_state.view = "combat"
            enemies = ["Piraten-Fregatte 'Skull Grin'", "Schwerer Feindkreuzer", "Versteckter U-Boot-Verband"]
            st.session_state.enemy_name = random.choice(enemies)
            st.session_state.enemy_max_hp = random.randint(50, 90)
            st.session_state.enemy_hp = st.session_state.enemy_max_hp
            add_log(f"⚠️ Feindkontakt hergestellt: {st.session_state.enemy_name}")
            st.rerun()
            
        if st.button("⚓ Drydock / Flotten-Hafen ansteuern"):
            st.session_state.view = "dock"
            st.rerun()

# --- VIEW 2: DOCK & REPARATUR ---
elif st.session_state.view == "dock":
    st.subheader("⚓ Marine-Werft & Versorgungszentrum")
    
    c_img, c_actions = st.columns([1, 1])
    
    with c_img:
        render_image("port.png", "Marinebasis Fort Vanguard")
        
    with c_actions:
        st.markdown("### 🔧 Werft-Dienste")
        
        if st.button("🛠️ Rumpf reparieren (+40 HP) - 40 Credits"):
            if st.session_state.credits >= 40:
                st.session_state.credits -= 40
                st.session_state.fleet_hp = min(st.session_state.max_hp, st.session_state.fleet_hp + 40)
                add_log("🔧 Werft hat Hülle wiederhergestellt.")
                st.rerun()
            else:
                st.error("Nicht genügend Credits!")
                
        if st.button("💣 Munition aufmunitionieren (+30 Schuss) - 30 Credits"):
            if st.session_state.credits >= 30:
                st.session_state.credits -= 30
                st.session_state.ammo += 30
                add_log("💣 Depot hat Munition aufgestockt.")
                st.rerun()
            else:
                st.error("Nicht genügend Credits!")

        if st.button("⬆️ Panzerung aufrüsten (+20 Max HP) - 100 Credits"):
            if st.session_state.credits >= 100:
                st.session_state.credits -= 100
                st.session_state.max_hp += 20
                st.session_state.fleet_hp += 20
                add_log("🛡️ Maximale Panzerung erhöht.")
                st.rerun()
            else:
                st.error("Nicht genügend Credits!")
                
        st.markdown("---")
        if st.button("⬅️ Zurück zum Hauptquartier"):
            st.session_state.view = "hq"
            st.rerun()

# --- VIEW 3: GEFECHTS-DASHBOARD ---
elif st.session_state.view == "combat":
    st.subheader(f"⚔️ Taktisches Gefecht vs. {st.session_state.enemy_name}")
    
    col_player, col_vs, col_enemy = st.columns([4, 1, 4])
    
    with col_player:
        st.markdown("### 🛡️ Eigenes Flaggschiff")
        render_image("player_ship.png", "Black Sea")
        st.progress(max(0.0, min(1.0, st.session_state.fleet_hp / st.session_state.max_hp)))
        st.write(f"Hüllen-Integrität: **{st.session_state.fleet_hp} / {st.session_state.max_hp} HP**")

    with col_vs:
        st.markdown("<h1 style='text-align: center; margin-top: 120px; color: #ef4444;'>VS</h1>", unsafe_allow_html=True)

    with col_enemy:
        st.markdown(f"### 🏴‍☠️ {st.session_state.enemy_name}")
        render_image("enemy_ship.png", "Feindverband")
        st.progress(max(0.0, min(1.0, st.session_state.enemy_hp / st.session_state.enemy_max_hp)))
        st.write(f"Feind-Integrität: **{st.session_state.enemy_hp} / {st.session_state.enemy_max_hp} HP**")

    st.markdown("---")
    st.markdown("### 🎯 Feuerbefehle")
    
    b1, b2, b3 = st.columns(3)
    
    with b1:
        if st.button("💥 Breitseite abfeuern (-5 Munition)"):
            if st.session_state.ammo >= 5:
                st.session_state.ammo -= 5
                dmg = random.randint(20, 40)
                st.session_state.enemy_hp -= dmg
                add_log(f"💥 Breitseite trifft! Feind erleidet {dmg} Schaden.")
                
                # Counter Attack
                if st.session_state.enemy_hp > 0:
                    e_dmg = random.randint(10, 25)
                    st.session_state.fleet_hp -= e_dmg
                    add_log(f"⚠️ Feind erwidert das Feuer! {e_dmg} Schaden erlitten.")
                else:
                    reward = random.randint(60, 110)
                    st.session_state.credits += reward
                    st.session_state.ammo += 15
                    st.session_state.victories += 1
                    add_log(f"🎉 Sieg! Feind zerstört. Belohnung: {reward} Credits & 15 Munition.")
                    st.session_state.view = "hq"
            else:
                st.error("Keine Munition mehr verfügbar!")
            st.rerun()

    with b2:
        if st.button("🛡️ Nebelwand & Ausweichen (Geringer Gegenschaden)"):
            e_dmg = random.randint(3, 10)
            st.session_state.fleet_hp -= e_dmg
            add_log(f"🛡️ Nebelwand gelegt. Feindfeuer abgeschwächt ({e_dmg} Schaden).")
            st.rerun()

    with b3:
        if st.button("💨 Rückzug zum HQ"):
            if random.random() > 0.3:
                add_log("💨 Erfolgreich aus dem Gefecht abgezogen.")
                st.session_state.view = "hq"
            else:
                e_dmg = random.randint(15, 30)
                st.session_state.fleet_hp -= e_dmg
                add_log(f"⚠️ Rückzug abgefangen! Feind trifft Heck ({e_dmg} Schaden).")
            st.rerun()

# --- LOGBUCH UNTEN ---
st.markdown("---")
st.subheader("📜 Logbuch der Operationen")
for log_entry in st.session_state.log[:4]:
    st.text(log_entry)

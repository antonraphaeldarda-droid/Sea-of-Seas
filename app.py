import streamlit as st
import random
import os

# Page configuration
st.set_page_config(page_title="Sea of Seas: Command HQ", page_icon="⚓", layout="wide")

# Custom UI Styling
st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #e2e8f0; }
    .stButton>button {
        border-radius: 8px; font-weight: bold; padding: 10px 16px;
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #475569; color: #f8fafc;
    }
    .stButton>button:hover { border-color: #38bdf8; color: #38bdf8; }
</style>
""", unsafe_allow_html=True)

def render_image(image_path, caption=""):
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True, caption=caption)
    else:
        st.info(f"📷 [Artwork: {caption}]")

# Initialize Session States
if "view" not in st.session_state:
    st.session_state.view = "hq"
if "ship_class" not in st.session_state:
    st.session_state.ship_class = "Panzerkreuzer"
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
if "torpedo_cooldown" not in st.session_state:
    st.session_state.torpedo_cooldown = 0
if "log" not in st.session_state:
    st.session_state.log = ["Willkommen im Hauptquartier, Kommandant."]

def add_log(msg):
    st.session_state.log.insert(0, msg)

# --- SIDEBAR STATUS ---
st.sidebar.markdown("## ⚓ FLOTTEN-DASHBOARD")
st.sidebar.markdown(f"**Schiff:** {st.session_state.ship_class}")
st.sidebar.progress(max(0.0, min(1.0, st.session_state.fleet_hp / st.session_state.max_hp)), 
                    text=f"Hülle: {st.session_state.fleet_hp}/{st.session_state.max_hp} HP")
st.sidebar.metric("Munition 💣", f"{st.session_state.ammo} Schuss")
st.sidebar.metric("Credits 🪙", f"{st.session_state.credits} G")
st.sidebar.metric("Siege 🏆", f"{st.session_state.victories}")

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Spiel zurücksetzen"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- TOP HEADER ---
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>⚓ SEA OF SEAS</h1>", unsafe_allow_html=True)
st.markdown("---")

# Check Game Over
if st.session_state.fleet_hp <= 0:
    st.error("💥 IHRE FLOTTE WURDE ZERSTÖRT! DAS SEEMANDAT IST GESCHEITERT.")
    if st.button("Neuen Verband aufstellen"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- VIEW 1: HAUPTQUARTIER ---
elif st.session_state.view == "hq":
    st.subheader("🌐 Befehlslage & Operationen")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        render_image("player_ship.png", f"Flaggschiff '{st.session_state.ship_class}'")
    with col2:
        st.markdown("### 📋 Status")
        st.write(f"- **Klasse:** {st.session_state.ship_class}")
        st.write(f"- **Hülle:** {st.session_state.fleet_hp} / {st.session_state.max_hp} HP")
        st.write(f"- **Freigeschaltete Schiffe:** {'Flugzeugträger' if st.session_state.victories >= 7 else ('Zerstörer' if st.session_state.victories >= 3 else 'Panzerkreuzer')}")
        
        st.markdown("---")
        st.markdown("### 🗺️ Befehle")
        
        if st.button("🎯 Mission / Gefecht suchen"):
            # 30% Chance auf ein Zufallsevent vor dem Kampf
            if random.random() < 0.4:
                st.session_state.view = "event"
            else:
                st.session_state.view = "combat"
                enemies = ["Piraten-Fregatte", "Schwerer Feindkreuzer", "Versteckter U-Boot-Verband"]
                st.session_state.enemy_name = random.choice(enemies)
                st.session_state.enemy_max_hp = random.randint(60, 110)
                st.session_state.enemy_hp = st.session_state.enemy_max_hp
                st.session_state.torpedo_cooldown = 0
                add_log(f"⚠️ Feindkontakt: {st.session_state.enemy_name}")
            st.rerun()
            
        if st.button("⚓ Drydock & Werft ansteuern"):
            st.session_state.view = "dock"
            st.rerun()

# --- VIEW 2: ZUFALLS-EVENTS ---
elif st.session_state.view == "event":
    st.subheader("📜 Unerwartetes Ereignis auf See!")
    
    events = [
        {"title": "Brennendes Handelsschiff", "desc": "Sie sichten ein ziviles Schiff in Not. Es sendet Mayday-Signale."},
        {"title": "Treibendes Frachtgut", "desc": "Ein verlassener Container treibt im Wasser. Könnte wertvoll oder eine Falle sein."},
        {"title": "Dichter Seenebel", "desc": "Ihr Radar fällt teilweise aus. Eine unbekannte Silhouette nähert sich."}
    ]
    ev = random.choice(events)
    
    st.warning(f"**{ev['title']}**: {ev['desc']}")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🤝 Helfen / Untersuchen"):
            if random.random() > 0.3:
                gold = random.randint(40, 80)
                st.session_state.credits += gold
                add_log(f"✅ Rettung erfolgreich! Belohnung: +{gold} Credits.")
            else:
                dmg = random.randint(10, 20)
                st.session_state.fleet_hp -= dmg
                add_log(f"⚠️ Falle! Hinterhalt erlitten (-{dmg} HP).")
            st.session_state.view = "hq"
            st.rerun()
    with c2:
        if st.button("⏩ Ignorieren & Weiterfahren"):
            add_log("Kurs beibehalten. Ereignis ignoriert.")
            st.session_state.view = "hq"
            st.rerun()

# --- VIEW 3: DOCK & SCHIFFSWECHSEL ---
elif st.session_state.view == "dock":
    st.subheader("⚓ Marine-Werft & Upgrade-Zentrum")
    
    c_img, c_actions = st.columns([1, 1])
    with c_img:
        render_image("port.png", "Marinebasis Fort Vanguard")
        
    with c_actions:
        st.markdown("### 🔧 Werft-Dienste")
        if st.button("🛠️ Reparieren (+40 HP) - 40 G"):
            if st.session_state.credits >= 40:
                st.session_state.credits -= 40
                st.session_state.fleet_hp = min(st.session_state.max_hp, st.session_state.fleet_hp + 40)
                add_log("🔧 Flotte repariert.")
                st.rerun()
                
        if st.button("💣 Munition (+30) - 30 G"):
            if st.session_state.credits >= 30:
                st.session_state.credits -= 30
                st.session_state.ammo += 30
                add_log("💣 Munition aufgestockt.")
                st.rerun()

        st.markdown("---")
        st.markdown("### 🛳️ Schiffsklassen-Upgrade")
        if st.session_state.victories >= 3 and st.session_state.ship_class == "Panzerkreuzer":
            if st.button("🚀 Auf 'Zerstörer' aufrüsten (Kostenlos)"):
                st.session_state.ship_class = "Zerstörer"
                st.session_state.max_hp += 30
                st.session_state.fleet_hp += 30
                add_log("🎉 Neuer Zerstörer in Dienst gestellt!")
                st.rerun()
                
        if st.session_state.victories >= 7 and st.session_state.ship_class != "Flugzeugträger":
            if st.button("✈️ Auf 'Flugzeugträger' aufrüsten (Kostenlos)"):
                st.session_state.ship_class = "Flugzeugträger"
                st.session_state.max_hp += 50
                st.session_state.fleet_hp += 50
                add_log("🎉 Flugzeugträger freigeschaltet!")
                st.rerun()
                
        if st.button("⬅️ Zurück zum HQ"):
            st.session_state.view = "hq"
            st.rerun()

# --- VIEW 4: GEFECHT PRO MIT SPEZIALFÄHIGKEITEN ---
elif st.session_state.view == "combat":
    st.subheader(f"⚔️ Gefecht vs. {st.session_state.enemy_name}")
    
    col_player, col_vs, col_enemy = st.columns([4, 1, 4])
    with col_player:
        render_image("player_ship.png", st.session_state.ship_class)
        st.progress(max(0.0, min(1.0, st.session_state.fleet_hp / st.session_state.max_hp)))
        st.caption(f"HP: {st.session_state.fleet_hp} / {st.session_state.max_hp}")

    with col_vs:
        st.markdown("<h1 style='text-align: center; color: #ef4444;'>VS</h1>", unsafe_allow_html=True)

    with col_enemy:
        render_image("enemy_ship.png", st.session_state.enemy_name)
        st.progress(max(0.0, min(1.0, st.session_state.enemy_hp / st.session_state.enemy_max_hp)))
        st.caption(f"HP: {st.session_state.enemy_hp} / {st.session_state.enemy_max_hp}")

    st.markdown("---")
    st.markdown("### 🎯 Taktische Aktionen")
    
    b1, b2, b3 = st.columns(3)
    
    with b1:
        if st.button("💥 Standard-Breitseite (-5 Munition)"):
            if st.session_state.ammo >= 5:
                st.session_state.ammo -= 5
                dmg = random.randint(20, 35)
                st.session_state.enemy_hp -= dmg
                add_log(f"💥 Breitseite trifft für {dmg} Schaden.")
                if st.session_state.torpedo_cooldown > 0:
                    st.session_state.torpedo_cooldown -= 1
            st.rerun()

    with b2:
        # Special Ability: Torpedosalve
        if st.session_state.torpedo_cooldown == 0:
            if st.button("🚀 TORPEDOSALVE (-15 Munition)"):
                if st.session_state.ammo >= 15:
                    st.session_state.ammo -= 15
                    dmg = random.randint(45, 70)
                    st.session_state.enemy_hp -= dmg
                    st.session_state.torpedo_cooldown = 2
                    add_log(f"🚀 TORPEDOTREFFER! Massive {dmg} Schaden angerichtet.")
                st.rerun()
        else:
            st.button(f"⏳ Torpedo Cooldown ({st.session_state.torpedo_cooldown} Runden)", disabled=True)

    with b3:
        if st.button("💨 Rückzug"):
            st.session_state.view = "hq"
            add_log("Rückzug angetreten.")
            st.rerun()

    # Feind-Gegenschlag Prüfung
    if st.session_state.enemy_hp <= 0:
        st.balloons()
        reward = random.randint(70, 120)
        st.session_state.credits += reward
        st.session_state.victories += 1
        add_log(f"🎉 SIEG! Feind zerstört (+{reward} G).")
        st.session_state.view = "hq"
        st.rerun()
    elif st.session_state.enemy_hp < st.session_state.enemy_max_hp:
        # Feind greift am Rundenende an
        e_dmg = random.randint(8, 20)
        st.session_state.fleet_hp -= e_dmg

# Logbuch
st.markdown("---")
st.subheader("📜 Logbuch")
for log_entry in st.session_state.log[:4]:
    st.text(log_entry)

import streamlit as st
import random
import os

st.set_page_config(page_title="Sea of Seas: Command HQ", page_icon="⚓", layout="wide")

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

# Init Session States
if "view" not in st.session_state:
    st.session_state.view = "hq"
if "ship_class" not in st.session_state:
    st.session_state.ship_class = "Panzerkreuzer"
if "unlocked_ships" not in st.session_state:
    st.session_state.unlocked_ships = ["Panzerkreuzer"]
if "fleet_hp" not in st.session_state:
    st.session_state.fleet_hp = 100
if "max_hp" not in st.session_state:
    st.session_state.max_hp = 100
if "ammo" not in st.session_state:
    st.session_state.ammo = 60
if "planes" not in st.session_state:
    st.session_state.planes = 20  # Für Flugzeugträger
if "max_planes" not in st.session_state:
    st.session_state.max_planes = 20
if "credits" not in st.session_state:
    st.session_state.credits = 150
if "victories" not in st.session_state:
    st.session_state.victories = 0
if "cooldown" not in st.session_state:
    st.session_state.cooldown = 0
if "log" not in st.session_state:
    st.session_state.log = ["Willkommen im Hauptquartier, Kommandant."]

def add_log(msg):
    st.session_state.log.insert(0, msg)

# --- UNLOCK CHECK ---
if st.session_state.victories >= 3 and "Zerstörer" not in st.session_state.unlocked_ships:
    st.session_state.unlocked_ships.append("Zerstörer")
    add_log("🎉 NEUES SCHIFF FREIGESCHALTET: Zerstörer!")
if st.session_state.victories >= 7 and "Flugzeugträger" not in st.session_state.unlocked_ships:
    st.session_state.unlocked_ships.append("Flugzeugträger")
    add_log("🎉 NEUES SCHIFF FREIGESCHALTET: Flugzeugträger!")

# --- SIDEBAR DASHBOARD ---
st.sidebar.markdown("## ⚓ FLOTTEN-DASHBOARD")
st.sidebar.markdown(f"**Aktuelles Schiff:** {st.session_state.ship_class}")
st.sidebar.progress(max(0.0, min(1.0, st.session_state.fleet_hp / st.session_state.max_hp)), 
                    text=f"Hülle: {st.session_state.fleet_hp}/{st.session_state.max_hp} HP")

if st.session_state.ship_class == "Flugzeugträger":
    st.sidebar.metric("Flugzeug-Staffel ✈️", f"{st.session_state.planes} / {st.session_state.max_planes}")
else:
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

# Game Over Check
if st.session_state.fleet_hp <= 0:
    st.error("💥 IHRE FLOTTE WURDE ZERSTÖRT!")
    if st.button("Neues Spiel beginnen"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- VIEW 1: HAUPTQUARTIER & SCHIFFSWECHSEL ---
elif st.session_state.view == "hq":
    st.subheader("🌐 Befehlslage & Flotten-Hangar")
    
    col1, col2 = st.columns([3, 2])
    
    # Dynamisches Bild je nach Klasse
    img_name = "player_ship.png"
    if st.session_state.ship_class == "Zerstörer":
        img_name = "destroyer.png"  # Falls du später ein neues Bild hochlädst
    elif st.session_state.ship_class == "Flugzeugträger":
        img_name = "carrier.png"
        
    with col1:
        render_image(img_name, f"Flaggschiff: {st.session_state.ship_class}")
    
    with col2:
        st.markdown("### 🛳️ Schiffsklasse wählen")
        selected_ship = st.selectbox("Aktives Flaggschiff:", st.session_state.unlocked_ships, index=st.session_state.unlocked_ships.index(st.session_state.ship_class))
        
        if selected_ship != st.session_state.ship_class:
            st.session_state.ship_class = selected_ship
            if selected_ship == "Panzerkreuzer":
                st.session_state.max_hp = 100
            elif selected_ship == "Zerstörer":
                st.session_state.max_hp = 80
            elif selected_ship == "Flugzeugträger":
                st.session_state.max_hp = 140
            st.session_state.fleet_hp = st.session_state.max_hp
            add_log(f"Kommando gewechselt auf: {selected_ship}")
            st.rerun()

        st.markdown("---")
        st.markdown("### 📊 Klassenspezifikationen")
        if st.session_state.ship_class == "Panzerkreuzer":
            st.write("- **Bewaffnung:** Kanonen & Torpedos")
            st.write("- **Schaden:** Mittel (20-35)")
            st.write("- **Ressource:** Munition")
        elif st.session_state.ship_class == "Zerstörer":
            st.write("- **Bewaffnung:** Schnelle Torpedos")
            st.write("- **Schaden:** Hoch (30-55), aber geringere HP")
            st.write("- **Ressource:** Munition")
        elif st.session_state.ship_class == "Flugzeugträger":
            st.write("- **Bewaffnung:** Sturzkampfbomber")
            st.write("- **Schaden:** Extrem Hoch (40-75)")
            st.write("- **Ressource:** Flugzeug-Staffeln")

        st.markdown("---")
        if st.button("🎯 Mission starten"):
            st.session_state.view = "combat"
            enemies = ["Feindliche Fregatte", "Schwerer Feindkreuzer", "Flotten-Schlachtschiff"]
            st.session_state.enemy_name = random.choice(enemies)
            st.session_state.enemy_max_hp = random.randint(70, 130)
            st.session_state.enemy_hp = st.session_state.enemy_max_hp
            st.session_state.cooldown = 0
            add_log(f"⚠️ Feindkontakt: {st.session_state.enemy_name}")
            st.rerun()
            
        if st.button("⚓ Drydock / Werft"):
            st.session_state.view = "dock"
            st.rerun()

# --- VIEW 2: DOCK & WERFT ---
elif st.session_state.view == "dock":
    st.subheader("⚓ Marine-Werft")
    
    c_img, c_actions = st.columns([1, 1])
    with c_img:
        render_image("port.png", "Marinebasis Fort Vanguard")
        
    with c_actions:
        st.markdown("### 🔧 Wartung & Nachschub")
        if st.button("🛠️ Hülle reparieren (+40 HP) - 40 G"):
            if st.session_state.credits >= 40:
                st.session_state.credits -= 40
                st.session_state.fleet_hp = min(st.session_state.max_hp, st.session_state.fleet_hp + 40)
                add_log("🔧 Hülle repariert.")
                st.rerun()

        if st.session_state.ship_class == "Flugzeugträger":
            if st.button("✈️ Flugzeuge ersetzen (+5 Maschinen) - 40 G"):
                if st.session_state.credits >= 40:
                    st.session_state.credits -= 40
                    st.session_state.planes = min(st.session_state.max_planes, st.session_state.planes + 5)
                    add_log("✈️ Neue Flugzeuge geliefert.")
                    st.rerun()
        else:
            if st.button("💣 Munition aufstocken (+30) - 30 G"):
                if st.session_state.credits >= 30:
                    st.session_state.credits -= 30
                    st.session_state.ammo += 30
                    add_log("💣 Munition geladen.")
                    st.rerun()

        st.markdown("---")
        if st.button("⬅️ Zurück zum HQ"):
            st.session_state.view = "hq"
            st.rerun()

# --- VIEW 3: KLASSENSPEZIFISCHER KAMPF ---
elif st.session_state.view == "combat":
    st.subheader(f"⚔️ Gefecht: {st.session_state.ship_class} vs. {st.session_state.enemy_name}")
    
    col_p, col_vs, col_e = st.columns([4, 1, 4])
    with col_p:
        render_image("player_ship.png", st.session_state.ship_class)
        st.progress(max(0.0, min(1.0, st.session_state.fleet_hp / st.session_state.max_hp)))
        st.caption(f"HP: {st.session_state.fleet_hp} / {st.session_state.max_hp}")

    with col_vs:
        st.markdown("<h1 style='text-align: center; color: #ef4444;'>VS</h1>", unsafe_allow_html=True)

    with col_e:
        render_image("enemy_ship.png", st.session_state.enemy_name)
        st.progress(max(0.0, min(1.0, st.session_state.enemy_hp / st.session_state.enemy_max_hp)))
        st.caption(f"HP: {st.session_state.enemy_hp} / {st.session_state.enemy_max_hp}")

    st.markdown("---")
    st.markdown("### 🎯 Taktische Befehle")
    
    b1, b2, b3 = st.columns(3)
    
    # PANZERKREUZER ANGRIFFE
    if st.session_state.ship_class == "Panzerkreuzer":
        with b1:
            if st.button("💥 Breitseite (-5 Munition)"):
                if st.session_state.ammo >= 5:
                    st.session_state.ammo -= 5
                    dmg = random.randint(20, 35)
                    st.session_state.enemy_hp -= dmg
                    add_log(f"💥 Breitseite trifft für {dmg} Schaden.")
                st.rerun()
        with b2:
            if st.button("🚀 Torpedosalve (-12 Munition)"):
                if st.session_state.ammo >= 12:
                    st.session_state.ammo -= 12
                    dmg = random.randint(40, 60)
                    st.session_state.enemy_hp -= dmg
                    add_log(f"🚀 Torpedos treffen für {dmg} Schaden!")
                st.rerun()

    # ZERSTÖRER ANGRIFFE
    elif st.session_state.ship_class == "Zerstörer":
        with b1:
            if st.button("🚀 Schnellfeuer-Torpedos (-8 Munition)"):
                if st.session_state.ammo >= 8:
                    st.session_state.ammo -= 8
                    dmg = random.randint(35, 55)
                    st.session_state.enemy_hp -= dmg
                    add_log(f"🚀 Zerstörer-Torpedos schlagen ein! ({dmg} Schaden)")
                st.rerun()
        with b2:
            if st.button("💨 Nebelwand legen (Ausweichen)"):
                add_log("🛡️ Im Nebel abgetaucht. Feindfeuer verfehlt!")
                st.rerun()

    # FLUGZEUGTRÄGER ANGRIFFE (MECHANIK MIT VERLUST-RISIKO)
    elif st.session_state.ship_class == "Flugzeugträger":
        with b1:
            if st.button("✈️ Bomber-Staffel starten"):
                if st.session_state.planes > 0:
                    dmg = random.randint(45, 75)
                    st.session_state.enemy_hp -= dmg
                    
                    # Chance, dass Flugzeuge abgeschossen werden
                    lost_planes = random.choice([0, 0, 1, 2])
                    st.session_state.planes = max(0, st.session_state.planes - lost_planes)
                    
                    if lost_planes > 0:
                        add_log(f"✈️ Luftschlag trifft ({dmg} Schaden)! Aber {lost_planes} Flugzeug(e) wurden von der Flak abgeschossen.")
                    else:
                        add_log(f"✈️ Perfekter Luftschlag ({dmg} Schaden)! Alle Bomber kehrten sicher zurück.")
                else:
                    st.error("Keine einsatzbereiten Flugzeuge mehr auf dem Deck!")
                st.rerun()
        with b2:
            if st.button("🛡️ Jäger-Eskorte (Abwehr)"):
                add_log("🛡️ Jäger fangen feindlichen Beschuss teilweise ab.")
                st.rerun()

    with b3:
        if st.button("🏃 Rückzug"):
            st.session_state.view = "hq"
            add_log("Rückzug angetreten.")
            st.rerun()

    # Feind-Gegenschlag
    if st.session_state.enemy_hp <= 0:
        st.balloons()
        reward = random.randint(80, 140)
        st.session_state.credits += reward
        st.session_state.victories += 1
        add_log(f"🎉 SIEG! Feind zerstört (+{reward} G).")
        st.session_state.view = "hq"
        st.rerun()
    elif st.session_state.enemy_hp < st.session_state.enemy_max_hp:
        e_dmg = random.randint(8, 22)
        st.session_state.fleet_hp -= e_dmg

# Logbuch
st.markdown("---")
st.subheader("📜 Logbuch")
for log_entry in st.session_state.log[:4]:
    st.text(log_entry)

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

# Initialize Global Session States
if "view" not in st.session_state:
    st.session_state.view = "hq"
if "ship_class" not in st.session_state:
    st.session_state.ship_class = "Panzerkreuzer"
if "unlocked_ships" not in st.session_state:
    st.session_state.unlocked_ships = ["Panzerkreuzer"]
if "credits" not in st.session_state:
    st.session_state.credits = 250
if "victories" not in st.session_state:
    st.session_state.victories = 0
if "log" not in st.session_state:
    st.session_state.log = ["Willkommen im Hauptquartier, Kommandant."]

# SCHIFFS-SPEZIFISCHE UPGRADES & STATS
if "ship_stats" not in st.session_state:
    st.session_state.ship_stats = {
        "Panzerkreuzer": {
            "hp": 100, "max_hp": 100, "ammo": 60,
            "armor_level": 0, "gun_level": 1, "torpedo_level": 1
        },
        "Zerstörer": {
            "hp": 80, "max_hp": 80, "ammo": 50,
            "armor_level": 0, "gun_level": 1, "torpedo_level": 1
        },
        "Flugzeugträger": {
            "hp": 140, "max_hp": 140, "planes": 20, "max_planes": 20,
            "armor_level": 0, "plane_level": 1
        }
    }

def add_log(msg):
    st.session_state.log.insert(0, msg)

# Helper for current ship
current_ship = st.session_state.ship_class
ship_data = st.session_state.ship_stats[current_ship]

# --- UNLOCK CHECK ---
if st.session_state.victories >= 3 and "Zerstörer" not in st.session_state.unlocked_ships:
    st.session_state.unlocked_ships.append("Zerstörer")
    add_log("🎉 NEUES SCHIFF FREIGESCHALTET: Zerstörer!")
if st.session_state.victories >= 7 and "Flugzeugträger" not in st.session_state.unlocked_ships:
    st.session_state.unlocked_ships.append("Flugzeugträger")
    add_log("🎉 NEUES SCHIFF FREIGESCHALTET: Flugzeugträger!")

# Armor Helper
armor_names = ["Keine Panzerung (0 cm)", "Leicht (10 cm / -10% Dmg)", "Mittel (20 cm / -20% Dmg)", "Schwer (30 cm / -30% Dmg)"]
armor_reductions = [0.0, 0.10, 0.20, 0.30]

# --- SIDEBAR DASHBOARD ---
st.sidebar.markdown("## ⚓ FLOTTEN-DASHBOARD")
st.sidebar.markdown(f"**Aktuelles Schiff:** {current_ship}")
st.sidebar.progress(max(0.0, min(1.0, ship_data["hp"] / ship_data["max_hp"])), 
                    text=f"Hülle: {ship_data['hp']}/{ship_data['max_hp']} HP")

if current_ship == "Flugzeugträger":
    st.sidebar.metric("Flugzeug-Staffel ✈️", f"{ship_data['planes']} / {ship_data['max_planes']}")
else:
    st.sidebar.metric("Munition 💣", f"{ship_data['ammo']} Schuss")

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
if ship_data["hp"] <= 0:
    st.error(f"💥 IHR {current_ship.upper()} WURDE ZERSTÖRT!")
    if st.button("Schiff in der Werft wiederaufbauen (100 G)"):
        if st.session_state.credits >= 100:
            st.session_state.credits -= 100
            ship_data["hp"] = ship_data["max_hp"]
            st.rerun()
        else:
            st.error("Nicht genug Credits! Neues Spiel erforderlich.")
            if st.button("Neustart"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

# --- VIEW 1: HAUPTQUARTIER ---
elif st.session_state.view == "hq":
    st.subheader("🌐 Befehlslage & Flotten-Hangar")
    
    col1, col2 = st.columns([3, 2])
    
    img_name = "player_ship.png"
    if current_ship == "Zerstörer":
        img_name = "destroyer.png"
    elif current_ship == "Flugzeugträger":
        img_name = "carrier.png"
        
    with col1:
        render_image(img_name, f"Flaggschiff: {current_ship}")
    
    with col2:
        st.markdown("### 🛳️ Schiffsklasse wählen")
        selected_ship = st.selectbox("Aktives Flaggschiff:", st.session_state.unlocked_ships, index=st.session_state.unlocked_ships.index(current_ship))
        
        if selected_ship != current_ship:
            st.session_state.ship_class = selected_ship
            add_log(f"Kommando gewechselt auf: {selected_ship}")
            st.rerun()

        # Damage Stats Calculator
        st.markdown("---")
        st.markdown("### 📊 Kampfwert & Schadensanzeige")
        
        if current_ship == "Panzerkreuzer":
            g_dmg = "20-35" if ship_data["gun_level"] == 1 else "40-55 (16-Zoll Mark 7)"
            t_dmg = "40-60" if ship_data["torpedo_level"] == 1 else "65-85 (Mk 24 Akustik)"
            st.write(f"- 💥 **Breitseiten-Schaden:** `{g_dmg}` HP")
            st.write(f"- 🚀 **Torpedo-Schaden:** `{t_dmg}` HP")
        elif current_ship == "Zerstörer":
            t_dmg = "35-55" if ship_data["torpedo_level"] == 1 else "60-80 (Mk 24 Akustik)"
            st.write(f"- 🚀 **Schnellfeuer-Torpedos:** `{t_dmg}` HP")
            st.write(f"- 💨 **Nebelwand:** 100% Ausweichchance für 1 Runde")
        elif current_ship == "Flugzeugträger":
            p_dmg = "45-75 (SBD Dauntless)" if ship_data["plane_level"] == 1 else "75-105 (F-4 Phantom Jets)"
            st.write(f"- ✈️ **Luftschlag-Schaden:** `{p_dmg}` HP")

        st.write(f"- 🛡️ **Panzerung:** {armor_names[ship_data['armor_level']]}")

        st.markdown("---")
        st.markdown("### 🎯 Gegner wählen & Mission starten")
        
        diff = st.radio("Schwierigkeitsgrad wählen:", ["🟢 Leichte Patrouille", "🟡 Schweres Kampfgeschwader", "🔴 Elite-Flaggschiff (Boss)"])
        
        if st.button("🚀 Gefecht beginnen"):
            st.session_state.view = "combat"
            if "🟢" in diff:
                st.session_state.enemy_name = "Piraten-Fregatte"
                st.session_state.enemy_max_hp = random.randint(50, 80)
                st.session_state.enemy_min_dmg = 5
                st.session_state.enemy_max_dmg = 12
                st.session_state.reward = random.randint(50, 80)
            elif "🟡" in diff:
                st.session_state.enemy_name = "Schwerer Feindkreuzer"
                st.session_state.enemy_max_hp = random.randint(100, 140)
                st.session_state.enemy_min_dmg = 12
                st.session_state.enemy_max_dmg = 24
                st.session_state.reward = random.randint(100, 160)
            else: # Boss
                st.session_state.enemy_name = "Dreadnought-Schlachtschiff 'Kraken'"
                st.session_state.enemy_max_hp = random.randint(180, 250)
                st.session_state.enemy_min_dmg = 20
                st.session_state.enemy_max_dmg = 38
                st.session_state.reward = random.randint(250, 400)
                
            st.session_state.enemy_hp = st.session_state.enemy_max_hp
            add_log(f"⚠️ FEINDKONTAKT: {st.session_state.enemy_name} ({st.session_state.enemy_hp} HP)")
            st.rerun()
            
        if st.button("⚓ Drydock & Werft (Upgrades)"):
            st.session_state.view = "dock"
            st.rerun()

# --- VIEW 2: DOCK & UPGRADE-WERFT ---
elif st.session_state.view == "dock":
    st.subheader(f"⚓ Marine-Werft: Upgrades für {current_ship}")
    
    c_img, c_actions = st.columns([1, 1])
    with c_img:
        render_image("port.png", "Marinebasis Fort Vanguard")
        
    with c_actions:
        st.markdown("### 🔧 Hülleninstandhaltung & Nachschub")
        col_rep1, col_rep2 = st.columns(2)
        with col_rep1:
            if st.button("🛠️ Reparieren (+40 HP) - 40 G"):
                if st.session_state.credits >= 40:
                    st.session_state.credits -= 40
                    ship_data["hp"] = min(ship_data["max_hp"], ship_data["hp"] + 40)
                    add_log("🔧 Hülle repariert.")
                    st.rerun()
        with col_rep2:
            if current_ship == "Flugzeugträger":
                if st.button("✈️ Flugzeuge (+5) - 40 G"):
                    if st.session_state.credits >= 40:
                        st.session_state.credits -= 40
                        ship_data["planes"] = min(ship_data["max_planes"], ship_data["planes"] + 5)
                        add_log("✈️ Nachschub geliefert.")
                        st.rerun()
            else:
                if st.button("💣 Munition (+30) - 30 G"):
                    if st.session_state.credits >= 30:
                        st.session_state.credits -= 30
                        ship_data["ammo"] += 30
                        add_log("💣 Munition geladen.")
                        st.rerun()

        st.markdown("---")
        st.markdown(f"### 🛡️ Upgrades nur für: **{current_ship}**")
        
        # Max HP Upgrade
        if st.button("🏗️ Hüllenverstärkung (+30 Max HP) - 100 G"):
            if st.session_state.credits >= 100:
                st.session_state.credits -= 100
                ship_data["max_hp"] += 30
                ship_data["hp"] += 30
                add_log(f"🏗️ Hüllenstruktur von {current_ship} verstärkt.")
                st.rerun()

        # Armor Upgrade
        if ship_data["armor_level"] < 3:
            next_armor = armor_names[ship_data["armor_level"] + 1]
            cost = (ship_data["armor_level"] + 1) * 80
            if st.button(f"🛡️ Upgrade: {next_armor} - {cost} G"):
                if st.session_state.credits >= cost:
                    st.session_state.credits -= cost
                    ship_data["armor_level"] += 1
                    add_log(f"🛡️ Panzerung von {current_ship} aufgerüstet!")
                    st.rerun()
        else:
            st.info("🛡️ Maximale Panzerung installiert.")

        st.markdown("---")
        st.markdown("### 💥 Waffen-Upgrades")
        
        if current_ship != "Flugzeugträger":
            if ship_data["gun_level"] == 1 and current_ship == "Panzerkreuzer":
                if st.button("💥 Geschütz-Upgrade: 16-Zoll/50 Mark 7 (Schaden: 40-55) - 120 G"):
                    if st.session_state.credits >= 120:
                        st.session_state.credits -= 120
                        ship_data["gun_level"] = 2
                        add_log("💥 Geschütz auf 16-Zoll Mark 7 aufgerüstet!")
                        st.rerun()
            elif current_ship == "Panzerkreuzer":
                st.write("✅ 16-Zoll/50 Mark 7 installiert")

            if ship_data["torpedo_level"] == 1:
                if st.button("🚀 Torpedo-Upgrade: Mk 24 Akustisch (+25 Schaden) - 100 G"):
                    if st.session_state.credits >= 100:
                        st.session_state.credits -= 100
                        ship_data["torpedo_level"] = 2
                        add_log(f"🚀 Akustische Torpedos Mk 24 für {current_ship} montiert!")
                        st.rerun()
            else:
                st.write("✅ Akustische Torpedos Mark 24 installiert")

        else: # Träger Upgrade
            if ship_data["plane_level"] == 1:
                if st.button("✈️ Upgrade: F-4 Phantom Jetbomber (Schaden: 75-105) - 150 G"):
                    if st.session_state.credits >= 150:
                        st.session_state.credits -= 150
                        ship_data["plane_level"] = 2
                        add_log("✈️ Staffel auf F-4 Phantom Jetbomber aufgerüstet!")
                        st.rerun()
            else:
                st.write("✅ F-4 Phantom Jetbomber im Einsatz")

        st.markdown("---")
        if st.button("⬅️ Zurück zum HQ"):
            st.session_state.view = "hq"
            st.rerun()

# --- VIEW 3: KAMPF SESSIONS ---
elif st.session_state.view == "combat":
    st.subheader(f"⚔️ Gefecht: {current_ship} vs. {st.session_state.enemy_name}")
    
    col_p, col_vs, col_e = st.columns([4, 1, 4])
    with col_p:
        render_image("player_ship.png", current_ship)
        st.progress(max(0.0, min(1.0, ship_data["hp"] / ship_data["max_hp"])))
        st.caption(f"HP: {ship_data['hp']} / {ship_data['max_hp']} | Panzerung: {ship_data['armor_level'] * 10} cm")

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
    if current_ship == "Panzerkreuzer":
        with b1:
            title = "💥 Breitseite (20-35 Dmg) [-5 Mun]" if ship_data["gun_level"] == 1 else "💥 16-Zoll Breitseite (40-55 Dmg) [-5 Mun]"
            if st.button(title):
                if ship_data["ammo"] >= 5:
                    ship_data["ammo"] -= 5
                    dmg = random.randint(20, 35) if ship_data["gun_level"] == 1 else random.randint(40, 55)
                    st.session_state.enemy_hp -= dmg
                    add_log(f"💥 Breitseite trifft für {dmg} Schaden.")
                st.rerun()
        with b2:
            title = "🚀 Torpedo (40-60 Dmg) [-12 Mun]" if ship_data["torpedo_level"] == 1 else "🚀 Mk 24 Torpedo (65-85 Dmg) [-12 Mun]"
            if st.button(title):
                if ship_data["ammo"] >= 12:
                    ship_data["ammo"] -= 12
                    dmg = random.randint(40, 60) if ship_data["torpedo_level"] == 1 else random.randint(65, 85)
                    st.session_state.enemy_hp -= dmg
                    add_log(f"🚀 Torpedo trifft für {dmg} Schaden!")
                st.rerun()

    # ZERSTÖRER ANGRIFFE
    elif current_ship == "Zerstörer":
        with b1:
            title = "🚀 Schnellfeuer-Torpedo (35-55 Dmg) [-8 Mun]" if ship_data["torpedo_level"] == 1 else "🚀 Mk 24 Torpedo (60-80 Dmg) [-8 Mun]"
            if st.button(title):
                if ship_data["ammo"] >= 8:
                    ship_data["ammo"] -= 8
                    dmg = random.randint(35, 55) if ship_data["torpedo_level"] == 1 else random.randint(60, 80)
                    st.session_state.enemy_hp -= dmg
                    add_log(f"🚀 Zerstörer-Torpedo trifft für {dmg} Schaden!")
                st.rerun()
        with b2:
            if st.button("💨 Nebelwand (Gegner verfehlt)"):
                add_log("🛡️ Im Nebel abgetaucht. Feindfeuer verfehlt!")
                st.rerun()

    # FLUGZEUGTRÄGER ANGRIFFE
    elif current_ship == "Flugzeugträger":
        with b1:
            title = "✈️ SBD Bomber (45-75 Dmg)" if ship_data["plane_level"] == 1 else "✈️ F-4 Phantom Jets (75-105 Dmg)"
            if st.button(title):
                if ship_data["planes"] > 0:
                    dmg = random.randint(45, 75) if ship_data["plane_level"] == 1 else random.randint(75, 105)
                    st.session_state.enemy_hp -= dmg
                    
                    lost = random.choice([0, 0, 1]) if ship_data["plane_level"] == 2 else random.choice([0, 0, 1, 2])
                    ship_data["planes"] = max(0, ship_data["planes"] - lost)
                    
                    if lost > 0:
                        add_log(f"✈️ Luftschlag trifft ({dmg} Dmg)! {lost} Maschinen abgeschossen.")
                    else:
                        add_log(f"✈️ Perfekter Luftschlag ({dmg} Dmg)! Keine Verluste.")
                else:
                    st.error("Keine Flugzeuge mehr!")
                st.rerun()
        with b2:
            if st.button("🛡️ Jäger-Eskorte"):
                add_log("🛡️ Jäger schützen das Deck.")
                st.rerun()

    with b3:
        if st.button("🏃 Rückzug"):
            st.session_state.view = "hq"
            add_log("Rückzug angetreten.")
            st.rerun()

    # Feind-Gegenschlag
    if st.session_state.enemy_hp <= 0:
        st.balloons()
        reward = st.session_state.reward
        st.session_state.credits += reward
        st.session_state.victories += 1
        add_log(f"🎉 SIEG! Feind zerstört (+{reward} G).")
        st.session_state.view = "hq"
        st.rerun()
    elif st.session_state.enemy_hp < st.session_state.enemy_max_hp:
        raw_dmg = random.randint(st.session_state.enemy_min_dmg, st.session_state.enemy_max_dmg)
        reduction = armor_reductions[ship_data["armor_level"]]
        actual_dmg = int(raw_dmg * (1.0 - reduction))
        ship_data["hp"] -= actual_dmg

# Logbuch
st.markdown("---")
st.subheader("📜 Logbuch")
for log_entry in st.session_state.log[:4]:
    st.text(log_entry)

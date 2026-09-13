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
    st.session_state.planes = 20
if "max_planes" not in st.session_state:
    st.session_state.max_planes = 20
if "credits" not in st.session_state:
    st.session_state.credits = 200
if "victories" not in st.session_state:
    st.session_state.victories = 0
if "log" not in st.session_state:
    st.session_state.log = ["Willkommen im Hauptquartier, Kommandant."]

# Upgrades System States
if "armor_level" not in st.session_state:
    st.session_state.armor_level = 0  # 0: Standard, 1: Leicht (10cm), 2: Mittel (20cm), 3: Schwer (30cm)
if "gun_level" not in st.session_state:
    st.session_state.gun_level = 1    # 1: 5-Zoll/38, 2: 16-Zoll/50 Mark 7
if "torpedo_level" not in st.session_state:
    st.session_state.torpedo_level = 1 # 1: Standard, 2: Akustische Torpedos Mark 24
if "plane_level" not in st.session_state:
    st.session_state.plane_level = 1   # 1: Propeller-Bomber, 2: Strahlbomber

def add_log(msg):
    st.session_state.log.insert(0, msg)

# --- UNLOCK CHECK ---
if st.session_state.victories >= 3 and "Zerstörer" not in st.session_state.unlocked_ships:
    st.session_state.unlocked_ships.append("Zerstörer")
    add_log("🎉 NEUES SCHIFF FREIGESCHALTET: Zerstörer!")
if st.session_state.victories >= 7 and "Flugzeugträger" not in st.session_state.unlocked_ships:
    st.session_state.unlocked_ships.append("Flugzeugträger")
    add_log("🎉 NEUES SCHIFF FREIGESCHALTET: Flugzeugträger!")

# Armor Data Helper
armor_names = ["Keine Panzerung (0 cm)", "Leichte Panzerung (10 cm / -10% Dmg)", "Mittlere Panzerung (20 cm / -20% Dmg)", "Schwere Gürtelpanzerung (30 cm / -30% Dmg)"]
armor_reductions = [0.0, 0.10, 0.20, 0.30]

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

# --- VIEW 1: HAUPTQUARTIER & SPECKS ---
elif st.session_state.view == "hq":
    st.subheader("🌐 Befehlslage & Flotten-Hangar")
    
    col1, col2 = st.columns([3, 2])
    
    img_name = "player_ship.png"
    if st.session_state.ship_class == "Zerstörer":
        img_name = "destroyer.png"
    elif st.session_state.ship_class == "Flugzeugträger":
        img_name = "carrier.png"
        
    with col1:
        render_image(img_name, f"Flaggschiff: {st.session_state.ship_class}")
    
    with col2:
        st.markdown("### 🛳️ Schiffsklasse wählen")
        selected_ship = st.selectbox("Aktives Flaggschiff:", st.session_state.unlocked_ships, index=st.session_state.unlocked_ships.index(st.session_state.ship_class))
        
        if selected_ship != st.session_state.ship_class:
            st.session_state.ship_class = selected_ship
            base_hp = 100 if selected_ship == "Panzerkreuzer" else (80 if selected_ship == "Zerstörer" else 140)
            st.session_state.max_hp = base_hp
            st.session_state.fleet_hp = st.session_state.max_hp
            add_log(f"Kommando gewechselt auf: {selected_ship}")
            st.rerun()

        st.markdown("---")
        st.markdown("### ⚙️ Aktuelle Spezifikationen")
        st.write(f"- **Panzerung:** {armor_names[st.session_state.armor_level]}")
        
        if st.session_state.ship_class == "Flugzeugträger":
            plane_name = "Standard SBD Dauntless" if st.session_state.plane_level == 1 else "F-4 Phantom Jetbomber (Heavy)"
            st.write(f"- **Luftflotte:** {plane_name}")
        else:
            gun_name = "5-Zoll/38-Kaliber" if st.session_state.gun_level == 1 else "16-Zoll/50-Kaliber Mark 7"
            torp_name = "Standard G7a Torpedo" if st.session_state.torpedo_level == 1 else "Akustischer Torpedo Mark 24"
            st.write(f"- **Hauptgeschütz:** {gun_name}")
            st.write(f"- **Torpedosystem:** {torp_name}")

        st.markdown("---")
        if st.button("🎯 Mission starten"):
            st.session_state.view = "combat"
            enemies = ["Feindliche Fregatte", "Schwerer Feindkreuzer", "Flotten-Schlachtschiff"]
            st.session_state.enemy_name = random.choice(enemies)
            st.session_state.enemy_max_hp = random.randint(80, 150)
            st.session_state.enemy_hp = st.session_state.enemy_max_hp
            add_log(f"⚠️ Feindkontakt: {st.session_state.enemy_name}")
            st.rerun()
            
        if st.button("⚓ Drydock & Werft (Upgrades)"):
            st.session_state.view = "dock"
            st.rerun()

# --- VIEW 2: DOCK & UPGRADE-WERFT ---
elif st.session_state.view == "dock":
    st.subheader("⚓ Marine-Werft & Upgrade-Zentrum")
    
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
                    st.session_state.fleet_hp = min(st.session_state.max_hp, st.session_state.fleet_hp + 40)
                    add_log("🔧 Hülle repariert.")
                    st.rerun()
        with col_rep2:
            if st.session_state.ship_class == "Flugzeugträger":
                if st.button("✈️ Flugzeuge (+5) - 40 G"):
                    if st.session_state.credits >= 40:
                        st.session_state.credits -= 40
                        st.session_state.planes = min(st.session_state.max_planes, st.session_state.planes + 5)
                        add_log("✈️ Nachschub geliefert.")
                        st.rerun()
            else:
                if st.button("💣 Munition (+30) - 30 G"):
                    if st.session_state.credits >= 30:
                        st.session_state.credits -= 30
                        st.session_state.ammo += 30
                        add_log("💣 Munition geladen.")
                        st.rerun()

        st.markdown("---")
        st.markdown("### 🛡️ Panzerungs- & Hüllen-Upgrades")
        
        # HP Upgrade
        if st.button(f"🏗️ Hüllenverstärkung (+30 Max HP) - 100 G"):
            if st.session_state.credits >= 100:
                st.session_state.credits -= 100
                st.session_state.max_hp += 30
                st.session_state.fleet_hp += 30
                add_log("🏗️ Hüllenstruktur verstärkt (+30 Max HP).")
                st.rerun()

        # Armor Upgrade
        if st.session_state.armor_level < 3:
            next_armor = ["Leichte Panzerung (10 cm)", "Mittlere Panzerung (20 cm)", "Schwere Gürtelpanzerung (30 cm)"][st.session_state.armor_level]
            cost = (st.session_state.armor_level + 1) * 80
            if st.button(f"🛡️ Upgrade: {next_armor} - {cost} G"):
                if st.session_state.credits >= cost:
                    st.session_state.credits -= cost
                    st.session_state.armor_level += 1
                    add_log(f"🛡️ Panzerung auf {next_armor} aufgerüstet!")
                    st.rerun()
        else:
            st.info("🛡️ Maximale Panzerung (30 cm Gürtelpanzerung) installiert.")

        st.markdown("---")
        st.markdown("### 💥 Waffen- & System-Upgrades")
        
        if st.session_state.ship_class != "Flugzeugträger":
            if st.session_state.gun_level == 1:
                if st.button("💥 Geschütz-Upgrade: 16-Zoll/50-Kaliber Mark 7 - 120 G"):
                    if st.session_state.credits >= 120:
                        st.session_state.credits -= 120
                        st.session_state.gun_level = 2
                        add_log("💥 Geschütz auf 16-Zoll/50 Mark 7 aufgerüstet (+Schaden)!")
                        st.rerun()
            else:
                st.write("✅ Hauptgeschütz: 16-Zoll/50-Kaliber Mark 7 installiert")

            if st.session_state.torpedo_level == 1:
                if st.button("🚀 Torpedo-Upgrade: Akustischer Torpedo Mk 24 - 100 G"):
                    if st.session_state.credits >= 100:
                        st.session_state.credits -= 100
                        st.session_state.torpedo_level = 2
                        add_log("🚀 Akustische Torpedos Mk 24 installiert (+Schaden)!")
                        st.rerun()
            else:
                st.write("✅ Torpedos: Akustischer Torpedo Mark 24 installiert")

        else: # Flugzeugträger Upgrades
            if st.session_state.plane_level == 1:
                if st.button("✈️ Staffel-Upgrade: F-4 Phantom Strahlbomber - 150 G"):
                    if st.session_state.credits >= 150:
                        st.session_state.credits -= 150
                        st.session_state.plane_level = 2
                        add_log("✈️ Flugzeug-Staffel auf F-4 Phantom Jetbomber aufrüster!")
                        st.rerun()
            else:
                st.write("✅ Luftflotte: F-4 Phantom Jetbomber im Dienst")

        st.markdown("---")
        if st.button("⬅️ Zurück zum HQ"):
            st.session_state.view = "hq"
            st.rerun()

# --- VIEW 3: KAMPF MIT GEPUFFERTEM SCHADEN & UPGRADES ---
elif st.session_state.view == "combat":
    st.subheader(f"⚔️ Gefecht: {st.session_state.ship_class} vs. {st.session_state.enemy_name}")
    
    col_p, col_vs, col_e = st.columns([4, 1, 4])
    with col_p:
        render_image("player_ship.png", st.session_state.ship_class)
        st.progress(max(0.0, min(1.0, st.session_state.fleet_hp / st.session_state.max_hp)))
        st.caption(f"HP: {st.session_state.fleet_hp} / {st.session_state.max_hp} | Panzerung: {st.session_state.armor_level * 10} cm")

    with col_vs:
        st.markdown("<h1 style='text-align: center; color: #ef4444;'>VS</h1>", unsafe_allow_html=True)

    with col_e:
        render_image("enemy_ship.png", st.session_state.enemy_name)
        st.progress(max(0.0, min(1.0, st.session_state.enemy_hp / st.session_state.enemy_max_hp)))
        st.caption(f"HP: {st.session_state.enemy_hp} / {st.session_state.enemy_max_hp}")

    st.markdown("---")
    st.markdown("### 🎯 Taktische Befehle")
    
    b1, b2, b3 = st.columns(3)
    
    # Damage Multipliers based on Upgrades
    gun_bonus = 20 if st.session_state.gun_level == 2 else 0
    torp_bonus = 25 if st.session_state.torpedo_level == 2 else 0
    plane_bonus = 30 if st.session_state.plane_level == 2 else 0

    # PANZERKREUZER ANGRIFFE
    if st.session_state.ship_class == "Panzerkreuzer":
        with b1:
            gun_title = "💥 5-Zoll Breitseite (-5 Mun)" if st.session_state.gun_level == 1 else "💥 16-Zoll Breitseite (-5 Mun)"
            if st.button(gun_title):
                if st.session_state.ammo >= 5:
                    st.session_state.ammo -= 5
                    dmg = random.randint(20 + gun_bonus, 35 + gun_bonus)
                    st.session_state.enemy_hp -= dmg
                    add_log(f"💥 Breitseite trifft für {dmg} Schaden.")
                st.rerun()
        with b2:
            torp_title = "🚀 Torpedosalve (-12 Mun)" if st.session_state.torpedo_level == 1 else "🚀 Mk 24 Torpedosalve (-12 Mun)"
            if st.button(torp_title):
                if st.session_state.ammo >= 12:
                    st.session_state.ammo -= 12
                    dmg = random.randint(40 + torp_bonus, 60 + torp_bonus)
                    st.session_state.enemy_hp -= dmg
                    add_log(f"🚀 Torpedos treffen für {dmg} Schaden!")
                st.rerun()

    # ZERSTÖRER ANGRIFFE
    elif st.session_state.ship_class == "Zerstörer":
        with b1:
            if st.button("🚀 Schnellfeuer-Torpedos (-8 Mun)"):
                if st.session_state.ammo >= 8:
                    st.session_state.ammo -= 8
                    dmg = random.randint(35 + torp_bonus, 55 + torp_bonus)
                    st.session_state.enemy_hp -= dmg
                    add_log(f"🚀 Zerstörer-Torpedos schlagen ein! ({dmg} Schaden)")
                st.rerun()
        with b2:
            if st.button("💨 Nebelwand (Ausweichen)"):
                add_log("🛡️ Im Nebel abgetaucht. Feindfeuer verfehlt!")
                st.rerun()

    # FLUGZEUGTRÄGER ANGRIFFE
    elif st.session_state.ship_class == "Flugzeugträger":
        with b1:
            strike_title = "✈️ SBD Bomber-Staffel" if st.session_state.plane_level == 1 else "✈️ F-4 Phantom Jet-Angriff"
            if st.button(strike_title):
                if st.session_state.planes > 0:
                    dmg = random.randint(45 + plane_bonus, 75 + plane_bonus)
                    st.session_state.enemy_hp -= dmg
                    
                    # JET-UPGRADE reduziert Verlustrisiko
                    lost_planes = random.choice([0, 0, 1]) if st.session_state.plane_level == 2 else random.choice([0, 0, 1, 2])
                    st.session_state.planes = max(0, st.session_state.planes - lost_planes)
                    
                    if lost_planes > 0:
                        add_log(f"✈️ Luftschlag trifft ({dmg} Schaden)! Aber {lost_planes} Flugzeug(e) verloren.")
                    else:
                        add_log(f"✈️ Perfekter Luftschlag ({dmg} Schaden)! Keine Verluste.")
                else:
                    st.error("Keine einsatzbereiten Flugzeuge mehr!")
                st.rerun()
        with b2:
            if st.button("🛡️ Jäger-Eskorte (Abwehr)"):
                add_log("🛡️ Jäger fangen feindlichen Beschuss ab.")
                st.rerun()

    with b3:
        if st.button("🏃 Rückzug"):
            st.session_state.view = "hq"
            add_log("Rückzug angetreten.")
            st.rerun()

    # Feind-Gegenschlag mit Panzerungsberechnung
    if st.session_state.enemy_hp <= 0:
        st.balloons()
        reward = random.randint(90, 160)
        st.session_state.credits += reward
        st.session_state.victories += 1
        add_log(f"🎉 SIEG! Feind zerstört (+{reward} G).")
        st.session_state.view = "hq"
        st.rerun()
    elif st.session_state.enemy_hp < st.session_state.enemy_max_hp:
        raw_dmg = random.randint(12, 26)
        # Apply armor reduction
        reduction = armor_reductions[st.session_state.armor_level]
        actual_dmg = int(raw_dmg * (1.0 - reduction))
        st.session_state.fleet_hp -= actual_dmg

# Logbuch
st.markdown("---")
st.subheader("📜 Logbuch")
for log_entry in st.session_state.log[:4]:
    st.text(log_entry)

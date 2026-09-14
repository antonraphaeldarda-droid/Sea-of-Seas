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

# Global Session State Initialisierung
if "game_mode" not in st.session_state:
    st.session_state.game_mode = "Normal"
if "view" not in st.session_state:
    st.session_state.view = "hq"
if "ship_class" not in st.session_state:
    st.session_state.ship_class = "Panzerkreuzer"
if "unlocked_ships" not in st.session_state:
    st.session_state.unlocked_ships = ["Panzerkreuzer"]
if "credits" not in st.session_state:
    st.session_state.credits = 150
if "victories" not in st.session_state:
    st.session_state.victories = 0
if "log" not in st.session_state:
    st.session_state.log = ["🚨 Flottenkommando betriebsbereit."]
if "is_submerged" not in st.session_state:
    st.session_state.is_submerged = False

# UPGRADE-TABELLEN (JEWEILS 5 STUFEN)
CRUISER_GUNS = {
    1: {"name": "20,3-cm-L/55 Geschütz", "dmg": (30, 45), "cost": 0},
    2: {"name": "20,3-cm-Mark 16 Dreifachturm", "dmg": (45, 60), "cost": 140},
    3: {"name": "24-cm-Schnellladekanone", "dmg": (65, 85), "cost": 300},
    4: {"name": "28-cm-Schwerkanone", "dmg": (85, 110), "cost": 500},
    5: {"name": "30,5-cm-Prototyp-Geschütz", "dmg": (110, 140), "cost": 850}
}

BATTLESHIP_GUNS = {
    1: {"name": "38-cm-SK C/34", "dmg": (60, 90), "cost": 0},
    2: {"name": "40,6-cm-Mark 7 Drillingsgeschütz", "dmg": (90, 120), "cost": 250},
    3: {"name": "46-cm-Typ 94 Megakanone", "dmg": (130, 170), "cost": 500},
    4: {"name": "50-cm-Super-Schwerkanone", "dmg": (175, 220), "cost": 850},
    5: {"name": "53-cm-Orbitalkanone Proto", "dmg": (230, 290), "cost": 1300}
}

TORPEDO_UPGRADES = {
    1: {"name": "Standard G7a Torpedo", "dmg": (35, 55), "cost": 0},
    2: {"name": "Akustischer Torpedo Mk 24", "dmg": (55, 75), "cost": 110},
    3: {"name": "Sauerstoff-Torpedo Typ 93", "dmg": (80, 105), "cost": 250},
    4: {"name": "Schwerer Homing-Torpedo T-5", "dmg": (110, 145), "cost": 450},
    5: {"name": "Magma-Kern Torpedo", "dmg": (150, 195), "cost": 750}
}

PLANE_UPGRADES = {
    1: {"name": "SBD Dauntless Bomber", "dmg": (45, 75), "cost": 0},
    2: {"name": "SB2C Helldiver Staffel", "dmg": (70, 100), "cost": 150},
    3: {"name": "A-6 Intruder Jetstaffel", "dmg": (110, 150), "cost": 350},
    4: {"name": "F-14 Tomcat Präzisionsbomber", "dmg": (155, 200), "cost": 600},
    5: {"name": "Hyperschall-Drohnenstaffel", "dmg": (210, 270), "cost": 950}
}

ARMOR_UPGRADES = {
    0: {"name": "Standard-Panzerung", "red": 0.0, "cost": 0},
    1: {"name": "Gürtelpanzerung Stufe I (-10% Dmg)", "red": 0.10, "cost": 80},
    2: {"name": "Zitadellen-Schutz Stufe II (-20% Dmg)", "red": 0.20, "cost": 180},
    3: {"name": "Verstärkter Komposit-Stahl (-30% Dmg)", "red": 0.30, "cost": 350},
    4: {"name": "Titanium-Legierung (-40% Dmg)", "red": 0.40, "cost": 600},
    5: {"name": "Verbund-Panzergitter (-50% Dmg)", "red": 0.50, "cost": 950}
}

HP_UPGRADES = {
    0: {"name": "Standard-Rumpf", "bonus": 0, "cost": 0},
    1: {"name": "Schottwand-Verstärkung I (+25 HP)", "bonus": 25, "cost": 90},
    2: {"name": "Doppelter Stahlrumpf (+60 HP)", "bonus": 60, "cost": 200},
    3: {"name": "Mehrkammer-Rumpfsystem (+100 HP)", "bonus": 100, "cost": 380},
    4: {"name": "Schwere Titan-Spanten (+150 HP)", "bonus": 150, "cost": 650},
    5: {"name": "Extremer Tiefsee-Panzerhülle (+220 HP)", "bonus": 220, "cost": 1000}
}

SHIP_PRICES = {
    "Schnellboot": 200,
    "Zerstörer": 300,
    "Panzerkreuzer": 0,
    "U-Boot": 400,
    "Schlachtschiff": 550,
    "Flugzeugträger": 700
}

ALL_SHIPS = ["Schnellboot", "Zerstörer", "Panzerkreuzer", "U-Boot", "Schlachtschiff", "Flugzeugträger"]

if "ship_stats" not in st.session_state:
    st.session_state.ship_stats = {
        "Schnellboot": {
            "hp": 45, "base_max_hp": 45, "max_hp": 45, "ammo": 24, 
            "armor_level": 0, "hp_level": 0, "torpedo_level": 1,
            "desc": "Extrem wendig (40% Ausweichchance), greift mit Torpedos an."
        },
        "Zerstörer": {
            "hp": 75, "base_max_hp": 75, "max_hp": 75, "ammo": 40, 
            "armor_level": 0, "hp_level": 0, "torpedo_level": 1, "depth_charges": 10,
            "desc": "Jäger & Begleitschiff. Verfügt über verheerende WASSERBOMBEN!"
        },
        "Panzerkreuzer": {
            "hp": 110, "base_max_hp": 110, "max_hp": 110, "ammo": 60, 
            "armor_level": 0, "hp_level": 0, "cruiser_gun_level": 1, "torpedo_level": 1,
            "desc": "Ausgewogener Allrounder mit mittleren Geschützen & Torpedos."
        },
        "U-Boot": {
            "hp": 65, "base_max_hp": 65, "max_hp": 65, "ammo": 30,
            "armor_level": 0, "hp_level": 0, "torpedo_level": 1,
            "desc": "Lautloser Jäger. Kann abtauchen, um Feuer komplett auszuweichen!"
        },
        "Schlachtschiff": {
            "hp": 200, "base_max_hp": 200, "max_hp": 200, "ammo": 80, 
            "armor_level": 0, "hp_level": 0, "bs_gun_level": 1,
            "desc": "Schwimmende Festung mit gigantischer Feuerkraft."
        },
        "Flugzeugträger": {
            "hp": 130, "base_max_hp": 130, "max_hp": 130, "planes": 15, "max_planes": 15, 
            "armor_level": 0, "hp_level": 0, "plane_level": 1,
            "desc": "Greift über Distanz mit Flugzeugstaffeln an."
        }
    }

def add_log(msg):
    st.session_state.log.insert(0, msg)

def apply_hp_upgrade(ship_dict):
    bonus = HP_UPGRADES[ship_dict["hp_level"]]["bonus"]
    old_max = ship_dict["max_hp"]
    ship_dict["max_hp"] = ship_dict["base_max_hp"] + bonus
    ship_dict["hp"] += (ship_dict["max_hp"] - old_max)

# --- SIDEBAR ---
st.sidebar.markdown("## 🚨 STEUERUNG & STATS")

mode_options = ["Standard (Karriere)", "🧪 Test / Sandbox"]
mode_idx = 0 if st.session_state.game_mode == "Normal" else 1
selected_mode_str = st.sidebar.radio("Spielmodus wählen:", mode_options, index=mode_idx)

if selected_mode_str == "🧪 Test / Sandbox" and st.session_state.game_mode != "Test":
    st.session_state.game_mode = "Test"
    st.session_state.unlocked_ships = list(ALL_SHIPS)
    st.session_state.credits = 99999
    add_log("🚨 TEST-MODUS AKTIVIERT: Alle Schiffe freigeschaltet.")
    st.rerun()
elif selected_mode_str == "Standard (Karriere)" and st.session_state.game_mode != "Normal":
    st.session_state.game_mode = "Normal"
    st.session_state.unlocked_ships = ["Panzerkreuzer"]
    st.session_state.ship_class = "Panzerkreuzer"
    st.session_state.credits = 150
    add_log("🚨 Karrieremodus aktiv: Gestartet mit Panzerkreuzer.")
    st.rerun()

current_ship = st.session_state.ship_class
ship_data = st.session_state.ship_stats[current_ship]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Modus:** `{st.session_state.game_mode}`")
st.sidebar.markdown(f"**Schiff:** {current_ship}")
st.sidebar.progress(max(0.0, min(1.0, ship_data["hp"] / ship_data["max_hp"])), 
                    text=f"Hülle: {ship_data['hp']}/{ship_data['max_hp']} HP")

if current_ship == "Flugzeugträger":
    st.sidebar.metric("Flugzeuge ✈️", f"{ship_data['planes']} / {ship_data['max_planes']}")
else:
    st.sidebar.metric("Munition 💣", f"{ship_data['ammo']} Schuss")

if current_ship == "Zerstörer":
    st.sidebar.metric("Wasserbomben 💣", f"{ship_data.get('depth_charges', 10)} Stk")

st.sidebar.metric("Credits 🪙", f"{st.session_state.credits} G")
st.sidebar.metric("Siege 🏆", f"{st.session_state.victories}")

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Spiel zurücksetzen"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- HEADER ---
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>⚓ SEA OF SEAS: FLEET COMMAND HQ</h1>", unsafe_allow_html=True)
st.markdown("---")

# GAME OVER HANDLER
if ship_data["hp"] <= 0:
    st.error(f"🚨 SCHIFF ZERSTÖRT! Mission gescheitert.")
    if st.button("Schiff für 50 G bergen & reparieren"):
        if st.session_state.credits >= 50 or st.session_state.game_mode == "Test":
            if st.session_state.game_mode != "Test": st.session_state.credits -= 50
            ship_data["hp"] = ship_data["max_hp"]
            st.session_state.view = "hq"
            add_log("🚨 Schiff geborgen und instandgesetzt.")
            st.rerun()

# --- VIEW 1: HQ ---
elif st.session_state.view == "hq":
    st.subheader("🌐 Hauptquartier & Flotten-Sektor")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        render_image(f"{current_ship.lower().replace('-', '').replace(' ', '')}.png", f"Flaggschiff: {current_ship}")
    
    with col2:
        st.markdown("### 🛳️ Flaggschiff Auswählen")
        available = st.session_state.unlocked_ships
        selected_ship = st.selectbox("Aktives Schiff:", available, index=available.index(current_ship) if current_ship in available else 0)
        if selected_ship != current_ship:
            st.session_state.ship_class = selected_ship
            add_log(f"🚨 Kommando gewechselt auf: {selected_ship}")
            st.rerun()

        st.caption(f"ℹ️ {ship_data['desc']}")
        
        if st.session_state.game_mode == "Normal":
            st.markdown("---")
            st.markdown("### 🛒 Neue Schiffsklassen freischalten")
            for s_name in ALL_SHIPS:
                price = SHIP_PRICES[s_name]
                if s_name not in st.session_state.unlocked_ships:
                    c_buy1, c_buy2 = st.columns([2, 1])
                    c_buy1.write(f"**{s_name}** ({price} G)")
                    if c_buy2.button("Kaufen", key=f"buy_{s_name}"):
                        if st.session_state.credits >= price:
                            st.session_state.credits -= price
                            st.session_state.unlocked_ships.append(s_name)
                            add_log(f"🚨 Neue Schiffsklasse freigeschaltet: {s_name}!")
                            st.rerun()

    st.markdown("---")
    st.markdown("### 📋 Misions-Terminal")
    m_col1, m_col2, m_col3 = st.columns(3)
    
    with m_col1:
        st.markdown("#### ⚔️ Feindgefecht")
        st.caption("Standard-Kampfeinsatz gegen feindliche Kriegsschiffe.")
        if st.button("🚀 Patrouille / Kampf"):
            st.session_state.view = "combat"
            st.session_state.is_submerged = False
            lvl = st.session_state.victories
            enemy_types = [
                ("Spähboot", 35 + lvl*8, 5 + lvl*2, 10 + lvl*2, 20 + lvl*5),
                ("Fregatte", 65 + lvl*12, 8 + lvl*2, 18 + lvl*3, 35 + lvl*8),
                ("Feindliches U-Boot", 50 + lvl*10, 10 + lvl*3, 22 + lvl*4, 40 + lvl*8),
                ("Panzerschiff", 110 + lvl*15, 12 + lvl*3, 25 + lvl*4, 60 + lvl*12),
                ("Elite-Schlachtschiff", 170 + lvl*25, 22 + lvl*4, 40 + lvl*5, 100 + lvl*20)
            ]
            chosen = random.choice(enemy_types)
            st.session_state.enemy_name = chosen[0]
            st.session_state.enemy_max_hp = chosen[1]
            st.session_state.enemy_min_dmg = chosen[2]
            st.session_state.enemy_max_dmg = chosen[3]
            st.session_state.reward = chosen[4]
            st.session_state.enemy_hp = st.session_state.enemy_max_hp
            add_log(f"🚨 FEINDKONTAKT: {st.session_state.enemy_name}!")
            st.rerun()

    with m_col2:
        st.markdown("#### 🌊 Zivil- & Spezialmissionen")
        st.caption("Führe Rettungseinsätze, Kartierungen oder Eskorten durch.")
        if st.button("🗺️ Spezialaufträge öffnen"):
            st.session_state.view = "missions"
            st.rerun()

    with m_col3:
        st.markdown("#### ⚓ Marine-Werft")
        st.caption("Hülle reparieren, Waffen & Panzerung aufrüsten.")
        if st.button("🔧 Werft betreten"):
            st.session_state.view = "dock"
            st.rerun()

# --- VIEW 2: DOCK ---
elif st.session_state.view == "dock":
    st.subheader(f"⚓ Marine-Werft: Arsenalkatalog für {current_ship}")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🛠️ Reparieren (+40 HP) - 25 G"):
            if st.session_state.credits >= 25 or st.session_state.game_mode == "Test":
                if st.session_state.game_mode != "Test": st.session_state.credits -= 25
                ship_data["hp"] = min(ship_data["max_hp"], ship_data["hp"] + 40)
                add_log("🚨 Hülle repariert.")
                st.rerun()
    with c2:
        if current_ship == "Flugzeugträger":
            if st.button("✈️ Flugzeuge (+5) - 30 G"):
                if st.session_state.credits >= 30 or st.session_state.game_mode == "Test":
                    if st.session_state.game_mode != "Test": st.session_state.credits -= 30
                    ship_data["planes"] = min(ship_data["max_planes"], ship_data["planes"] + 5)
                    add_log("🚨 Staffel aufgestockt.")
                    st.rerun()
        elif current_ship == "Zerstörer":
            if st.button("💣 Wasserbomben (+5) - 30 G"):
                if st.session_state.credits >= 30 or st.session_state.game_mode == "Test":
                    if st.session_state.game_mode != "Test": st.session_state.credits -= 30
                    ship_data["depth_charges"] = ship_data.get("depth_charges", 10) + 5
                    add_log("🚨 Wasserbomben aufgestockt.")
                    st.rerun()
        else:
            if st.button("💣 Munition (+25) - 20 G"):
                if st.session_state.credits >= 20 or st.session_state.game_mode == "Test":
                    if st.session_state.game_mode != "Test": st.session_state.credits -= 20
                    ship_data["ammo"] += 25
                    add_log("🚨 Munition nachgeladen.")
                    st.rerun()

    st.markdown("---")
    st.markdown("### 🛡️ Rumpf & Panzerung (5 Stufen)")
    col_arm, col_hp = st.columns(2)
    
    with col_arm:
        st.markdown("**Panzerung**")
        for lvl in range(1, 6):
            info = ARMOR_UPGRADES[lvl]
            if ship_data["armor_level"] >= lvl:
                st.write(f"• Stufe {lvl}: {info['name']} (✅)")
            else:
                if st.button(f"Kaufen Stufe {lvl} ({info['cost']} G)", key=f"arm_{lvl}"):
                    if st.session_state.credits >= info["cost"] or st.session_state.game_mode == "Test":
                        if st.session_state.game_mode != "Test": st.session_state.credits -= info["cost"]
                        ship_data["armor_level"] = lvl
                        add_log(f"🚨 Panzerung Stufe {lvl} montiert!")
                        st.rerun()

    with col_hp:
        st.markdown("**Rumpf-HP**")
        for lvl in range(1, 6):
            info = HP_UPGRADES[lvl]
            if ship_data["hp_level"] >= lvl:
                st.write(f"• Stufe {lvl}: {info['name']} (✅)")
            else:
                if st.button(f"Kaufen Stufe {lvl} ({info['cost']} G)", key=f"hp_{lvl}"):
                    if st.session_state.credits >= info["cost"] or st.session_state.game_mode == "Test":
                        if st.session_state.game_mode != "Test": st.session_state.credits -= info["cost"]
                        ship_data["hp_level"] = lvl
                        apply_hp_upgrade(ship_data)
                        add_log(f"🚨 Rumpf Stufe {lvl} eingebaut!")
                        st.rerun()

    st.markdown("---")
    if st.button("⬅️ Zurück zum HQ"):
        st.session_state.view = "hq"
        st.rerun()

# --- VIEW 3: SPEZIALMISSIONEN ---
elif st.session_state.view == "missions":
    st.subheader("🗺️ Spezialaufträge & Nicht-Kombatante Missionen")
    st.write("Wähle einen Auftrag für deine Besatzung:")

    mis1, mis2, mis3 = st.columns(3)
    
    with mis1:
        st.markdown("### 🛟 Rettungseinsatz")
        st.write("Ein Zivilschiff ist auf Grund gelaufen. Berge Überlebende aus rauem Seegang.")
        st.caption("Erfolgssatzerhöhung bei wendigen Schiffen.")
        if st.button("Einsatz starten"):
            if random.random() < 0.8:
                gain = random.randint(40, 90)
                st.session_state.credits += gain
                add_log(f"🚨 RETTUNG ERFOLGREICH: {gain} G Belohnung erhalten!")
            else:
                ship_data["hp"] -= 15
                add_log("🚨 Unwetter! Schiff erlitt 15 HP Schaden bei der Rettung.")
            st.rerun()

    with mis2:
        st.markdown("### 🧭 Sektor-Kartierung")
        st.write("Erkunde unbekannte Gewässer und kartiere Riffe für die Marine-Akademie.")
        if st.button("Erkunden"):
            gain = random.randint(30, 70)
            st.session_state.credits += gain
            add_log(f"🚨 SEKTOR KARTIERT: {gain} G Forschungsprämie kassiert.")
            st.rerun()

    with mis3:
        st.markdown("### 📦 Geleitzug-Eskorte")
        st.write("Begleite ein Frachtschiff durch gefährliches Piratengebiet.")
        if st.button("Geleitschutz geben"):
            if random.random() < 0.65:
                gain = random.randint(100, 180)
                st.session_state.credits += gain
                add_log(f"🚨 GELEITZUG SICHER GEFLÜCHTET: {gain} G Prämie erhalten!")
            else:
                ship_data["hp"] -= 30
                add_log("🚨 PIRATENANGRIFF! 30 HP Schaden während des Gefechts kassiert.")
            st.rerun()

    st.markdown("---")
    if st.button("⬅️ Zurück zum HQ"):
        st.session_state.view = "hq"
        st.rerun()

# --- VIEW 4: KAMPF ---
elif st.session_state.view == "combat":
    st.subheader(f"⚔️ Gefecht: {current_ship} vs. {st.session_state.enemy_name}")
    
    col_p, col_vs, col_e = st.columns([4, 1, 4])
    with col_p:
        render_image(f"{current_ship.lower().replace('-', '').replace(' ', '')}.png", current_ship)
        st.progress(max(0.0, min(1.0, ship_data["hp"] / ship_data["max_hp"])))
        status_sub = " 🌊 [ABGETAUCHT]" if st.session_state.is_submerged else ""
        st.caption(f"HP: {ship_data['hp']} / {ship_data['max_hp']}{status_sub}")

    with col_vs:
        st.markdown("<h1 style='text-align: center; color: #ef4444;'>VS</h1>", unsafe_allow_html=True)

    with col_e:
        render_image("enemy_ship.png", st.session_state.enemy_name)
        st.progress(max(0.0, min(1.0, st.session_state.enemy_hp / st.session_state.enemy_max_hp)))
        st.caption(f"HP: {st.session_state.enemy_hp} / {st.session_state.enemy_max_hp}")

    st.markdown("---")
    b1, b2, b3 = st.columns(3)

    if current_ship == "Zerstörer":
        t_info = TORPEDO_UPGRADES[ship_data["torpedo_level"]]
        dc_count = ship_data.get("depth_charges", 10)
        
        with b1:
            if st.button(f"🚀 {t_info['name']} [-8 Mun]"):
                if ship_data["ammo"] >= 8:
                    ship_data["ammo"] -= 8
                    dmg = random.randint(t_info["dmg"][0], t_info["dmg"][1])
                    st.session_state.enemy_hp -= dmg
                    add_log(f"🚨 Torpedo trifft für {dmg} Schaden!")
                st.rerun()
        with b2:
            if st.button(f"💣 WASSERBOMBEN WERFEN ({dc_count} übrig)"):
                if dc_count > 0:
                    ship_data["depth_charges"] -= 1
                    is_sub = "U-Boot" in st.session_state.enemy_name
                    # Doppelter Bonusschaden gegen U-Boote!
                    dmg = random.randint(90, 130) if is_sub else random.randint(40, 65)
                    st.session_state.enemy_hp -= dmg
                    if is_sub:
                        add_log(f"🚨 VOLLE TREFFER-SALVE! Wasserbomben vernichten U-Boot ({dmg} Dmg)!")
                    else:
                        add_log(f"🚨 Wasserbomben-Teppich trifft Ziel für {dmg} Schaden!")
                else:
                    st.warning("Keine Wasserbomben mehr übrig!")
                st.rerun()

    elif current_ship == "Schnellboot":
        t_info = TORPEDO_UPGRADES[ship_data["torpedo_level"]]
        with b1:
            if st.button(f"🚀 {t_info['name']} [-5 Mun]"):
                if ship_data["ammo"] >= 5:
                    ship_data["ammo"] -= 5
                    dmg = random.randint(t_info["dmg"][0], t_info["dmg"][1])
                    st.session_state.enemy_hp -= dmg
                    add_log(f"🚨 Torpedo trifft für {dmg} Schaden!")
                st.rerun()

    elif current_ship == "U-Boot":
        t_info = TORPEDO_UPGRADES[ship_data["torpedo_level"]]
        with b1:
            if st.button(f"🚀 Lautloser Torpedo [-6 Mun]"):
                if ship_data["ammo"] >= 6:
                    ship_data["ammo"] -= 6
                    dmg = random.randint(t_info["dmg"][0], t_info["dmg"][1])
                    st.session_state.enemy_hp -= dmg
                    st.session_state.is_submerged = False
                    add_log(f"🚨 Torpedo trifft für {dmg} Schaden!")
                st.rerun()
        with b2:
            sub_label = "⬆️ Auftauchen" if st.session_state.is_submerged else "🌊 Abtauchen (Tauchfahrt)"
            if st.button(sub_label):
                st.session_state.is_submerged = not st.session_state.is_submerged
                add_log("🚨 U-Boot hat die Tauchtiefe geändert.")
                st.rerun()

    elif current_ship == "Panzerkreuzer":
        g_info = CRUISER_GUNS[ship_data["cruiser_gun_level"]]
        t_info = TORPEDO_UPGRADES[ship_data["torpedo_level"]]
        with b1:
            if st.button(f"💥 {g_info['name']} [-4 Mun]"):
                if ship_data["ammo"] >= 4:
                    ship_data["ammo"] -= 4
                    dmg = random.randint(g_info["dmg"][0], g_info["dmg"][1])
                    st.session_state.enemy_hp -= dmg
                    add_log(f"🚨 Geschütz trifft für {dmg} Schaden.")
                st.rerun()
        with b2:
            if st.button(f"🚀 {t_info['name']} [-10 Mun]"):
                if ship_data["ammo"] >= 10:
                    ship_data["ammo"] -= 10
                    dmg = random.randint(t_info["dmg"][0], t_info["dmg"][1])
                    st.session_state.enemy_hp -= dmg
                    add_log(f"🚨 Torpedo trifft für {dmg} Schaden!")
                st.rerun()

    elif current_ship == "Schlachtschiff":
        g_info = BATTLESHIP_GUNS[ship_data["bs_gun_level"]]
        with b1:
            if st.button(f"💥 Breitseite [-12 Mun]"):
                if ship_data["ammo"] >= 12:
                    ship_data["ammo"] -= 12
                    dmg = random.randint(g_info["dmg"][0], g_info["dmg"][1])
                    st.session_state.enemy_hp -= dmg
                    add_log(f"🚨 ZERSTÖRERISCHE BREITSEITE ({dmg} Dmg)!")
                st.rerun()

    elif current_ship == "Flugzeugträger":
        p_info = PLANE_UPGRADES[ship_data["plane_level"]]
        with b1:
            if st.button(f"✈️ {p_info['name']}"):
                if ship_data["planes"] > 0:
                    dmg = random.randint(p_info["dmg"][0], p_info["dmg"][1])
                    st.session_state.enemy_hp -= dmg
                    if random.random() < 0.3: ship_data["planes"] -= 1
                    add_log(f"🚨 Luftschlag trifft für {dmg} Schaden!")
                st.rerun()

    with b3:
        if st.button("🏃 Rückzug"):
            st.session_state.view = "hq"
            add_log("🚨 Rückzug angetreten.")
            st.rerun()

    # FEINDREAKTION
    if st.session_state.enemy_hp <= 0:
        st.balloons()
        reward = st.session_state.reward
        st.session_state.credits += reward
        st.session_state.victories += 1
        add_log(f"🚨 SIEG! Feind vernichtet (+{reward} G).")
        st.session_state.view = "hq"
        st.rerun()
    elif st.session_state.enemy_hp < st.session_state.enemy_max_hp:
        raw_dmg = random.randint(st.session_state.enemy_min_dmg, st.session_state.enemy_max_dmg)
        if st.session_state.is_submerged:
            add_log("🚨 Feindliches Feuer verfehlt! U-Boot war abgetaucht.")
        elif current_ship == "Schnellboot" and random.random() < 0.40:
            add_log("🚨 Ausgewichen!")
        else:
            red = ARMOR_UPGRADES[ship_data["armor_level"]]["red"]
            actual_dmg = int(raw_dmg * (1.0 - red))
            ship_data["hp"] -= actual_dmg

# LOG
st.markdown("---")
st.subheader("📜 Logbuch")
for log_entry in st.session_state.log[:4]:
    st.text(log_entry)

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
if "view" not in st.session_state:
    st.session_state.view = "hq"
if "ship_class" not in st.session_state:
    st.session_state.ship_class = "Panzerkreuzer"
if "unlocked_ships" not in st.session_state:
    st.session_state.unlocked_ships = ["Schnellboot", "Zerstörer", "Panzerkreuzer", "Schlachtschiff", "Flugzeugträger"]
if "credits" not in st.session_state:
    st.session_state.credits = 150
if "victories" not in st.session_state:
    st.session_state.victories = 0
if "log" not in st.session_state:
    st.session_state.log = ["Flottenkommando bereit. Klassendifferenzierung überarbeitet!"]

# --- UPGRADE-TABELLEN ---

# Kreuzer-Geschütze (Mittlere Kaliber)
CRUISER_GUNS = {
    1: {"name": "20,3-cm-L/55 Geschütz", "dmg": (30, 45), "cost": 0},
    2: {"name": "20,3-cm-Mark 16 Dreifachturm", "dmg": (45, 60), "cost": 140},
    3: {"name": "24-cm-Schnellladekanone", "dmg": (65, 85), "cost": 300}
}

# Schlachtschiff-Geschütze (Schwere Kaliber)
BATTLESHIP_GUNS = {
    1: {"name": "38-cm-SK C/34 (Schwere Artillerie)", "dmg": (60, 90), "cost": 0},
    2: {"name": "40,6-cm-Mark 7 Drillingsgeschütz", "dmg": (90, 120), "cost": 250},
    3: {"name": "46-cm-Typ 94 Megakanone", "dmg": (130, 170), "cost": 500}
}

TORPEDO_UPGRADES = {
    1: {"name": "Standard G7a Torpedo", "dmg": (35, 55), "cost": 0},
    2: {"name": "Akustischer Torpedo Mk 24", "dmg": (55, 75), "cost": 110},
    3: {"name": "Sauerstoff-Torpedo Typ 93", "dmg": (80, 105), "cost": 250}
}

PLANE_UPGRADES = {
    1: {"name": "SBD Dauntless Bomber", "dmg": (45, 75), "cost": 0},
    2: {"name": "SB2C Helldiver Staffel", "dmg": (70, 100), "cost": 150},
    3: {"name": "A-6 Intruder Jetstaffel", "dmg": (110, 150), "cost": 350}
}

ARMOR_UPGRADES = {
    0: {"name": "Standard-Panzerung", "red": 0.0, "cost": 0},
    1: {"name": "Gürtelpanzerung (-15% Dmg)", "red": 0.15, "cost": 120},
    2: {"name": "Zitadellen-Schutz (-30% Dmg)", "red": 0.30, "cost": 280}
}

HP_UPGRADES = {
    0: {"name": "Standard-Rumpf", "bonus": 0, "cost": 0},
    1: {"name": "Verstärkte Schottwände (+40 HP)", "bonus": 40, "cost": 130},
    2: {"name": "Doppelter Stahlrumpf (+90 HP)", "bonus": 90, "cost": 300}
}

# Schiffswerte-Initialisierung
if "ship_stats" not in st.session_state:
    st.session_state.ship_stats = {
        "Schnellboot": {
            "hp": 45, "base_max_hp": 45, "max_hp": 45, "ammo": 24, 
            "armor_level": 0, "hp_level": 0, "torpedo_level": 1,
            "desc": "Extrem wendig (Ausweichchance), greift nur mit Torpedos an."
        },
        "Zerstörer": {
            "hp": 75, "base_max_hp": 75, "max_hp": 75, "ammo": 40, 
            "armor_level": 0, "hp_level": 0, "torpedo_level": 1,
            "desc": "Schnell & getarnt (Nebelwand), fokussiert auf Torpedoangriffe."
        },
        "Panzerkreuzer": {
            "hp": 110, "base_max_hp": 110, "max_hp": 110, "ammo": 60, 
            "armor_level": 0, "hp_level": 0, "cruiser_gun_level": 1, "torpedo_level": 1,
            "desc": "Ausgewogener Allrounder mit mittleren Geschützen & Torpedos."
        },
        "Schlachtschiff": {
            "hp": 200, "base_max_hp": 200, "max_hp": 200, "ammo": 80, 
            "armor_level": 0, "hp_level": 0, "bs_gun_level": 1,
            "desc": "Schwimmende Festung. Enormer Schaden durch schwerste Artillerie, keine Torpedos."
        },
        "Flugzeugträger": {
            "hp": 130, "base_max_hp": 130, "max_hp": 130, "planes": 15, "max_planes": 15, 
            "armor_level": 0, "hp_level": 0, "plane_level": 1,
            "desc": "Greift über Distanz mit Flugzeugstaffeln an."
        }
    }

def add_log(msg):
    st.session_state.log.insert(0, msg)

current_ship = st.session_state.ship_class
ship_data = st.session_state.ship_stats[current_ship]

# --- SIDEBAR ---
st.sidebar.markdown("## ⚓ FLOTTEN-DASHBOARD")
st.sidebar.markdown(f"**Rang / Niveau:** Level {st.session_state.victories + 1}")
st.sidebar.markdown(f"**Aktuelles Schiff:** {current_ship}")
st.sidebar.progress(max(0.0, min(1.0, ship_data["hp"] / ship_data["max_hp"])), 
                    text=f"Hülle: {ship_data['hp']}/{ship_data['max_hp']} HP")

if current_ship == "Flugzeugträger":
    st.sidebar.metric("Flugzeuge ✈️", f"{ship_data['planes']} / {ship_data['max_planes']}")
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

# GAME OVER HANDLER
if ship_data["hp"] <= 0:
    st.error(f"💥 IHR SCHIFF WURDE ZERSTÖRT! Mission gescheitert.")
    if st.button("Schiff für 50 G bergen & reparieren"):
        if st.session_state.credits >= 50:
            st.session_state.credits -= 50
            ship_data["hp"] = ship_data["max_hp"]
            st.session_state.view = "hq"
            add_log("🛠️ Schiff geborgen und neu aufgestellt.")
            st.rerun()
        else:
            st.error("Insolvent! Nicht genug Credits zur Bergung.")
            if st.button("Neues Spiel beginnen"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

# --- VIEW 1: HQ ---
elif st.session_state.view == "hq":
    st.subheader("🌐 Befehlslage & Flotten-Hangar")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        render_image(f"{current_ship.lower()}.png", f"Flaggschiff: {current_ship}")
    
    with col2:
        st.markdown("### 🛳️ Schiffsklasse wählen")
        selected_ship = st.selectbox("Aktives Flaggschiff:", st.session_state.unlocked_ships, index=st.session_state.unlocked_ships.index(current_ship))
        if selected_ship != current_ship:
            st.session_state.ship_class = selected_ship
            add_log(f"Kommando gewechselt auf: {selected_ship}")
            st.rerun()

        st.caption(f"ℹ️ {ship_data['desc']}")
        st.markdown("---")
        st.markdown("### 📊 Bewaffnung & Stats")
        st.write(f"- ❤️ **Max HP:** {ship_data['max_hp']} HP")
        
        if current_ship in ["Schnellboot", "Zerstörer"]:
            t_info = TORPEDO_UPGRADES[ship_data["torpedo_level"]]
            st.write(f"- 🚀 **Torpedos:** {t_info['name']} (`{t_info['dmg'][0]}-{t_info['dmg'][1]}` HP)")
        elif current_ship == "Panzerkreuzer":
            g_info = CRUISER_GUNS[ship_data["cruiser_gun_level"]]
            t_info = TORPEDO_UPGRADES[ship_data["torpedo_level"]]
            st.write(f"- 💥 **Mittlere Artillerie:** {g_info['name']} (`{g_info['dmg'][0]}-{g_info['dmg'][1]}` HP)")
            st.write(f"- 🚀 **Torpedos:** {t_info['name']} (`{t_info['dmg'][0]}-{t_info['dmg'][1]}` HP)")
        elif current_ship == "Schlachtschiff":
            g_info = BATTLESHIP_GUNS[ship_data["bs_gun_level"]]
            st.write(f"- 💥 **Schwerste Artillerie:** {g_info['name']} (`{g_info['dmg'][0]}-{g_info['dmg'][1]}` HP)")
        elif current_ship == "Flugzeugträger":
            p_info = PLANE_UPGRADES[ship_data["plane_level"]]
            st.write(f"- ✈️ **Staffel:** {p_info['name']} (`{p_info['dmg'][0]}-{p_info['dmg'][1]}` HP)")

        st.write(f"- 🛡️ **Panzerung:** {ARMOR_UPGRADES[ship_data['armor_level']]['name']}")

        st.markdown("---")
        if st.button("🚀 Feindbegegnung suchen"):
            st.session_state.view = "combat"
            lvl = st.session_state.victories
            enemy_types = [
                ("Spähboot", 35 + lvl*8, 5 + lvl*2, 10 + lvl*2, 20 + lvl*5),
                ("Fregatte", 65 + lvl*12, 8 + lvl*2, 18 + lvl*3, 35 + lvl*8),
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
            
            add_log(f"⚠️ FEINDKONTAKT: {st.session_state.enemy_name} (HP: {st.session_state.enemy_hp})")
            st.rerun()
            
        if st.button("⚓ Drydock & Werft (Upgrades)"):
            st.session_state.view = "dock"
            st.rerun()

# --- VIEW 2: DOCK ---
elif st.session_state.view == "dock":
    st.subheader(f"⚓ Marine-Werft: Arsenalkatalog für {current_ship}")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🛠️ Reparieren (+40 HP) - 25 G"):
            if st.session_state.credits >= 25:
                st.session_state.credits -= 25
                ship_data["hp"] = min(ship_data["max_hp"], ship_data["hp"] + 40)
                add_log("🔧 Hülle repariert.")
                st.rerun()
    with c2:
        if current_ship == "Flugzeugträger":
            if st.button("✈️ Flugzeuge (+5) - 30 G"):
                if st.session_state.credits >= 30:
                    st.session_state.credits -= 30
                    ship_data["planes"] = min(ship_data["max_planes"], ship_data["planes"] + 5)
                    add_log("✈️ Staffel aufgestockt.")
                    st.rerun()
        else:
            if st.button("💣 Munition (+25) - 20 G"):
                if st.session_state.credits >= 20:
                    st.session_state.credits -= 20
                    ship_data["ammo"] += 25
                    add_log("💣 Munition nachgeladen.")
                    st.rerun()

    # --- GESCHÜTZE ---
    if current_ship == "Panzerkreuzer":
        st.markdown("---")
        st.markdown("### 💥 Mittlere Artillerie (Kreuzer-Geschütze)")
        cols_g = st.columns(2)
        for lvl in [2, 3]:
            info = CRUISER_GUNS[lvl]
            with cols_g[lvl-2]:
                st.markdown(f"**Stufe {lvl}: {info['name']}**")
                st.write(f"Schaden: `{info['dmg'][0]}-{info['dmg'][1]}`")
                st.caption(f"Preis: {info['cost']} G")
                if ship_data.get("cruiser_gun_level") == lvl:
                    st.success("✅ Ausgerüstet")
                else:
                    if st.button(f"Kaufen ({info['cost']} G)", key=f"cgun_{lvl}"):
                        if st.session_state.credits >= info["cost"]:
                            st.session_state.credits -= info["cost"]
                            ship_data["cruiser_gun_level"] = lvl
                            add_log(f"💥 Kreuzer-Geschütz auf Stufe {lvl} aufgerüstet!")
                            st.rerun()

    elif current_ship == "Schlachtschiff":
        st.markdown("---")
        st.markdown("### 💥 Schwerste Artillerie (Schlachtschiff-Hauptkanonen)")
        cols_g = st.columns(2)
        for lvl in [2, 3]:
            info = BATTLESHIP_GUNS[lvl]
            with cols_g[lvl-2]:
                st.markdown(f"**Stufe {lvl}: {info['name']}**")
                st.write(f"Schaden: `{info['dmg'][0]}-{info['dmg'][1]}`")
                st.caption(f"Preis: {info['cost']} G")
                if ship_data.get("bs_gun_level") == lvl:
                    st.success("✅ Ausgerüstet")
                else:
                    if st.button(f"Kaufen ({info['cost']} G)", key=f"bsgun_{lvl}"):
                        if st.session_state.credits >= info["cost"]:
                            st.session_state.credits -= info["cost"]
                            ship_data["bs_gun_level"] = lvl
                            add_log(f"💥 Schweres Schlachtschiff-Geschütz auf Stufe {lvl} aufgerüstet!")
                            st.rerun()

    # TORPEDOS (Schnellboot, Zerstörer & Panzerkreuzer)
    if current_ship in ["Schnellboot", "Zerstörer", "Panzerkreuzer"]:
        st.markdown("---")
        st.markdown("### 🚀 Torpedo-Systeme")
        cols_t = st.columns(2)
        for lvl in [2, 3]:
            info = TORPEDO_UPGRADES[lvl]
            with cols_t[lvl-2]:
                st.markdown(f"**Stufe {lvl}: {info['name']}**")
                st.write(f"Schaden: `{info['dmg'][0]}-{info['dmg'][1]}`")
                st.caption(f"Preis: {info['cost']} G")
                if ship_data.get("torpedo_level") == lvl:
                    st.success("✅ Ausgerüstet")
                else:
                    if st.button(f"Kaufen ({info['cost']} G)", key=f"torp_{lvl}"):
                        if st.session_state.credits >= info["cost"]:
                            st.session_state.credits -= info["cost"]
                            ship_data["torpedo_level"] = lvl
                            add_log(f"🚀 Torpedosystem auf Stufe {lvl} aufgerüstet!")
                            st.rerun()

    # --- PANZERUNG & HP ---
    st.markdown("---")
    st.markdown("### 🛡️ Rumpf & Panzerung")
    col_hp, col_arm = st.columns(2)
    with col_hp:
        st.markdown("**HP-Erweiterung (Stufe 2):**")
        info_hp = HP_UPGRADES[2]
        st.caption(f"{info_hp['name']} (+90 HP) - {info_hp['cost']} G")
        if ship_data["hp_level"] < 2:
            if st.button(f"Rumpf aufrüsten ({info_hp['cost']} G)"):
                if st.session_state.credits >= info_hp["cost"]:
                    st.session_state.credits -= info_hp["cost"]
                    ship_data["hp_level"] = 2
                    ship_data["max_hp"] = ship_data["base_max_hp"] + info_hp["bonus"]
                    ship_data["hp"] += 90
                    add_log("❤️ Rumpf auf Stufe 2 verstärkt!")
                    st.rerun()
        else:
            st.success("✅ Rumpf auf Maximum")

    with col_arm:
        st.markdown("**Zitadellen-Panzerung (Stufe 2):**")
        info_arm = ARMOR_UPGRADES[2]
        st.caption(f"{info_arm['name']} (-30% Dmg) - {info_arm['cost']} G")
        if ship_data["armor_level"] < 2:
            if st.button(f"Panzerung installieren ({info_arm['cost']} G)"):
                if st.session_state.credits >= info_arm["cost"]:
                    st.session_state.credits -= info_arm["cost"]
                    ship_data["armor_level"] = 2
                    add_log("🛡️ Schwerste Panzerung installiert!")
                    st.rerun()
        else:
            st.success("✅ Panzerung auf Maximum")

    st.markdown("---")
    if st.button("⬅️ Zurück zum HQ"):
        st.session_state.view = "hq"
        st.rerun()

# --- VIEW 3: KAMPF ---
elif st.session_state.view == "combat":
    st.subheader(f"⚔️ Gefecht: {current_ship} vs. {st.session_state.enemy_name}")
    
    col_p, col_vs, col_e = st.columns([4, 1, 4])
    with col_p:
        render_image(f"{current_ship.lower()}.png", current_ship)
        st.progress(max(0.0, min(1.0, ship_data["hp"] / ship_data["max_hp"])))
        st.caption(f"HP: {ship_data['hp']} / {ship_data['max_hp']} | Panzerung: {ARMOR_UPGRADES[ship_data['armor_level']]['name']}")

    with col_vs:
        st.markdown("<h1 style='text-align: center; color: #ef4444;'>VS</h1>", unsafe_allow_html=True)

    with col_e:
        render_image("enemy_ship.png", st.session_state.enemy_name)
        st.progress(max(0.0, min(1.0, st.session_state.enemy_hp / st.session_state.enemy_max_hp)))
        st.caption(f"HP: {st.session_state.enemy_hp} / {st.session_state.enemy_max_hp}")

    st.markdown("---")
    b1, b2, b3 = st.columns(3)
    
    if current_ship == "Schnellboot":
        t_info = TORPEDO_UPGRADES[ship_data["torpedo_level"]]
        with b1:
            if st.button(f"🚀 {t_info['name']} [-5 Mun]"):
                if ship_data["ammo"] >= 5:
                    ship_data["ammo"] -= 5
                    dmg = random.randint(t_info["dmg"][0], t_info["dmg"][1])
                    st.session_state.enemy_hp -= dmg
                    add_log(f"🚀 Schnellboot-Torpedo trifft für {dmg} Schaden!")
                st.rerun()
        with b2:
            if st.button("⚡ High-Speed-Ausweichen"):
                add_log("⚡ Schnellboot schlägt Zick-Zack-Kurs ein!")
                st.rerun()

    elif current_ship == "Zerstörer":
        t_info = TORPEDO_UPGRADES[ship_data["torpedo_level"]]
        with b1:
            if st.button(f"🚀 {t_info['name']} [-8 Mun]"):
                if ship_data["ammo"] >= 8:
                    ship_data["ammo"] -= 8
                    dmg = random.randint(t_info["dmg"][0], t_info["dmg"][1])
                    st.session_state.enemy_hp -= dmg
                    add_log(f"🚀 Torpedo trifft für {dmg} Schaden!")
                st.rerun()
        with b2:
            if st.button("💨 Nebelwand legen"):
                add_log("🛡️ In Nebelwand abgetaucht!")
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
                    add_log(f"💥 Kanone trifft für {dmg} Schaden.")
                st.rerun()
        with b2:
            if st.button(f"🚀 {t_info['name']} [-10 Mun]"):
                if ship_data["ammo"] >= 10:
                    ship_data["ammo"] -= 10
                    dmg = random.randint(t_info["dmg"][0], t_info["dmg"][1])
                    st.session_state.enemy_hp -= dmg
                    add_log(f"🚀 Torpedo trifft für {dmg} Schaden!")
                st.rerun()

    elif current_ship == "Schlachtschiff":
        g_info = BATTLESHIP_GUNS[ship_data["bs_gun_level"]]
        with b1:
            if st.button(f"💥 Brecher-Breitseite: {g_info['name']} [-12 Mun]"):
                if ship_data["ammo"] >= 12:
                    ship_data["ammo"] -= 12
                    dmg = random.randint(g_info["dmg"][0], g_info["dmg"][1])
                    st.session_state.enemy_hp -= dmg
                    add_log(f"💥 ZERSTÖRERISCHE BREITSEITE trifft für {dmg} Schaden!")
                st.rerun()
        with b2:
            if st.button("🛡️ Schadenskontroll-Team"):
                ship_data["hp"] = min(ship_data["max_hp"], ship_data["hp"] + 20)
                add_log("🛠️ Crew führt Reparaturen durch (+20 HP).")
                st.rerun()

    elif current_ship == "Flugzeugträger":
        p_info = PLANE_UPGRADES[ship_data["plane_level"]]
        with b1:
            if st.button(f"✈️ {p_info['name']}"):
                if ship_data["planes"] > 0:
                    dmg = random.randint(p_info["dmg"][0], p_info["dmg"][1])
                    st.session_state.enemy_hp -= dmg
                    if random.random() < 0.3:
                        ship_data["planes"] -= 1
                    add_log(f"✈️ Luftschlag trifft für {dmg} Schaden!")
                st.rerun()

    with b3:
        if st.button("🏃 Rückzug"):
            st.session_state.view = "hq"
            add_log("Rückzug angetreten.")
            st.rerun()

    # FEINDREAKTION
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
        
        # Schnellboot hat 40% Ausweichchance
        if current_ship == "Schnellboot" and random.random() < 0.40:
            add_log("💨 Schnellboot ist dem Gegner durch Tempo ausgewichen!")
        else:
            red = ARMOR_UPGRADES[ship_data["armor_level"]]["red"]
            actual_dmg = int(raw_dmg * (1.0 - red))
            ship_data["hp"] -= actual_dmg

# LOG
st.markdown("---")
st.subheader("📜 Logbuch")
for log_entry in st.session_state.log[:4]:
    st.text(log_entry)

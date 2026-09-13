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

# Global Session State
if "view" not in st.session_state:
    st.session_state.view = "hq"
if "ship_class" not in st.session_state:
    st.session_state.ship_class = "Panzerkreuzer"
if "unlocked_ships" not in st.session_state:
    st.session_state.unlocked_ships = ["Schnellboot", "Zerstörer", "Panzerkreuzer", "Schlachtschiff", "Flugzeugträger"]
if "credits" not in st.session_state:
    st.session_state.credits = 150  # Ausgewogenes Startkapital
if "victories" not in st.session_state:
    st.session_state.victories = 0
if "log" not in st.session_state:
    st.session_state.log = ["Flottenkommando bereit. Belohnungs-Balancing überarbeitet!"]

GUN_UPGRADES = {
    1: {"name": "5-Zoll/38-Kaliber", "dmg": (20, 35), "cost": 0},
    2: {"name": "8-Zoll/55-Kaliber Mark 12", "dmg": (35, 50), "cost": 120},
    3: {"name": "16-Zoll/50-Kaliber Mark 7", "dmg": (55, 75), "cost": 280},
    4: {"name": "18-Zoll/45-Kaliber Schweres Geschütz", "dmg": (80, 110), "cost": 500}
}

TORPEDO_UPGRADES = {
    1: {"name": "Standard G7a Torpedo", "dmg": (35, 55), "cost": 0},
    2: {"name": "Akustischer Torpedo Mk 24", "dmg": (55, 75), "cost": 110},
    3: {"name": "Sauerstoff-Torpedo Typ 93", "dmg": (80, 105), "cost": 250},
    4: {"name": "Schwerer Homing-Torpedo Mk 48", "dmg": (110, 145), "cost": 480}
}

PLANE_UPGRADES = {
    1: {"name": "SBD Dauntless (Propeller)", "dmg": (45, 75), "cost": 0},
    2: {"name": "SB2C Helldiver (Erweitert)", "dmg": (70, 100), "cost": 150},
    3: {"name": "F-4 Phantom Jetbomber", "dmg": (100, 140), "cost": 320},
    4: {"name": "A-6 Intruder Stealth-Bomber", "dmg": (145, 190), "cost": 550}
}

ARMOR_UPGRADES = {
    0: {"name": "Keine Panzerung (0 cm)", "red": 0.0, "cost": 0},
    1: {"name": "Leichte Panzerung (10 cm / -10% Dmg)", "red": 0.10, "cost": 90},
    2: {"name": "Mittlere Panzerung (20 cm / -20% Dmg)", "red": 0.20, "cost": 220},
    3: {"name": "Schwere Gürtelpanzerung (30 cm / -30% Dmg)", "red": 0.30, "cost": 450}
}

HP_UPGRADES = {
    0: {"name": "Standard-Rumpf", "bonus": 0, "cost": 0},
    1: {"name": "Verstärkte Schottwände (+30 HP)", "bonus": 30, "cost": 110},
    2: {"name": "Doppelter Stahlrumpf (+70 HP)", "bonus": 70, "cost": 260},
    3: {"name": "Titan-Schiffs Panzer (+120 HP)", "bonus": 120, "cost": 480}
}

if "ship_stats" not in st.session_state:
    st.session_state.ship_stats = {
        "Schnellboot": {"hp": 50, "base_max_hp": 50, "max_hp": 50, "ammo": 30, "armor_level": 0, "hp_level": 0, "torpedo_level": 1},
        "Zerstörer": {"hp": 80, "base_max_hp": 80, "max_hp": 80, "ammo": 50, "armor_level": 0, "hp_level": 0, "torpedo_level": 1},
        "Panzerkreuzer": {"hp": 110, "base_max_hp": 110, "max_hp": 110, "ammo": 60, "armor_level": 0, "hp_level": 0, "gun_level": 1, "torpedo_level": 1},
        "Schlachtschiff": {"hp": 180, "base_max_hp": 180, "max_hp": 180, "ammo": 80, "armor_level": 0, "hp_level": 0, "gun_level": 1},
        "Flugzeugträger": {"hp": 140, "base_max_hp": 140, "max_hp": 140, "planes": 20, "max_planes": 20, "armor_level": 0, "hp_level": 0, "plane_level": 1}
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
    st.error(f"💥 IHR SCHIFF WURDE IM KAMPF ZERSTÖRT! Mission gescheitert.")
    if st.button("Schiff für 50 G bergen & reparieren"):
        if st.session_state.credits >= 50:
            st.session_state.credits -= 50
            ship_data["hp"] = ship_data["max_hp"]
            st.session_state.view = "hq"
            add_log("🛠️ Schiff geborgen und im HQ neu aufgestellt.")
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
    
    img_name = f"{current_ship.lower()}.png"
    with col1:
        render_image(img_name, f"Flaggschiff: {current_ship}")
    
    with col2:
        st.markdown("### 🛳️ Schiffsklasse wählen")
        selected_ship = st.selectbox("Aktives Flaggschiff:", st.session_state.unlocked_ships, index=st.session_state.unlocked_ships.index(current_ship))
        if selected_ship != current_ship:
            st.session_state.ship_class = selected_ship
            add_log(f"Kommando gewechselt auf: {selected_ship}")
            st.rerun()

        st.markdown("---")
        st.markdown("### 📊 Aktuelle Bewaffnung & Stats")
        st.write(f"- ❤️ **Max HP:** {ship_data['max_hp']} HP")
        
        if current_ship == "Schnellboot":
            t_info = TORPEDO_UPGRADES[ship_data["torpedo_level"]]
            st.write(f"- 🚀 **Torpedos:** {t_info['name']} (`{t_info['dmg'][0]}-{t_info['dmg'][1]}` HP)")
            st.write(f"- ⚡ **Eigenschaft:** Hohe Ausweichchance")
        elif current_ship == "Zerstörer":
            t_info = TORPEDO_UPGRADES[ship_data["torpedo_level"]]
            st.write(f"- 🚀 **Torpedos:** {t_info['name']} (`{t_info['dmg'][0]}-{t_info['dmg'][1]}` HP)")
            st.write(f"- 💨 **Eigenschaft:** Nebelwand-Tarnung")
        elif current_ship == "Panzerkreuzer":
            g_info = GUN_UPGRADES[ship_data["gun_level"]]
            t_info = TORPEDO_UPGRADES[ship_data["torpedo_level"]]
            st.write(f"- 💥 **Geschütz:** {g_info['name']} (`{g_info['dmg'][0]}-{g_info['dmg'][1]}` HP)")
            st.write(f"- 🚀 **Torpedos:** {t_info['name']} (`{t_info['dmg'][0]}-{t_info['dmg'][1]}` HP)")
        elif current_ship == "Schlachtschiff":
            g_info = GUN_UPGRADES[ship_data["gun_level"]]
            st.write(f"- 💥 **Schwere Artillerie:** {g_info['name']} (`{g_info['dmg'][0]}-{g_info['dmg'][1]}` HP)")
            st.write(f"- 🛡️ **Eigenschaft:** Hohe Panzerung & HP")
        elif current_ship == "Flugzeugträger":
            p_info = PLANE_UPGRADES[ship_data["plane_level"]]
            st.write(f"- ✈️ **Staffel:** {p_info['name']} (`{p_info['dmg'][0]}-{p_info['dmg'][1]}` HP)")

        st.write(f"- 🛡️ **Panzerung:** {ARMOR_UPGRADES[ship_data['armor_level']]['name']}")

        st.markdown("---")
        if st.button("🚀 Feindbegegnung suchen"):
            st.session_state.view = "combat"
            
            lvl = st.session_state.victories
            # Reduzierte Belohnungen für besseres Balancing
            enemy_types = [
                ("Spähboot", 35 + lvl*8, 5 + lvl*2, 10 + lvl*2, 15 + lvl*5),
                ("Fregatte", 65 + lvl*12, 8 + lvl*2, 18 + lvl*3, 30 + lvl*8),
                ("Panzerschiff", 110 + lvl*15, 12 + lvl*3, 25 + lvl*4, 55 + lvl*12),
                ("Elite-Schlachtschiff", 160 + lvl*25, 20 + lvl*4, 38 + lvl*5, 90 + lvl*20)
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
                    add_log("✈️ Nachschub geliefert.")
                    st.rerun()
        else:
            if st.button("💣 Munition (+25) - 20 G"):
                if st.session_state.credits >= 20:
                    st.session_state.credits -= 20
                    ship_data["ammo"] += 25
                    add_log("💣 Munition geladen.")
                    st.rerun()

    # --- HP UPGRADES ---
    st.markdown("---")
    st.markdown("### ❤️ Max-HP & Rumpf-Verstärkung")
    cols_hp = st.columns(3)
    for lvl in range(1, 4):
        info = HP_UPGRADES[lvl]
        with cols_hp[lvl-1]:
            st.markdown(f"**Stufe {lvl}: {info['name']}**")
            st.caption(f"Preis: {info['cost']} G")
            if ship_data["hp_level"] == lvl:
                st.success("✅ Ausgerüstet")
            else:
                if st.button(f"Ausrüsten ({info['cost']} G)", key=f"hp_{lvl}"):
                    if st.session_state.credits >= info["cost"]:
                        st.session_state.credits -= info["cost"]
                        hp_diff = info["bonus"] - HP_UPGRADES[ship_data["hp_level"]]["bonus"]
                        ship_data["hp_level"] = lvl
                        ship_data["max_hp"] = ship_data["base_max_hp"] + info["bonus"]
                        ship_data["hp"] = max(1, ship_data["hp"] + hp_diff)
                        add_log(f"❤️ Max-HP erhöht auf {ship_data['max_hp']}!")
                        st.rerun()

    # --- PANZERUNGS UPGRADES ---
    st.markdown("---")
    st.markdown("### 🛡️ Panzerungs-Upgrades")
    cols_arm = st.columns(3)
    for lvl in range(1, 4):
        info = ARMOR_UPGRADES[lvl]
        with cols_arm[lvl-1]:
            st.markdown(f"**Stufe {lvl}: {info['name']}**")
            st.caption(f"Preis: {info['cost']} G")
            if ship_data["armor_level"] == lvl:
                st.success("✅ Ausgerüstet")
            else:
                if st.button(f"Ausrüsten ({info['cost']} G)", key=f"arm_{lvl}"):
                    if st.session_state.credits >= info["cost"]:
                        st.session_state.credits -= info["cost"]
                        ship_data["armor_level"] = lvl
                        add_log(f"🛡️ Panzerung gewechselt auf Stufe {lvl}!")
                        st.rerun()

    # GESCHÜTZE (Panzerkreuzer & Schlachtschiff)
    if current_ship in ["Panzerkreuzer", "Schlachtschiff"]:
        st.markdown("---")
        st.markdown("### 💥 Geschütz-Upgrades")
        cols_g = st.columns(3)
        for lvl in range(2, 5):
            info = GUN_UPGRADES[lvl]
            with cols_g[lvl-2]:
                st.markdown(f"**Stufe {lvl}: {info['name']}**")
                st.write(f"Schaden: `{info['dmg'][0]}-{info['dmg'][1]}`")
                st.caption(f"Preis: {info['cost']} G")
                if ship_data.get("gun_level") == lvl:
                    st.success("✅ Ausgerüstet")
                else:
                    if st.button(f"Ausrüsten ({info['cost']} G)", key=f"gun_{lvl}"):
                        if st.session_state.credits >= info["cost"]:
                            st.session_state.credits -= info["cost"]
                            ship_data["gun_level"] = lvl
                            add_log(f"💥 Geschütz gewechselt auf Stufe {lvl}!")
                            st.rerun()

    # TORPEDOS (Schnellboot, Zerstörer & Panzerkreuzer)
    if current_ship in ["Schnellboot", "Zerstörer", "Panzerkreuzer"]:
        st.markdown("---")
        st.markdown("### 🚀 Torpedo-Upgrades")
        cols_t = st.columns(3)
        for lvl in range(2, 5):
            info = TORPEDO_UPGRADES[lvl]
            with cols_t[lvl-2]:
                st.markdown(f"**Stufe {lvl}: {info['name']}**")
                st.write(f"Schaden: `{info['dmg'][0]}-{info['dmg'][1]}`")
                st.caption(f"Preis: {info['cost']} G")
                if ship_data.get("torpedo_level") == lvl:
                    st.success("✅ Ausgerüstet")
                else:
                    if st.button(f"Ausrüsten ({info['cost']} G)", key=f"torp_{lvl}"):
                        if st.session_state.credits >= info["cost"]:
                            st.session_state.credits -= info["cost"]
                            ship_data["torpedo_level"] = lvl
                            add_log(f"🚀 Torpedo gewechselt auf Stufe {lvl}!")
                            st.rerun()

    # STAFFELN (Flugzeugträger)
    if current_ship == "Flugzeugträger":
        st.markdown("---")
        st.markdown("### ✈️ Staffel-Upgrades")
        cols_p = st.columns(3)
        for lvl in range(2, 5):
            info = PLANE_UPGRADES[lvl]
            with cols_p[lvl-2]:
                st.markdown(f"**Stufe {lvl}: {info['name']}**")
                st.write(f"Schaden: `{info['dmg'][0]}-{info['dmg'][1]}`")
                st.caption(f"Preis: {info['cost']} G")
                if ship_data["plane_level"] == lvl:
                    st.success("✅ Ausgerüstet")
                else:
                    if st.button(f"Ausrüsten ({info['cost']} G)", key=f"plane_{lvl}"):
                        if st.session_state.credits >= info["cost"]:
                            st.session_state.credits -= info["cost"]
                            ship_data["plane_level"] = lvl
                            add_log(f"✈️ Staffel gewechselt auf Stufe {lvl}!")
                            st.rerun()

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
            if st.button(f"🚀 {t_info['name']} [-6 Mun]"):
                if ship_data["ammo"] >= 6:
                    ship_data["ammo"] -= 6
                    dmg = random.randint(t_info["dmg"][0], t_info["dmg"][1])
                    st.session_state.enemy_hp -= dmg
                    add_log(f"🚀 Schnellboot-Torpedo trifft für {dmg} Schaden!")
                st.rerun()
        with b2:
            if st.button("⚡ High-Speed Ausweichen"):
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
        g_info = GUN_UPGRADES[ship_data["gun_level"]]
        t_info = TORPEDO_UPGRADES[ship_data["torpedo_level"]]
        with b1:
            if st.button(f"💥 {g_info['name']} [-5 Mun]"):
                if ship_data["ammo"] >= 5:
                    ship_data["ammo"] -= 5
                    dmg = random.randint(g_info["dmg"][0], g_info["dmg"][1])
                    st.session_state.enemy_hp -= dmg
                    add_log(f"💥 Kanone trifft für {dmg} Schaden.")
                st.rerun()
        with b2:
            if st.button(f"🚀 {t_info['name']} [-12 Mun]"):
                if ship_data["ammo"] >= 12:
                    ship_data["ammo"] -= 12
                    dmg = random.randint(t_info["dmg"][0], t_info["dmg"][1])
                    st.session_state.enemy_hp -= dmg
                    add_log(f"🚀 Torpedo trifft für {dmg} Schaden!")
                st.rerun()

    elif current_ship == "Schlachtschiff":
        g_info = GUN_UPGRADES[ship_data["gun_level"]]
        with b1:
            if st.button(f"💥 Breitseite: {g_info['name']} [-10 Mun]"):
                if ship_data["ammo"] >= 10:
                    ship_data["ammo"] -= 10
                    dmg = int(random.randint(g_info["dmg"][0], g_info["dmg"][1]) * 1.25)
                    st.session_state.enemy_hp -= dmg
                    add_log(f"💥 Massive Breitseite trifft für {dmg} Schaden!")
                st.rerun()
        with b2:
            if st.button("🛡️ Schadenskontrolle"):
                ship_data["hp"] = min(ship_data["max_hp"], ship_data["hp"] + 15)
                add_log("🛠️ Crew führt Notfall-Reparaturen durch (+15 HP).")
                st.rerun()

    elif current_ship == "Flugzeugträger":
        p_info = PLANE_UPGRADES[ship_data["plane_level"]]
        with b1:
            if st.button(f"✈️ {p_info['name']}"):
                if ship_data["planes"] > 0:
                    dmg = random.randint(p_info["dmg"][0], p_info["dmg"][1])
                    st.session_state.enemy_hp -= dmg
                    lost = random.choice([0, 0, 1])
                    ship_data["planes"] = max(0, ship_data["planes"] - lost)
                    add_log(f"✈️ Luftschlag trifft für {dmg} Schaden!")
                st.rerun()
        with b2:
            if st.button("🛡️ Jäger-Eskorte"):
                add_log("🛡️ Luftraum gesichert.")
                st.rerun()

    with b3:
        if st.button("🏃 Rückzug"):
            st.session_state.view = "hq"
            add_log("Rückzug angetreten. Gefecht abgebrochen.")
            st.rerun()

    if st.session_state.enemy_hp <= 0:
        st.balloons()
        reward = st.session_state.reward
        st.session_state.credits += reward
        st.session_state.victories += 1
        add_log(f"🎉 SIEG! Feind zerstört (+{reward} G). Rang gestiegen!")
        st.session_state.view = "hq"
        st.rerun()
    elif st.session_state.enemy_hp < st.session_state.enemy_max_hp:
        raw_dmg = random.randint(st.session_state.enemy_min_dmg, st.session_state.enemy_max_dmg)
        
        # Schnellboot-Ausweichchance
        if current_ship == "Schnellboot" and random.random() < 0.35:
            add_log("💨 Schnellboot ist dem Ausweichmanöver geglückt!")
        else:
            red = ARMOR_UPGRADES[ship_data["armor_level"]]["red"]
            actual_dmg = int(raw_dmg * (1.0 - red))
            ship_data["hp"] -= actual_dmg

# LOG
st.markdown("---")
st.subheader("📜 Logbuch")
for log_entry in st.session_state.log[:4]:
    st.text(log_entry)

import streamlit as st
import random
import os

# Page configuration
st.set_page_config(page_title="Sea of Seas", page_icon="⚓", layout="wide")

# Custom CSS styling for a naval dashboard feel
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        font-weight: bold;
    }
    .metric-box {
        background-color: #1e293b;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

# Grid Settings
GRID_SIZE = 6

# Initialize session state variables
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "player_pos" not in st.session_state:
    st.session_state.player_pos = [0, 0]
if "fleet_hp" not in st.session_state:
    st.session_state.fleet_hp = 100
if "max_hp" not in st.session_state:
    st.session_state.max_hp = 100
if "ammo" not in st.session_state:
    st.session_state.ammo = 50
if "credits" not in st.session_state:
    st.session_state.credits = 100
if "in_combat" not in st.session_state:
    st.session_state.in_combat = False
if "enemy_hp" not in st.session_state:
    st.session_state.enemy_hp = 0
if "enemy_max_hp" not in st.session_state:
    st.session_state.enemy_max_hp = 0
if "log" not in st.session_state:
    st.session_state.log = ["Willkommen auf den Meeren, Kapitän!"]

# Map items generator
if "map_items" not in st.session_state:
    items = {}
    # Place Port at bottom-right
    items[(5, 5)] = "port"
    # Place some enemies and treasure randomly
    random.seed(42)  # Fixed layout per game restart
    for _ in range(4):
        rx, ry = random.randint(0, 5), random.randint(0, 5)
        if (rx, ry) not in [(0, 0), (5, 5)]:
            items[(rx, ry)] = "enemy"
    for _ in range(3):
        rx, ry = random.randint(0, 5), random.randint(0, 5)
        if (rx, ry) not in [(0, 0), (5, 5)] and (rx, ry) not in items:
            items[(rx, ry)] = "treasure"
    st.session_state.map_items = items

def add_log(text):
    st.session_state.log.insert(0, text)

# Function to safely load image if available
def show_image(image_path, caption=""):
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True, caption=caption)
    else:
        st.info(f"📷 [{caption}] (Bild '{image_path}' nicht gefunden)")

# ----------------- MAIN TITLE -----------------
st.title("⚓ Sea of Seas: Tactical Naval Operations")

# Sidebar Status Dashboard
st.sidebar.header("📊 COMMAND DASHBOARD")
st.sidebar.progress(max(0.0, min(1.0, st.session_state.fleet_hp / st.session_state.max_hp)), 
                    text=f"Hülle: {st.session_state.fleet_hp}/{st.session_state.max_hp} HP")
st.sidebar.metric("Munition 💣", f"{st.session_state.ammo} Schuss")
st.sidebar.metric("Schatz / Credits 🪙", f"{st.session_state.credits} G")

if st.sidebar.button("🔄 Spiel neustarten"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Check Game Over
if st.session_state.fleet_hp <= 0:
    st.error("💥 IHRE FLOTTE WURDE ZERSTÖRT! DAS SPIEL IST VORBEI.")
    if st.button("Neues Spiel beginnen"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ----------------- COMBAT DASHBOARD -----------------
elif st.session_state.in_combat:
    st.subheader("⚔️ KAMPFMODUS: FEINDKONTAKT!")
    
    col_play, col_vs, col_ene = st.columns([4, 1, 4])
    
    with col_play:
        st.markdown("### 🚢 Ihr Flaggschiff")
        show_image("player_ship.png", "Black Sea - Panzerkreuzer")
        st.progress(max(0.0, min(1.0, st.session_state.fleet_hp / st.session_state.max_hp)))
        st.caption(f"HP: {st.session_state.fleet_hp} / {st.session_state.max_hp}")

    with col_vs:
        st.markdown("<h2 style='text-align: center; margin-top: 100px;'>VS</h2>", unsafe_allow_html=True)

    with col_ene:
        st.markdown("### 🏴‍☠️ Feindliche Fregatte")
        show_image("enemy_ship.png", "Skull's Grin - Piratenfregatte")
        st.progress(max(0.0, min(1.0, st.session_state.enemy_hp / st.session_state.enemy_max_hp)))
        st.caption(f"HP: {st.session_state.enemy_hp} / {st.session_state.enemy_max_hp}")

    st.markdown("---")
    st.subheader("🎯 Gefechtsbefehle")
    
    btn1, btn2, btn3 = st.columns(3)
    
    with btn1:
        if st.button("💥 Breitseite feuern (-5 Munition)"):
            if st.session_state.ammo >= 5:
                st.session_state.ammo -= 5
                dmg = random.randint(18, 35)
                st.session_state.enemy_hp -= dmg
                add_log(f"⚔️ Breitseite! Feind erleidet {dmg} Schaden.")
                
                # Counter Attack
                if st.session_state.enemy_hp > 0:
                    e_dmg = random.randint(8, 22)
                    st.session_state.fleet_hp -= e_dmg
                    add_log(f"💥 Feind schlägt zurück! {e_dmg} Schaden erlitten.")
                else:
                    st.success("🎉 FEIND ZERSTÖRT! Belohnung: +60 Credits, +15 Munition")
                    st.session_state.credits += 60
                    st.session_state.ammo += 15
                    st.session_state.in_combat = False
                    # Remove enemy from map
                    pos = tuple(st.session_state.player_pos)
                    if pos in st.session_state.map_items:
                        del st.session_state.map_items[pos]
            else:
                st.error("Keine Munition mehr verfügbar!")
            st.rerun()

    with btn2:
        if st.button("🛡️ Ausweichmanöver (Schaden halbieren)"):
            e_dmg = random.randint(3, 10)
            st.session_state.fleet_hp -= e_dmg
            add_log(f"🛡️ Ausweichmanöver ausgeführt. Geringer Schaden erlitten ({e_dmg} HP).")
            st.rerun()

    with btn3:
        if st.button("💨 Fluchtversuch"):
            if random.random() > 0.4:
                st.success("Erfolgreich entkommen!")
                st.session_state.in_combat = False
                add_log("💨 Aus dem Gefecht geflohen.")
            else:
                e_dmg = random.randint(12, 25)
                st.session_state.fleet_hp -= e_dmg
                add_log(f"⚠️ Flucht fehlgeschlagen! Feind trifft das Heck ({e_dmg} Schaden).")
            st.rerun()

# ----------------- MAP & EXPLORATION MODE -----------------
else:
    col_map, col_controls = st.columns([3, 2])
    
    with col_map:
        st.subheader("🗺️ Seekarte der Region")
        
        # Draw 6x6 Grid
        grid_html = ""
        px, py = st.session_state.player_pos
        
        for r in range(GRID_SIZE):
            cols = st.columns(GRID_SIZE)
            for c in range(GRID_SIZE):
                cell_icon = "🌊"
                if [r, c] == [px, py]:
                    cell_icon = "🚢"
                elif (r, c) in st.session_state.map_items:
                    item = st.session_state.map_items[(r, c)]
                    if item == "port":
                        cell_icon = "⚓"
                    elif item == "enemy":
                        cell_icon = "🏴‍☠️"
                    elif item == "treasure":
                        cell_icon = "📦"
                
                cols[c].button(cell_icon, key=f"cell_{r}_{c}", disabled=True)

    with col_controls:
        st.subheader("🧭 Navigationsbrücke")
        st.write(f"Aktuelle Position: **Sektor [{px}, {py}]**")
        
        # Navigation Buttons (D-Pad style)
        _, u_btn, _ = st.columns(3)
        l_btn, _, r_btn = st.columns(3)
        _, d_btn, _ = st.columns(3)
        
        moved = False
        with u_btn:
            if st.button("⬆️ Nord") and px > 0:
                st.session_state.player_pos[0] -= 1
                moved = True
        with l_btn:
            if st.button("⬅️ West") and py > 0:
                st.session_state.player_pos[1] -= 1
                moved = True
        with r_btn:
            if st.button("East ➡️") and py < GRID_SIZE - 1:
                st.session_state.player_pos[1] += 1
                moved = True
        with d_btn:
            if st.button("⬇️ Süd") and px < GRID_SIZE - 1:
                st.session_state.player_pos[0] += 1
                moved = True
                
        if moved:
            pos = tuple(st.session_state.player_pos)
            add_log(f"Neuer Kurs gesetzt: Sektor {pos}")
            
            # Check for events on current cell
            if pos in st.session_state.map_items:
                item_type = st.session_state.map_items[pos]
                
                if item_type == "enemy":
                    st.session_state.in_combat = True
                    st.session_state.enemy_hp = 50
                    st.session_state.enemy_max_hp = 50
                    add_log("⚠️ FEINDKONTAKT! Piratenschiff gesichtet!")
                    st.rerun()
                    
                elif item_type == "treasure":
                    gold = random.randint(30, 80)
                    ammo = random.randint(10, 25)
                    st.session_state.credits += gold
                    st.session_state.ammo += ammo
                    add_log(f"📦 Treibgut aufgefischt! +{gold} Gold, +{ammo} Munition erhalten.")
                    del st.session_state.map_items[pos]
                    st.rerun()

        # Check Port interaction
        if tuple(st.session_state.player_pos) == (5, 5):
            st.markdown("---")
            st.subheader("⚓ Marine-Hafen Fort Vanguard")
            show_image("port.png", "Fort Vanguard - Sichere Zuflucht")
            
            p1, p2 = st.columns(2)
            with p1:
                if st.button("🔧 Flotte reparieren (+40 HP / 40 G)"):
                    if st.session_state.credits >= 40:
                        st.session_state.credits -= 40
                        st.session_state.fleet_hp = min(st.session_state.max_hp, st.session_state.fleet_hp + 40)
                        add_log("🔧 Flotte im Hafen repariert.")
                        st.rerun()
                    else:
                        st.error("Nicht genug Credits!")
            with p2:
                if st.button("💣 Munition aufstocken (+30 Schuss / 30 G)"):
                    if st.session_state.credits >= 30:
                        st.session_state.credits -= 30
                        st.session_state.ammo += 30
                        add_log("💣 Munitionsdepot aufgestockt.")
                        st.rerun()
                    else:
                        st.error("Nicht genug Credits!")

# Log Output Bottom
st.markdown("---")
st.subheader("📜 Logbuch des Kommandanten")
for log_entry in st.session_state.log[:5]:
    st.text(log_entry)

import streamlit as st
import random

# Seite konfigurieren
st.set_page_config(page_title="Sea of Seas", page_icon="⚓", layout="wide")

st.title("⚓ Sea of Seas - Tactical Fleet Commander")

# Spielstatus initialisieren
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "fleet_hp" not in st.session_state:
    st.session_state.fleet_hp = 100
if "max_hp" not in st.session_state:
    st.session_state.max_hp = 100
if "ammo" not in st.session_state:
    st.session_state.ammo = 50
if "credits" not in st.session_state:
    st.session_state.credits = 100
if "day" not in st.session_state:
    st.session_state.day = 1
if "log" not in st.session_state:
    st.session_state.log = []
if "enemy_hp" not in st.session_state:
    st.session_state.enemy_hp = 0
if "in_combat" not in st.session_state:
    st.session_state.in_combat = False

# Funktion für Logbucheinträge
def add_log(text):
    st.session_state.log.insert(0, f"Tag {st.session_state.day}: {text}")

# ----------------- KAPITÄNS-AUSWAHL -----------------
if not st.session_state.game_started:
    st.subheader("Wilkommen, Kommandant! Wählen Sie Ihre Startflotte:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("### 🚤 Schnelle EsSKORTE")
        st.write("- **Hülle:** 80")
        st.write("- **Munition:** 70")
        st.write("- **Start-Credits:** 150")
        if st.button("Eskorte wählen"):
            st.session_state.fleet_hp = 80
            st.session_state.max_hp = 80
            st.session_state.ammo = 70
            st.session_state.credits = 150
            st.session_state.game_started = True
            add_log("Kommando über die Schnelle Eskorte übernommen.")
            st.rerun()

    with col2:
        st.write("### 🛳️ Schlachtflotte")
        st.write("- **Hülle:** 120")
        st.write("- **Munition:** 40")
        st.write("- **Start-Credits:** 100")
        if st.button("Schlachtflotte wählen"):
            st.session_state.fleet_hp = 120
            st.session_state.max_hp = 120
            st.session_state.ammo = 40
            st.session_state.credits = 100
            st.session_state.game_started = True
            add_log("Kommando über die Schlachtflotte übernommen.")
            st.rerun()

    with col3:
        st.write("### ⚓ Ausgewogene Task Force")
        st.write("- **Hülle:** 100")
        st.write("- **Munition:** 50")
        st.write("- **Start-Credits:** 100")
        if st.button("Task Force wählen"):
            st.session_state.fleet_hp = 100
            st.session_state.max_hp = 100
            st.session_state.ammo = 50
            st.session_state.credits = 100
            st.session_state.game_started = True
            add_log("Kommando über die Task Force übernommen.")
            st.rerun()

# ----------------- SPIELSCHLEIFE -----------------
else:
    # Statusleiste oben anzeigen
    st.sidebar.header("📊 Flottenstatus")
    st.sidebar.metric("Tag auf See", st.session_state.day)
    st.sidebar.progress(st.session_state.fleet_hp / st.session_state.max_hp, text=f"Hülle: {st.session_state.fleet_hp}/{st.session_state.max_hp}")
    st.sidebar.metric("Munition", f"{st.session_state.ammo} Schuss")
    st.sidebar.metric("Credits", f"{st.session_state.credits} 🪙")
    
    if st.sidebar.button("Game Reset / Neustart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # Game Over Prüfung
    if st.session_state.fleet_hp <= 0:
        st.error("💥 Ihre Flotte wurde zerstört! Das Spiel ist vorbei.")
        if st.button("Neues Spiel starten"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    else:
        # KAMPFMODUS
        if st.session_state.in_combat:
            st.warning("⚠️ **FEINDKONTAKT! Ein feindlicher Verband greift an!**")
            st.write(f"Feindliche Flottenstärke: **{st.session_state.enemy_hp} HP**")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("🎯 Breitseite feuern (-5 Munition)"):
                    if st.session_state.ammo >= 5:
                        dmg = random.randint(15, 35)
                        st.session_state.ammo -= 5
                        st.session_state.enemy_hp -= dmg
                        add_log(f"Volltreffer gelandet! Feind erleidet {dmg} Schaden.")
                        
                        # Feind schlägt zurück
                        if st.session_state.enemy_hp > 0:
                            e_dmg = random.randint(5, 20)
                            st.session_state.fleet_hp -= e_dmg
                            add_log(f"Feind feuert zurück und verursacht {e_dmg} Schaden!")
                        else:
                            st.success("🎉 Feindlicher Verband zerstört! Belohnung: 50 Credits & 15 Munition.")
                            st.session_state.credits += 50
                            st.session_state.ammo += 15
                            st.session_state.in_combat = False
                    else:
                        st.error("Keine Munition mehr!")
                    st.rerun()
            
            with c2:
                if st.button("🛡️ Defensivmanöver"):
                    e_dmg = random.randint(0, 8)
                    st.session_state.fleet_hp -= e_dmg
                    add_log(f"Defensivmanöver ausgeführt. Geringer Schaden erlitten: {e_dmg} HP.")
                    st.rerun()
                    
            with c3:
                if st.button("💨 Rückzug versuchen"):
                    if random.choice([True, False]):
                        st.success("Erfolgreich aus dem Kampf zurückgezogen!")
                        st.session_state.in_combat = False
                    else:
                        e_dmg = random.randint(10, 25)
                        st.session_state.fleet_hp -= e_dmg
                        add_log(f"Rückzug fehlgeschlagen! Feind schießt in den Rumpf ({e_dmg} Schaden).")
                    st.rerun()

        # ERFORSCHUNG & EVENT-MODUS
        else:
            st.subheader("🌐 Befehlsstand")
            st.write("Wählen Sie Ihre nächste Aktion für den heutigen Tag:")
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("🧭 Kurs halten / Patrouille"):
                    st.session_state.day += 1
                    event = random.choice(["combat", "supply", "quiet", "storm"])
                    
                    if event == "combat":
                        st.session_state.in_combat = True
                        st.session_state.enemy_hp = random.randint(30, 70)
                        add_log("Feindliche Signale auf dem Radar entdeckt!")
                    elif event == "supply":
                        gained = random.randint(10, 25)
                        st.session_state.ammo += gained
                        add_log(f"Treibendes Versorgungsdepot gefunden! +{gained} Munition.")
                    elif event == "storm":
                        damage = random.randint(5, 15)
                        st.session_state.fleet_hp -= damage
                        add_log(f"In einen schweren Sturm geraten! {damage} Schaden am Rumpf.")
                    else:
                        add_log("Ruhiger Tag auf See. Keine Vorkommnisse.")
                    st.rerun()

            with col_b:
                if st.button("⚓ Hafen ansteuern (Reparatur & Versorgen)"):
                    st.session_state.day += 1
                    if st.session_state.credits >= 30:
                        st.session_state.credits -= 30
                        st.session_state.fleet_hp = min(st.session_state.max_hp, st.session_state.fleet_hp + 30)
                        st.session_state.ammo += 20
                        add_log("Im Versorgungs-Hafen angedockt. Flotte repariert und aufgerüstet (-30 Credits).")
                    else:
                        add_log("Nicht genug Credits für Hafendienste!")
                    st.rerun()

            with col_c:
                if st.button("📜 Handelskonvoi eskortieren"):
                    st.session_state.day += 1
                    if random.random() > 0.3:
                        earned = random.randint(40, 80)
                        st.session_state.credits += earned
                        add_log(f"Konvoi sicher befördert! Belohnung: {earned} Credits.")
                    else:
                        st.session_state.in_combat = True
                        st.session_state.enemy_hp = 60
                        add_log("Der Konvoi wurde überfallen! Gefecht beginnt!")
                    st.rerun()

    # Logbuch anzeigen
    st.markdown("---")
    st.subheader("📜 Logbuch des Kommandanten")
    for entry in st.session_state.log:
        st.text(entry)

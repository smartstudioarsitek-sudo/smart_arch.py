import streamlit as st
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Smart Arch Prompter",
    page_icon="🏡",
    layout="centered"
)

# --- 2. DATABASE OPSI (BANK DATA) ---
DB_TIPE = [
    "Modern Minimalist House", "Grand Mosque (Masjid)", "Tropical Villa", 
    "Industrial Office", "Futuristic Skyscraper", "Bamboo Eco-Lodge",
    "Luxury Penthouse", "Cultural Center", "Parametric Pavilion"
]

DB_GAYA = [
    "Futuristic", "Contemporary", "Islamic Modern", "Biophilic/Green", 
    "Brutalist", "Zaha Hadid Style", "Parametric Design", 
    "Scandinavian", "Japanese Zen"
]

DB_MATERIAL = [
    "concrete, glass, and wood accents", "white marble and gold trim", 
    "exposed brick and steel", "sustainable bamboo and stone", 
    "reflective glass facade", "weathered corten steel",
    "polished travertin stone"
]

DB_SUASANA = [
    "Golden Hour (Sunset)", "Blue Hour (Twilight)", "Sunny Day", 
    "Foggy Morning", "Cinematic Night Lighting", "Rainy Cyberpunk Mood",
    "Overcast Soft Light"
]

DB_ENGINE = [
    "Unreal Engine 5", "V-Ray Render", "Octane Render", 
    "Corona Render", "Lumion Render"
]

# --- 3. FUNGSI LOGIKA ---

def generate_prompt_text(target, tipe, gaya, material, pencahayaan, render_engine, strict_mode, additional_details):
    """Fungsi untuk menyusun string prompt sesuai target AI"""
    
    # Isi deskripsi visual utama
    core_prompt = f"Hyper-realistic architectural render of a {tipe}, designed in {gaya} style. "
    core_prompt += f"Featuring {material} facade details. "
    core_prompt += f"Atmosphere: {pencahayaan}. "
    
    # Menambahkan detail tambahan dari user jika ada
    if additional_details:
        # Menambahkan input user ke dalam kalimat
        core_prompt += f"Specific details: {additional_details}. "
        
    core_prompt += f"High quality, 8k resolution, detailed texture, photorealistic, {render_engine}."

    # Tambahan perintah "Kunci Sketsa" jika Strict Mode aktif
    strict_instruction = ""
    if strict_mode and target == "Gemini":
        strict_instruction = " IMPORTANT: Follow the structure and shape of the sketch exactly. Do not change the window placement or building geometry. Just change the texture and material based on this description."

    if target == "Midjourney":
        # Format Midjourney
        final_prompt = f"/imagine prompt: {core_prompt} --ar 16:9 --v 6.0"
    else:
        # Format Gemini / Nano Banana
        final_prompt = f"Please create a {core_prompt} Make sure the aspect ratio is wide (16:9) landscape.{strict_instruction}"
        
    return final_prompt

def acak_semua():
    """Callback function untuk mengacak nilai di session state"""
    st.session_state.k_tipe = random.choice(DB_TIPE)
    st.session_state.k_gaya = random.choice(DB_GAYA)
    st.session_state.k_material = random.choice(DB_MATERIAL)
    st.session_state.k_suasana = random.choice(DB_SUASANA)
    st.session_state.k_engine = random.choice(DB_ENGINE)
    # Catatan: Detail tambahan user (Text Area) tidak ikut diacak agar user tidak kehilangan ketikannya.

# --- 4. INISIALISASI SESSION STATE ---
if 'k_tipe' not in st.session_state: st.session_state.k_tipe = DB_TIPE[0]
if 'k_gaya' not in st.session_state: st.session_state.k_gaya = DB_GAYA[0]
if 'k_material' not in st.session_state: st.session_state.k_material = DB_MATERIAL[0]
if 'k_suasana' not in st.session_state: st.session_state.k_suasana = DB_SUASANA[0]
if 'k_engine' not in st.session_state: st.session_state.k_engine = DB_ENGINE[0]

# --- 5. TAMPILAN UI (USER INTERFACE) ---

st.title("🏡 Smart Arch Prompter")
st.write("Generator prompt arsitektur otomatis + Detail Custom.")

# Sidebar Pengaturan
st.sidebar.header("⚙️ Pengaturan")
target_ai = st.sidebar.radio(
    "Pilih AI Koki:",
    ["Gemini (Nano Banana Mode) 🍌", "Midjourney 🎨"]
)

# Fitur Strict Mode
use_strict = False
if "Gemini" in target_ai:
    st.sidebar.markdown("---")
    use_strict = st.sidebar.checkbox("🔒 Mode Patuh Sketsa", value=True, help="Centang ini agar AI mengikuti garis sketsa dengan ketat.")

st.markdown("---")

# Tombol Random
st.button("🎲 Random Surprise Me!", type="secondary", on_click=acak_semua, use_container_width=True)
st.write("") 

# Form Input Utama
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Tipe Bangunan", DB_TIPE, key='k_tipe')
        st.selectbox("Gaya Desain", DB_GAYA, key='k_gaya')
    with col2:
        st.text_input("Material Utama", key='k_material') 
        st.selectbox("Pencahayaan / Suasana", DB_SUASANA, key='k_suasana')
    
    st.markdown("---")
    st.radio("Engine Style", DB_ENGINE, horizontal=True, key='k_engine')

# --- AREA INPUT TAMBAHAN (BARU) ---
st.write("")
st.markdown("##### 📝 Detail Tambahan (Opsional)")
detail_user = st.text_area(
    "Masukkan detail objek lain (Mobil, Pohon, Orang, dll):", 
    placeholder="Contoh: Ada mobil Pajero Sport hitam di carport, taman bunga merah di depan, jalan basah sehabis hujan...",
    height=100
)

# --- 6. OUTPUT SECTION ---
st.write("") 
generate_btn = st.button("✨ Generate Prompt Akhir", type="primary", use_container_width=True)

if generate_btn:
    mode_name = "Midjourney" if "Midjourney" in target_ai else "Gemini"
    
    final_prompt = generate_prompt_text(
        mode_name,
        st.session_state.k_tipe,
        st.session_state.k_gaya,
        st.session_state.k_material,
        st.session_state.k_suasana,
        st.session_state.k_engine,
        use_strict,
        detail_user # Mengirim input detail tambahan ke fungsi
    )
    
    st.success(f"Prompt Siap! (Mode: {mode_name}) 👇")
    st.code(final_prompt, language="text")
    
    if mode_name == "Gemini":
        if use_strict:
            st.info("💡 PENTING: Jangan lupa upload SKETSA gambar tangan Kakak bersamaan dengan prompt ini!")
    else:
        st.caption("Tips: Copy teks di atas, lalu paste ke Discord Midjourney.")

# Footer
st.markdown("---")
st.caption("Developed for Civil & Arch Engineering | v1.3 Custom Detail Edition")

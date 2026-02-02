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
    "Scandinavian (Japandi)", "Industrial"
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

# --- DATABASE BARU (GAYA PRESENTASI) ---
# Fitur baru v1.6: Pilihan gaya render (Sketsa Teknis, Blueprint, Realis)
DB_PRESENTASI = {
    "📸 Clean Photorealistic (Polos)": "clean, no text, pure photography style",
    "📏 Technical Concept (Ada Ukuran & Teks)": "architectural concept sheet style, mixed media, photorealistic render overlaid with hand-drawn technical annotations, dimension lines, measurement arrows, material callouts, handwritten notes, sketch aesthetic",
    "📝 Blueprint / Wireframe (Garis)": "blueprint style, white lines on blue background, technical drawing, wireframe structural view",
    "🎨 Watercolor Sketch (Artist)": "watercolor painting style, soft edges, artistic architectural sketch, ink outline"
}

DB_VIEW = [
    "Eye Level (Human View)", "Drone / Bird's Eye View", "Worm's Eye View (Low Angle)",
    "Isometric View (3D Cutaway)", "Close-up Detail Shot", "Interior Wide Angle"
]

DB_RASIO = {
    "Landscape (16:9)": "--ar 16:9",
    "Portrait / Story (9:16)": "--ar 9:16",
    "Square / Feed (1:1)": "--ar 1:1",
    "Classic Photo (4:3)": "--ar 4:3"
}

DB_ENGINE = [
    "Unreal Engine 5", "V-Ray Render", "Octane Render", 
    "Corona Render", "Lumion Render"
]

# --- 3. FUNGSI LOGIKA ---

def generate_prompt_text(target, tipe, gaya, material, pencahayaan, render_engine, view_angle, rasio_label, presentasi_label, strict_mode, style_ref_mode, additional_details):
    
    # Ambil detail gaya presentasi dari dictionary
    gaya_presentasi_prompt = DB_PRESENTASI[presentasi_label]
    kode_rasio_mj = DB_RASIO[rasio_label]
    
    # Susun Kalimat Inti
    core_prompt = f"Architectural image of a {tipe}, designed in {gaya} style. "
    core_prompt += f"Style: {gaya_presentasi_prompt}. " # Masukkan gaya presentasi
    core_prompt += f"View angle: {view_angle}. "
    core_prompt += f"Featuring {material} facade details. "
    core_prompt += f"Atmosphere: {pencahayaan}. "
    
    if additional_details:
        core_prompt += f"Specific details: {additional_details}. "
        
    core_prompt += f"High quality, 8k resolution, detailed texture, {render_engine}."

    # --- LOGIKA INSTRUKSI AI (GEMINI vs MIDJOURNEY) ---
    instruction_text = ""
    
    if target == "Gemini":
        # Instruksi Bahasa Manusia (Natural) untuk Gemini
        instruction_text = f"Please create a {core_prompt} "
        instruction_text += f"Make sure the image aspect ratio is {rasio_label}. " 
        
        # Tambahan khusus jika pilih Technical Concept
        if "Technical" in presentasi_label:
             instruction_text += " IMPORTANT: Please add visual technical elements like measurement lines, arrows pointing to materials, and handwritten labels (e.g. 'wood', 'glass') to make it look like an architect's concept board."

        # Logika Gambar Upload
        if style_ref_mode:
            instruction_text += " [IMPORTANT: I have uploaded TWO images]. "
            instruction_text += "IMAGE 1 is the SKETCH (Structure). "
            instruction_text += "IMAGE 2 is the STYLE REFERENCE (Mood/Colors). "
            instruction_text += "Please apply the visual style of Image 2 to the geometry of Image 1."
        elif strict_mode:
            instruction_text += " IMPORTANT: Follow the structure and shape of the uploaded sketch exactly."
            
        final_prompt = instruction_text

    else:
        # Format Midjourney
        final_prompt = f"/imagine prompt: {core_prompt} {kode_rasio_mj} --v 6.0"
        
    return final_prompt

def acak_semua():
    """Fungsi untuk mengacak input (kecuali Rasio & Gaya Presentasi)"""
    st.session_state.k_tipe = random.choice(DB_TIPE)
    st.session_state.k_gaya = random.choice(DB_GAYA)
    st.session_state.k_material = random.choice(DB_MATERIAL)
    st.session_state.k_suasana = random.choice(DB_SUASANA)
    st.session_state.k_engine = random.choice(DB_ENGINE)
    st.session_state.k_view = random.choice(DB_VIEW)

# --- 4. INISIALISASI SESSION STATE ---
# Agar widget tidak error saat pertama kali load
if 'k_tipe' not in st.session_state: st.session_state.k_tipe = DB_TIPE[0]
if 'k_gaya' not in st.session_state: st.session_state.k_gaya = DB_GAYA[0]
if 'k_material' not in st.session_state: st.session_state.k_material = DB_MATERIAL[0]
if 'k_suasana' not in st.session_state: st.session_state.k_suasana = DB_SUASANA[0]
if 'k_engine' not in st.session_state: st.session_state.k_engine = DB_ENGINE[0]
if 'k_view' not in st.session_state: st.session_state.k_view = DB_VIEW[0]

# --- 5. TAMPILAN UI (USER INTERFACE) ---

st.title("🏡 Smart Arch Prompter v1.6")
st.write("Generator Arsitektur: Sekarang bisa request gaya sketsa teknis! 📐")

# Sidebar Pengaturan
st.sidebar.header("⚙️ Target AI")
target_ai = st.sidebar.radio(
    "Pilih Koki:",
    ["Gemini (Nano Banana) 🍌", "Midjourney 🎨"]
)

use_strict = False
use_style_ref = False

if "Gemini" in target_ai:
    st.sidebar.markdown("---")
    st.sidebar.caption("📸 Mode Upload Gemini:")
    use_strict = st.sidebar.checkbox("🔒 Kunci Bentuk Sketsa", value=True)
    use_style_ref = st.sidebar.checkbox("🎨 Pakai Referensi Warna", value=False)
    
    if use_style_ref:
        st.sidebar.info("Upload 2 Gambar: Sketsa + Referensi Warna.")

st.markdown("---")
st.button("🎲 Random Surprise Me!", type="secondary", on_click=acak_semua, use_container_width=True)
st.write("") 

# Form Input Utama
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Tipe Bangunan", DB_TIPE, key='k_tipe')
        st.selectbox("Gaya Desain", DB_GAYA, key='k_gaya')
        st.selectbox("Sudut Pandang (View)", DB_VIEW, key='k_view') 
        
    with col2:
        st.text_input("Material Utama", key='k_material') 
        st.selectbox("Pencahayaan", DB_SUASANA, key='k_suasana')
        st.selectbox("Rasio Gambar", list(DB_RASIO.keys()), index=0, key='k_rasio') 

    st.markdown("---")
    # Menu Gaya Presentasi (Fitur v1.6)
    st.selectbox("🎨 Gaya Presentasi (Render Style)", list(DB_PRESENTASI.keys()), index=0, key='k_presentasi')
    st.caption("Tips: Pilih 'Technical Concept' untuk hasil gambar dengan coretan ukuran & teks.")
    
    st.markdown("---")
    st.radio("Engine Style", DB_ENGINE, horizontal=True, key='k_engine')

# Area Input Tambahan
st.write("")
st.markdown("##### 📝 Detail Tambahan")
detail_user = st.text_area(
    "Detail Khusus:", 
    placeholder="Contoh: Ada mobil Pajero, jalan basah, tulisan dimensi harus jelas...",
    height=80
)

# --- 6. OUTPUT SECTION ---
st.write("") 
generate_btn = st.button("✨ Generate Prompt Akhir", type="primary", use_container_width=True)

if generate_btn:
    mode_name = "Midjourney" if "Midjourney" in target_ai else "Gemini"
    
    # Memanggil fungsi generator dengan semua parameter terbaru
    final_prompt = generate_prompt_text(
        mode_name,
        st.session_state.k_tipe,
        st.session_state.k_gaya,
        st.session_state.k_material,
        st.session_state.k_suasana,
        st.session_state.k_engine,
        st.session_state.k_view, 
        st.session_state.k_rasio,          
        st.session_state.k_presentasi, # Parameter baru
        use_strict,
        use_style_ref,
        detail_user
    )
    
    st.success(f"Prompt Siap! (Mode: {mode_name}) 👇")
    st.code(final_prompt, language="text")
    
    if mode_name == "Gemini":
        if "Technical" in st.session_state.k_presentasi:
             st.info("💡 Keren! Prompt ini akan meminta AI membuat coretan teknis & ukuran dimensi.")

# Footer
st.markdown("---")
st.caption("Developed for Civil & Arch Engineering | v1.6 Presentation Master")

import streamlit as st
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor

# Cấu hình giao diện Ngô Đình Quyền - Giữ nguyên tuyệt đối
st.set_page_config(page_title="Đóng dấu ảnh - Ngô Đình Quyền", layout="centered")

# CSS TÙY CHỈNH: Ép nút fullscreen hiện sẵn (không cần hover) ở góc dưới bên phải
st.markdown("""
    <style>
    /* 1. Luôn hiển thị nút Action (Fullscreen) không cần hover */
    [data-testid="stImage"] [data-testid="stImageActionButton"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        bottom: 15px !important;
        right: 15px !important;
        top: auto !important;
        left: auto !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid #ddd !important;
        border-radius: 8px !important;
        padding: 8px !important;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.2) !important;
    }
    /* 2. Làm icon phóng to rõ rệt hơn */
    [data-testid="stImageActionButton"] svg {
        width: 35px !important;
        height: 35px !important;
        fill: #333 !important;
    }
    /* 3. Chỉnh khoảng cách bảng 9 ô cho cân đối */
    .stCheckbox { margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

# Tiêu đề gốc
st.markdown("<h1 style='text-align: center;'>🚀 CÔNG CỤ ĐÓNG DẤU ẢNH CHUYÊN NGHIỆP</h1>", unsafe_allow_html=True)

# BƯỚC 1: CHỌN LOGO
logo_file = st.file_uploader("🖼️ Bước 1: Chọn Logo (PNG trong suốt)", type=['png'])

# BƯỚC 2: CHỌN ẢNH CẦN XỬ LÝ
image_files = st.file_uploader("📁 Bước 2: Chọn các ảnh muốn đóng dấu", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

# BẢNG 9 Ô VỊ TRÍ (3x3 Grid)
st.subheader("📍 Vị trí đóng dấu (9 ô)")
pos_options = [
    "Trên - Trái", "Trên - Giữa", "Trên - Phải",
    "Giữa - Trái", "Chính Giữa", "Giữa - Phải",
    "Dưới - Trái", "Dưới - Giữa", "Dưới - Phải"
]

# Chia 3 cột để tạo hình vuông 9 ô
c1, c2, c3 = st.columns(3)
with c1:
    tl = st.checkbox("Trên - Trái", key="tl")
    ml = st.checkbox("Giữa - Trái", key="ml")
    bl = st.checkbox("Dưới - Trái", key="bl")
with c2:
    tc = st.checkbox("Trên - Giữa", key="tc")
    mc = st.checkbox("Chính Giữa", key="mc", value=True)
    bc = st.checkbox("Dưới - Giữa", key="bc")
with c3:
    tr = st.checkbox("Trên - Phải", key="tr")
    mr = st.checkbox("Giữa - Phải", key="mr")
    br = st.checkbox("Dưới - Phải", key="br")

def get_selected_pos():
    if tl: return "Trên - Trái"
    if tc: return "Trên - Giữa"
    if tr: return "Trên - Phải"
    if ml: return "Giữa - Trái"
    if mc: return "Chính Giữa"
    if mr: return "Giữa - Phải"
    if bl: return "Dưới - Trái"
    if bc: return "Dưới - Giữa"
    return "Dưới - Phải"

# CẤU HÌNH WATERMARK (GIỮ NGUYÊN)
st.subheader("⚙️ Cấu hình Watermark")
col_s1, col_s2 = st.columns(2)
with col_s1:
    size_percent = st.slider("Kích thước (%)", 5, 100, 15)
with col_s2:
    opacity = st.slider("Độ rõ nét (%)", 0, 100, 80)

def tinh_toa_do(img_w, img_h, wm_w, wm_h, pos, offset=30):
    mapping = {
        "Trên - Trái": (offset, offset),
        "Trên - Giữa": ((img_w - wm_w) // 2, offset),
        "Trên - Phải": (img_w - wm_w - offset, offset),
        "Giữa - Trái": (offset, (img_h - wm_h) // 2),
        "Chính Giữa": ((img_w - wm_w) // 2, (img_h - wm_h) // 2),
        "Giữa - Phải": (img_w - wm_w - offset, (img_h - wm_h) // 2),
        "Dưới - Trái": (offset, img_h - wm_h - offset),
        "Dưới - Giữa": ((img_w - wm_w) // 2, img_h - wm_h - offset),
        "Dưới - Phải": (img_w - wm_w - offset, img_h - wm_h - offset)
    }
    return mapping.get(pos, (offset, offset))

def process_single_image(uploaded_file, logo_raw, size_percent, opacity, current_pos):
    img = Image.open(uploaded_file).convert("RGBA")
    img_w, img_h = img.size
    scale = (img_w * size_percent / 100) / logo_raw.size[0]
    wm_w, wm_h = int(logo_raw.size[0] * scale), int(logo_raw.size[1] * scale)
    wm_final = logo_raw.resize((wm_w, wm_h), Image.LANCZOS)
    alpha = wm_final.split()[3].point(lambda p: p * (opacity / 100))
    wm_final.putalpha(alpha)
    x, y = tinh_toa_do(img_w, img_h, wm_w, wm_h, current_pos)
    img.paste(wm_final, (x, y), wm_final)
    res_img = img.convert("RGB")
    buf = io.BytesIO()
    res_img.save(buf, format="JPEG", quality=90)
    return uploaded_file.name, res_img, buf.getvalue()

# XỬ LÝ CHÍNH
if st.button("🚀 BẮT ĐẦU XỬ LÝ (TỐC ĐỘ CAO)"):
    if logo_file and image_files:
        current_pos = get_selected_pos()
        logo_raw = Image.open(logo_file).convert("RGBA")
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_single_image, f, logo_raw, size_percent, opacity, current_pos) for f in image_files]
            for future in futures:
                name, res_img, byte_data = future.result()
                # Hiển thị ảnh - Nút fullscreen sẽ hiện sẵn ở góc dưới bên phải
                st.image(res_img, caption=name, use_container_width=True)
                st.download_button(label=f"📥 Tải {name}", data=byte_data, file_name=f"wm_{name}", mime="image/jpeg")

# CHÂN TRANG BẢN QUYỀN (GIỮ NGUYÊN)
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: red;'>Bản quyền thuộc về Ngô Đình Quyền</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Hotline / Zalo hỗ trợ: 0325.545.767</p>", unsafe_allow_html=True)

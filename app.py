import streamlit as st
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor

# 1. CẤU HÌNH GIAO DIỆN CHUẨN NGÔ ĐÌNH QUYỀN
st.set_page_config(page_title="Đóng dấu ảnh - Ngô Đình Quyền", layout="centered")

# CSS ĐẶC BIỆT: Ép nút phóng to hiện sẵn ở góc dưới bên phải (Cả trong và ngoài)
st.markdown("""
    <style>
    /* Nút phóng to hiện sẵn 100% thời gian */
    [data-testid="stImage"] [data-testid="stImageActionButton"],
    .st-emotion-cache-15zrgzn [data-testid="stImageActionButton"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        bottom: 25px !important;
        right: 25px !important;
        top: auto !important;
        left: auto !important;
        position: absolute !important;
    }
    /* Làm nút to, trắng rõ, có bóng đổ chuyên nghiệp */
    [data-testid="stImageActionButton"] button {
        width: 48px !important;
        height: 48px !important;
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid #ddd !important;
        border-radius: 10px !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.4) !important;
    }
    /* Tăng kích thước biểu tượng phóng to bên trong nút */
    [data-testid="stImageActionButton"] svg {
        width: 30px !important;
        height: 30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🚀 CÔNG CỤ ĐÓNG DẤU ẢNH CHUYÊN NGHIỆP</h1>", unsafe_allow_html=True)

# BƯỚC 1 & 2: NHẬP LIỆU
logo_file = st.file_uploader("🖼️ Bước 1: Chọn Logo (PNG trong suốt)", type=['png'])
image_files = st.file_uploader("📁 Bước 2: Chọn các ảnh muốn đóng dấu", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

# BẢNG 9 Ô VỊ TRÍ - CHUẨN ILLUSTRATOR (3 Hàng x 3 Cột)
st.subheader("📍 Vị trí đóng dấu (9 ô)")
row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)

# Sử dụng radio riêng lẻ trong từng cột nhưng cùng logic
with row1[0]: p1 = st.radio("L1", ["Trên - Trái"], key="p1", label_visibility="collapsed")
with row1[1]: p2 = st.radio("L2", ["Trên - Giữa"], key="p2", label_visibility="collapsed")
with row1[2]: p3 = st.radio("L3", ["Trên - Phải"], key="p3", label_visibility="collapsed")

with row2[0]: p4 = st.radio("L4", ["Giữa - Trái"], key="p4", label_visibility="collapsed")
with row2[1]: p5 = st.radio("L5", ["Chính Giữa"], key="p5", label_visibility="collapsed")
with row2[2]: p6 = st.radio("L6", ["Giữa - Phải"], key="p6", label_visibility="collapsed")

with row3[0]: p7 = st.radio("L7", ["Dưới - Trái"], key="p7", label_visibility="collapsed")
with row3[1]: p8 = st.radio("L8", ["Dưới - Giữa"], key="p8", label_visibility="collapsed")
with row3[2]: p9 = st.radio("L9", ["Dưới - Phải"], key="p9", label_visibility="collapsed")

# Lựa chọn vị trí cuối cùng được người dùng nhấp vào (mặc định Chính Giữa)
pos_final = st.radio("Xác nhận vị trí (Bấm để chọn):", 
                    ["Trên - Trái", "Trên - Giữa", "Trên - Phải", 
                     "Giữa - Trái", "Chính Giữa", "Giữa - Phải", 
                     "Dưới - Trái", "Dưới - Giữa", "Dưới - Phải"], 
                    index=4, horizontal=True)

# CẤU HÌNH CHI TIẾT
st.subheader("⚙️ Cấu hình Watermark")
col_s1, col_s2 = st.columns(2)
with col_s1:
    size_percent = st.slider("Kích thước (%)", 5, 100, 15)
with col_s2:
    opacity = st.slider("Độ rõ nét (%)", 0, 100, 10) # Để mặc định 10% như bản đẹp của bạn

def tinh_toa_do(img_w, img_h, wm_w, wm_h, pos, offset=35):
    map_pos = {
        "Trên - Trái": (offset, offset), "Trên - Giữa": ((img_w - wm_w) // 2, offset), "Trên - Phải": (img_w - wm_w - offset, offset),
        "Giữa - Trái": (offset, (img_h - wm_h) // 2), "Chính Giữa": ((img_w - wm_w) // 2, (img_h - wm_h) // 2), "Giữa - Phải": (img_w - wm_w - offset, (img_h - wm_h) // 2),
        "Dưới - Trái": (offset, img_h - wm_h - offset), "Dưới - Giữa": ((img_w - wm_w) // 2, img_h - wm_h - offset), "Dưới - Phải": (img_w - wm_w - offset, img_h - wm_h - offset)
    }
    return map_pos.get(pos, (offset, offset))

def process_img(u_file, logo_raw, s_pct, opac, pos_choice):
    img = Image.open(u_file).convert("RGBA")
    img_w, img_h = img.size
    scale = (img_w * s_pct / 100) / logo_raw.size[0]
    wm_w, wm_h = int(logo_raw.size[0] * scale), int(logo_raw.size[1] * scale)
    wm = logo_raw.resize((wm_w, wm_h), Image.LANCZOS)
    alpha = wm.split()[3].point(lambda p: p * (opac / 100))
    wm.putalpha(alpha)
    x, y = tinh_toa_do(img_w, img_h, wm_w, wm_h, pos_choice)
    img.paste(wm, (x, y), wm)
    res = img.convert("RGB")
    buf = io.BytesIO()
    res.save(buf, format="JPEG", quality=95)
    return u_file.name, res, buf.getvalue()

# XỬ LÝ ĐA LUỒNG TĂNG TỐC
if st.button("🚀 BẮT ĐẦU XỬ LÝ (SIÊU TỐC)"):
    if logo_file and image_files:
        l_raw = Image.open(logo_file).convert("RGBA")
        with ThreadPoolExecutor() as exe:
            results = [exe.submit(process_img, f, l_raw, size_percent, opacity, pos_final) for f in image_files]
            for r in results:
                fname, fimg, fbyte = r.result()
                st.image(fimg, caption=fname, use_container_width=True)
                st.download_button(f"📥 Tải {fname}", fbyte, f"wm_{fname}", "image/jpeg")

# CHÂN TRANG BẢN QUYỀN
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: red;'>Bản quyền thuộc về Ngô Đình Quyền</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Hotline / Zalo hỗ trợ: 0325.545.767</p>", unsafe_allow_html=True)

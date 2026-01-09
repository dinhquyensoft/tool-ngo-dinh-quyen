import streamlit as st
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor

# Cấu hình giao diện Ngô Đình Quyền - Giữ nguyên tuyệt đối
st.set_page_config(page_title="Đóng dấu ảnh - Ngô Đình Quyền", layout="centered")

# CSS TÙY CHỈNH: Ép nút fullscreen hiện sẵn ở góc dưới bên phải (Cả ngoài và trong)
st.markdown("""
    <style>
    /* Ép nút hành động hiện sẵn ở góc dưới bên phải như bạn đã khoanh tròn */
    [data-testid="stImage"] [data-testid="stImageActionButton"],
    .st-emotion-cache-15zrgzn [data-testid="stImageActionButton"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        bottom: 20px !important;
        right: 20px !important;
        top: auto !important;
        left: auto !important;
        position: absolute !important;
    }
    /* Làm nút to rõ hơn */
    [data-testid="stImageActionButton"] button {
        width: 45px !important;
        height: 45px !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 8px !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Tiêu đề gốc
st.markdown("<h1 style='text-align: center;'>🚀 CÔNG CỤ ĐÓNG DẤU ẢNH CHUYÊN NGHIỆP</h1>", unsafe_allow_html=True)

# BƯỚC 1: CHỌN LOGO
logo_file = st.file_uploader("🖼️ Bước 1: Chọn Logo (PNG trong suốt)", type=['png'])

# BƯỚC 2: CHỌN ẢNH CẦN XỬ LÝ
image_files = st.file_uploader("📁 Bước 2: Chọn các ảnh muốn đóng dấu", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

# SỬA LỖI VỊ TRÍ: Chia 3 hàng 3 cột dùng Radio (Style Illustrator)
st.subheader("📍 Vị trí đóng dấu (9 ô)")
c1, c2, c3 = st.columns(3)

with c1:
    v1 = st.radio("Hàng 1", ["Trên - Trái"], key="p1", label_visibility="collapsed")
    v4 = st.radio("Hàng 2", ["Giữa - Trái"], key="p4", label_visibility="collapsed")
    v7 = st.radio("Hàng 3", ["Dưới - Trái"], key="p7", label_visibility="collapsed")
with c2:
    v2 = st.radio("Hàng 1", ["Trên - Giữa"], key="p2", label_visibility="collapsed")
    v5 = st.radio("Hàng 2", ["Chính Giữa"], key="p5", label_visibility="collapsed")
    v8 = st.radio("Hàng 3", ["Dưới - Giữa"], key="p8", label_visibility="collapsed")
with c3:
    v3 = st.radio("Hàng 1", ["Trên - Phải"], key="p3", label_visibility="collapsed")
    v6 = st.radio("Hàng 2", ["Giữa - Phải"], key="p6", label_visibility="collapsed")
    v9 = st.radio("Hàng 3", ["Dưới - Phải"], key="p9", label_visibility="collapsed")

# Radio chọn vị trí chính thức (ẩn để lấy giá trị logic)
pos_choice = st.radio("Xác nhận vị trí:", 
                      ["Trên - Trái", "Trên - Giữa", "Trên - Phải", 
                       "Giữa - Trái", "Chính Giữa", "Giữa - Phải", 
                       "Dưới - Trái", "Dưới - Giữa", "Dưới - Phải"], 
                      index=4, horizontal=True)

# CẤU HÌNH WATERMARK (GIỮ NGUYÊN)
st.subheader("⚙️ Cấu hình Watermark")
col_s1, col_s2 = st.columns(2)
with col_s1:
    size_percent = st.slider("Kích thước (%)", 5, 100, 15)
with col_s2:
    opacity = st.slider("Độ rõ nét (%)", 0, 100, 80)

def tinh_toa_do(img_w, img_h, wm_w, wm_h, pos, offset=30):
    mapping = {
        "Trên - Trái": (offset, offset), "Trên - Giữa": ((img_w - wm_w) // 2, offset), "Trên - Phải": (img_w - wm_w - offset, offset),
        "Giữa - Trái": (offset, (img_h - wm_h) // 2), "Chính Giữa": ((img_w - wm_w) // 2, (img_h - wm_h) // 2), "Giữa - Phải": (img_w - wm_w - offset, (img_h - wm_h) // 2),
        "Dưới - Trái": (offset, img_h - wm_h - offset), "Dưới - Giữa": ((img_w - wm_w) // 2, img_h - wm_h - offset), "Dưới - Phải": (img_w - wm_w - offset, img_h - wm_h - offset)
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
        logo_raw = Image.open(logo_file).convert("RGBA")
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_single_image, f, logo_raw, size_percent, opacity, pos_choice) for f in image_files]
            for future in futures:
                name, res_img, byte_data = future.result()
                st.image(res_img, caption=name, use_container_width=True)
                st.download_button(label=f"📥 Tải {name}", data=byte_data, file_name=f"wm_{name}", mime="image/jpeg")

# CHÂN TRANG BẢN QUYỀN (GIỮ NGUYÊN)
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: red;'>Bản quyền thuộc về Ngô Đình Quyền</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Hotline / Zalo hỗ trợ: 0325.545.767</p>", unsafe_allow_html=True)

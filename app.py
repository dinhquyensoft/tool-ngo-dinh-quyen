import streamlit as st
from PIL import Image
import io
import os

# Cấu hình giao diện Web chuyên nghiệp
st.set_page_config(page_title="Đóng dấu ảnh - Ngô Đình Quyền", layout="centered")

st.markdown("<h1 style='text-align: center;'>🚀 CÔNG CỤ ĐÓNG DẤU ẢNH CHUYÊN NGHIỆP</h1>", unsafe_allow_html=True)

# Khung chọn Logo và Ảnh
logo_file = st.file_uploader("🖼️ Bước 1: Chọn Logo (PNG trong suốt)", type=['png'])
image_files = st.file_uploader("📁 Bước 2: Chọn các ảnh muốn đóng dấu", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

def tinh_toa_do(img_w, img_h, logo_w, logo_h, pos, offset=20):
    if pos == "Trên - Trái": return (offset, offset)
    if pos == "Trên - Giữa": return ((img_w - logo_w) // 2, offset)
    if pos == "Trên - Phải": return (img_w - logo_w - offset, offset)
    if pos == "Giữa - Trái": return (offset, (img_h - logo_h) // 2)
    if pos == "Chính Giữa": return ((img_w - logo_w) // 2, (img_h - logo_h) // 2)
    if pos == "Giữa - Phải": return (img_w - logo_w - offset, (img_h - logo_h) // 2)
    if pos == "Dưới - Trái": return (offset, img_h - logo_h - offset)
    if pos == "Dưới - Giữa": return ((img_w - logo_w) // 2, img_h - logo_h - offset)
    return (img_w - logo_w - offset, img_h - logo_h - offset)

if logo_file and image_files:
    st.subheader("⚙️ Cấu hình Watermark")
    col1, col2 = st.columns(2)
    with col1:
        pos = st.selectbox("Vị trí đóng dấu:", ["Trên - Trái", "Trên - Giữa", "Trên - Phải", "Giữa - Trái", "Chính Giữa", "Giữa - Phải", "Dưới - Trái", "Dưới - Giữa", "Dưới - Phải"], index=4)
    with col2:
        size_percent = st.slider("Kích thước Logo (% ảnh):", 5, 50, 15)
        opacity = st.slider("Độ rõ nét Logo (%):", 0, 100, 80)

    if st.button("🚀 BẮT ĐẦU XỬ LÝ"):
        logo_raw = Image.open(logo_file).convert("RGBA")
        for uploaded_file in image_files:
            img = Image.open(uploaded_file).convert("RGBA")
            img_w, img_h = img.size
            
            # Tính toán kích thước Logo
            scale = size_percent / 100
            new_w = int(img_w * scale)
            new_h = int(logo_raw.size[1] * (new_w / logo_raw.size[0]))
            logo = logo_raw.resize((new_w, new_h), Image.LANCZOS)
            
            # Xử lý độ mờ
            alpha = logo.split()[3].point(lambda p: p * (opacity / 100))
            logo.putalpha(alpha)
            
            # Chèn logo
            x, y = tinh_toa_do(img_w, img_h, new_w, new_h, pos)
            img.paste(logo, (x, y), logo)
            
            # Hiển thị kết quả
            st.image(img.convert("RGB"), caption=f"Ảnh đã xử lý: {uploaded_file.name}", use_container_width=True)
            
            # Tạo bộ nhớ đệm để tải về
            buf = io.BytesIO()
            img.convert("RGB").save(buf, format="JPEG", quality=95)
            byte_im = buf.getvalue()
            
            st.download_button(label=f"📥 Tải ảnh {uploaded_file.name} về máy", data=byte_im, file_name=f"watermarked_{uploaded_file.name}", mime="image/jpeg")

# Chân trang bản quyền nổi bật
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: red;'>Bản quyền thuộc về Ngô Đình Quyền</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Hotline / Zalo hỗ trợ: 0325.545.767</p>", unsafe_allow_html=True)

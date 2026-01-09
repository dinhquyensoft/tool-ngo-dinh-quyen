import streamlit as st
from PIL import Image
import os

# Cấu hình giao diện Web
st.set_page_config(page_title="Đóng dấu ảnh - Ngô Đình Quyền", layout="centered")

st.title("🚀 CÔNG CỤ ĐÓNG DẤU ẢNH CHUYÊN NGHIỆP")

# Khung chọn Logo và Ảnh
logo_file = st.file_uploader("🖼️ Bước 1: Chọn Logo (PNG trong suốt)", type=['png'])
image_files = st.file_uploader("📁 Bước 2: Chọn các ảnh muốn đóng dấu", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if logo_file and image_files:
    # Cấu hình logic linh hoạt
    st.subheader("⚙️ Cấu hình Watermark")
    col1, col2 = st.columns(2)
    
    with col1:
        pos = st.selectbox("Vị trí đóng dấu:", 
                          ["Trên - Trái", "Trên - Giữa", "Trên - Phải", 
                           "Giữa - Trái", "Chính Giữa", "Giữa - Phải",
                           "Dưới - Trái", "Dưới - Giữa", "Dưới - Phải"])
        
    with col2:
        size_percent = st.slider("Kích thước Logo (% ảnh):", 5, 50, 15)
        opacity = st.slider("Độ rõ nét Logo (%):", 0, 100, 80)

    if st.button("🚀 BẮT ĐẦU XỬ LÝ"):
        logo_raw = Image.open(logo_file).convert("RGBA")
        
        for uploaded_file in image_files:
            img = Image.open(uploaded_file).convert("RGBA")
            img_w, img_h = img.size
            
            # Logic tính toán kích thước và vị trí (giữ nguyên độ ổn định)
            scale = size_percent / 100
            new_w = int(img_w * scale)
            new_h = int(logo_raw.size[1] * (new_w / logo_raw.size[0]))
            logo = logo_raw.resize((new_w, new_h), Image.LANCZOS)
            
            # Xử lý độ mờ
            alpha = logo.split()[3].point(lambda p: p * (opacity / 100))
            logo.putalpha(alpha)
            
            # (Tính toán tọa độ x, y dựa trên pos - tương tự bản PC)
            # ... [Logic tính toán giữ nguyên như bản phanmemnenanh.py] ...
            
            st.image(img, caption=f"Đã xử lý: {uploaded_file.name}", use_column_width=True)
            # Cho phép khách hàng tải về ngay trên điện thoại
            st.download_button(label=f"Tải ảnh {uploaded_file.name}", data=..., file_name=f"watermarked_{uploaded_file.name}")

# Chân trang bản quyền nổi bật
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: red;'>Bản quyền thuộc về Ngô Đình Quyền</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Hotline / Zalo hỗ trợ: 0325.545.767</p>", unsafe_allow_html=True)

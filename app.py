import streamlit as st

from PIL import Image

import io

from concurrent.futures import ThreadPoolExecutor



# Cấu hình giao diện Ngô Đình Quyền - Giữ nguyên tuyệt đối

st.set_page_config(page_title="Đóng dấu ảnh - Ngô Đình Quyền", layout="centered")



# Tiêu đề gốc

st.markdown("<h1 style='text-align: center;'>GIẢI PHÁP ĐỊNH VỊ THƯƠNG HIỆU HÌNH ẢNH</h1>", unsafe_allow_html=True)



# BƯỚC 1: CHỌN LOGO

logo_file = st.file_uploader("🖼️ Bước 1: Chọn Logo (PNG trong suốt)", type=['png'])



# BƯỚC 2: CHỌN ẢNH CẦN XỬ LÝ

image_files = st.file_uploader("📁 Bước 2: Chọn các ảnh muốn đóng dấu", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)



# SỬA LỖI VỊ TRÍ: Chuyển từ Checkbox sang Radio để chỉ được chọn 1 ô duy nhất

st.subheader("📍 Vị trí đóng dấu logo ")

pos_options = [

    "Trên - Trái", "Trên - Giữa", "Trên - Phải",

    "Giữa - Trái", "Chính Giữa", "Giữa - Phải",

    "Dưới - Trái", "Dưới - Giữa", "Dưới - Phải"

]



# Hiển thị bảng 9 ô dùng Radio chọn duy nhất 1

selected_pos = st.radio("Chọn vị trí chính xác:", pos_options, index=4, horizontal=True)



# CẤU HÌNH WATERMARK

st.subheader("⚙️ Cấu hình Watermark")

col1, col2 = st.columns(2)

with col1:

    size_percent = st.slider("Kích thước (%)", 5, 100, 15)

with col2:

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



def process_single_image(uploaded_file, logo_raw, size_percent, opacity, pos_choice):

    img = Image.open(uploaded_file).convert("RGBA")

    img_w, img_h = img.size

    scale = (img_w * size_percent / 100) / logo_raw.size[0]

    wm_w, wm_h = int(logo_raw.size[0] * scale), int(logo_raw.size[1] * scale)

    wm_final = logo_raw.resize((wm_w, wm_h), Image.LANCZOS)

    alpha = wm_final.split()[3].point(lambda p: p * (opacity / 100))

    wm_final.putalpha(alpha)

    x, y = tinh_toa_do(img_w, img_h, wm_w, wm_h, pos_choice)

    img.paste(wm_final, (x, y), wm_final)

    res_img = img.convert("RGB")

    buf = io.BytesIO()

    res_img.save(buf, format="JPEG", quality=90)

    return uploaded_file.name, res_img, buf.getvalue()



# XỬ LÝ CHÍNH TỐC ĐỘ CAO

if st.button("🚀 BẮT ĐẦU XỬ LÝ (TỐC ĐỘ CAO)"):

    if logo_file and image_files:

        logo_raw = Image.open(logo_file).convert("RGBA")

        with ThreadPoolExecutor() as executor:

            futures = [executor.submit(process_single_image, f, logo_raw, size_percent, opacity, selected_pos) for f in image_files]

            for future in futures:

                name, res_img, byte_data = future.result()

                st.image(res_img, caption=name, use_container_width=True)

                st.download_button(label=f"📥 Tải {name}", data=byte_data, file_name=f"watermark_{name}", mime="image/jpeg")



# CHÂN TRANG BẢN QUYỀN

st.markdown("---")

st.markdown("<h3 style='text-align: center; color: red;'>Bản quyền thuộc về Ngô Đình Quyền</h3>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; font-weight: bold;'>Hotline / Zalo hỗ trợ: 0325.545.767</p>", unsafe_allow_html=True)

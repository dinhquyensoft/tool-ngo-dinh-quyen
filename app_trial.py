import streamlit as st
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor
import time

# Cấu hình giao diện Ngô Đình Quyền
st.set_page_config(page_title="Đóng dấu ảnh - Ngô Đình Quyền", layout="centered")

# --- KHỞI TẠO BỘ NHỚ TẠM CHO ẢNH ---
if 'processed_images' not in st.session_state:
    st.session_state.processed_images = []

# --- HỆ THỐNG ĐẾM LƯỢT CHỐNG F5 (Dùng Session State kết hợp thông báo) ---
if 'usage_count' not in st.session_state:
    st.session_state.usage_count = 0

# ĐOẠN MÃ NÚT LIÊN HỆ GÓC DƯỚI BÊN TRÁI
st.markdown("""
    <style>
    .contact-container { position: fixed; bottom: 20px; left: 20px; display: flex; flex-direction: column-reverse; gap: 12px; z-index: 999999; }
    .contact-btn { text-decoration: none !important; color: white !important; padding: 10px 18px; border-radius: 50px; font-weight: bold; font-size: 15px; display: flex; align-items: center; justify-content: flex-start; gap: 10px; box-shadow: 2px 4px 12px rgba(0,0,0,0.3); transition: transform 0.2s; min-width: 180px; }
    .btn-zalo { background-color: #0068ff; } .btn-call { background-color: #28a745; }
    .icon-svg { width: 24px; height: 24px; fill: white; }
    </style>
    <div class="contact-container">
        <a href="https://zalo.me/0325545767" target="_blank" class="contact-btn btn-zalo">
            <svg class="icon-svg" viewBox="0 0 40 40"><path d="M20,2C10.1,2,2,8.3,2,16.1c0,4.4,2.6,8.3,6.7,10.9L7,34l7.1-3.6c1.9,0.5,3.9,0.8,5.9,0.8c9.9,0,18-6.3,18-14.1 C38,8.3,29.9,2,20,2z M28.5,22c-0.4,1.1-2.1,1.8-3.3,1.8c-1.3,0-2.6-0.4-3.8-1.2c-1.1-0.7-2.1-1.6-2.9-2.7c-0.7-1-1.3-2.1-1.6-3.3 c-0.3-1.2-0.2-2.1,0.2-2.6c0.4-0.5,1.1-0.8,1.8-0.8c0.3,0,0.6,0.1,0.8,0.2c0.2,0.1,0.4,0.3,0.5,0.6c0.4,1,0.9,2,1.3,3 c0.1,0.3,0.1,0.5,0,0.8c-0.1,0.3-0.4,0.6-0.7,0.9c-0.1,0.1-0.1,0.2-0.1,0.3c0,0.1,0.1,0.3,0.2,0.5c0.6,0.9,1.4,1.7,2.3,2.3 c0.2,0.1,0.4,0.2,0.5,0.2c0.1,0,0.2-0.1,0.3-0.1c0.3-0.3,0.6-0.6,0.9-0.7c0.3-0.1,0.5-0.1,0.8,0c1,0.4,2,0.9,3,1.3 c0.3,0.1,0.5,0.3,0.6,0.5C29.3,21.4,29,21.7,28.5,22z"/></svg>
            Zalo: 0325.545.767
        </a>
        <a href="tel:0325545767" class="contact-btn btn-call">
            <svg class="icon-svg" viewBox="0 0 24 24"><path d="M6.62,10.79C8.06,13.62 10.38,15.94 13.21,17.38L15.41,15.18C15.69,14.9 16.08,14.82 16.43,14.93C17.55,15.3 18.75,15.5 20,15.5A1,1 0 0,1 21,16.5V20A1,1 0 0,1 20,21A17,17 0 0,1 3,4A1,1 0 0,1 4,3H7.5A1,1 0 0,1 8.5,4C8.5,5.25 8.7,6.45 9.07,7.57C9.18,7.92 9.1,8.31 8.82,8.59L6.62,10.79Z"/></svg>
            Gọi: 0325.545.767
        </a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #D4AF37;'>🚀 GIẢI PHÁP THƯƠNG HIỆU (TRIAL)</h1>", unsafe_allow_html=True)

# Hiển thị số lượt dùng thử hiện tại
remaining = 5 - st.session_state.usage_count
if remaining > 0:
    st.info(f"💡 Bạn còn **{remaining}/5** lượt dùng thử miễn phí trong phiên làm việc này.")
else:
    st.error("❌ Bạn đã hết lượt dùng thử miễn phí.")

logo_file = st.file_uploader("🖼️ Bước 1: Chọn Logo (PNG trong suốt)", type=['png'])
image_files = st.file_uploader("📁 Bước 2: Chọn các ảnh muốn đóng dấu", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

st.subheader("📍 Vị trí đóng dấu logo")
pos_options = ["Trên - Trái", "Trên - Giữa", "Trên - Phải", "Giữa - Trái", "Chính Giữa", "Giữa - Phải", "Dưới - Trái", "Dưới - Giữa", "Dưới - Phải"]
selected_pos = st.radio("Chọn vị trí chính xác:", pos_options, index=4, horizontal=True)

st.subheader("⚙️ Cấu hình Watermark")
col1, col2 = st.columns(2)
with col1: size_percent = st.slider("Kích thước (%)", 5, 100, 15)
with col2: opacity = st.slider("Độ rõ nét (%)", 0, 100, 80)

def tinh_toa_do(img_w, img_h, wm_w, wm_h, pos, offset=30):
    mapping = {
        "Trên - Trái": (offset, offset), "Trên - Giữa": ((img_w - wm_w) // 2, offset), "Trên - Phải": (img_w - wm_w - offset, offset),
        "Giữa - Trái": (offset, (img_h - wm_h) // 2), "Chính Giữa": ((img_w - wm_w) // 2, (img_h - wm_h) // 2), "Giữa - Phải": (img_w - wm_w - offset, (img_h - wm_h) // 2),
        "Dưới - Trái": (offset, img_h - wm_h - offset), "Dưới - Giữa": ((img_w - wm_w) // 2, img_h - wm_h - offset), "Dưới - Phải": (img_w - wm_w - offset, img_h - wm_h - offset)
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

# KHỐI XỬ LÝ CHÍNH
if st.button("🚀 BẮT ĐẦU XỬ LÝ"):
    if st.session_state.usage_count >= 5:
        st.markdown("""
            <div style='padding: 25px; border-radius: 15px; background-color: #1a1a1a; border: 2px solid #D4AF37; text-align: center; color: white;'>
                <h2 style='color: #D4AF37;'>💎 NÂNG CẤP BẢN PRO</h2>
                <p>Bạn đã hoàn thành 5 lượt dùng thử xuất sắc!</p>
                <p>Để tiếp tục đóng dấu <b>KHÔNG GIỚI HẠN</b> và hỗ trợ kỹ thuật 24/7:</p>
                <br>
                <a href='https://zalo.me/0325545767' target='_blank' style='background: linear-gradient(45deg, #D4AF37, #F9F0B5); color: black; padding: 12px 30px; border-radius: 25px; text-decoration: none; font-weight: bold; font-size: 18px;'>MỞ KHÓA BẢN QUYỀN NGAY</a>
                <p style='margin-top: 20px; font-size: 12px;'>Sở hữu phần mềm vĩnh viễn chỉ với một chi phí nhỏ</p>
            </div>
        """, unsafe_allow_html=True)
    elif logo_file and image_files:
        with st.spinner('Đang xử lý tốc độ cao...'):
            st.session_state.usage_count += 1
            st.session_state.processed_images = []
            logo_raw = Image.open(logo_file).convert("RGBA")
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(process_single_image, f, logo_raw, size_percent, opacity, selected_pos) for f in image_files]
                for future in futures:
                    name, res_img, byte_data = future.result()
                    st.session_state.processed_images.append({"name": name, "img": res_img, "data": byte_data})
        st.rerun()
    else:
        st.warning("Vui lòng chọn đầy đủ Logo và Ảnh.")

# HIỂN THỊ KẾT QUẢ (CHỐNG REFRESH)
if st.session_state.processed_images:
    for item in st.session_state.processed_images:
        st.image(item["img"], caption=item["name"], use_container_width=True)
        st.download_button(label=f"📥 Tải {item['name']}", data=item["data"], file_name=f"watermark_{item['name']}", mime="image/jpeg", key=f"dl_{item['name']}")
    st.markdown("<p style='text-align: center; color: #D4AF37;'>✨ <i>Đẳng cấp thương hiệu từ Ngô Đình Quyền</i></p>", unsafe_allow_html=True)

# CHÂN TRANG
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: red;'>Bản quyền thuộc về Ngô Đình Quyền</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Hotline / Zalo hỗ trợ: 0325.545.767</p>", unsafe_allow_html=True)

import streamlit as st

from PIL import Image

import io

from concurrent.futures import ThreadPoolExecutor



# Cấu hình giao diện Ngô Đình Quyền - Giữ nguyên tuyệt đối

st.set_page_config(page_title="Đóng dấu ảnh - Ngô Đình Quyền", layout="centered")



# --- CHÈN SAU DÒNG ST.SET_PAGE_CONFIG ---

def check_password():
    """Trả về True nếu người dùng nhập đúng mật khẩu."""
    def password_entered():
        """Kiểm tra mật khẩu người dùng nhập vào."""
        if st.session_state["username"] in st.secrets["users"] and \
           st.session_state["password"] == st.secrets["users"][st.session_state["username"]]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Xóa mật khẩu tạm để bảo mật
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Màn hình đăng nhập khi khách mới truy cập
        st.markdown("<h2 style='text-align: center;'>🔐 ĐĂNG NHẬP ĐỂ SỬ DỤNG</h2>", unsafe_allow_html=True)
        st.text_input("Tên đăng nhập", key="username")
        st.text_input("Mật khẩu", type="password", key="password", on_keydown=None)
        if st.button("Đăng nhập"):
            password_entered()
            st.rerun()
        st.info("💡 Liên hệ Ngô Đình Quyền (0325.545.767) để nhận tài khoản.")
        return False
    elif not st.session_state["password_correct"]:
        # Thông báo khi nhập sai
        st.error("❌ Sai tài khoản hoặc mật khẩu.")
        st.text_input("Tên đăng nhập", key="username")
        st.text_input("Mật khẩu", type="password", key="password")
        if st.button("Thử lại"):
            password_entered()
            st.rerun()
        return False
    else:
        return True

# DỪNG TOÀN BỘ CODE BÊN DƯỚI NẾU CHƯA ĐĂNG NHẬP
if not check_password():
    st.stop()



# --- CHÈN VÀO DƯỚI DÒNG 13 (st.set_page_config) ---
if 'processed_images' not in st.session_state:
    st.session_state.processed_images = []



# ĐOẠN MÃ BỔ SUNG: NÚT LIÊN HỆ GÓC DƯỚI BÊN TRÁI (SỬ DỤNG ICON ZALO CHUẨN)
st.markdown("""
    <style>
    .contact-container {
        position: fixed;
        bottom: 20px;
        left: 20px;
        display: flex;
        flex-direction: column-reverse; 
        gap: 12px;
        z-index: 999999;
    }
    .contact-btn {
        text-decoration: none !important;
        color: white !important;
        padding: 10px 18px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 15px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 10px;
        box-shadow: 2px 4px 12px rgba(0,0,0,0.3);
        transition: transform 0.2s;
        min-width: 180px;
    }
    .contact-btn:hover {
        transform: scale(1.05);
        text-decoration: none !important;
    }
    .btn-zalo { background-color: #0068ff; }
    .btn-call { background-color: #28a745; }
    
    /* Cấu hình icon */
    .icon-svg {
        width: 24px;
        height: 24px;
        fill: white;
    }
    </style>

    <div class="contact-container">
        <a href="https://zalo.me/0325545767" target="_blank" class="contact-btn btn-zalo">
            <svg class="icon-svg" viewBox="0 0 40 40">
                <path d="M20,2C10.1,2,2,8.3,2,16.1c0,4.4,2.6,8.3,6.7,10.9L7,34l7.1-3.6c1.9,0.5,3.9,0.8,5.9,0.8c9.9,0,18-6.3,18-14.1 C38,8.3,29.9,2,20,2z M28.5,22c-0.4,1.1-2.1,1.8-3.3,1.8c-1.3,0-2.6-0.4-3.8-1.2c-1.1-0.7-2.1-1.6-2.9-2.7c-0.7-1-1.3-2.1-1.6-3.3 c-0.3-1.2-0.2-2.1,0.2-2.6c0.4-0.5,1.1-0.8,1.8-0.8c0.3,0,0.6,0.1,0.8,0.2c0.2,0.1,0.4,0.3,0.5,0.6c0.4,1,0.9,2,1.3,3 c0.1,0.3,0.1,0.5,0,0.8c-0.1,0.3-0.4,0.6-0.7,0.9c-0.1,0.1-0.1,0.2-0.1,0.3c0,0.1,0.1,0.3,0.2,0.5c0.6,0.9,1.4,1.7,2.3,2.3 c0.2,0.1,0.4,0.2,0.5,0.2c0.1,0,0.2-0.1,0.3-0.1c0.3-0.3,0.6-0.6,0.9-0.7c0.3-0.1,0.5-0.1,0.8,0c1,0.4,2,0.9,3,1.3 c0.3,0.1,0.5,0.3,0.6,0.5C29.3,21.4,29,21.7,28.5,22z"/>
            </svg>
            Zalo: 0325.545.767
        </a>
        <a href="tel:0325545767" class="contact-btn btn-call">
            <svg class="icon-svg" viewBox="0 0 24 24">
                <path d="M6.62,10.79C8.06,13.62 10.38,15.94 13.21,17.38L15.41,15.18C15.69,14.9 16.08,14.82 16.43,14.93C17.55,15.3 18.75,15.5 20,15.5A1,1 0 0,1 21,16.5V20A1,1 0 0,1 20,21A17,17 0 0,1 3,4A1,1 0 0,1 4,3H7.5A1,1 0 0,1 8.5,4C8.5,5.25 8.7,6.45 9.07,7.57C9.18,7.92 9.1,8.31 8.82,8.59L6.62,10.79Z"/>
            </svg>
            Gọi: 0325.545.767
        </a>
    </div>
    """, unsafe_allow_html=True)



# Tiêu đề gốc

st.markdown("<h1 style='text-align: center;'>🚀 GIẢI PHÁP ĐỊNH VỊ THƯƠNG HIỆU HÌNH ẢNH</h1>", unsafe_allow_html=True)

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



# THAY THẾ TOÀN BỘ KHỐI LỆNH NÚT BẤM VÀ HIỂN THỊ CŨ BẰNG ĐOẠN NÀY
if st.button("🚀 BẮT ĐẦU XỬ LÝ (TỐC ĐỘ CAO)"):
    if logo_file and image_files:
        st.session_state.processed_images = [] # Làm mới bộ nhớ mỗi lần nhấn nút
        logo_raw = Image.open(logo_file).convert("RGBA")
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_single_image, f, logo_raw, size_percent, opacity, selected_pos) for f in image_files]
            for future in futures:
                name, res_img, byte_data = future.result()
                # Cất ảnh vào bộ nhớ thay vì chỉ hiển thị
                st.session_state.processed_images.append({"name": name, "img": res_img, "data": byte_data})

# HIỂN THỊ KẾT QUẢ TỪ BỘ NHỚ (Giúp ảnh không bị mất khi bấm tải)
if st.session_state.processed_images:
    for item in st.session_state.processed_images:
        st.image(item["img"], caption=item["name"], use_container_width=True)
        st.download_button(
            label=f"📥 Tải {item['name']}", 
            data=item["data"], 
            file_name=f"watermark_{item['name']}", 
            mime="image/jpeg", 
            key=f"dl_{item['name']}" # Key này giữ cho trang web không bị reset
        )


# CHÂN TRANG BẢN QUYỀN

st.markdown("---")

st.markdown("<h3 style='text-align: center; color: red;'>Bản quyền thuộc về Ngô Đình Quyền</h3>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; font-weight: bold;'>Hotline / Zalo hỗ trợ: 0325.545.767</p>", unsafe_allow_html=True)

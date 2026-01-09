import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Cấu hình giao diện Web nguyên bản của Ngô Đình Quyền
st.set_page_config(page_title="Đóng dấu ảnh - Ngô Đình Quyền", layout="centered")

st.markdown("<h1 style='text-align: center;'>🚀 CÔNG CỤ ĐÓNG DẤU ẢNH CHUYÊN NGHIỆP</h1>", unsafe_allow_html=True)

# --- PHẦN 1: CHỌN HÌNH THỨC ĐÓNG DẤU ---
type_wm = st.radio("Chọn loại đóng dấu:", ["Dùng Logo (Ảnh PNG)", "Dùng Chữ (Nhập text)"], horizontal=True)

logo_file = None
wm_text = ""
font_choice = "Arial"

if type_wm == "Dùng Logo (Ảnh PNG)":
    logo_file = st.file_uploader("🖼️ Bước 1: Chọn Logo (PNG trong suốt)", type=['png'])
else:
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1:
        wm_text = st.text_input("Nhập nội dung chữ:", "Ngô Đình Quyền - 0325 545 767")
    with col_t2:
        font_choice = st.selectbox("Font chữ:", ["Arial", "Courier", "Verdana", "Times New Roman"])

image_files = st.file_uploader("📁 Bước 2: Chọn các ảnh muốn đóng dấu", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

# --- PHẦN 2: BẢNG 9 Ô VỊ TRÍ (STYLE ILLUSTRATOR) ---
st.subheader("📍 Vị trí đóng dấu (9 ô)")
# Giữ nguyên logic 3 cột tơi ưu cho điện thoại
c_left, c_mid, c_right = st.columns(3)

with c_left:
    pos_tl = st.checkbox("Trên - Trái", key="tl")
    pos_ml = st.checkbox("Giữa - Trái", key="ml")
    pos_bl = st.checkbox("Dưới - Trái", key="bl")
with c_mid:
    pos_tc = st.checkbox("Trên - Giữa", key="tc")
    pos_mc = st.checkbox("Chính Giữa", key="mc", value=True) # Mặc định giữa
    pos_bc = st.checkbox("Dưới - Giữa", key="bc")
with c_right:
    pos_tr = st.checkbox("Trên - Phải", key="tr")
    pos_mr = st.checkbox("Giữa - Phải", key="mr")
    pos_br = st.checkbox("Dưới - Phải", key="br")

def get_selected_pos():
    if pos_tl: return "Trên - Trái"
    if pos_tc: return "Trên - Giữa"
    if pos_tr: return "Trên - Phải"
    if pos_ml: return "Giữa - Trái"
    if pos_mc: return "Chính Giữa"
    if pos_mr: return "Giữa - Phải"
    if pos_bl: return "Dưới - Trái"
    if pos_bc: return "Dưới - Giữa"
    return "Dưới - Phải"

# --- PHẦN 3: CẤU HÌNH WATERMARK (GIỮ NGUYÊN GIAO DIỆN CŨ) ---
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

# --- PHẦN 4: XỬ LÝ VÀ HIỂN THỊ ---
if st.button("🚀 BẮT ĐẦU XỬ LÝ"):
    if image_files:
        current_pos = get_selected_pos()
        
        # Chuẩn bị Logo nếu chọn chế độ ảnh
        logo_raw = None
        if type_wm == "Dùng Logo (Ảnh PNG)" and logo_file:
            logo_raw = Image.open(logo_file).convert("RGBA")

        for uploaded_file in image_files:
            img = Image.open(uploaded_file).convert("RGBA")
            img_w, img_h = img.size
            
            # Khởi tạo lớp đè
            overlay = Image.new("RGBA", img.size, (0,0,0,0))
            
            if type_wm == "Dùng Logo (Ảnh PNG)" and logo_raw:
                # Logic Resize Logo theo % ảnh gốc
                scale = (img_w * size_percent / 100) / logo_raw.size[0]
                wm_w = int(logo_raw.size[0] * scale)
                wm_h = int(logo_raw.size[1] * scale)
                wm_final = logo_raw.resize((wm_w, wm_h), Image.LANCZOS)
            else:
                # Logic đóng dấu Chữ
                draw = ImageDraw.Draw(overlay)
                # Tự động tính kích cỡ font theo chiều rộng ảnh
                f_size = int(img_w * size_percent / 500) 
                try:
                    font = ImageFont.truetype(f"{font_choice}.ttf", f_size)
                except:
                    font = ImageFont.load_default()
                
                left, top, right, bottom = draw.textbbox((0, 0), wm_text, font=font)
                wm_w, wm_h = right - left, bottom - top
                wm_final = Image.new("RGBA", (wm_w + 10, wm_h + 10), (0,0,0,0))
                d = ImageDraw.Draw(wm_final)
                d.text((5, 5), wm_text, font=font, fill=(255, 255, 255, int(255 * opacity / 100)))

            # Xử lý độ mờ cho Logo ảnh
            if type_wm == "Dùng Logo (Ảnh PNG)":
                alpha = wm_final.split()[3].point(lambda p: p * (opacity / 100))
                wm_final.putalpha(alpha)

            # Tính tọa độ và dán
            x, y = tinh_toa_do(img_w, img_h, wm_w, wm_h, current_pos)
            img.paste(wm_final, (x, y), wm_final)
            
            # Hiển thị kết quả
            res_img = img.convert("RGB")
            st.image(res_img, caption=uploaded_file.name, use_container_width=True)
            
            # Nút tải về (Fixed lỗi data=...)
            buf = io.BytesIO()
            res_img.save(buf, format="JPEG", quality=90)
            st.download_button(label=f"📥 Tải {uploaded_file.name}", data=buf.getvalue(), file_name=f"wm_{uploaded_file.name}", mime="image/jpeg")

# --- PHẦN 5: CHÂN TRANG BẢN QUYỀN (GIỮ NGUYÊN) ---
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: red;'>Bản quyền thuộc về Ngô Đình Quyền</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Hotline / Zalo hỗ trợ: 0325.545.767</p>", unsafe_allow_html=True)

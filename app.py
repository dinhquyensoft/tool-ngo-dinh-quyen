import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Cấu hình Web App Ngô Đình Quyền
st.set_page_config(page_title="Watermark Pro - Ngô Đình Quyền", layout="centered")

st.markdown("<h1 style='text-align: center;'>🎨 WATERMARK PRO (ILLUSTRATOR STYLE)</h1>", unsafe_allow_html=True)

# 1. CHỌN NGUỒN (Ảnh hoặc Chữ)
type_wm = st.radio("Chọn loại đóng dấu:", ["Dùng Logo (Ảnh PNG)", "Dùng Chữ (Nhập text)"], horizontal=True)

logo_file = None
wm_text = ""
if type_wm == "Dùng Logo (Ảnh PNG)":
    logo_file = st.file_uploader("🖼️ Bước 1: Chọn Logo PNG", type=['png'])
else:
    wm_text = st.text_input("Nhập chữ muốn đóng dấu:", "Ngô Đình Quyền - 0325 545 767")
    font_choice = st.selectbox("Chọn Font chữ:", ["Arial", "Courier", "Verdana", "Times New Roman"])

image_files = st.file_uploader("📁 Bước 2: Chọn ảnh cần xử lý", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)

# 2. BẢNG CHỌN 9 VỊ TRÍ (STYLE ILLUSTRATOR)
st.subheader("📍 Vị trí đóng dấu (9 ô)")
col_a, col_b, col_c = st.columns([1,1,1])

# Tạo logic 9 ô chọn bằng Radio theo dạng Grid
with col_a:
    pos_tl = st.checkbox("Trên - Trái", key="tl")
    pos_ml = st.checkbox("Giữa - Trái", key="ml")
    pos_bl = st.checkbox("Dưới - Trái", key="bl")
with col_b:
    pos_tc = st.checkbox("Trên - Giữa", key="tc")
    pos_mc = st.checkbox("Chính Giữa", key="mc", value=True)
    pos_bc = st.checkbox("Dưới - Giữa", key="bc")
with col_c:
    pos_tr = st.checkbox("Trên - Phải", key="tr")
    pos_mr = st.checkbox("Giữa - Phải", key="mr")
    pos_br = st.checkbox("Dưới - Phải", key="br")

# Logic chuyển đổi checkbox thành vị trí
def get_pos():
    if pos_tl: return "Trên - Trái"
    if pos_tc: return "Trên - Giữa"
    if pos_tr: return "Trên - Phải"
    if pos_ml: return "Giữa - Trái"
    if pos_mc: return "Chính Giữa"
    if pos_mr: return "Giữa - Phải"
    if pos_bl: return "Dưới - Trái"
    if pos_bc: return "Dưới - Giữa"
    return "Dưới - Phải"

# 3. CẤU HÌNH THÔNG SỐ
st.subheader("⚙️ Cấu hình chi tiết")
c1, c2 = st.columns(2)
with c1:
    size_percent = st.slider("Kích thước (%)", 5, 100, 20)
with c2:
    opacity = st.slider("Độ mờ (%)", 10, 100, 80)

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

if st.button("🚀 XỬ LÝ VÀ TẢI VỀ"):
    if not image_files:
        st.error("Vui lòng chọn ảnh!")
    else:
        for uploaded_file in image_files:
            img = Image.open(uploaded_file).convert("RGBA")
            img_w, img_h = img.size
            
            # TẠO LỚP WATERMARK
            wm_layer = Image.new("RGBA", (img_w, img_h), (0,0,0,0))
            
            if type_wm == "Dùng Logo (Ảnh PNG)" and logo_file:
                logo = Image.open(logo_file).convert("RGBA")
                scale = (img_w * size_percent / 100) / logo.size[0]
                logo = logo.resize((int(logo.size[0]*scale), int(logo.size[1]*scale)), Image.LANCZOS)
                wm_w, wm_h = logo.size
            else:
                # Tạo watermark bằng chữ
                draw = ImageDraw.Draw(wm_layer)
                f_size = int(img_w * size_percent / 500) # Tính font size theo ảnh
                try:
                    font = ImageFont.truetype(f"{font_choice}.ttf", f_size)
                except:
                    font = ImageFont.load_default()
                
                left, top, right, bottom = draw.textbbox((0, 0), wm_text, font=font)
                wm_w, wm_h = right - left, bottom - top
                logo = Image.new("RGBA", (wm_w + 10, wm_h + 10), (0,0,0,0))
                d = ImageDraw.Draw(logo)
                d.text((5, 5), wm_text, font=font, fill=(255, 255, 255, int(255 * opacity / 100)))

            x, y = tinh_toa_do(img_w, img_h, wm_w, wm_h, get_pos())
            img.paste(logo, (x, y), logo if type_wm == "Dùng Logo (Ảnh PNG)" else None)
            
            # Hiển thị và cho tải về
            final_img = img.convert("RGB")
            st.image(final_img, caption=uploaded_file.name, use_container_width=True)
            
            buf = io.BytesIO()
            final_img.save(buf, format="JPEG", quality=90)
            st.download_button(f"📥 Tải {uploaded_file.name}", buf.getvalue(), f"wm_{uploaded_file.name}", "image/jpeg")

# Chân trang Ngô Đình Quyền
st.markdown("---")
st.markdown("<p style='text-align: center; color: red; font-weight: bold;'>Bản quyền thuộc về Ngô Đình Quyền. Zalo: 0325.545.767</p>", unsafe_allow_html=True)

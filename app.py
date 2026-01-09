import streamlit as st
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor

# Cấu hình giao diện Ngô Đình Quyền - Giữ nguyên tuyệt đối
st.set_page_config(page_title="Đóng dấu ảnh - Ngô Đình Quyền", layout="centered")

# CSS TÙY CHỈNH: Đưa nút phóng to (fullscreen) xuống góc dưới bên phải và làm to hơn
st.markdown("""
    <style>
    /* Ép nút fullscreen của ảnh xuống vị trí bạn khoanh tròn */
    [data-testid="stImage"] [data-testid="stImageActionButton"] {
        bottom: 10px !important;
        right: 10px !important;
        top: auto !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 5px !important;
        padding: 5px !important;
    }
    /* Làm icon to hơn để dễ bấm trên điện thoại */
    [data-testid="stImageActionButton"] svg {
        width: 30px !important;
        height: 30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Tiêu đề gốc
st.markdown("<h1 style='text-align: center;'>🚀 CÔNG CỤ ĐÓNG DẤU ẢNH CHUYÊN NGHIỆP</h1>", unsafe_allow_html=True)

# BƯỚC 1: CHỌN LOGO
logo_file = st.file_uploader("🖼️ Bước 1: Chọn Logo (PNG trong suốt)", type=['png'])

# BƯỚC 2: CHỌN ẢNH CẦN XỬ LÝ
image_files = st.file_uploader("📁 Bước 2: Chọn các ảnh muốn đóng dấu", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

# CẬP NHẬT VỊ TRÍ 9 NÚT: Chia thành 3 hàng 3 cột (Style Illustrator)
st.subheader("📍 Vị trí đóng dấu (9 ô)")
row1_col1, row1_col2, row1_col3 = st.columns(3)
row2_col1, row2_col2, row2_col3 = st.columns(3)
row3_col1, row3_col2, row3_col3 = st.columns(3)

with row1_col1: tl = st.radio(" ", ["Trên - Trái"], key="r_tl", label_visibility="collapsed")
with row1_col2: tc = st.radio(" ", ["Trên - Giữa"], key="r_tc", label_visibility="collapsed")
with row1_col3: tr = st.radio(" ", ["Trên - Phải"], key="r_tr", label_visibility="collapsed")

with row2_col1: ml = st.radio(" ", ["Giữa - Trái"], key="r_ml", label_visibility="collapsed")
with row2_col2: mc = st.radio(" ", ["Chính Giữa"], key="r_mc", label_visibility="collapsed")
with row2_col3: mr = st.radio(" ", ["Giữa - Phải"], key="r_mr", label_visibility="collapsed")

with row3_col1: bl = st.radio(" ", ["Dưới - Trái"], key="r_bl", label_visibility="collapsed")
with row3_col2: bc = st.radio(" ", ["Dưới - Giữa"], key="r_bc", label_visibility="collapsed")
with row3_col3: br = st.radio(" ", ["Dưới - Phải"], key="r_br", label_visibility="collapsed")

# Logic Radio giả lập Grid (Chỉ chọn được 1 trong 9 hàng ngang)
# Để đơn giản và chính xác nhất, tôi dùng 1 Radio duy nhất nhưng chia Layout
st.write("---")
pos_choice = st.radio("Xác nhận vị trí đóng dấu:", 
                      ["Trên - Trái", "Trên - Giữa", "Trên - Phải", 
                       "Giữa - Trái", "Chính Giữa", "Giữa - Phải", 
                       "Dưới - Trái", "Dưới - Giữa", "Dưới - Phải"], 
                      index=4, horizontal=True)

# CẤU HÌNH WATERMARK (GIỮ NGUYÊN)
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
                # Hiển thị ảnh với tùy chỉnh nút fullscreen ở góc dưới bên phải
                st.image(res_img, caption=name, use_container_width=True)
                st.download_button(label=f"📥 Tải {name}", data=byte_data, file_name=f"wm_{name}", mime="image/jpeg")

# CHÂN TRANG BẢN QUYỀN (GIỮ NGUYÊN)
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: red;'>Bản quyền thuộc về Ngô Đình Quyền</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Hotline / Zalo hỗ trợ: 0325.545.767</p>", unsafe_allow_html=True)

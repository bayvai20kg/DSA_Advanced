import streamlit as st
import json
import os
from radix_trie import RadixTrie

DATA_FILE = "dictionary_data.json"

# Cấu hình trang web (Phải đặt ở dòng đầu tiên của Streamlit)
st.set_page_config(page_title="Từ Điển Radix Trie", page_icon="📖", layout="centered")

# --- MODEL: Khởi tạo & Lưu trữ dữ liệu ---
# Đảm bảo Trie chỉ được khởi tạo và load file 1 lần duy nhất
if 'trie' not in st.session_state:
    st.session_state.trie = RadixTrie()
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for word, definition in data.items():
            st.session_state.trie.insert(word, definition)

def save_data():
    data = {word: definition for word, definition in st.session_state.trie.all_words()}
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# --- SIDEBAR THỐNG KÊ (Nâng cấp giao diện 1) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2232/2232688.png", width=120)
    st.markdown("## 📊 Thống Kê")
    total_words = len(st.session_state.trie.all_words())
    st.metric(label="Tổng số mục từ", value=total_words)
    st.divider()
    st.info("💡 Mẹo: Sử dụng tab 'Trực quan hóa' để xem cấu trúc cây Radix Trie thay đổi sau mỗi thao tác.")

# --- VIEW & CONTROLLER ---
st.title("📖 Từ Điển Tiếng Anh")
st.markdown("**Cấu trúc dữ liệu lõi:** `Radix Trie` (Patricia Trie)")

# Chia giao diện thành các Tab cho gọn gàng
tab_search, tab_add, tab_delete, tab_tree = st.tabs([
    "🔍 Tra cứu", "➕ Thêm / Cập nhật", "🗑️ Xóa từ", "🌳 Trực quan hóa Cây"
])

# 1. TAB TÌM KIẾM
with tab_search:
    st.header("Tra cứu từ vựng")
    search_word = st.text_input("Nhập từ cần tìm:", key="search_input").strip()
    
    if st.button("Tìm kiếm", type="primary"):
        if search_word:
            meaning = st.session_state.trie.search(search_word)
            if meaning:
                # Nâng cấp giao diện 3: Thẻ kết quả HTML/CSS siêu đẹp
                st.markdown(f"""
                <div style="padding: 20px; border-radius: 10px; background-color: #f0f7ff; border-left: 6px solid #0068c9; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
                    <h2 style="margin-top: 0; color: #0068c9; font-family: sans-serif;">{search_word}</h2>
                    <p style="font-size: 18px; color: #333; margin-bottom: 0;">{meaning}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"Không tìm thấy từ '{search_word}' trong từ điển.")
        else:
            st.warning("Vui lòng nhập từ để tìm.")

# 2. TAB THÊM TỪ
with tab_add:
    st.header("Thêm hoặc Cập nhật từ")
    col1, col2 = st.columns(2)
    with col1:
        add_word = st.text_input("Từ (Word):", key="add_word").strip()
    with col2:
        add_meaning = st.text_input("Nghĩa (Definition):", key="add_meaning").strip()
    
    if st.button("Lưu từ vựng", type="primary", use_container_width=True):
        if add_word and add_meaning:
            is_new = st.session_state.trie.insert(add_word, add_meaning)
            save_data()
            if is_new:
                # Nâng cấp giao diện 2: Toast thông báo và bóng bay
                st.toast(f"Đã thêm từ mới: {add_word}", icon="🎉")
                st.balloons()
                st.success(f"✔ Đã thêm từ mới: **{add_word}** ➞ {add_meaning}")
            else:
                st.toast(f"Đã cập nhật nghĩa từ: {add_word}", icon="🔄")
                st.info(f"ℹ Đã cập nhật nghĩa: **{add_word}** ➞ {add_meaning}")
        else:
            st.warning("Vui lòng nhập đầy đủ cả từ và nghĩa.")

# 3. TAB XÓA TỪ
with tab_delete:
    st.header("Xóa từ vựng")
    del_word = st.text_input("Nhập từ cần xóa:", key="del_word").strip()
    
    if st.button("Xóa từ", type="primary"):
        if del_word:
            if st.session_state.trie.search(del_word) is not None:
                st.session_state.trie.delete(del_word)
                save_data()
                st.success(f"✔ Đã xóa từ '{del_word}' thành công.")
            else:
                st.error(f"✘ Từ '{del_word}' không tồn tại.")
        else:
            st.warning("Vui lòng nhập từ để xóa.")

# 4. TAB TRỰC QUAN HÓA (Hiển thị Cây)
with tab_tree:
    st.header("Trạng thái Radix Trie hiện tại")
    st.info("Chụp ảnh phần này đưa vào báo cáo PDF để thể hiện sự thay đổi dữ liệu sau các thao tác Thêm/Xóa.")
    
    # Nút refresh để cập nhật lại view
    st.button("🔄 Làm mới hiển thị")
    
    tree_str = st.session_state.trie.visualize()
    st.code(tree_str, language="text")

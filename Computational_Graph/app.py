import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from backend import (
    train_linear_regression,
    predict,
    compute_metrics,
    plot_regression,
    plot_loss_curve,
    draw_manual_computational_graph,
    Value,
)

st.set_page_config(page_title="Dự đoán điểm cuối kỳ", page_icon="", layout="wide")
st.title("Dự đoán điểm cuối kỳ dựa trên điểm giữa kỳ")
st.markdown("---")

# --- Session state ---
for key in ['log', 'W', 'b', 'losses', 'trained', 'X', 'Y']:
    if key not in st.session_state:
        if key == 'log':
            st.session_state[key] = ""
        elif key == 'trained':
            st.session_state[key] = False
        else:
            st.session_state[key] = None


def log_msg(msg):
    st.session_state.log += msg + "\n"


# --- Dataset ---
uploaded_file = st.sidebar.file_uploader("Tải lên file dataset (.xlsx)", type="xlsx")

if uploaded_file is None:
    base = Path(__file__).resolve().parent.parent
    candidates = [
        base / "Homework" / "TRAIN2.xlsx",
        base / "Program (Demo)" / "TRAIN.xlsx",
    ]
    data_path = None
    for p in candidates:
        if p.exists():
            data_path = p
            break
    if data_path is None:
        st.error("Không tìm thấy file dataset. Vui lòng upload file .xlsx.")
        st.stop()
    df = pd.read_excel(data_path)
else:
    df = pd.read_excel(uploaded_file)

st.subheader("Dữ liệu")
st.dataframe(df.head(10), width=800)
st.caption(f"Số mẫu: {df.shape[0]} | Số cột: {df.shape[1]}")

cols = df.columns.tolist()
if 'midterm' in cols and 'final' in cols:
    x_col, y_col = 'midterm', 'final'
elif len(cols) >= 2:
    x_col = st.selectbox("Cột đầu vào (giữa kỳ)", cols, index=0)
    y_col = st.selectbox("Cột đầu ra (cuối kỳ)", cols, index=1)
else:
    st.error("Dataset cần ít nhất 2 cột.")
    st.stop()

X_data = df[x_col].values.astype(np.float32)
Y_data = df[y_col].values.astype(np.float32)

# --- Training controls ---
st.sidebar.header("Cấu hình huấn luyện")
c1, c2, c3 = st.sidebar.columns(3)
lr = c1.number_input("Learning rate", value=0.01, format="%.4f")
epochs = c2.number_input("Số epoch", value=500, step=100)
train_btn = c3.button("Huấn luyện", type="primary")

if train_btn:
    st.session_state.log = ""
    st.session_state.trained = False
    with st.spinner("Đang huấn luyện mô hình..."):
        W, b, losses = train_linear_regression(
            X_data, Y_data, lr=lr, epochs=int(epochs), log_callback=log_msg
        )
    st.session_state.W = W
    st.session_state.b = b
    st.session_state.losses = losses
    st.session_state.X = X_data
    st.session_state.Y = Y_data
    st.session_state.trained = True

# --- Results ---
if st.session_state.trained:
    W = st.session_state.W
    b = st.session_state.b
    losses = st.session_state.losses
    X_data = st.session_state.X
    Y_data = st.session_state.Y

    st.markdown("---")
    st.subheader("Kết quả huấn luyện")

    Y_pred = predict(X_data, W, b)
    mse_final, r2 = compute_metrics(Y_data, Y_pred)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("W (trọng số)", f"{W:.6f}")
    col2.metric("b (bias)", f"{b:.6f}")
    col3.metric("MSE", f"{mse_final:.6f}")
    col4.metric("R²", f"{r2:.6f}")

    st.markdown("### Công thức toán học")
    st.latex(f"\\text{{final}} = {W:.4f} \\times \\text{{midterm}} + {b:.4f}")

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_regression(X_data, Y_data, W, b))
    with col2:
        st.pyplot(plot_loss_curve(losses))

    st.markdown("### Đồ thị tính toán (Computational Graph)")
    st.pyplot(draw_manual_computational_graph())

    with st.expander("Xem log huấn luyện"):
        st.text(st.session_state.log)

    # --- Prediction ---
    st.markdown("---")
    st.subheader("Dự đoán điểm cuối kỳ")

    val = st.number_input("Nhập điểm giữa kỳ:", min_value=0.0, max_value=10.0, value=5.0, step=0.5)
    if st.button("Dự đoán", type="primary"):
        pred = float(predict(np.array([val]), W, b)[0])
        pred_clipped = np.clip(pred, 0, 10)
        st.success(f"Điểm cuối kỳ dự đoán: **{pred:.4f}** (đã làm tròn: {pred_clipped:.4f})")

        fig = plot_regression(X_data, Y_data, W, b)
        ax = fig.axes[0]
        ax.scatter([val], [pred], color='green', s=200, zorder=5,
                   marker='*', label=f'Dự đoán: {pred:.4f}')
        ax.legend()
        st.pyplot(fig)

else:
    st.info("Nhấn **Huấn luyện** ở sidebar để bắt đầu training.")

st.markdown("---")
st.caption("CS523 - Computational Graph | Hồi quy tuyến tính với đồ thị tính toán")

# ==============================================================================
# កម្មវិធី៖ គ្រប់គ្រងចំណូល-ចំណាយការចិញ្ចឹមជ្រូក (Pig Farming Income-Expense Management)
# ផ្លែតហ្វម៖ Python Streamlit
# អ្នកអភិវឌ្ឍន៍៖ អ្នកជំនាញបង្កើតកម្មវិធី និងអ្នកឯកទេសហិរញ្ញវត្ថុ
# ==============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# ------------------------------------------------------------------------------
# ១. ការកំណត់រចនាសម្ព័ន្ធទូទៅ (Page Configuration)
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="ប្រព័ន្ធគ្រប់គ្រងចំណូល-ចំណាយការចិញ្ចឹមជ្រូក",
    page_icon="🐖",
    layout="wide",
    initial_sidebar_state="expanded"
)

BATCHES_FILE = "batches.csv"
TRANSACTIONS_FILE = "transactions.csv"

# ------------------------------------------------------------------------------
# ២. មុខងារគ្រប់គ្រងទិន្នន័យ CSV (Data Storage Helper Functions)
# ------------------------------------------------------------------------------
def load_batches():
    if os.path.exists(BATCHES_FILE):
        return pd.read_csv(BATCHES_FILE)
    else:
        default_df = pd.DataFrame([
            {
                "batch_id": "BATCH_001",
                "batch_name": "វគ្គទី១ - ដើមឆ្នាំ២០២៦",
                "start_date": "2026-01-01",
                "pig_count": 20,
                "status": "កំពុងចិញ្ចឹម",
                "note": "ចិញ្ចឹមជ្រូកសាច់ ២០ ក្បាល"
            }
        ])
        default_df.to_csv(BATCHES_FILE, index=False)
        return default_df

def save_batches(df):
    df.to_csv(BATCHES_FILE, index=False)

def load_transactions():
    if os.path.exists(TRANSACTIONS_FILE):
        df = pd.read_csv(TRANSACTIONS_FILE)
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
        return df
    else:
        default_df = pd.DataFrame([
            {
                "id": "TXN_001",
                "batch_id": "BATCH_001",
                "date": "2026-01-05",
                "type": "ចំណាយ",
                "category": "ថ្លៃកូនជ្រូក",
                "description": "ទិញកូនជ្រូក ២០ ក្បាល",
                "amount": 5000000,
                "qty": 20,
                "unit": "ក្បាល"
            },
            {
                "id": "TXN_002",
                "batch_id": "BATCH_001",
                "date": "2026-01-10",
                "type": "ចំណាយ",
                "category": "ថ្លៃចំណី+កន្ទក់",
                "description": "ទិញចំណី ១០ បាវ",
                "amount": 1200000,
                "qty": 10,
                "unit": "បាវ"
            },
            {
                "id": "TXN_003",
                "batch_id": "BATCH_001",
                "date": "2026-01-15",
                "type": "ចំណាយ",
                "category": "ថ្លៃថ្នាំពេទ្យ",
                "description": "ចាក់វ៉ាក់សាំងការពារជំងឺ",
                "amount": 350000,
                "qty": 1,
                "unit": "ឈុត"
            },
            {
                "id": "TXN_004",
                "batch_id": "BATCH_001",
                "date": "2026-05-20",
                "type": "ចំណូល",
                "category": "លក់ជ្រូកសាច់",
                "description": "លក់ជ្រូក ២០ ក្បាល",
                "amount": 11500000,
                "qty": 20,
                "unit": "ក្បាល"
            }
        ])
        default_df.to_csv(TRANSACTIONS_FILE, index=False)
        return default_df

def save_transactions(df):
    df.to_csv(TRANSACTIONS_FILE, index=False)

def format_khr(val):
    return f"{int(val):,} ៛"

# ------------------------------------------------------------------------------
# ៣. ផ្ទុកទិន្នន័យចូលក្នុង Session State
# ------------------------------------------------------------------------------
if "batches_df" not in st.session_state:
    st.session_state["batches_df"] = load_batches()

if "txns_df" not in st.session_state:
    st.session_state["txns_df"] = load_transactions()

batches_df = st.session_state["batches_df"]
txns_df = st.session_state["txns_df"]

# ------------------------------------------------------------------------------
# ៤. របារខាងឆ្វេង (Sidebar Layout & Batch Navigation)
# ------------------------------------------------------------------------------
st.sidebar.title("🐖 ប្រព័ន្ធគ្រប់គ្រងជ្រូក")
st.sidebar.markdown("---")

st.sidebar.subheader("📌 ជ្រើសរើសវគ្គចិញ្ចឹម")
batch_options = ["បង្ហាញទាំងអស់ (All Batches)"] + list(batches_df["batch_name"].unique())
selected_batch_name = st.sidebar.selectbox("ជ្រើសរើសវគ្គ៖", batch_options)

selected_batch_id = None
if selected_batch_name != "បង្ហាញទាំងអស់ (All Batches)":
    selected_batch_id = batches_df[batches_df["batch_name"] == selected_batch_name]["batch_id"].values[0]

# ទម្រង់បង្កើតវគ្គថ្មី
with st.sidebar.expander("➕ បង្កើតវគ្គចិញ្ចឹមថ្មី"):
    with st.form("new_batch_form", clear_on_submit=True):
        new_batch_name = st.text_input("ឈ្មោះវគ្គ៖")
        new_start_date = st.date_input("ថ្ងៃចាប់ផ្តើម៖", datetime.today())
        new_pig_count = st.number_input("ចំនួនជ្រូក (ក្បាល)៖", min_value=1, value=10)
        new_note = st.text_area("ចំណាំបន្ថែម៖")
        submit_batch = st.form_submit_button("រក្សាទុកវគ្គថ្មី")

        if submit_batch:
            if new_batch_name.strip() != "":
                new_id = f"BATCH_{len(batches_df) + 1:03d}"
                new_row = {
                    "batch_id": new_id,
                    "batch_name": new_batch_name,
                    "start_date": str(new_start_date),
                    "pig_count": new_pig_count,
                    "status": "កំពុងចិញ្ចឹម",
                    "note": new_note
                }
                batches_df = pd.concat([batches_df, pd.DataFrame([new_row])], ignore_index=True)
                save_batches(batches_df)
                st.session_state["batches_df"] = batches_df
                st.success("បានបង្កើតវគ្គថ្មី!")
                st.rerun()

# ------------------------------------------------------------------------------
# ៥. ផ្នែកកណ្តាល - ផ្ទាំងគ្រប់គ្រង និងទិន្នន័យ (Main UI & Metrics)
# ------------------------------------------------------------------------------
st.title("🐖 ប្រព័ន្ធគ្រប់គ្រងចំណូល-ចំណាយការចិញ្ចឹមជ្រូក")
st.subheader(f"📊 ទិន្នន័យ៖ {selected_batch_name}")

if selected_batch_id:
    filtered_txns = txns_df[txns_df["batch_id"] == selected_batch_id]
else:
    filtered_txns = txns_df.copy()

total_income = filtered_txns[filtered_txns["type"] == "ចំណូល"]["amount"].sum()
total_expense = filtered_txns[filtered_txns["type"] == "ចំណាយ"]["amount"].sum()
net_profit = total_income - total_expense

m1, m2, m3 = st.columns(3)
m1.metric("💵 ចំណូលសរុប", format_khr(total_income))
m2.metric("💸 ចំណាយសរុប", format_khr(total_expense))
m3.metric("🟢 ប្រាក់ចំណេញ/ខាតសុទ្ធ", format_khr(net_profit))

# ------------------------------------------------------------------------------
# ៦. ផ្ទាំងទំព័រ (Tabs: ក្រាប, កត់ត្រា, តារាង)
# ------------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📈 ក្រាបបង្ហាញទិន្នន័យ", "📝 កត់ត្រាចំណូល-ចំណាយ", "📋 តារាងប្រតិបត្តិការ"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📊 ប្រៀបធៀប ចំណូល vs ចំណាយ")
        summary_df = pd.DataFrame({
            "ប្រភេទ": ["ចំណូលសរុប", "ចំណាយសរុប"],
            "ចំនួនប្រាក់ (៛)": [total_income, total_expense]
        })
        fig_bar = px.bar(summary_df, x="ប្រភេទ", y="ចំនួនប្រាក់ (៛)", color="ប្រភេទ", text_auto=',.0f')
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.subheader("🍕 ភាគរយចំណាយតាមប្រភេទទំនិញ")
        expenses_only = filtered_txns[filtered_txns["type"] == "ចំណាយ"]
        if not expenses_only.empty:
            exp_cat_df = expenses_only.groupby("category")["amount"].sum().reset_index()
            fig_pie = px.pie(exp_cat_df, values="amount", names="category")
            st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    st.subheader("➕ បញ្ចូលប្រតិបត្តិការថ្មី")
    with st.form("txn_form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            txn_type = st.radio("ប្រភេទប្រតិបត្តិការ៖", ["ចំណាយ", "ចំណូល"], horizontal=True)
            txn_cat = st.selectbox("ជំពូក/ប្រភេទ៖", ["ថ្លៃកូនជ្រូក", "ថ្លៃចំណី+កន្ទក់", "ថ្លៃថ្នាំពេទ្យ", "លក់ជ្រូកសាច់", "ផ្សេងៗ"])
            txn_date = st.date_input("កាលបរិច្ឆេទ៖", datetime.today())
        with col_b:
            txn_amount = st.number_input("ចំនួនប្រាក់ (រៀល ៛)៖", min_value=0, step=50000, value=100000)
            txn_qty = st.number_input("បរិមាណ៖", min_value=0.0, value=1.0)
            txn_unit = st.text_input("ខ្នាត៖", value="បាវ")
        
        txn_desc = st.text_input("បរិយាយ/ចំណាំបន្ថែម៖")
        btn_submit = st.form_submit_button("💾 រក្សាទុកប្រតិបត្តិការ")

        if btn_submit and txn_amount > 0:
            target_b_id = selected_batch_id if selected_batch_id else batches_df["batch_id"].iloc[0]
            new_txn = {
                "id": f"TXN_{len(txns_df) + 1:04d}",
                "batch_id": target_b_id,
                "date": str(txn_date),
                "type": txn_type,
                "category": txn_cat,
                "description": txn_desc if txn_desc else txn_cat,
                "amount": txn_amount,
                "qty": txn_qty,
                "unit": txn_unit
            }
            txns_df = pd.concat([txns_df, pd.DataFrame([new_txn])], ignore_index=True)
            save_transactions(txns_df)
            st.session_state["txns_df"] = txns_df
            st.success("បានរក្សាទុក!")
            st.rerun()

with tab3:
    st.subheader("📋 បញ្ជីប្រតិបត្តិការដែលបានកត់ត្រា")
    st.dataframe(filtered_txns, use_container_width=True)
    csv_data = filtered_txns.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 ទាញយកទិន្នន័យជា CSV", csv_data, f"pig_farm_{selected_batch_name}.csv", "text/csv")

# ==========================================
# SOFTWARE VERSION: v2.8 (Consolidated)
# Sidebar menu styling; module icons
# ==========================================
import base64
import os
import re
import datetime
import pandas as pd
import requests
import streamlit as st



# 1. Page Configuration optimized for mobile viewport
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="MyScholar Operation Center",
    page_icon=str(Path(__file__).parent / "myscholar_oc_favicon_32.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for 4 columns desktop, and cleanly transforming into a 2x6 grid on mobile
st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 0.8rem !important;
        padding-bottom: 1rem !important;
    }
    div.stSelectbox > div > div { background-color: #f8f9fa; }
    thead tr th { text-align: center !important; }
    tbody tr td { text-align: center !important; }
    .stDataFrame { text-align: center; }
    .header-logo img {
        width: 75px !important;
        max-width: 75px !important;
    }
    .header-text h2 {
        margin: 0 !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px !important;
        line-height: 1.1 !important;
    }
    .header-text p {
        margin: 0 !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        color: #333 !important;
    }

    /* Desktop layout: 4 columns per row */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 4px !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        width: 23.5% !important;
        flex: 1 1 23.5% !important;
        min-width: 80px !important;
    }

    /* Mobile layout: Transform into a clean 2x6 grid */
    @media (max-width: 768px) {
        [data-testid="stHorizontalBlock"] {
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 4px !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            width: 100% !important;
            flex: unset !important;
            min-width: 0 !important;
        }
        button[kind="secondary"], button[kind="primary"] {
            font-size: 10px !important;
            padding: 6px 2px !important;
        }
    }

    /* ===== Desktop: give data tables room to breathe ===== */
    .main .block-container { max-width: 95% !important; padding-left: 1.5rem; padding-right: 1.5rem; }

    /* ===== Sidebar nav: menu-style radio ===== */
    section[data-testid="stSidebar"] div[role="radiogroup"] { gap: 2px; }
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
      width: 100%; padding: 8px 10px !important; border-radius: 8px;
      margin: 1px 0; cursor: pointer; transition: background 0.12s;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
      background: #fff0e0;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label svg { display: none; }
    section[data-testid="stSidebar"] div[role="radiogroup"] label p {
      font-size: 14.5px !important; line-height: 1.35 !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
      background: #f58220;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
      color: #fff !important; font-weight: 700 !important;
    }

    /* ===== Mobile refinements ===== */
    @media (max-width: 768px) {
        .main .block-container { max-width: 100% !important; padding-left: 0.4rem !important; padding-right: 0.4rem !important; padding-top: 0.5rem !important; }
        .main [data-testid="stVerticalBlock"] { gap: 0.45rem !important; }
        hr { margin: 0.35rem 0 !important; }
        h1, h2, h3 { margin: 0.15rem 0 0.4rem !important; }
        h1 { font-size: 21px !important; }
        h2 { font-size: 18px !important; }
        h3 { font-size: 15px !important; }
        [data-testid="stDataFrame"] * { font-size: 12px !important; }
        [data-testid="stMetric"] { padding: 2px 4px !important; }
        [data-testid="stMetricValue"] { font-size: 15px !important; }
        [data-testid="stMetricLabel"] { font-size: 11px !important; }
        div[data-testid="stButton"] button[kind="primary"],
        div[data-testid="stButton"] button[kind="secondary"] {
            min-height: 46px; font-size: 13px !important; font-weight: 700; white-space: pre-line; line-height: 1.15;
        }
        section[data-testid="stSidebar"] { min-width: 230px !important; }
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# LOAD DATA & EXACT GITHUB COMMIT TIMESTAMP
# ==========================================
CSV_URL = "https://raw.githubusercontent.com/myscholar2298-coder/myscholar-dashboard/main/Extract_Dispatch_Data.csv"


@st.cache_data(ttl=60)
def load_data_from_github():
  df = pd.read_csv(CSV_URL)

  # Fetch exact last commit timestamp for this file from GitHub API
  api_url = "https://api.github.com/repos/myscholar2298-coder/myscholar-dashboard/commits?path=Extract_Dispatch_Data.csv&per_page=1"
  malaysia_tz = datetime.timezone(datetime.timedelta(hours=8))
  pub_time_str = ""

  try:
    response = requests.get(api_url, timeout=5)
    if response.status_code == 200:
      commit_data = response.json()
      if commit_data and len(commit_data) > 0:
        date_str = commit_data[0]["commit"]["committer"]["date"]
        utc_time = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        utc_time = utc_time.replace(tzinfo=datetime.timezone.utc)
        pub_time_str = (
            utc_time.astimezone(malaysia_tz)
            .strftime("%Y-%m-%d %I:%M:%S %p MYT")
        )
  except:
    pass

  # Fallback to local time if API fails or rate-limits
  if not pub_time_str:
    pub_time_str = (
        datetime.datetime.now(malaysia_tz)
        .strftime("%Y-%m-%d %I:%M:%S %p MYT")
    )

  return df, pub_time_str



# ==========================================
# SIDEBAR: BRANDING + MODULE NAVIGATION
# ==========================================
if os.path.exists('logo.png'):
  st.sidebar.image('logo.png', width=150)
st.sidebar.markdown('## 🏫 MyScholar Operation Center')
st.sidebar.divider()
if 'main_menu' not in st.session_state:
  st.session_state['main_menu'] = '🚚 1. Logistic Matrix'
main_menu = st.sidebar.radio(
    'Module',
    [
        '🚚 1. Logistic Matrix',
        '👤 2. Customer Transaction Analysis',
        '💰 3. Top Outstanding Tracking',
        '🚨 4. Cancel Order & High Return Analysis',
        '📋 5. Inventory Audit',
        '📦 6. Purchase and Return Analysis',
    ],
    key='main_menu',
    label_visibility='collapsed',
)
st.sidebar.divider()

# ===== BI MODULE LOADERS (local preprocessed CSVs) =====
def normalize_subject(subj_str):
  """Treat PAx and PAMx as interchangeable (e.g., PAM3 -> PA3)."""
  if not subj_str:
    return ''
  s = str(subj_str).upper().strip()
  return re.sub(r'^PAM', 'PA', s)



# --- INSTANT LOCAL CSV LOADING (Zero Lag) ---
@st.cache_data(ttl=21600)
def load_all_preprocessed_data():
  df_sales = (
      pd.read_csv('sales_transactions.csv')
      if os.path.exists('sales_transactions.csv')
      else pd.DataFrame()
  )
  df_ledger = (
      pd.read_csv('stock_ledger.csv')
      if os.path.exists('stock_ledger.csv')
      else pd.DataFrame()
  )
  df_audit = (
      pd.read_csv('stock_summary.csv')
      if os.path.exists('stock_summary.csv')
      else pd.DataFrame()
  )
  df_pay = (
      pd.read_csv('payments.csv')
      if os.path.exists('payments.csv')
      else pd.DataFrame()
  )
  df_adj = (
      pd.read_csv('adjustments.csv')
      if os.path.exists('adjustments.csv')
      else pd.DataFrame()
  )
  return df_sales, df_ledger, df_audit, df_pay, df_adj


ITEM_PREFERENCE = ['LEMB', 'SPM', 'MTP', 'NOTA']


def get_master_price(book_title):
  """Look up Unit Price from Master_Settings (multiple title formats)."""
  t = str(book_title).strip().upper().replace(' ', '_')
  if t in SETTINGS_PRICE:
    return SETTINGS_PRICE[t]
  parts = t.split('_', 1)
  if len(parts) == 2 and parts[0] and parts[1]:
    subj = normalize_subject(parts[0])
    item = parts[1]
    key = f'{subj}_{item}'
    if key in SETTINGS_PRICE:
      return SETTINGS_PRICE[key]
    # trailing phase digits: PA1_MTP_2 -> PA1_MTP
    item_core = re.sub(r'_?\d+$', '', item)
    if item_core and item_core != item:
      key = f'{subj}_{item_core}'
      if key in SETTINGS_PRICE:
        return SETTINGS_PRICE[key]
    # item prefix: SV1_RUJUK -> SV1_RUJ
    for k, v in SETTINGS_PRICE.items():
      k_subj, _, k_item = k.partition('_')
      if normalize_subject(k_subj) == subj and item.startswith(k_item):
        return v
  # full-name containment (IPG books): 'SINTAKSIS BAHASA MELAYU' -> SINTAKSIS_RUJ
  title_words = t.replace('_', ' ')
  best_len, best_price = 0, None
  for k, v in SETTINGS_PRICE.items():
    ks, _, ki = k.partition('_')
    kt = k.replace('_', ' ')
    score = 0
    if len(kt) >= 4 and (kt in title_words or title_words in kt):
      score = len(kt)
    elif len(ks) >= 5 and ks in title_words:
      score = len(ks)
    elif len(ki) >= 5 and ki in title_words:
      score = len(ki)
    if score > best_len:
      best_len, best_price = score, v
  if best_price is not None:
    return best_price
  # GKT/LK patterns: "GKT T4'26" -> GKT4, "MTP GKT SPM'25" -> GKT+SPM
  words = title_words.replace("'", '')
  m = re.search(r'\b(GKT|LK)\s*T\s?(\d)', words)
  if m:
    base = f'{m.group(1)}{m.group(2)}'
    for kw in ['SPM', 'MTP', 'LEMB', 'NOTA']:
      if kw in words and f'{base}_{kw}' in SETTINGS_PRICE:
        return SETTINGS_PRICE[f'{base}_{kw}']
    for kw in ITEM_PREFERENCE:
      if f'{base}_{kw}' in SETTINGS_PRICE:
        return SETTINGS_PRICE[f'{base}_{kw}']
  else:
    fam = next(
        (f for f in ['GKT', 'LK'] if re.search(rf'\b{f}\b', words)), None
    )
    if fam:
      for kw in ['SPM', 'MTP', 'LEMB', 'NOTA']:
        if kw in words:
          hits = [
              v for k, v in SETTINGS_PRICE.items()
              if k.startswith(fam) and k.endswith(f'_{kw}')
          ]
          if hits:
            return hits[-1]
  return None


  return None


def get_unit_price_for_book(book_title):
  mp = get_master_price(book_title)
  if mp is not None:
    return mp
  if (
      not master_sales_df.empty
      and 'Book_Title' in master_sales_df.columns
      and 'Unit_Price' in master_sales_df.columns
  ):
    match = master_sales_df[
        master_sales_df['Book_Title'] == str(book_title).strip().upper()
    ]
    if not match.empty:
      return float(match['Unit_Price'].iloc[0])
  return 38.0


master_sales_df, master_ledger_df, master_stock_summary_df, df_payment, df_adjustments = load_all_preprocessed_data()

MASTER_SETTINGS_URL = (
    "https://raw.githubusercontent.com/myscholar2298-coder/"
    "myscholar-dashboard/main/Master_Settings.xlsx"
)


def _pick_settings_sheet(xls):
  """Book prices live in the 'Inventory' tab of Master_Settings."""
  for s in xls.sheet_names:
    if any(k in s.lower() for k in ['invent', 'price', 'harga', 'buku']):
      return s
  return xls.sheet_names[0]


@st.cache_data(ttl=3600)
def load_master_settings():
  """Pull Master_Settings.xlsx from GitHub (Inventory tab); fall back local."""
  try:
    xls = pd.ExcelFile(MASTER_SETTINGS_URL, engine='openpyxl')
    return pd.read_excel(xls, sheet_name=_pick_settings_sheet(xls))
  except Exception:
    for cand in ['Master_Settings.xlsx', 'Master_Settings.csv']:
      if os.path.exists(cand):
        try:
          if cand.endswith('.csv'):
            return pd.read_csv(cand)
          xls = pd.ExcelFile(cand, engine='openpyxl')
          return pd.read_excel(xls, sheet_name=_pick_settings_sheet(xls))
        except Exception:
          continue
    return pd.DataFrame()


def _parse_rm(val):
  try:
    return float(str(val).replace('RM', '').replace(',', '').strip())
  except Exception:
    return None


master_settings_df = load_master_settings()
SETTINGS_PRICE = {}
if not master_settings_df.empty:
  for _r in master_settings_df.itertuples(index=False):
    _row = _r._asdict()
    _subj = str(_row.get('Subject', '')).upper().strip()
    _item = str(_row.get('Item', '')).upper().strip()
    _p = _parse_rm(_row.get('Unit Price', ''))
    if _subj and _item and _p is not None:
      SETTINGS_PRICE[f'{_subj}_{_item}'] = _p


OUTSTANDING_URL = (
    "https://raw.githubusercontent.com/myscholar2298-coder/"
    "myscholar-dashboard/main/outstanding_summary.csv"
)


@st.cache_data(ttl=300)
def load_outstanding_summary():
  """Pull outstanding_summary.csv from GitHub; fall back to local file."""
  try:
    return pd.read_csv(OUTSTANDING_URL)
  except Exception:
    if os.path.exists('outstanding_summary.csv'):
      return pd.read_csv('outstanding_summary.csv')
    return pd.DataFrame()


try:
  with st.spinner("Loading live data from GitHub..."):
    df, published_time = load_data_from_github()

except Exception as e:
  st.error(f"Error loading dashboard data: {e}")
  st.stop()

st.sidebar.caption(f'🕒 Data updated: {published_time}')
# Clean up column names safely
df.columns = df.columns.str.strip()

if "School Name" in df.columns:
  df = df[df["School Name"] != "School Name"]

if "\\#Delivery" in df.columns:
  df = df.rename(columns={"\\#Delivery": "#Delivery"})

expected_cols = [
    "Group",
    "Date",
    "School Name",
    "Teacher",
    "Task",
    "Route",
    "Remark",
    "Title/Panitia",
    "Sample",
    "Qty",
    "#Delivery",
]
for col in expected_cols:
  if col not in df.columns:
    df[col] = ""
  else:
    df[col] = df[col].fillna("").astype(str)


def format_qty(val):
  try:
    if (
        pd.isna(val)
        or str(val).strip() == ""
        or str(val).lower() == "nan"
    ):
      return "0"
    return str(int(float(val)))
  except:
    return str(val)


df["Sample"] = df["Sample"].apply(format_qty)
df["Qty"] = df["Qty"].apply(format_qty)
df["#Delivery"] = df["#Delivery"].apply(format_qty)

# ==========================================
# NAVIGATION MENU (Pages)
# ==========================================

def _jump_to_transaction(debtor_code):
  """Module 3 -> Module 2 jump: prefill debtor input and switch module."""
  st.session_state['debtor_input'] = debtor_code
  st.session_state['main_menu'] = '👤 2. Customer Transaction Analysis'


if main_menu == '🚚 1. Logistic Matrix':
  st.title('🚚 Logistic Matrix')
  st.caption('Route-level dispatch, collection & task control')
  if 'page_mode' not in st.session_state:
    st.session_state['page_mode'] = '🏠 Main Dashboard'
  _sub1, _sub2, _sub3 = st.columns(3)
  with _sub1:
    if st.button(
        '🏠\nMain Dashboard',
        key='sub_nav_main',
        use_container_width=True,
        type='primary' if st.session_state['page_mode'] == '🏠 Main Dashboard' else 'secondary',
    ):
      st.session_state['page_mode'] = '🏠 Main Dashboard'
      st.rerun()
  with _sub2:
    if st.button(
        '💳\nCheque Details',
        key='sub_nav_cheque',
        use_container_width=True,
        type='primary' if st.session_state['page_mode'] == '💳 Cheque Details' else 'secondary',
    ):
      st.session_state['page_mode'] = '💳 Cheque Details'
      st.rerun()
  with _sub3:
    if st.button(
        '📋\nPanitia Details',
        key='sub_nav_panitia',
        use_container_width=True,
        type='primary' if st.session_state['page_mode'] == '📋 Panitia Details' else 'secondary',
    ):
      st.session_state['page_mode'] = '📋 Panitia Details'
      st.rerun()
  page_mode = st.session_state['page_mode']
  st.divider()
  valid_df = df[df["School Name"].str.strip() != ""].copy()


  def is_panitia_row(title, task, date_val):
    if str(task).strip().lower() == "cheque":
      return False
    t_str = str(title).strip()
    d_str = str(date_val).strip()
    if not t_str or not d_str or d_str.lower() == "nan":
      return False
    if "_" in t_str or "." in t_str or any(char.isdigit() for char in t_str):
      return False
    return True


  valid_df["Is_Panitia"] = valid_df.apply(
      lambda row: is_panitia_row(row["Title/Panitia"], row["Task"], row["Date"]),
      axis=1,
  )

  cheque_mask = valid_df["Task"].str.strip().str.lower() == "cheque"
  panitia_mask = valid_df["Is_Panitia"]
  stpm_mask = (
      ~panitia_mask
      & ~cheque_mask
      & (valid_df["Title/Panitia"].str.strip() != "")
  )

  # ==========================================
  # PAGE 1: MAIN DASHBOARD
  # ==========================================
  if page_mode == "🏠 Main Dashboard":
    st.subheader("📊 Overview Summary")

    exclude_no_stock = st.checkbox(
        "🚫 Exclude 'No Sample' / 'No Stock'", value=True
    )
    exclude_pending = st.checkbox("🚫 Exclude 'Pending' Tasks", value=True)

    filtered_df = df.copy()
    if exclude_no_stock:
      filtered_df = filtered_df[
          ~filtered_df["Remark"]
          .str.lower()
          .str.contains("no sample|no stock", na=False)
      ]
    if exclude_pending:
      filtered_df = filtered_df[
          filtered_df["Task"].str.strip().str.lower() != "pending"
      ]

    f_valid_df = filtered_df[filtered_df["School Name"].str.strip() != ""].copy()
    f_valid_df["Is_Panitia"] = f_valid_df.apply(
        lambda row: is_panitia_row(
            row["Title/Panitia"], row["Task"], row["Date"]
        ),
        axis=1,
    )

    f_cheque_mask = f_valid_df["Task"].str.strip().str.lower() == "cheque"
    f_panitia_mask = f_valid_df["Is_Panitia"]
    f_stpm_mask = (
        ~f_panitia_mask
        & ~f_cheque_mask
        & (f_valid_df["Title/Panitia"].str.strip() != "")
    )

    total_schools_visit = f_valid_df["School Name"].nunique()
    cheque_schools_count = f_valid_df[f_cheque_mask]["School Name"].nunique()

    valid_teachers = f_valid_df[
        (f_valid_df["Teacher"].str.strip() != "")
        & (f_valid_df["Teacher"].str.strip() != "Pjbt")
    ]
    stpm_teachers_count = valid_teachers[
        f_stpm_mask[valid_teachers.index]
    ]["Teacher"].nunique()
    panitia_teachers_count = valid_teachers[
        f_panitia_mask[valid_teachers.index]
    ]["Teacher"].nunique()

    summary_data = {
        "Total Schools": [total_schools_visit],
        "Cheques": [cheque_schools_count],
        "STPM": [stpm_teachers_count],
        "Panitia": [panitia_teachers_count],
    }
    summary_df = pd.DataFrame(summary_data)

    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.divider()
    st.info(f"💡 Active records: **{len(filtered_df)}** across all routes.")
    st.divider()

    # ==========================================
    # 4 COLUMNS DESKTOP / 2x6 MOBILE RESPONSIVE GRID
    # ==========================================
    st.subheader("🛣️ Route Breakdown & Task Inspector")

    if "selected_route" not in st.session_state:
      st.session_state.selected_route = "A"

    query_params = st.query_params
    if "route" in query_params:
      r_val = query_params["route"]
      if r_val in [
          "A",
          "B",
          "C",
          "D",
          "E",
          "F",
          "G",
          "H",
          "I",
          "J",
          "K",
          "L",
      ]:
        st.session_state.selected_route = r_val

    routes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

    for i in range(0, len(routes), 4):
      col1, col2, col3, col4 = st.columns(4)
      row_routes = [
          routes[i],
          routes[i + 1] if i + 1 < len(routes) else None,
          routes[i + 2] if i + 2 < len(routes) else None,
          routes[i + 3] if i + 3 < len(routes) else None,
      ]

      for idx, r in enumerate(row_routes):
        if r is not None:
          r_sub_df = filtered_df[
              filtered_df["Route"].astype(str).str.upper().str.startswith(r)
          ]
          r_sch_count = r_sub_df[
              r_sub_df["School Name"].str.strip() != ""
          ]["School Name"].nunique()
          r_tch_count = r_sub_df[
              (r_sub_df["Teacher"].str.strip() != "")
              & (r_sub_df["Teacher"].str.strip() != "Pjbt")
          ]["Teacher"].nunique()
          r_chq_count = r_sub_df[
              r_sub_df["Task"].str.strip().str.lower() == "cheque"
          ].shape[0]

          is_selected = st.session_state.selected_route == r
          btn_label = f"{r} | 🏫{r_sch_count} 👨‍🏫{r_tch_count} 💳{r_chq_count}"

          target_col = [col1, col2, col3, col4][idx]
          with target_col:
            if st.button(
                btn_label,
                key=f"btn_route_{r}",
                use_container_width=True,
                type="primary" if is_selected else "secondary",
            ):
              st.session_state.selected_route = r
              st.rerun()

    selected_route = st.session_state.selected_route
    route_df = filtered_df[
        filtered_df["Route"]
        .astype(str)
        .str.upper()
        .str.startswith(selected_route.upper())
    ].reset_index(drop=True)

    r_schools = route_df[route_df["School Name"].str.strip() != ""][
        "School Name"
    ].nunique()
    r_teachers = route_df[route_df["Teacher"].str.strip() != ""][
        "Teacher"
    ].nunique()
    r_cheques = route_df[
        route_df["Task"].str.strip().str.lower() == "cheque"
    ].shape[0]

    st.markdown(f"### Route {selected_route} Summary")
    st.info(
        f"🏫 Schools: **{r_schools}** | 👨‍🏫 Teachers: **{r_teachers}** | 💳"
        f" Cheques: **{r_cheques}** | 📋 Tasks: **{len(route_df)}**"
    )

    if not route_df.empty:
      st.write(
          f"**Task List (Route {selected_route})** — *Click any row below to view"
          " details:*"
      )

      display_list = route_df[
          ["School Name", "Teacher", "Title/Panitia", "Task"]
      ]


      def highlight_full_row(row):
        task_val = str(row["Task"]).strip().lower()
        if "delivery" in task_val:
          return ["background-color: #d1e7dd; color: #0f5132"] * len(row)
        elif "cheque" in task_val:
          return ["background-color: #fff3cd; color: #664d03"] * len(row)
        elif "payment" in task_val:
          return ["background-color: #e2d9f3; color: #3b1f6e"] * len(row)
        elif "return" in task_val:
          return ["background-color: #cfe2ff; color: #084298"] * len(row)
        else:
          return ["background-color: #f8f9fa; color: #383d41"] * len(row)


      styled_table = display_list.style.apply(highlight_full_row, axis=1)

      event = st.dataframe(
          styled_table,
          use_container_width=True,
          hide_index=True,
          on_select="rerun",
          selection_mode="single-row",
          key=f"table_route_{selected_route}",
      )

      st.divider()

      st.subheader("🔍 Individual Task Details")
      selected_rows = event.selection.rows if event and event.selection else []
      task_detail = (
          route_df.iloc[selected_rows[0]]
          if selected_rows
          else route_df.iloc[0]
      )

      task_type = task_detail["Task"].strip()
      badge_style = (
          "background-color: #d1e7dd; color: #0f5132; padding: 2px 8px;"
          " border-radius: 4px; font-weight: bold;"
          if task_type.lower() == "delivery"
          else (
              "background-color: #fff3cd; color: #664d03; padding: 2px 8px;"
              " border-radius: 4px; font-weight: bold;"
              if task_type.lower() == "cheque"
              else (
                  "background-color: #e2d9f3; color: #3b1f6e; padding: 2px 8px;"
                  " border-radius: 4px; font-weight: bold;"
                  if task_type.lower() == "payment"
                  else (
                      "background-color: #cfe2ff; color: #084298; padding: 2px"
                      " 8px; border-radius: 4px; font-weight: bold;"
                  )
              )
          )
      )

      with st.container(border=True):
        st.markdown(f"### 🏢 {task_detail['School Name']}")
        st.markdown(
            f"**Route:** {task_detail['Route']}  |  **Task Type:** <span"
            f" style='{badge_style}'>{task_type}</span>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "**Teacher/Contact:**"
            f" {task_detail['Teacher'] if task_detail['Teacher'] else 'N/A'}"
        )
        st.markdown(f"**Book / Panitia:** {task_detail['Title/Panitia']}")

        col_a, col_b = st.columns(2)
        col_a.metric("Sample Qty", task_detail["Sample"])
        col_b.metric("Actual Qty", task_detail["Qty"])

        if task_detail["Remark"]:
          st.warning(f"📝 **Remark:** {task_detail['Remark']}")
        else:
          st.success("📝 **Remark:** None")
    else:
      st.warning(f"No records found for Route {selected_route}.")

  # ==========================================
  # PAGE 2: CHEQUE DETAILS REVIEW
  # ==========================================
  elif page_mode == "💳 Cheque Details":
    st.subheader("💳 Cheque Collection Tasks Review")

    cheque_df = valid_df[cheque_mask].copy()
    cheque_df = cheque_df.drop_duplicates(
        subset=["Date", "Route", "School Name", "Teacher", "Title/Panitia", "Remark"]
    )
    cheque_df = cheque_df.sort_values(
        by="Date", na_position="last"
    ).reset_index(drop=True)

    st.info(
        f"Total Cheque Collection Tasks: **{len(cheque_df)}** across"
        f" **{cheque_df['School Name'].nunique()}** schools."
    )

    if not cheque_df.empty:
      cheque_df["Route_Initial"] = (
          cheque_df["Route"].astype(str).str.strip().str[0].str.upper()
      )
      cheque_display = cheque_df[
          ["Date", "Route_Initial", "School Name", "Teacher", "Title/Panitia", "Remark"]
      ]
      cheque_display.columns = [
          "Date",
          "Route",
          "School Name",
          "Teacher",
          "Panitia",
          "Remark",
      ]
      st.dataframe(cheque_display, use_container_width=True, hide_index=True)
    else:
      st.success("No cheque tasks found.")

  # ==========================================
  # PAGE 3: PANITIA DETAILS REVIEW
  # ==========================================
  elif page_mode == "📋 Panitia Details":
    st.subheader("📋 Panitia Order Overview")

    panitia_df = valid_df[panitia_mask].copy()

    pending_df = panitia_df[
        panitia_df["Task"].astype(str).str.strip().str.lower() == "pending"
    ].drop_duplicates(
        subset=[
            "Date",
            "School Name",
            "Teacher",
            "Title/Panitia",
            "#Delivery",
            "Remark",
        ]
    )
    pending_df = pending_df.sort_values(
        by="Date", na_position="last"
    ).reset_index(drop=True)

    other_df = panitia_df[
        panitia_df["Task"].astype(str).str.strip().str.lower() != "pending"
    ].drop_duplicates(
        subset=[
            "Date",
            "School Name",
            "Teacher",
            "Title/Panitia",
            "Task",
            "#Delivery",
            "Remark",
        ]
    )
    other_df = other_df.sort_values(
        by="Date", na_position="last"
    ).reset_index(drop=True)

    st.info(
        f"Total Unique Panitia Tasks: **{len(pending_df) + len(other_df)}**"
        f" (Pending: **{len(pending_df)}** | Other: **{len(other_df)}**)"
    )

    # Section A: Pending Tasks
    st.markdown("### ⏳ Order Pending Incoming Items")
    if not pending_df.empty:
      pending_display = pending_df[
          ["Date", "School Name", "Teacher", "Title/Panitia", "#Delivery", "Remark"]
      ].copy()
      pending_display.columns = [
          "Date",
          "School Name",
          "Teacher",
          "Panitia",
          "#Delivery",
          "Remark",
      ]


      def highlight_delivered(row):
        try:
          val = float(row["#Delivery"])
          if val > 0:
            return ["background-color: #fff3cd; color: #664d03"] * len(row)
        except:
          pass
        return [""] * len(row)


      styled_pending = pending_display.style.apply(
          highlight_delivered, axis=1
      )
      st.dataframe(styled_pending, use_container_width=True, hide_index=True)
    else:
      st.success("No pending Panitia tasks.")

    st.divider()

    # Section B: Other Panitia Tasks
    st.markdown("### ✅ Outstanding Operation Assignment")
    if not other_df.empty:
      other_display = other_df[
          [
              "Date",
              "School Name",
              "Teacher",
              "Title/Panitia",
              "Task",
              "#Delivery",
              "Remark",
          ]
      ].copy()
      other_display.columns = [
          "Date",
          "School Name",
          "Teacher",
          "Panitia",
          "Task",
          "#Delivery",
          "Remark",
      ]

      p_event = st.dataframe(
          other_display,
          use_container_width=True,
          hide_index=True,
          on_select="rerun",
          selection_mode="single-row",
          key="table_panitia_other",
      )

      st.divider()
      st.subheader("🔍 Panitia Task Detail Box")

      p_selected_rows = (
          p_event.selection.rows if p_event and p_event.selection else []
      )
      p_task_detail = (
          other_df.iloc[p_selected_rows[0]]
          if p_selected_rows
          else other_df.iloc[0]
      )

      p_task_type = p_task_detail["Task"].strip()
      p_badge_style = (
          "background-color: #d1e7dd; color: #0f5132; padding: 2px 8px;"
          " border-radius: 4px; font-weight: bold;"
          if p_task_type.lower() == "delivery"
          else (
              "background-color: #cfe2ff; color: #084298; padding: 2px 8px;"
              " border-radius: 4px; font-weight: bold;"
          )
      )

      with st.container(border=True):
        st.markdown(f"### 🏫 Route {p_task_detail['Route']} Task")
        st.markdown(
            f"**Task Type:** <span"
            f" style='{p_badge_style}'>{p_task_type}</span>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "**Teacher/Contact:**"
            f" {p_task_detail['Teacher'] if p_task_detail['Teacher'] else 'N/A'}"
        )
        st.markdown(f"**Book / Panitia:** {p_task_detail['Title/Panitia']}")

        col_a, col_b = st.columns(2)
        col_a.metric("Sample Qty", p_task_detail["Sample"])
        col_b.metric("Actual Qty", p_task_detail["Qty"])

        if p_task_detail["Remark"]:
          st.warning(f"📝 **Remark:** {p_task_detail['Remark']}")
        else:
          st.success("📝 **Remark:** None")
    else:
      st.success("No other Panitia tasks found.")

# ==========================================
# FUNCTION 1: CUSTOMER TRANSACTION ANALYSIS
# ==========================================
elif main_menu == '👤 2. Customer Transaction Analysis':
  selected_year = st.selectbox('⚙️ Operational Year', ['2026','2027','2025','2024','2023'], index=0)
  st.title('👤 Customer Transaction Analysis')

  default_school_idx = 0
  all_schools = (
      sorted(master_sales_df['School_Name'].unique().tolist())
      if not master_sales_df.empty
      else []
  )


  ALL_SUBJECTS = 'All Subjects (Combined)'

  col1, col2, col3 = st.columns(3)

  with col1:
    selected_school = st.selectbox(
        '1. School / Department', [''] + all_schools, index=default_school_idx
    )

  with col2:
    if selected_school and not master_sales_df.empty:
      sch_df = master_sales_df[
          master_sales_df['School_Name'] == selected_school
      ]
      teachers = sorted(
          [t for t in sch_df['Teacher'].unique() if t and t != 'N/A']
      )
    else:
      teachers = []

    selected_teacher = st.selectbox(
        '2. Teacher Name', [''] + teachers, index=0
    )

  with col3:
    if selected_school and not master_sales_df.empty:
      subj_df = master_sales_df[
          master_sales_df['School_Name'] == selected_school
      ]
      if selected_teacher:
        subj_df = subj_df[subj_df['Teacher'] == selected_teacher]
      subjects = sorted(subj_df['Subject'].unique().tolist())
    else:
      subjects = []

    selected_subject = st.selectbox(
        '3. Subject', [ALL_SUBJECTS] + subjects, index=0
    )

  debtor_input = (
      st.text_input(
          'Debtor Code (Direct Input, e.g., 300-K081)',
          key='debtor_input',
      )
      .strip()
      .upper()
  )
  if debtor_input and not debtor_input.startswith('300-'):
    debtor_input = f'300-{debtor_input}'

  if selected_school or debtor_input:
    df_filtered_sales = pd.DataFrame()
    active_debtor = debtor_input

    if selected_school:
      df_filtered_sales = master_sales_df[
          master_sales_df['School_Name'] == selected_school
      ]
      if selected_teacher:
        df_filtered_sales = df_filtered_sales[
            df_filtered_sales['Teacher'] == selected_teacher
        ]
      if selected_subject and selected_subject != ALL_SUBJECTS:
        df_filtered_sales = df_filtered_sales[
            df_filtered_sales['Subject'] == selected_subject
        ]

      if not active_debtor and not df_filtered_sales.empty:
        exp_matches = df_filtered_sales['Explicit_Debtor'].dropna().unique()
        if len(exp_matches) > 0 and exp_matches[0]:
          active_debtor = exp_matches[0]

    elif active_debtor and not master_sales_df.empty:
      # Debtor-only lookup: pull all his records across every school/subject
      df_filtered_sales = master_sales_df[
          master_sales_df['Explicit_Debtor'].astype(str).str.upper().str.strip()
          == str(active_debtor).upper().strip()
      ]

    if active_debtor:
      st.markdown(f'### 🏷️ Active Debtor Code: **{active_debtor}**')

    total_value = 0.0
    total_qty = 0
    phase_rows = []
    delivery_counts = {}
    return_counts = {}

    if not df_filtered_sales.empty:
      for _, row in df_filtered_sales.iterrows():
        book = row['Book_Title']
        qty = row['Quantity']
        unit_price = row['Unit_Price']
        subtotal = row['Total_Value']
        total_value += subtotal
        total_qty += qty

        if qty > 0:
          delivery_counts[book] = delivery_counts.get(book, 0) + 1
          seq_num = delivery_counts[book]
          row_label = f'{book} (Delivery #{seq_num})'
          desc_text = f'Deliver {qty}pcs'
        else:
          return_counts[book] = return_counts.get(book, 0) + 1
          seq_num = return_counts[book]
          row_label = f'{book} (Return #{seq_num})'
          desc_text = f'Return {abs(qty)}pcs'

        phase_rows.append({
            'Book / Phase': row_label,
            'Description': desc_text,
            'Qty': qty,
            'Unit Price (RM)': unit_price,
            'Total (RM)': subtotal,
        })

    matched_payments = []
    total_payments = 0.0

    if (
        df_payment is not None
        and not df_payment.empty
        and not df_filtered_sales.empty
    ):
      clean_target_debtor = (
          active_debtor.upper().replace('300-', '').strip()
          if active_debtor
          else ''
      )
      valid_books = set(
          df_filtered_sales['Book_Title'].str.upper().str.strip().tolist()
      )

      for _, row in df_payment.iterrows():
        row_str = ' '.join(
            [str(val) for val in row.values if pd.notna(val)]
        ).upper()

        is_debtor_match = False
        if clean_target_debtor and (
            f'300-{clean_target_debtor}' in row_str
            or row_str.startswith(clean_target_debtor)
            or f' {clean_target_debtor} ' in row_str
        ):
          is_debtor_match = True

        if not is_debtor_match:
          continue

        raw_date = ''
        for val in row.values:
          if pd.notna(val) and ('202' in str(val) or '201' in str(val)):
            raw_date = str(val)
            break
        if not raw_date:
          raw_date = str(row.iloc[0]) if len(row) > 0 else ''

        clean_date = raw_date.split(' ')[0] if ' ' in raw_date else raw_date

        if selected_year and not clean_date.startswith(selected_year):
          continue

        desc = str(
            row.get('Description', row.iloc[1] if len(row) > 1 else '')
        )
        desc_upper = desc.upper()

        item_matches = re.findall(
            r'([A-Z0-9_\-\.]+)\s*(?:[xX]|\*|\b)(\d+)', desc_upper
        )
        parsed_payment_val = 0.0
        parsed_details = []

        if item_matches:
          for code, qty_str in item_matches:
            qty = int(qty_str)
            code_clean = code.strip()

            matched_book = None
            for b in valid_books:
              if (
                  code_clean in b
                  or b in code_clean
                  or code_clean == b.replace(' ', '_')
              ):
                matched_book = b
                break

            if matched_book:
              u_price = get_unit_price_for_book(matched_book)
              sub_val = qty * u_price
              parsed_payment_val += sub_val
              parsed_details.append(
                  f'{matched_book} x{qty} (RM {sub_val:,.2f})'
              )

        has_matching_context = any(
            vb.replace('_', ' ') in desc_upper or vb in desc_upper
            for vb in valid_books
        )
        if has_matching_context:
          loose_rm_matches = re.findall(r'\bRM\s*(\d+(?:\.\d{2})?)', desc_upper)
          if loose_rm_matches:
            loose_sum = sum([float(m) for m in loose_rm_matches])
            parsed_payment_val += loose_sum
            parsed_details.append(f'Additional Amount: RM {loose_sum:,.2f}')

        if parsed_payment_val > 0:
          detail_str = f'{desc} -> Parsed: ' + ', '.join(parsed_details)
          matched_payments.append({
              'Date': clean_date,
              'Description': detail_str,
              'Amount (RM)': parsed_payment_val,
          })
          total_payments += parsed_payment_val

    matched_adjs = []
    total_adj = 0.0
    if df_adjustments is not None and not df_adjustments.empty:
      clean_target_debtor = (
          active_debtor.upper().replace('300-', '').strip()
          if active_debtor
          else ''
      )
      active_subj_normalized = (
          '' if selected_subject == ALL_SUBJECTS
          else normalize_subject(selected_subject)
      )

      for _, row in df_adjustments.iterrows():
        row_str = ' '.join(
            [str(val) for val in row.values if pd.notna(val)]
        ).upper()

        is_match = False
        if clean_target_debtor and (
            f'300-{clean_target_debtor}' in row_str
            or row_str.startswith(clean_target_debtor)
            or clean_target_debtor in row_str
        ):
          is_match = True

        if not is_match:
          continue

        row_subj_raw = str(
            row.iloc[3] if len(row) > 3 and pd.notna(row.iloc[3]) else ''
        ).strip()
        row_subj_normalized = normalize_subject(row_subj_raw)

        if (
            active_subj_normalized
            and row_subj_normalized
            and row_subj_normalized != active_subj_normalized
        ):
          continue

        raw_date = str(row.iloc[0] if len(row) > 0 else '')
        clean_date = raw_date.split(' ')[0] if ' ' in raw_date else raw_date

        if (
            selected_year
            and clean_date
            and not clean_date.startswith(selected_year)
            and '202' in clean_date
        ):
          continue

        amt = 0.0
        desc = 'Adjustment / Credit Note'
        for val in row.values:
          try:
            p_val = float(str(val).replace(',', '').replace('RM', '').strip())
            if p_val > 0 and p_val != float(selected_year or 0):
              amt = p_val
          except ValueError:
            pass

        if amt > 0:
          matched_adjs.append({
              'Date': clean_date,
              'Description': desc,
              'Amount (RM)': amt,
          })
          total_adj += amt

    balance_due = total_value - total_payments - total_adj

    st.markdown('---')
    st.subheader('📊 Financial Summary & Balance Due')
    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric('Deliveries Value', f'RM {total_value:,.2f}')
    sc2.metric('Payments Made', f'RM {total_payments:,.2f}')
    sc3.metric('Credit Notes', f'RM {total_adj:,.2f}')
    sc4.metric(
        'Outstanding Balance', f'RM {balance_due:,.2f}', delta_color='inverse'
    )
    st.markdown('---')

    if active_debtor and not df_filtered_sales.empty:
      subj_break = (
          df_filtered_sales.groupby('Subject')
          .agg(**{
              'Net Qty': ('Quantity', 'sum'),
              'Deliveries Value (RM)': ('Total_Value', 'sum'),
          })
          .reset_index()
          .sort_values('Deliveries Value (RM)', ascending=False)
      )
      if len(subj_break) > 1:
        st.subheader('📚 Subject / Penggal Breakdown')
        st.dataframe(subj_break, use_container_width=True, hide_index=True)
        st.markdown('---')

    st.subheader('1. Itemized Deliveries (Combined Breakdown)')
    if len(phase_rows) > 0:
      st.dataframe(pd.DataFrame(phase_rows), use_container_width=True)
      f_col1, f_col2 = st.columns(2)
      f_col1.info(f'**Net Total Qty:** {total_qty} pcs')
      f_col2.success(f'**Total Deliveries Value:** RM {total_value:,.2f}')
    else:
      st.warning('No delivery records found for this specific selection.')

    st.subheader('2. Payment Records & Balance Summary')
    df_pay_view = pd.DataFrame(matched_payments)
    if not df_pay_view.empty:
      st.dataframe(df_pay_view, use_container_width=True)
      st.success(f'**Total Payments:** RM {total_payments:,.2f}')
    else:
      st.info('No matching payment records found for this operational year.')

    st.subheader('3. Adjustments & Credit Notes')
    df_adj_view = pd.DataFrame(matched_adjs)
    if not df_adj_view.empty:
      st.dataframe(df_adj_view, use_container_width=True)
      st.success(f'**Total Adjustments / Credit Notes:** RM {total_adj:,.2f}')
    else:
      st.info('No adjustments found for this subject.')


# ==========================================
# FUNCTION 2: OUTSTANDING TRACKING DASHBOARD (INSTANT LOAD)
# ==========================================
elif main_menu == '💰 3. Top Outstanding Tracking':
  st.title('📈 Outstanding Tracking Dashboard')
  st.markdown('⚡ *Top 15 Outstanding Debtors Across All Files (Instant Load)*')

  df_summary = load_outstanding_summary()


  if df_summary.empty:
    st.warning('No outstanding summary found. Please run backend sync script.')
  else:
    st.markdown('---')
    st.subheader('📑 Top 15 Outstanding Debtors Per File Source')

    file_sources = sorted(df_summary['File Source'].unique().tolist())

    for f_src in file_sources:
      st.markdown(f'**Source File: `{f_src}`**')
      df_file_sub = df_summary[df_summary['File Source'] == f_src].copy()
      df_file_sub = (
          df_file_sub.sort_values(by='Outstanding (RM)', ascending=False)
          .head(15)
          .reset_index(drop=True)
      )

      total_file_top15_outstanding = df_file_sub['Outstanding (RM)'].sum()
      st.metric(
          f'Total Outstanding (Top 15 - {f_src})',
          f'RM {total_file_top15_outstanding:,.2f}',
      )

      file_cols = [
          'Subject',
          'Debtor Code',
          'Teacher',
          'Associated School(s)',
          'Net Qty',
          'Outstanding (RM)',
          'Transactions',
      ]
      df_file_display = df_file_sub[
          [c for c in file_cols if c in df_file_sub.columns]
      ]

      styled_file_df = (
          df_file_display.style.format({'Outstanding (RM)': '{:,.2f}'})
          .set_properties(
              subset=['Net Qty', 'Outstanding (RM)', 'Transactions'],
              **{'text-align': 'center'},
          )
          .set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])
      )

      event = st.dataframe(
          styled_file_df,
          use_container_width=True,
          on_select='rerun',
          selection_mode='single-row',
          key=f'table_{f_src}',
      )

      selected_rows = event.selection.rows if event and event.selection else []
      if selected_rows:
        sel_row = df_file_sub.iloc[selected_rows[0]]
        sel_code = str(sel_row['Debtor Code'])
        st.button(
            f'👤 Jump to Customer Transaction Analysis - {sel_code}'
            f' ({sel_row["Teacher"]})',
            key=f'jump_btn_{f_src}',
            use_container_width=True,
            on_click=_jump_to_transaction,
            args=(sel_code,),
        )



# ==========================================
# FUNCTION 3: CANCELLED & HIGH-RETURN ANALYSIS
# ==========================================
elif main_menu == '🚨 4. Cancel Order & High Return Analysis':
  st.title('🚨 Cancelled Orders & High-Return Customer Analysis')

  if master_sales_df.empty:
    st.warning('No sales records loaded.')
  else:
    pos_sales = (
        master_sales_df[master_sales_df['Quantity'] > 0]
        .groupby([
            'Subject',
            'Book_Title',
            'School_Name',
            'Teacher',
            'Explicit_Debtor',
        ])['Quantity']
        .sum()
        .reset_index()
        .rename(columns={'Quantity': 'Order_Qty'})
    )

    neg_sales = (
        master_sales_df[master_sales_df['Quantity'] < 0]
        .groupby([
            'Subject',
            'Book_Title',
            'School_Name',
            'Teacher',
            'Explicit_Debtor',
        ])['Quantity']
        .sum()
        .reset_index()
        .rename(columns={'Quantity': 'Return_Qty'})
    )
    neg_sales['Return_Qty'] = neg_sales['Return_Qty'].abs()

    merged_analysis = pd.merge(
        pos_sales,
        neg_sales,
        on=[
            'Subject',
            'Book_Title',
            'School_Name',
            'Teacher',
            'Explicit_Debtor',
        ],
        how='outer',
    ).fillna(0)

    merged_analysis = merged_analysis.rename(columns={
        'Subject': 'Subject',
        'Book_Title': 'BookType',
        'School_Name': 'School',
        'Teacher': 'Teacher',
        'Explicit_Debtor': 'Debtor Code',
        'Order_Qty': 'Order Qty',
        'Return_Qty': 'Return Qty',
    })

    merged_analysis['Return Ratio (%)'] = merged_analysis.apply(
        lambda r: (r['Return Qty'] / r['Order Qty'] * 100)
        if r['Order Qty'] > 0
        else 0.0,
        axis=1,
    )

    st.markdown('---')
    st.subheader('🛑 Table 1: Cancelled Orders')

    cancelled_df = merged_analysis[
        (merged_analysis['Return Qty'] > 0)
        & (merged_analysis['Return Qty'] >= merged_analysis['Order Qty'])
    ].copy()

    c_subj_list = sorted(cancelled_df['Subject'].unique().tolist())
    sel_cancel_subj = st.selectbox(
        'Filter Cancelled Orders by Subject', ['All'] + c_subj_list
    )
    if sel_cancel_subj != 'All':
      cancelled_df = cancelled_df[cancelled_df['Subject'] == sel_cancel_subj]

    cancel_display_cols = [
        'BookType',
        'School',
        'Teacher',
        'Debtor Code',
        'Order Qty',
        'Return Qty',
    ]

    styled_cancel_df = (
        cancelled_df[cancel_display_cols]
        .style.format({'Order Qty': '{:,.0f}', 'Return Qty': '{:,.0f}'})
        .set_properties(
            subset=['Order Qty', 'Return Qty'], **{'text-align': 'center'}
        )
        .set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])
    )

    st.metric('Total Cancelled Orders Found', f'{len(cancelled_df):,}')
    st.dataframe(styled_cancel_df, use_container_width=True)

    st.markdown('---')
    st.subheader('⚠️ Table 2: High Return Accounts')

    hr_col1, hr_col2, hr_col3 = st.columns(3)

    with hr_col1:
      hr_book_list = sorted(merged_analysis['BookType'].unique().tolist())
      sel_hr_book = st.selectbox(
          'Filter High Return by BookType', ['All'] + hr_book_list
      )

    with hr_col2:
      qty_options = list(range(5, 201, 5))
      default_qty_idx = qty_options.index(10) if 10 in qty_options else 1
      selected_min_qty = st.selectbox(
          'Min Delivery Qty Threshold', qty_options, index=default_qty_idx
      )

    with hr_col3:
      ratio_options = list(range(5, 101, 5))
      default_ratio_idx = ratio_options.index(60) if 60 in ratio_options else 11
      selected_min_ratio = st.selectbox(
          'Min Return Ratio (%) Threshold', ratio_options, index=default_ratio_idx
      )

    high_return_df = merged_analysis[
        (merged_analysis['Return Qty'] < merged_analysis['Order Qty'])
        & (merged_analysis['Order Qty'] > selected_min_qty)
        & (merged_analysis['Return Ratio (%)'] > selected_min_ratio)
    ].copy()

    if sel_hr_book != 'All':
      high_return_df = high_return_df[high_return_df['BookType'] == sel_hr_book]

    hr_display_cols = [
        'Subject',
        'BookType',
        'School',
        'Teacher',
        'Debtor Code',
        'Return Ratio (%)',
        'Order Qty',
        'Return Qty',
    ]

    styled_hr_df = (
        high_return_df[hr_display_cols]
        .sort_values(by='Return Ratio (%)', ascending=False)
        .style.format({
            'Return Ratio (%)': '{:.2f}%',
            'Order Qty': '{:,.0f}',
            'Return Qty': '{:,.0f}',
        })
        .set_properties(
            subset=['Order Qty', 'Return Qty', 'Return Ratio (%)'],
            **{'text-align': 'center'},
        )
        .set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])
    )

    st.metric('Total High Return Accounts Found', f'{len(high_return_df):,}')
    st.dataframe(styled_hr_df, use_container_width=True)


# ==========================================
# FUNCTION 5: INVENTORY AUDIT
# ==========================================
elif main_menu == '📋 5. Inventory Audit':
  st.title('📋 Inventory Audit Summary')

  if master_stock_summary_df.empty:
    st.warning('No records loaded from STOCK SUMMARY tab.')
  else:
    file_sources = sorted(
        master_stock_summary_df['File_Source'].unique().tolist()
    )

    for f_src in file_sources:
      st.markdown('---')
      st.markdown(f'### 📑 Audit Table for: **{f_src}**')

      df_audit_sub = master_stock_summary_df[
          master_stock_summary_df['File_Source'] == f_src
      ].copy()
      df_audit_sub = df_audit_sub.drop(columns=['File_Source']).reset_index(
          drop=True
      )

      audit_view_mode = st.selectbox(
          f'Select Audit View for {f_src}',
          ['Stock Audit', 'Sample Audit', 'Both'],
          index=0,
          key=f'audit_filter_{f_src}',
      )

      if audit_view_mode in ['Stock Audit', 'Both']:
        st.markdown('#### 📦 Stock Audit')
        stock_cols = [
            'BookType',
            'Job Completion',
            'Stock Balance',
            'Stock On Hand',
        ]
        stock_table = df_audit_sub[stock_cols].copy()
        stock_table.columns = [
            'Book',
            'Job Completion',
            'Stock Balance',
            'Stock On Hand',
        ]
        st.dataframe(stock_table, use_container_width=True, hide_index=True)

      if audit_view_mode in ['Sample Audit', 'Both']:
        st.markdown('#### 📝 Sample Audit')
        sample_cols = [
            'BookType',
            'Job Completion',
            'Sample Balance',
            'Sample On Hand',
        ]
        sample_table = df_audit_sub[sample_cols].copy()
        sample_table.columns = [
            'Book',
            'Job Completion',
            'Sample Balance',
            'Sample On Hand',
        ]
        st.dataframe(sample_table, use_container_width=True, hide_index=True)

      discrepancies = []
      for _, row in df_audit_sub.iterrows():
        s_disc = row['Stock Discrepancy']
        sa_disc = row['Sample Discrepancy']
        b_name = row['BookType']

        if s_disc != 0:
          discrepancies.append(
              f'Stock discrepancy found at **{b_name}** with {int(s_disc)} unit(s)'
          )

        if sa_disc != 0:
          discrepancies.append(
              f'Sample discrepancy found at **{b_name}** with {int(sa_disc)} unit(s)'
          )

      if discrepancies:
        st.markdown('**⚠️ Discrepancies Found**')
        for disc_msg in discrepancies:
          st.error(disc_msg)
      else:
        st.success('✅ All items are fully reconciled with zero discrepancies.')
# ==========================================
# FUNCTION 4: PURCHASE & RETURN RATE ANALYSIS
# ==========================================
elif main_menu == '📦 6. Purchase and Return Analysis':
  st.title('📦 Stock In & Return Ledger Analysis')

  if master_ledger_df.empty:
    st.warning('No ledger records loaded.')
  else:
    file_sources = sorted(master_ledger_df['File_Source'].unique().tolist())

    for f_src in file_sources:
      st.markdown('---')
      st.markdown(f'### 📑 Source File: `{f_src}`')

      file_sub_df = master_ledger_df[master_ledger_df['File_Source'] == f_src]

      table_region_filter = st.selectbox(
          f'Filter Region for {f_src}',
          ['TOTAL', 'Johor', 'Melaka'],
          index=0,
          key=f'region_filter_{f_src}',
      )

      filtered_ledger = file_sub_df[
          file_sub_df['Region'] == table_region_filter
      ].copy()

      display_ledger = filtered_ledger[[
          'Book_Title',
          'Unit_Price',
          'Return_%',
          'Total_In',
          'Total_Return',
          'Net_Purchase',
      ]].rename(columns={
          'Book_Title': 'Book Title',
          'Unit_Price': 'Unit Price (RM)',
          'Return_%': '% Return',
          'Total_In': 'Total In',
          'Total_Return': 'Total Return',
          'Net_Purchase': 'Net Purchase',
      })

      def _price_override(row):
        mp = get_master_price(row['Book Title'])
        return mp if mp is not None else row['Unit Price (RM)']

      display_ledger['Unit Price (RM)'] = display_ledger.apply(
          _price_override, axis=1
      )

      f_tot_in = display_ledger['Total In'].sum()
      f_tot_ret = display_ledger['Total Return'].sum()
      f_net_pur = display_ledger['Net Purchase'].sum()
      f_avg_ret_pct = (
          (f_tot_ret / f_tot_in * 100) if f_tot_in > 0 else 0.0
      )

      kc1, kc2, kc3, kc4 = st.columns(4)
      kc1.metric(f'Gross In ({f_src})', f'{f_tot_in:,.0f} pcs')
      kc2.metric(f'Returns ({f_src})', f'{f_tot_ret:,.0f} pcs')
      kc3.metric(f'Net Purchase ({f_src})', f'{f_net_pur:,.0f} pcs')
      kc4.metric(f'Return Rate ({f_src})', f'{f_avg_ret_pct:.2f}%')

      styled_ledger = (
          display_ledger.style.format({
              'Unit Price (RM)': '{:,.2f}',
              '% Return': '{:.2f}%',
              'Total In': '{:,.0f}',
              'Total Return': '{:,.0f}',
              'Net Purchase': '{:,.0f}',
          })
          .set_properties(
              subset=[
                  'Unit Price (RM)',
                  '% Return',
                  'Total In',
                  'Total Return',
                  'Net Purchase',
              ],
              **{'text-align': 'center'},
          )
          .set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])
      )

      st.dataframe(styled_ledger, use_container_width=True)


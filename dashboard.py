import streamlit as st
import pandas as pd
import os
from datetime import datetime
import numpy as np
import streamlit.components.v1 as components
import html

# --- Function to load and inject custom CSS ---
def load_custom_css():
    """Loads Google Fonts and injects custom CSS for a beautiful look."""
    css = """
    <style>
    /* --- Import Google Font --- */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    /* --- Apply Font Globally --- */
    html, body, [class*="st-"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* --- Background Gradient --- */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* --- Stats Cards --- */
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin: 10px 0;
    }
    
    .stat-label {
        font-size: 1rem;
        color: #666;
        font-weight: 500;
    }
    
    .stat-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }

    /* --- Section Navigation Cards --- */
    .nav-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(102,126,234,0.3);
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        color: white;
        margin: 10px 0;
    }
    
    .nav-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 30px rgba(102,126,234,0.5);
    }
    
    .nav-card-icon {
        font-size: 3rem;
        margin-bottom: 15px;
    }
    
    .nav-card-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .nav-card-desc {
        font-size: 0.95rem;
        opacity: 0.9;
    }

    /* --- WhatsApp Chat Header --- */
    .whatsapp-header {
        background: #075e54;
        color: white;
        padding: 15px 20px;
        border-radius: 10px 10px 0 0;
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 0;
    }
    
    .whatsapp-header-avatar {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background: #25d366;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: 600;
    }
    
    .whatsapp-header-info h3 {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    .whatsapp-header-info p {
        margin: 2px 0 0 0;
        font-size: 0.85rem;
        opacity: 0.8;
    }
    
    /* --- Container Styling --- */
    [data-testid="stContainer"] {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* --- Header Styling --- */
    h2 {
        color: #667eea;
        font-weight: 600;
        margin-bottom: 20px;
    }
    
    /* --- Button Styling --- */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102,126,234,0.4);
    }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- Page Configuration ---
st.set_page_config(
    page_title="WhatsApp Bot Dashboard",
    page_icon="🤖",
    layout="wide"
)

# --- LOAD THE CUSTOM CSS ---
load_custom_css()

# --- File Paths ---
ORDERS_FILE = 'orders.csv'
CONVO_FILE = 'conversation_log.csv'

# --- Helper Function to Load Data ---
@st.cache_data(ttl=5)
def load_data(file_path, data_type):
    if not os.path.exists(file_path):
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(file_path, keep_default_na=False, na_values=[''])
        
        if data_type == 'orders':
            df.replace('N/A', np.nan, inplace=True)
            df.dropna(subset=['product_details', 'delivery_address', 'payment_method'], inplace=True)
            
        elif data_type == 'convos':
            df.dropna(subset=['message_content'], inplace=True)
            
        return df
        
    except pd.errors.EmptyDataError:
        return pd.DataFrame()

# --- Initialize Session State ---
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'home'

# --- Header ---
image_path = "images/Auagentphoto.png"
if os.path.exists(image_path):
    col1, col2 = st.columns([1, 9])
    with col1:
        st.image(image_path, width=100)
    with col2:
        st.markdown("""
        <div style='padding-top: 10px;'>
            <h1 style='color: #667eea; margin: 0;'>🤖 WhatsApp Bot Dashboard</h1>
            <p style='color: #666; margin: 5px 0 0 0; font-size: 1.1rem;'>Real-time monitoring and analytics</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='padding-top: 10px;'>
        <h1 style='color: #667eea; margin: 0;'>🤖 WhatsApp Bot Dashboard</h1>
        <p style='color: #666; margin: 5px 0 0 0; font-size: 1.1rem;'>Real-time monitoring and analytics</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Load Data ---
df_convo = load_data(CONVO_FILE, data_type='convos')
df_orders = load_data(ORDERS_FILE, data_type='orders')

# --- Statistics Cards ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_convos = len(df_convo['from_number'].unique()) if not df_convo.empty else 0
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-number">{total_convos}</div>
        <div class="stat-label">Active Users</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_messages = len(df_convo) if not df_convo.empty else 0
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">💬</div>
        <div class="stat-number">{total_messages}</div>
        <div class="stat-label">Total Messages</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_orders = len(df_orders) if not df_orders.empty else 0
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">🛒</div>
        <div class="stat-number">{total_orders}</div>
        <div class="stat-label">Completed Orders</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    bot_messages = len(df_convo[df_convo['message_type'] == 'bot']) if not df_convo.empty else 0
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">🤖</div>
        <div class="stat-number">{bot_messages}</div>
        <div class="stat-label">Bot Responses</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- Navigation Section ---
if st.session_state.current_view == 'home':
    st.markdown("### 📊 Choose a Section")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💬 Live Conversations", key="nav_conv", use_container_width=True):
            st.session_state.current_view = 'conversations'
            st.rerun()
        st.markdown("""
        <div class="nav-card">
            <div class="nav-card-icon">💬</div>
            <div class="nav-card-title">Live Conversations</div>
            <div class="nav-card-desc">View real-time WhatsApp chats with customers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🛒 Order History", key="nav_orders", use_container_width=True):
            st.session_state.current_view = 'orders'
            st.rerun()
        st.markdown("""
        <div class="nav-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="nav-card-icon">🛒</div>
            <div class="nav-card-title">Order History</div>
            <div class="nav-card-desc">Track and manage customer orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("📊 Analytics", key="nav_analytics", use_container_width=True):
            st.session_state.current_view = 'analytics'
            st.rerun()
        st.markdown("""
        <div class="nav-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="nav-card-icon">📊</div>
            <div class="nav-card-title">Analytics</div>
            <div class="nav-card-desc">Insights and performance metrics</div>
        </div>
        """, unsafe_allow_html=True)

# --- Conversations View ---
elif st.session_state.current_view == 'conversations':
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("### 💬 Live Conversations")
    with col2:
        if st.button("🏠 Home"):
            st.session_state.current_view = 'home'
            st.rerun()
    
    if not df_convo.empty:
        col_filter, col_refresh = st.columns([4, 1])
        
        with col_filter:
            all_users = df_convo.sort_values(by="timestamp", ascending=False)['from_number'].unique()
            selected_user = st.selectbox("Select a User Conversation:", all_users, key="user_select", label_visibility="collapsed")
        
        with col_refresh:
            if st.button("🔄 Refresh", key="refresh_convo"):
                st.rerun()
        
        if selected_user:
            user_chat = df_convo[df_convo['from_number'] == selected_user].sort_values(by="timestamp")

            # WhatsApp Header
            st.markdown(f"""
            <div class="whatsapp-header">
                <div class="whatsapp-header-avatar">👤</div>
                <div class="whatsapp-header-info">
                    <h3>{selected_user}</h3>
                    <p>{len(user_chat)} messages • Last seen: {user_chat.iloc[-1]['timestamp'] if not user_chat.empty else 'N/A'}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # WhatsApp Chat Body
            chat_html = """
            <style>
            .chat-body {
                background: #e5ddd5;
                padding: 20px;
                border-radius: 0 0 10px 10px;
                min-height: 500px;
                max-height: 600px;
                overflow-y: auto;
                box-shadow: inset 0 0 4px rgba(0,0,0,0.1);
                font-family: 'Poppins', sans-serif;
            }
            .message-row {
                display: flex;
                margin: 10px 0;
            }
            .bubble {
                padding: 10px 14px;
                border-radius: 10px;
                max-width: 70%;
                line-height: 1.4;
                box-shadow: 0 1px 1px rgba(0,0,0,0.1);
            }
            .user-bubble {
                background-color: #dcf8c6;
                margin-left: auto;
                border-bottom-right-radius: 0;
            }
            .bot-bubble {
                background-color: #fff;
                margin-right: auto;
                border-bottom-left-radius: 0;
            }
            .sender-name {
                font-size: 0.8rem;
                font-weight: 600;
                margin-bottom: 3px;
                color: #075e54;
            }
            .time {
                font-size: 0.7rem;
                color: #667781;
                text-align: right;
                margin-top: 4px;
            }
            </style>
            <div class="chat-body">
            """

            for _, row in user_chat.iterrows():
                message = html.escape(str(row['message_content'])).replace('\n', '<br>')
                time_str = row['timestamp'].split(' ')[-1] if ' ' in row['timestamp'] else row['timestamp']

                if row['message_type'] == 'user':
                    chat_html += f"""
                    <div class="message-row">
                        <div class="bubble user-bubble">
                            <div>{message}</div>
                            <div class="time">{time_str}</div>
                        </div>
                    </div>
                    """
                else:
                    chat_html += f"""
                    <div class="message-row">
                        <div class="bubble bot-bubble">
                            <div class="sender-name">Agent Bot</div>
                            <div>{message}</div>
                            <div class="time">{time_str}</div>
                        </div>
                    </div>
                    """

            chat_html += "</div>"
            components.html(chat_html, height=620, scrolling=True)
    else:
        st.info("📭 No conversations found yet. Waiting for users to interact with the bot...")

# --- Orders View ---
elif st.session_state.current_view == 'orders':
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("### 🛒 Order History")
    with col2:
        if st.button("🏠 Home"):
            st.session_state.current_view = 'home'
            st.rerun()
    
    with st.container(border=True):
        if not df_orders.empty:
            col_search, col_export = st.columns([4, 1])
            
            with col_search:
                search_term = st.text_input("🔍 Search orders...", placeholder="Search by product, address, or payment method")
            
            with col_export:
                st.markdown("<br>", unsafe_allow_html=True)
                csv = df_orders.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Export", csv, "orders.csv", "text/csv", key='download-csv')
            
            columns_to_show = ['timestamp', 'product_details', 'delivery_address', 'payment_method']
            existing_columns_to_show = [col for col in columns_to_show if col in df_orders.columns]
            
            df_display = df_orders.sort_values(by="timestamp", ascending=False)[existing_columns_to_show]
            
            if search_term:
                mask = df_display.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)
                df_display = df_display[mask]
            
            st.dataframe(df_display, use_container_width=True, height=500)
            
            st.markdown(f"""
            <div style='text-align: center; color: #666; margin-top: 10px;'>
                Showing {len(df_display)} orders
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("🛒 No completed orders yet. Orders will appear here once customers complete their purchases.")

# --- Analytics View ---
elif st.session_state.current_view == 'analytics':
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("### 📊 Dashboard Analytics")
    with col2:
        if st.button("🏠 Home"):
            st.session_state.current_view = 'home'
            st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("**💬 Message Distribution**")
            if not df_convo.empty:
                message_counts = df_convo['message_type'].value_counts()
                st.bar_chart(message_counts)
            else:
                st.info("No conversation data available")
    
    with col2:
        with st.container(border=True):
            st.markdown("**💳 Payment Methods**")
            if not df_orders.empty:
                payment_counts = df_orders['payment_method'].value_counts()
                st.bar_chart(payment_counts)
            else:
                st.info("No order data available")
    
    with st.container(border=True):
        st.markdown("**🕒 Recent Activity Timeline**")
        
        if not df_convo.empty:
            recent_activity = df_convo.sort_values(by="timestamp", ascending=False).head(10)
            for _, row in recent_activity.iterrows():
                icon = "🤖" if row['message_type'] == 'bot' else "👤"
                st.markdown(f"{icon} **{row['timestamp']}** - {row['from_number'][:15]}... sent a message")
        else:
            st.info("No recent activity to display.")

# --- Footer ---
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("🔄 Refresh All Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown(f"""
<div style='text-align: center; color: #666; padding: 20px;'>
    Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
    Status: <span style='color: #28a745;'>● Online</span>
</div>
""", unsafe_allow_html=True)
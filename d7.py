import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta, date
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="E-Commerce Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background: #f8fafc;
    }
    
    .main {
        padding: 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Header */
    .dashboard-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 2rem;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .dashboard-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1f2937;
        margin: 2rem 0 1rem 0;
        padding: 0.5rem 0;
        border-bottom: 2px solid #e5e7eb;
    }
    
    /* Cards */
    .content-card {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border: 1px solid #f3f4f6;
    }
    
    .insight-card {
        background: white;
        border-radius: 8px;
        padding: 1.25rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin: 0.75rem 0;
        border-left: 4px solid #3b82f6;
    }
    
    .insight-card.info { border-left-color: #3b82f6; }
    .insight-card.success { border-left-color: #10b981; }
    .insight-card.warning { border-left-color: #f59e0b; }
    .insight-card.critical { border-left-color: #ef4444; }
    
    .card-title {
        font-size: 1rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .card-content {
        color: #6b7280;
        line-height: 1.5;
        font-size: 0.9rem;
    }
    
    /* Charts */
    .chart-container {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border: 1px solid #f3f4f6;
    }
    
    /* Tables */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: white;
        padding: 4px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 6px;
        color: #6b7280;
        font-weight: 600;
        padding: 8px 16px;
        border: none;
        font-size: 0.9rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: #3b82f6;
        color: white;
    }
    
    /* Metrics */
    .stMetric {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border: 1px solid #f3f4f6;
    }
    
    /* Sidebar */
    .sidebar .stSelectbox > div > div {
        background: white;
        border-radius: 6px;
        border: 1px solid #d1d5db;
    }
    
    .sidebar .stDateInput > div > div > div {
        background: white;
        border-radius: 6px;
        border: 1px solid #d1d5db;
    }
    
    /* Summary Box */
    .summary-box {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        border-radius: 8px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .summary-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_comprehensive_data():
    """Load all e-commerce datasets"""
    datasets = {}
    file_paths = {
        'customers': 'C:/Users/nisma/OneDrive/Documents/Universitas Airlangga/Lomba/SSDC/E-Commerce/E-Commerce/customers_dataset.csv',
        'orders': 'C:/Users/nisma/OneDrive/Documents/Universitas Airlangga/Lomba/SSDC/E-Commerce/E-Commerce/orders_dataset.csv',
        'order_items': 'C:/Users/nisma/OneDrive/Documents/Universitas Airlangga/Lomba/SSDC/E-Commerce/E-Commerce/order_items_dataset.csv',
        'order_payments': 'C:/Users/nisma/OneDrive/Documents/Universitas Airlangga/Lomba/SSDC/E-Commerce/E-Commerce/order_payments_dataset.csv',
        'order_reviews': 'C:/Users/nisma/OneDrive/Documents/Universitas Airlangga/Lomba/SSDC/E-Commerce/E-Commerce/order_reviews_dataset.csv',
        'products': 'C:/Users/nisma/OneDrive/Documents/Universitas Airlangga/Lomba/SSDC/E-Commerce/E-Commerce/products_dataset.csv',
        'sellers': 'C:/Users/nisma/OneDrive/Documents/Universitas Airlangga/Lomba/SSDC/E-Commerce/E-Commerce/sellers_dataset.csv',
        'geolocation': 'C:/Users/nisma/OneDrive/Documents/Universitas Airlangga/Lomba/SSDC/E-Commerce/E-Commerce/geolocation_dataset.csv',
        'category_translation': 'C:/Users/nisma/OneDrive/Documents/Universitas Airlangga/Lomba/SSDC/E-Commerce/E-Commerce/product_category_name_translation.csv',
        'marketing_leads': 'C:/Users/nisma/OneDrive/Documents/Universitas Airlangga/Lomba/SSDC/E-Commerce/E-Commerce/marketing_qualified_leads_dataset.csv',
        'closed_deals': 'C:/Users/nisma/OneDrive/Documents/Universitas Airlangga/Lomba/SSDC/E-Commerce/E-Commerce/closed_deals_dataset.csv'
    }
    
    try:
        for dataset_name, file_path in file_paths.items():
            datasets[dataset_name] = pd.read_csv(file_path)
        
        # Data preprocessing
        datasets['orders']['order_purchase_timestamp'] = pd.to_datetime(datasets['orders']['order_purchase_timestamp'], errors='coerce')
        datasets['orders']['order_delivered_customer_date'] = pd.to_datetime(datasets['orders']['order_delivered_customer_date'], errors='coerce')
        datasets['orders']['order_estimated_delivery_date'] = pd.to_datetime(datasets['orders']['order_estimated_delivery_date'], errors='coerce')
        
        return datasets
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def create_business_dataframe(datasets):
    """Create comprehensive business dataframe"""
    df = datasets['order_items'].merge(
        datasets['orders'][['order_id', 'customer_id', 'order_purchase_timestamp', 'order_status', 
                          'order_delivered_customer_date', 'order_estimated_delivery_date']], 
        on='order_id', how='left'
    ).merge(
        datasets['products'][['product_id', 'product_category_name']], 
        on='product_id', how='left'
    ).merge(
        datasets['category_translation'], 
        on='product_category_name', how='left'
    ).merge(
        datasets['order_reviews'][['order_id', 'review_score']], 
        on='order_id', how='left'
    ).merge(
        datasets['customers'][['customer_id', 'customer_state', 'customer_city']], 
        on='customer_id', how='left'
    )
    
    # Business calculations
    df['total_value'] = df['price'] + df['freight_value']
    df['order_date'] = df['order_purchase_timestamp'].dt.date
    df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M')
    df['order_year'] = df['order_purchase_timestamp'].dt.year
    df['order_quarter'] = df['order_purchase_timestamp'].dt.quarter
    
    # Delivery performance
    df['delivery_days'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days
    df['estimated_days'] = (df['order_estimated_delivery_date'] - df['order_purchase_timestamp']).dt.days
    df['on_time_delivery'] = df['delivery_days'] <= df['estimated_days']
    
    return df

def calculate_kpis(df, start_date, end_date):
    """Calculate business KPIs with proper comparisons"""
    # Current period
    mask = (df['order_date'] >= start_date) & (df['order_date'] <= end_date)
    current_data = df[mask]
    
    if len(current_data) == 0:
        return None
    
    # Previous period for comparison (same duration)
    period_days = (end_date - start_date).days
    prev_start = start_date - timedelta(days=period_days + 1)
    prev_end = start_date - timedelta(days=1)
    prev_mask = (df['order_date'] >= prev_start) & (df['order_date'] <= prev_end)
    prev_data = df[prev_mask]
    
    # Current metrics
    current_revenue = current_data['total_value'].sum()
    current_orders = current_data['order_id'].nunique()
    current_customers = current_data['customer_id'].nunique()
    current_satisfaction = current_data['review_score'].mean()
    
    # Delivery metrics
    delivered_orders = current_data[current_data['on_time_delivery'].notna()]
    current_delivery_rate = delivered_orders['on_time_delivery'].mean() * 100 if len(delivered_orders) > 0 else 0
    
    # Previous metrics
    prev_revenue = prev_data['total_value'].sum() if len(prev_data) > 0 else 0
    prev_orders = prev_data['order_id'].nunique() if len(prev_data) > 0 else 0
    prev_customers = prev_data['customer_id'].nunique() if len(prev_data) > 0 else 0
    prev_satisfaction = prev_data['review_score'].mean() if len(prev_data) > 0 else 0
    
    prev_delivered = prev_data[prev_data['on_time_delivery'].notna()]
    prev_delivery_rate = prev_delivered['on_time_delivery'].mean() * 100 if len(prev_delivered) > 0 else 0
    
    # Growth calculations with better logic
    def safe_growth(current, previous):
        if previous == 0 or pd.isna(previous):
            if current > 0:
                return 100.0  # Show 100% instead of infinite growth
            else:
                return 0.0
        return ((current - previous) / previous) * 100
    
    def safe_change(current, previous):
        if pd.isna(previous) or pd.isna(current):
            return 0.0
        return current - previous
    
    revenue_growth = safe_growth(current_revenue, prev_revenue)
    orders_growth = safe_growth(current_orders, prev_orders)
    customers_growth = safe_growth(current_customers, prev_customers)
    satisfaction_change = safe_change(current_satisfaction, prev_satisfaction)
    delivery_change = current_delivery_rate - prev_delivery_rate
    
    # Cap extreme growth rates for display
    revenue_growth = min(revenue_growth, 999.9) if revenue_growth > 0 else max(revenue_growth, -99.9)
    orders_growth = min(orders_growth, 999.9) if orders_growth > 0 else max(orders_growth, -99.9)
    customers_growth = min(customers_growth, 999.9) if customers_growth > 0 else max(customers_growth, -99.9)
    
    kpis = {
        'revenue': {
            'value': current_revenue, 
            'growth': revenue_growth,
            'prev_value': prev_revenue,
            'period_info': f"Current: {start_date} to {end_date} | Previous: {prev_start} to {prev_end}"
        },
        'orders': {
            'value': current_orders, 
            'growth': orders_growth,
            'prev_value': prev_orders,
            'period_info': f"Current: {start_date} to {end_date} | Previous: {prev_start} to {prev_end}"
        },
        'customers': {
            'value': current_customers, 
            'growth': customers_growth,
            'prev_value': prev_customers,
            'period_info': f"Current: {start_date} to {end_date} | Previous: {prev_start} to {prev_end}"
        },
        'satisfaction': {
            'value': current_satisfaction if not pd.isna(current_satisfaction) else 0, 
            'growth': satisfaction_change,
            'prev_value': prev_satisfaction,
            'period_info': f"Current: {start_date} to {end_date} | Previous: {prev_start} to {prev_end}"
        },
        'delivery': {
            'value': current_delivery_rate, 
            'growth': delivery_change,
            'prev_value': prev_delivery_rate,
            'period_info': f"Current: {start_date} to {end_date} | Previous: {prev_start} to {prev_end}"
        }
    }
    
    return kpis, current_data

def create_comprehensive_visualizations(df, datasets):
    """Create comprehensive visualizations"""
    
    # 1. Revenue Trend Analysis
    monthly_data = df.groupby(df['order_purchase_timestamp'].dt.to_period('M')).agg({
        'total_value': 'sum',
        'order_id': 'nunique',
        'customer_id': 'nunique',
        'review_score': 'mean'
    }).reset_index()
    monthly_data['month'] = monthly_data['order_purchase_timestamp'].astype(str)
    monthly_data = monthly_data.sort_values('month')
    
    fig_revenue_trend = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Monthly Revenue', 'Monthly Orders', 'Active Customers', 'Customer Satisfaction'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Revenue
    fig_revenue_trend.add_trace(
        go.Scatter(x=monthly_data['month'], y=monthly_data['total_value'],
                  mode='lines+markers', name='Revenue',
                  line=dict(color='#10b981', width=3)),
        row=1, col=1
    )
    
    # Orders
    fig_revenue_trend.add_trace(
        go.Scatter(x=monthly_data['month'], y=monthly_data['order_id'],
                  mode='lines+markers', name='Orders',
                  line=dict(color='#f59e0b', width=3)),
        row=1, col=2
    )
    
    # Customers
    fig_revenue_trend.add_trace(
        go.Scatter(x=monthly_data['month'], y=monthly_data['customer_id'],
                  mode='lines+markers', name='Customers',
                  line=dict(color='#8b5cf6', width=3)),
        row=2, col=1
    )
    
    # Satisfaction
    fig_revenue_trend.add_trace(
        go.Scatter(x=monthly_data['month'], y=monthly_data['review_score'],
                  mode='lines+markers', name='Satisfaction',
                  line=dict(color='#ef4444', width=3)),
        row=2, col=2
    )
    
    fig_revenue_trend.update_layout(height=600, showlegend=False, title_text="Business Performance Trends")
    
    # 2. Category Performance Matrix
    category_data = df.groupby('product_category_name_english').agg({
        'total_value': 'sum',
        'order_id': 'nunique',
        'review_score': 'mean',
        'on_time_delivery': lambda x: x.mean() if x.notna().sum() > 0 else 0
    }).reset_index()
    category_data = category_data.dropna().sort_values('total_value', ascending=False).head(15)
    category_data['category_clean'] = category_data['product_category_name_english'].str.replace('_', ' ').str.title()
    
    fig_category_matrix = px.scatter(
        category_data,
        x='review_score',
        y='total_value',
        size='order_id',
        color='on_time_delivery',
        hover_name='category_clean',
        color_continuous_scale='RdYlGn',
        title='Category Performance Matrix: Revenue vs Satisfaction',
        labels={'review_score': 'Customer Satisfaction', 'total_value': 'Revenue (R$)', 'on_time_delivery': 'On-Time Rate'}
    )
    fig_category_matrix.update_layout(height=500)
    
    # 3. Geographic Revenue Distribution
    state_data = df.groupby('customer_state').agg({
        'total_value': 'sum',
        'customer_id': 'nunique',
        'order_id': 'nunique'
    }).reset_index()
    state_data = state_data.dropna().sort_values('total_value', ascending=True).tail(15)
    
    fig_geo = px.bar(
        state_data,
        x='total_value',
        y='customer_state',
        orientation='h',
        title='Revenue by State (Top 15)',
        color='customer_id',
        color_continuous_scale='Blues',
        labels={'total_value': 'Revenue (R$)', 'customer_state': 'State'}
    )
    fig_geo.update_layout(height=500)
    
    # 4. Order Volume by Day of Week
    df['day_of_week'] = df['order_purchase_timestamp'].dt.day_name()
    daily_orders = df.groupby('day_of_week')['order_id'].nunique().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ])
    
    fig_daily = px.bar(
        x=daily_orders.index,
        y=daily_orders.values,
        title='Order Volume by Day of Week',
        labels={'x': 'Day', 'y': 'Number of Orders'},
        color=daily_orders.values,
        color_continuous_scale='Viridis'
    )
    fig_daily.update_layout(height=400, showlegend=False)
    
    # 5. Payment Method Analysis
    payment_data = df.merge(
        datasets['order_payments'][['order_id', 'payment_type', 'payment_value']], 
        on='order_id', how='left'
    )
    payment_summary = payment_data.groupby('payment_type').agg({
        'payment_value': 'sum',
        'order_id': 'nunique'
    }).reset_index()
    payment_summary = payment_summary.sort_values('payment_value', ascending=False)
    
    fig_payment = px.pie(
        payment_summary,
        values='payment_value',
        names='payment_type',
        title='Payment Method Distribution by Value'
    )
    fig_payment.update_layout(height=400)
    
    # 6. Quarterly Performance
    quarterly_data = df.groupby(['order_year', 'order_quarter']).agg({
        'total_value': 'sum',
        'order_id': 'nunique'
    }).reset_index()
    quarterly_data['period'] = quarterly_data['order_year'].astype(str) + ' Q' + quarterly_data['order_quarter'].astype(str)
    
    fig_quarterly = go.Figure()
    fig_quarterly.add_trace(go.Bar(
        x=quarterly_data['period'],
        y=quarterly_data['total_value'],
        name='Revenue',
        marker_color='lightblue',
        yaxis='y'
    ))
    
    fig_quarterly.add_trace(go.Scatter(
        x=quarterly_data['period'],
        y=quarterly_data['order_id'],
        mode='lines+markers',
        name='Orders',
        line=dict(color='red', width=3),
        yaxis='y2'
    ))
    
    fig_quarterly.update_layout(
        title='Quarterly Performance: Revenue and Orders',
        xaxis_title='Quarter',
        yaxis=dict(title='Revenue (R$)', side='left'),
        yaxis2=dict(title='Number of Orders', side='right', overlaying='y'),
        height=400
    )
    
    return fig_revenue_trend, fig_category_matrix, fig_geo, fig_daily, fig_payment, fig_quarterly

def generate_data_driven_insights(kpis, df):
    """Generate objective, data-driven insights"""
    insights = []
    
    # Revenue performance analysis
    revenue_growth = kpis['revenue']['growth']
    revenue_value = kpis['revenue']['value']
    
    if revenue_growth > 10:
        insights.append({
            'type': 'success',
            'title': 'Strong Revenue Growth',
            'content': f"Revenue shows {revenue_growth:.1f}% growth with total value of R$ {revenue_value:,.0f}. This indicates positive market response."
        })
    elif revenue_growth > 0:
        insights.append({
            'type': 'info',
            'title': 'Moderate Revenue Growth',
            'content': f"Revenue increased by {revenue_growth:.1f}% to R$ {revenue_value:,.0f}. Performance is stable with potential for optimization."
        })
    else:
        insights.append({
            'type': 'warning',
            'title': 'Revenue Decline Observed',
            'content': f"Revenue decreased by {abs(revenue_growth):.1f}% to R$ {revenue_value:,.0f}. Requires analysis of contributing factors."
        })
    
    # Customer satisfaction analysis
    satisfaction = kpis['satisfaction']['value']
    if satisfaction >= 4.0:
        insights.append({
            'type': 'success',
            'title': 'Good Customer Satisfaction',
            'content': f"Average rating of {satisfaction:.2f}/5.0 indicates generally satisfied customers. Maintain quality standards."
        })
    elif satisfaction >= 3.5:
        insights.append({
            'type': 'warning',
            'title': 'Room for Satisfaction Improvement',
            'content': f"Average rating of {satisfaction:.2f}/5.0 suggests opportunities to enhance customer experience."
        })
    else:
        insights.append({
            'type': 'critical',
            'title': 'Customer Satisfaction Concern',
            'content': f"Average rating of {satisfaction:.2f}/5.0 is below expectations. Review service quality and processes."
        })
    
    # Delivery performance
    delivery_rate = kpis['delivery']['value']
    if delivery_rate >= 90:
        insights.append({
            'type': 'success',
            'title': 'Reliable Delivery Performance',
            'content': f"On-time delivery rate of {delivery_rate:.1f}% meets operational standards."
        })
    else:
        insights.append({
            'type': 'warning',
            'title': 'Delivery Performance Gap',
            'content': f"On-time delivery rate of {delivery_rate:.1f}% is below optimal levels. Consider logistics improvements."
        })
    
    # Market concentration analysis
    top_categories = df.groupby('product_category_name_english')['total_value'].sum().sort_values(ascending=False)
    if len(top_categories) > 0:
        top_category = top_categories.index[0]
        concentration = (top_categories.iloc[0] / top_categories.sum() * 100)
        
        insights.append({
            'type': 'info',
            'title': 'Category Performance Distribution',
            'content': f"{top_category.replace('_', ' ').title()} represents {concentration:.1f}% of revenue. {'High concentration in single category.' if concentration > 20 else 'Balanced category distribution.'}"
        })
    
    return insights

def main():
    # Dashboard Header
    st.markdown("""
    <div class="dashboard-header">
        <h1 class="dashboard-title">E-Commerce Business Intelligence</h1>
        <p class="dashboard-subtitle">Comprehensive Performance Analytics & Strategic Insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load and process data
    with st.spinner('Loading business data...'):
        datasets = load_comprehensive_data()
        if datasets is None:
            st.stop()
        
        df = create_business_dataframe(datasets)
    
    # Sidebar controls
    st.sidebar.header("🎛️ Analysis Controls")
    
    # Date filters
    min_date = df['order_date'].min()
    max_date = df['order_date'].max()
    default_start = max_date - timedelta(days=365)
    
    start_date = st.sidebar.date_input("Start Date", value=default_start, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)
    
    # Category filter
    categories = ['All Categories'] + sorted([cat for cat in df['product_category_name_english'].dropna().unique() if cat])
    selected_category = st.sidebar.selectbox("Product Category", categories)
    
    # State filter
    states = ['All States'] + sorted([state for state in df['customer_state'].dropna().unique() if state])
    selected_state = st.sidebar.selectbox("Geographic Region", states)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_category != 'All Categories':
        filtered_df = filtered_df[filtered_df['product_category_name_english'] == selected_category]
    if selected_state != 'All States':
        filtered_df = filtered_df[filtered_df['customer_state'] == selected_state]
    
    # Calculate KPIs
    result = calculate_kpis(filtered_df, start_date, end_date)
    if result is None:
        st.warning("No data available for the selected period")
        return
    
    kpis, analysis_df = result
    
    # KPI Dashboard using Streamlit columns and metrics
    st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)
    
    # Add explanation about period comparison
    with st.expander("ℹ️ How are growth percentages calculated?"):
        current_period_days = (end_date - start_date).days
        prev_start = start_date - timedelta(days=current_period_days + 1)
        prev_end = start_date - timedelta(days=1)
        
        st.write(f"""
        **Period Comparison Logic:**
        - **Current Period:** {start_date} to {end_date} ({current_period_days} days)
        - **Previous Period:** {prev_start} to {prev_end} ({current_period_days} days)
        
        **Growth Calculation Formula:**
        - Growth % = ((Current Value - Previous Value) / Previous Value) × 100
        - If Previous Value = 0, Growth is capped at 100% to avoid infinite values
        - Growth rates are capped at ±999.9% for display purposes
        
        **Example:**
        - Current Revenue: R$ {kpis['revenue']['value']:,.0f}
        - Previous Revenue: R$ {kpis['revenue']['prev_value']:,.0f}
        - Growth: {kpis['revenue']['growth']:+.1f}%
        """)
    
    # Display KPIs using Streamlit columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        delta_text = f"{kpis['revenue']['growth']:+.1f}% vs previous period"
        if abs(kpis['revenue']['growth']) > 500:
            delta_text += " ⚠️"
        st.metric(
            label="💰 Total Revenue",
            value=f"R$ {kpis['revenue']['value']:,.0f}",
            delta=delta_text
        )
        if kpis['revenue']['prev_value'] > 0:
            st.caption(f"Previous: R$ {kpis['revenue']['prev_value']:,.0f}")
        else:
            st.caption("Previous: No data")
    
    with col2:
        delta_text = f"{kpis['orders']['growth']:+.1f}% change"
        if abs(kpis['orders']['growth']) > 500:
            delta_text += " ⚠️"
        st.metric(
            label="📦 Total Orders",
            value=f"{kpis['orders']['value']:,}",
            delta=delta_text
        )
        if kpis['orders']['prev_value'] > 0:
            st.caption(f"Previous: {kpis['orders']['prev_value']:,}")
        else:
            st.caption("Previous: No data")
    
    with col3:
        delta_text = f"{kpis['customers']['growth']:+.1f}% change"
        if abs(kpis['customers']['growth']) > 500:
            delta_text += " ⚠️"
        st.metric(
            label="👥 Active Customers",
            value=f"{kpis['customers']['value']:,}",
            delta=delta_text
        )
        if kpis['customers']['prev_value'] > 0:
            st.caption(f"Previous: {kpis['customers']['prev_value']:,}")
        else:
            st.caption("Previous: No data")
    
    with col4:
        st.metric(
            label="⭐ Customer Satisfaction",
            value=f"{kpis['satisfaction']['value']:.2f}/5.0",
            delta=f"{kpis['satisfaction']['growth']:+.2f} rating change"
        )
        if kpis['satisfaction']['prev_value'] > 0:
            st.caption(f"Previous: {kpis['satisfaction']['prev_value']:.2f}/5.0")
        else:
            st.caption("Previous: No data")
    
    with col5:
        st.metric(
            label="🚚 On-Time Delivery",
            value=f"{kpis['delivery']['value']:.1f}%",
            delta=f"{kpis['delivery']['growth']:+.1f}% change"
        )
        if kpis['delivery']['prev_value'] > 0:
            st.caption(f"Previous: {kpis['delivery']['prev_value']:.1f}%")
        else:
            st.caption("Previous: No data")
    
    # Business Insights
    st.markdown('<div class="section-header">💡 Data-Driven Insights</div>', unsafe_allow_html=True)
    
    insights = generate_data_driven_insights(kpis, analysis_df)
    
    insight_cols = st.columns(len(insights) if len(insights) <= 4 else 4)
    for i, insight in enumerate(insights[:4]):
        with insight_cols[i % 4]:
            st.markdown(f"""
            <div class="insight-card {insight['type']}">
                <div class="card-title">{insight['title']}</div>
                <div class="card-content">{insight['content']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Main Analysis Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Performance Dashboard", 
        "🎯 Category Analysis", 
        "🗺️ Geographic Insights",
        "📊 Operational Analytics",
        "🚀 Strategic Summary"
    ])
    
    with tab1:
        st.markdown("### Comprehensive Performance Dashboard")
        
        # Create all visualizations
        try:
            fig_trends, fig_category_matrix, fig_geo, fig_daily, fig_payment, fig_quarterly = create_comprehensive_visualizations(analysis_df, datasets)
            
            # Display trend analysis
            st.plotly_chart(fig_trends, use_container_width=True)
            
            # Additional charts in columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(fig_daily, use_container_width=True)
                st.plotly_chart(fig_quarterly, use_container_width=True)
            
            with col2:
                st.plotly_chart(fig_payment, use_container_width=True)
                
                # Key metrics summary
                avg_order_value = analysis_df.groupby('order_id')['total_value'].sum().mean()
                items_per_order = len(analysis_df) / kpis['orders']['value'] if kpis['orders']['value'] > 0 else 0
                
                st.markdown("#### Key Business Metrics")
                
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric("Average Order Value", f"R$ {avg_order_value:,.0f}")
                    st.metric("Items per Order", f"{items_per_order:.1f}")
                with metric_col2:
                    revenue_per_customer = kpis['revenue']['value'] / kpis['customers']['value'] if kpis['customers']['value'] > 0 else 0
                    st.metric("Revenue per Customer", f"R$ {revenue_per_customer:,.0f}")
                    st.metric("Total Product Categories", f"{analysis_df['product_category_name_english'].nunique()}")
                    
        except Exception as e:
            st.error(f"Error creating visualizations: {str(e)}")
    
    with tab2:
        st.markdown("### Category Performance Analysis")
        
        try:
            # Category matrix visualization
            fig_trends, fig_category_matrix, fig_geo, fig_daily, fig_payment, fig_quarterly = create_comprehensive_visualizations(analysis_df, datasets)
            st.plotly_chart(fig_category_matrix, use_container_width=True)
        except:
            st.info("Category matrix visualization temporarily unavailable")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top Categories by Revenue")
            
            category_performance = analysis_df.groupby('product_category_name_english').agg({
                'total_value': 'sum',
                'order_id': 'nunique',
                'review_score': 'mean',
                'on_time_delivery': lambda x: x.mean() if x.notna().sum() > 0 else 0
            }).round(2)
            
            category_performance.columns = ['Revenue (R$)', 'Orders', 'Avg Rating', 'On-Time %']
            category_performance = category_performance.sort_values('Revenue (R$)', ascending=False).head(10)
            
            # Format for display
            category_display = category_performance.copy()
            category_display['Revenue (R$)'] = category_display['Revenue (R$)'].apply(lambda x: f"R$ {x:,.0f}")
            category_display['On-Time %'] = category_display['On-Time %'].apply(lambda x: f"{x*100:.1f}%")
            category_display.index = category_display.index.str.replace('_', ' ').str.title()
            
            st.dataframe(category_display, use_container_width=True)
        
        with col2:
            st.markdown("#### Category Insights")
            
            if len(category_performance) > 0:
                # Top performing categories
                top_revenue_cat = category_performance.index[0]
                top_revenue_value = category_performance.iloc[0]['Revenue (R$)']
                
                # Best satisfaction
                best_satisfaction_cat = category_performance.sort_values('Avg Rating', ascending=False).index[0]
                best_satisfaction_score = category_performance.sort_values('Avg Rating', ascending=False).iloc[0]['Avg Rating']
                
                # Market share calculation
                total_revenue = category_performance['Revenue (R$)'].sum()
                market_share = (top_revenue_value / total_revenue * 100)
                
                st.markdown(f"""
                <div class="insight-card success">
                    <div class="card-title">🏆 Top Revenue Category</div>
                    <div class="card-content">
                        <strong>{top_revenue_cat.replace('_', ' ').title()}</strong><br>
                        Revenue: R$ {top_revenue_value:,.0f}<br>
                        Market Share: {market_share:.1f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="insight-card info">
                    <div class="card-title">⭐ Best Customer Satisfaction</div>
                    <div class="card-content">
                        <strong>{best_satisfaction_cat.replace('_', ' ').title()}</strong><br>
                        Rating: {best_satisfaction_score:.2f}/5.0<br>
                        Indicates high customer approval
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Category diversification insight
                category_count = len(category_performance)
                st.markdown(f"""
                <div class="insight-card warning">
                    <div class="card-title">📊 Portfolio Diversification</div>
                    <div class="card-content">
                        Operating in {category_count} categories<br>
                        Top 3 categories represent {((category_performance.head(3)['Revenue (R$)'].sum() / total_revenue) * 100):.1f}% of revenue<br>
                        {'Well diversified portfolio' if market_share < 25 else 'High concentration risk'}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Geographic Market Analysis")
        
        try:
            # Geographic visualization
            fig_trends, fig_category_matrix, fig_geo, fig_daily, fig_payment, fig_quarterly = create_comprehensive_visualizations(analysis_df, datasets)
            st.plotly_chart(fig_geo, use_container_width=True)
        except:
            st.info("Geographic visualization temporarily unavailable")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### State Performance")
            
            state_performance = analysis_df.groupby('customer_state').agg({
                'total_value': 'sum',
                'customer_id': 'nunique',
                'order_id': 'nunique',
                'review_score': 'mean'
            }).round(2)
            
            state_performance.columns = ['Revenue (R$)', 'Customers', 'Orders', 'Avg Rating']
            state_performance = state_performance.sort_values('Revenue (R$)', ascending=False).head(10)
            
            # Format for display
            state_display = state_performance.copy()
            state_display['Revenue (R$)'] = state_display['Revenue (R$)'].apply(lambda x: f"R$ {x:,.0f}")
            
            st.dataframe(state_display, use_container_width=True)
        
        with col2:
            st.markdown("#### Geographic Insights")
            
            if len(state_performance) > 0:
                # Top state analysis
                top_state = state_performance.index[0]
                top_state_revenue = state_performance.iloc[0]['Revenue (R$)']
                top_state_customers = state_performance.iloc[0]['Customers']
                
                # Market concentration
                total_states = len(state_performance)
                total_geo_revenue = state_performance['Revenue (R$)'].sum()
                concentration = (top_state_revenue / total_geo_revenue * 100)
                
                st.markdown(f"""
                <div class="insight-card success">
                    <div class="card-title">🎯 Leading Market</div>
                    <div class="card-content">
                        <strong>{top_state}</strong> leads with:<br>
                        Revenue: R$ {top_state_revenue:,.0f}<br>
                        Customers: {top_state_customers:,}<br>
                        Market Share: {concentration:.1f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Coverage analysis
                states_covered = analysis_df['customer_state'].nunique()
                avg_revenue_per_state = total_geo_revenue / states_covered
                
                st.markdown(f"""
                <div class="insight-card info">
                    <div class="card-title">📍 Market Coverage</div>
                    <div class="card-content">
                        Operating in {states_covered} states<br>
                        Average revenue per state: R$ {avg_revenue_per_state:,.0f}<br>
                        {'Concentrated market presence' if concentration > 30 else 'Distributed market presence'}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### Operational Performance Analytics")
        
        # Operational metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Delivery Performance")
            
            delivery_data = analysis_df[analysis_df['delivery_days'].notna()]
            if len(delivery_data) > 0:
                avg_delivery = delivery_data['delivery_days'].mean()
                on_time_rate = (delivery_data['on_time_delivery'].sum() / len(delivery_data)) * 100
                
                st.metric("Average Delivery Time", f"{avg_delivery:.1f} days")
                st.metric("On-Time Delivery Rate", f"{on_time_rate:.1f}%")
                
                # Delivery distribution
                delivery_ranges = pd.cut(delivery_data['delivery_days'], 
                                       bins=[0, 7, 14, 21, 30, float('inf')], 
                                       labels=['1-7 days', '8-14 days', '15-21 days', '22-30 days', '30+ days'])
                delivery_dist = delivery_ranges.value_counts()
                
                fig_delivery_dist = px.pie(
                    values=delivery_dist.values,
                    names=delivery_dist.index,
                    title='Delivery Time Distribution'
                )
                st.plotly_chart(fig_delivery_dist, use_container_width=True)
            else:
                st.info("Delivery data not available for selected period")
        
        with col2:
            st.markdown("#### Order Patterns")
            
            # Order timing analysis
            df_with_hour = analysis_df.copy()
            df_with_hour['order_hour'] = df_with_hour['order_purchase_timestamp'].dt.hour
            hourly_orders = df_with_hour.groupby('order_hour')['order_id'].nunique()
            
            if len(hourly_orders) > 0:
                peak_hour = hourly_orders.idxmax()
                peak_orders = hourly_orders.max()
                
                st.metric("Peak Order Hour", f"{peak_hour}:00")
                st.metric("Peak Hour Orders", f"{peak_orders} orders")
                
                # Hourly distribution chart
                fig_hourly = px.bar(
                    x=hourly_orders.index,
                    y=hourly_orders.values,
                    title='Orders by Hour of Day',
                    labels={'x': 'Hour', 'y': 'Number of Orders'}
                )
                st.plotly_chart(fig_hourly, use_container_width=True)
            else:
                st.info("Order timing data not available")
        
        with col3:
            st.markdown("#### Payment Analysis")
            
            try:
                # Payment method insights
                payment_data = analysis_df.merge(
                    datasets['order_payments'][['order_id', 'payment_type', 'payment_installments']], 
                    on='order_id', how='left'
                )
                
                if len(payment_data.dropna(subset=['payment_type'])) > 0:
                    payment_methods = payment_data['payment_type'].value_counts()
                    top_payment = payment_methods.index[0]
                    top_payment_pct = (payment_methods.iloc[0] / payment_methods.sum()) * 100
                    
                    st.metric("Most Popular Payment", top_payment.title())
                    st.metric("Market Share", f"{top_payment_pct:.1f}%")
                    
                    # Average installments
                    avg_installments = payment_data[payment_data['payment_installments'].notna()]['payment_installments'].mean()
                    if not pd.isna(avg_installments):
                        st.metric("Avg Installments", f"{avg_installments:.1f}")
                else:
                    st.info("Payment data not available for selected period")
            except:
                st.info("Payment analysis temporarily unavailable")
    
    with tab5:
        st.markdown("### Strategic Business Summary")
        
        # Calculate summary metrics for strategic insights
        total_revenue = kpis['revenue']['value']
        total_customers = kpis['customers']['value']
        avg_order_value = analysis_df.groupby('order_id')['total_value'].sum().mean()
        customer_lifetime_value = total_revenue / total_customers if total_customers > 0 else 0
        
        # Market position analysis
        category_concentration = analysis_df.groupby('product_category_name_english')['total_value'].sum()
        top_3_categories_share = (category_concentration.nlargest(3).sum() / category_concentration.sum()) * 100 if len(category_concentration) > 0 else 0
        
        # Geographic concentration
        state_concentration = analysis_df.groupby('customer_state')['total_value'].sum()
        top_5_states_share = (state_concentration.nlargest(5).sum() / state_concentration.sum()) * 100 if len(state_concentration) > 0 else 0
        
        # Executive summary
        st.markdown("#### 📊 Executive Business Summary")
        
        # Financial Performance Section
        st.markdown("**Financial Performance**")
        fin_col1, fin_col2, fin_col3, fin_col4 = st.columns(4)
        
        with fin_col1:
            st.metric(
                "Total Revenue", 
                f"R$ {total_revenue:,.0f}",
                delta=f"{kpis['revenue']['growth']:+.1f}% growth"
            )
        
        with fin_col2:
            st.metric(
                "Customer Base", 
                f"{total_customers:,}",
                delta=f"{kpis['customers']['growth']:+.1f}% change"
            )
        
        with fin_col3:
            st.metric(
                "Average Order Value", 
                f"R$ {avg_order_value:,.0f}"
            )
        
        with fin_col4:
            st.metric(
                "Customer Lifetime Value", 
                f"R$ {customer_lifetime_value:,.0f}"
            )
        
        st.markdown("---")
        
        # Market Position Section
        st.markdown("**Market Position**")
        mkt_col1, mkt_col2, mkt_col3, mkt_col4 = st.columns(4)
        
        with mkt_col1:
            st.metric(
                "Product Portfolio", 
                f"{analysis_df['product_category_name_english'].nunique()} categories"
            )
        
        with mkt_col2:
            st.metric(
                "Category Concentration", 
                f"Top 3: {top_3_categories_share:.1f}%"
            )
        
        with mkt_col3:
            st.metric(
                "Geographic Coverage", 
                f"{analysis_df['customer_state'].nunique()} states"
            )
        
        with mkt_col4:
            st.metric(
                "Geographic Concentration", 
                f"Top 5: {top_5_states_share:.1f}%"
            )
        
        st.markdown("---")
        
        # Operational Excellence Section
        st.markdown("**Operational Excellence**")
        ops_col1, ops_col2, ops_col3 = st.columns(3)
        
        with ops_col1:
            st.metric(
                "Customer Satisfaction", 
                f"{kpis['satisfaction']['value']:.2f}/5.0",
                delta=f"{kpis['satisfaction']['growth']:+.2f} change"
            )
        
        with ops_col2:
            st.metric(
                "Delivery Performance", 
                f"{kpis['delivery']['value']:.1f}%",
                delta=f"{kpis['delivery']['growth']:+.1f}% change"
            )
        
        with ops_col3:
            st.metric(
                "Order Processing", 
                f"{kpis['orders']['value']:,}",
                delta=f"{kpis['orders']['growth']:+.1f}% change"
            )
        
        # Strategic recommendations based on data
        st.markdown("#### Data-Based Strategic Considerations")
        
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            st.markdown("##### Areas of Strength")
            
            strengths = []
            if kpis['revenue']['growth'] > 5:
                strengths.append("Strong revenue growth momentum")
            if kpis['satisfaction']['value'] >= 4.0:
                strengths.append("Good customer satisfaction levels")
            if kpis['delivery']['value'] >= 85:
                strengths.append("Reliable delivery performance")
            if top_3_categories_share < 60:
                strengths.append("Well-diversified product portfolio")
            if analysis_df['customer_state'].nunique() >= 20:
                strengths.append("Broad geographic market coverage")
            
            if not strengths:
                strengths = ["Stable business operations", "Established customer base"]
            
            for strength in strengths:
                st.write(f"✅ {strength}")
        
        with rec_col2:
            st.markdown("##### Areas for Attention")
            
            considerations = []
            if kpis['revenue']['growth'] < 0:
                considerations.append("Revenue decline requires analysis")
            if kpis['satisfaction']['value'] < 4.0:
                considerations.append("Customer satisfaction improvement opportunity")
            if kpis['delivery']['value'] < 85:
                considerations.append("Delivery performance optimization needed")
            if top_3_categories_share > 70:
                considerations.append("High category concentration risk")
            if top_5_states_share > 80:
                considerations.append("Geographic concentration risk")
            
            if not considerations:
                considerations = ["Monitor competitive positioning", "Continue operational optimization"]
            
            for consideration in considerations:
                st.write(f"⚠️ {consideration}")
        
        # Final data summary
        st.markdown("#### Business Intelligence Summary")
        
        items_per_order = len(analysis_df) / kpis['orders']['value'] if kpis['orders']['value'] > 0 else 0
        
        st.info(f"""
        **Analysis Period:** {start_date} to {end_date}
        
        **Key Findings:**
        • Processing {kpis['orders']['value']:,} orders from {total_customers:,} customers
        • Average order value of R$ {avg_order_value:,.0f} with {items_per_order:.1f} items per order
        • Customer satisfaction averaging {kpis['satisfaction']['value']:.2f}/5.0 across all categories
        • {kpis['delivery']['value']:.1f}% on-time delivery performance
        • Market presence across {analysis_df['customer_state'].nunique()} states and {analysis_df['product_category_name_english'].nunique()} product categories
         """)

if __name__ == "__main__":
    main()
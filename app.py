import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="FORESIGHT AI • v9",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# THEME / CSS
# ============================================================
st.markdown("""
<style>
.stApp {
    background: #070d18;
    color: #f8fafc;
}
.main .block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}
section[data-testid="stSidebar"] {
    background: #0b1424;
    border-right: 1px solid #1d2a3d;
}
section[data-testid="stSidebar"] * {
    color: #dbe4f0;
}
.sidebar-brand {
    padding: 4px 4px 18px 4px;
}
.sidebar-brand .brand {
    font-size: 26px;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: .4px;
}
.sidebar-brand .sub {
    color: #7f91a8;
    font-size: 11px;
    margin-top: 4px;
}
.nav-label {
    color: #62748b;
    font-size: 10px;
    font-weight: 900;
    letter-spacing: 1.4px;
    margin: 18px 0 7px 2px;
}
.hero {
    background:
        radial-gradient(circle at 85% 20%, rgba(37,99,235,.28), transparent 34%),
        linear-gradient(135deg, #101d35 0%, #112d55 52%, #0b1425 100%);
    border: 1px solid #28466f;
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 22px;
    box-shadow: 0 18px 45px rgba(0,0,0,.30);
}
.hero-title {
    font-size: 39px;
    font-weight: 900;
    color: white;
    line-height: 1.05;
}
.hero-subtitle {
    color: #a9c5ff;
    font-size: 15px;
    font-weight: 600;
    margin-top: 7px;
}
.hero-description {
    color: #8fa2ba;
    font-size: 12px;
    margin-top: 8px;
}
.online {
    display: inline-block;
    margin-top: 14px;
    padding: 5px 11px;
    border-radius: 999px;
    background: #063b2d;
    border: 1px solid #087f5b;
    color: #6ee7b7;
    font-size: 10px;
    font-weight: 900;
}
.section-title {
    color: #f8fafc;
    font-size: 19px;
    font-weight: 850;
    margin: 19px 0 5px;
}
.section-sub {
    color: #667990;
    font-size: 11px;
    margin-bottom: 12px;
}
.kpi {
    background: linear-gradient(145deg, #101a2a, #111d31);
    border: 1px solid #22334a;
    border-radius: 14px;
    padding: 17px 18px;
    min-height: 116px;
    box-shadow: 0 8px 24px rgba(0,0,0,.20);
}
.kpi-label {
    color: #8092aa;
    font-size: 10px;
    font-weight: 900;
    letter-spacing: .7px;
}
.kpi-value {
    color: #fff;
    font-size: 27px;
    font-weight: 900;
    margin-top: 7px;
}
.kpi-note {
    color: #5f7188;
    font-size: 10px;
    margin-top: 3px;
}
.panel {
    background: #0d1726;
    border: 1px solid #1e2d43;
    border-radius: 16px;
    padding: 16px;
}
.alert {
    background: linear-gradient(135deg, #351010, #240d12);
    border: 1px solid #7f1d1d;
    border-left: 4px solid #ef4444;
    border-radius: 13px;
    padding: 15px 17px;
}
.good {
    background: linear-gradient(135deg, #082c24, #0b211d);
    border: 1px solid #166534;
    border-left: 4px solid #22c55e;
    border-radius: 13px;
    padding: 15px 17px;
}
.info {
    background: #0e1a2a;
    border: 1px solid #20324a;
    border-left: 4px solid #3b82f6;
    border-radius: 13px;
    padding: 15px 17px;
}
.card-title {
    color: #f8fafc;
    font-size: 13px;
    font-weight: 800;
}
.card-text {
    color: #8294ab;
    font-size: 11px;
    line-height: 1.55;
    margin-top: 5px;
}
.footer {
    text-align: center;
    color: #44556b;
    font-size: 10px;
    padding: 28px 0 10px;
}
div[data-testid="stMetric"] {
    background: #101a2a;
    border: 1px solid #22334a;
    border-radius: 12px;
    padding: 12px;
}
button[data-baseweb="tab"] {
    color: #94a3b8;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPERS
# ============================================================
def html(content):
    st.markdown(content, unsafe_allow_html=True)


def money(v):
    return f"{v:,.0f}"


def plot_theme(fig, height=None):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0d1726",
        plot_bgcolor="#0d1726",
        font=dict(color="#dbe4f0"),
        margin=dict(l=20, r=20, t=55, b=25),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    if height:
        fig.update_layout(height=height)
    return fig


# ============================================================
# DATA
# ============================================================
@st.cache_data
def load_data():
    final_output = pd.read_csv("final_output.csv")
    forecast_data = pd.read_csv("forecast_data.csv")
    risk_data = pd.read_csv("risk_data.csv")
    model_comparison = pd.read_csv("model_comparison.csv")

    forecast_data["Week_Start"] = pd.to_datetime(forecast_data["Week_Start"])
    return final_output, forecast_data, risk_data, model_comparison


try:
    final_output, forecast_data, risk_data, model_comparison = load_data()
except FileNotFoundError:
    st.error("❌ Required CSV file was not found.")
    st.info(
        "Keep final_output.csv, forecast_data.csv, risk_data.csv and "
        "model_comparison.csv in the same folder as this Streamlit app."
    )
    st.stop()
except Exception as e:
    st.error("❌ Error loading dashboard data.")
    st.exception(e)
    st.stop()


required_final = [
    "Product ID", "Forecast_8_Weeks", "Average_Weekly_Demand",
    "On_Hand_Units", "On_Order_Units", "Inventory_Position",
    "Weeks_of_Supply", "Risk_Category", "Recommended_Action"
]
required_forecast = ["Product ID", "Week_Start", "Forecast_Units"]
required_model = ["Model", "WAPE"]

missing_final = [c for c in required_final if c not in final_output.columns]
missing_forecast = [c for c in required_forecast if c not in forecast_data.columns]
missing_model = [c for c in required_model if c not in model_comparison.columns]

if missing_final or missing_forecast or missing_model:
    if missing_final:
        st.error(f"Missing columns in final_output.csv: {missing_final}")
    if missing_forecast:
        st.error(f"Missing columns in forecast_data.csv: {missing_forecast}")
    if missing_model:
        st.error(f"Missing columns in model_comparison.csv: {missing_model}")
    st.stop()


# ============================================================
# CALCULATIONS
# ============================================================
total_products = final_output["Product ID"].nunique()
total_forecast_rows = len(forecast_data)
total_8_week_forecast = final_output["Forecast_8_Weeks"].sum()
total_inventory = final_output["Inventory_Position"].sum()
total_on_hand = final_output["On_Hand_Units"].sum()
total_on_order = final_output["On_Order_Units"].sum()
average_wos = final_output["Weeks_of_Supply"].mean()

critical_products = (
    final_output["Risk_Category"].astype(str).str.lower().eq("critical").sum()
)

risk_counts = (
    final_output["Risk_Category"].astype(str)
    .value_counts()
    .rename_axis("Risk_Category")
    .reset_index(name="Product_Count")
)

best_model_row = model_comparison.loc[model_comparison["WAPE"].idxmin()]
best_model = best_model_row["Model"]
best_wape = float(best_model_row["WAPE"])

# Use a real category column if the supplied data has one.
category_candidates = [
    "Category", "Product Category", "Product_Category",
    "category", "product_category"
]
category_col = next((c for c in category_candidates if c in final_output.columns), None)


# ============================================================
# SIDEBAR — STYLE SIMILAR TO THE REFERENCE DASHBOARD
# ============================================================
with st.sidebar:
    html("""
    <div class="sidebar-brand">
        <div class="brand">FORESIGHT AI</div>
        <div class="sub">Demand & Inventory Intelligence</div>
    </div>
    <hr style="border-color:#1d2a3d;">
    """)

    html('<div class="nav-label">NAVIGATION</div>')
    page = st.radio(
        "Navigate to",
        [
            "🏠 Home",
            "📊 Executive Dashboard",
            "📈 Sales Analytics",
            "🏷️ Product Performance",
            "📦 Inventory Dashboard",
            "🚨 Stockout Risk",
            "📦 Overstock Dashboard",
            "🔮 Forecast Dashboard",
            "🤖 AI Forecast",
            "📉 Forecast vs Actual",
            "💡 Recommendations",
            "🔎 Product 360",
            "🧠 ML Performance",
        ],
        label_visibility="collapsed",
    )

    html("""
    <hr style="border-color:#1d2a3d;">
    <div style="font-size:10px;color:#65788f;line-height:1.7;">
        <b style="color:#91a4ba;">SYSTEM</b><br>
        <span style="color:#6ee7b7;">● ONLINE</span><br>
        Forecasting Engine Active<br>
        <span style="color:#536a83;">BUILD v10</span>
    </div>
    """)


# ============================================================
# COMMON HERO
# ============================================================
def hero(title, subtitle, description):
    html(f"""
    <div class="hero">
        <div class="hero-title">{title}</div>
        <div class="hero-subtitle">{subtitle}</div>
        <div class="hero-description">{description}</div>
        <span class="online">● AI ENGINE ONLINE</span>
    </div>
    """)


def kpi_row(items):
    cols = st.columns(len(items))
    for col, (label, value, note) in zip(cols, items):
        with col:
            html(f"""
            <div class="kpi">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-note">{note}</div>
            </div>
            """)


# ============================================================
# HOME
# ============================================================
if page == "🏠 Home":
    hero(
        "FORESIGHT AI",
        "AI-Powered Demand Forecasting & Inventory Intelligence",
        "A professional decision-support dashboard connecting ML demand forecasts with inventory risk and replenishment actions."
    )

    html('<div class="section-title">Dashboard Snapshot</div>')
    html('<div class="section-sub">High-level view of the current forecasting and inventory position.</div>')

    kpi_row([
        ("PRODUCTS", f"{total_products}", "Products monitored"),
        ("8-WEEK FORECAST", f"{total_8_week_forecast:,.0f}", "Predicted demand units"),
        ("INVENTORY POSITION", f"{total_inventory:,.0f}", "On-hand + on-order"),
        ("CRITICAL PRODUCTS", f"{critical_products}", "Require attention"),
    ])

    st.markdown("")

    left, right = st.columns([1.55, 1])

    with left:
        html("""
        <div class="panel">
            <div class="card-title">📦 Inventory Position by Product</div>
            <div class="card-text">Products ranked by inventory coverage available against expected demand.</div>
        </div>
        """)
        inv = final_output[["Product ID", "Inventory_Position"]].sort_values(
            "Inventory_Position", ascending=False
        )
        fig = px.treemap(
            inv,
            path=["Product ID"],
            values="Inventory_Position",
            title="",
        )
        plot_theme(fig, 410)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        html("""
        <div class="panel">
            <div class="card-title">📦 Top Inventory Position</div>
            <div class="card-text">Products with the highest current inventory position.</div>
        </div>
        """)
        top_inv = (
            final_output[["Product ID", "Inventory_Position"]]
            .sort_values("Inventory_Position", ascending=False)
            .head(10)
        )
        fig = px.bar(
            top_inv,
            x="Inventory_Position",
            y="Product ID",
            orientation="h",
            text_auto=".2s",
            title="",
        )
        plot_theme(fig, 410)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    # Reference-style second row
    c3, c4 = st.columns(2)

    with c3:
        html("""
        <div class="panel">
            <div class="card-title">📊 Stock Distribution by Risk</div>
            <div class="card-text">On-hand units grouped by the project's risk category.</div>
        </div>
        """)
        stock_risk = (
            final_output.groupby("Risk_Category", as_index=False)["On_Hand_Units"]
            .sum()
            .sort_values("On_Hand_Units", ascending=False)
        )
        fig = px.bar(
            stock_risk,
            x="Risk_Category",
            y="On_Hand_Units",
            text_auto=".2s",
            title="",
        )
        plot_theme(fig, 300)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        html("""
        <div class="panel">
            <div class="card-title">💰 Stock Value Distribution</div>
            <div class="card-text">Inventory position across the monitored products.</div>
        </div>
        """)
        stock_value = final_output[["Product ID", "Inventory_Position"]].sort_values(
            "Inventory_Position", ascending=False
        )
        fig = px.bar(
            stock_value,
            x="Product ID",
            y="Inventory_Position",
            text_auto=".2s",
            title="",
        )
        plot_theme(fig, 300)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    html('<div class="section-title">Business Health</div>')
    c1, c2, c3 = st.columns(3)
    with c1:
        html(f"""
        <div class="good">
            <div class="card-title">🏆 Best Model</div>
            <div class="card-text"><b style="color:#86efac;font-size:18px;">{best_model}</b><br>
            Lowest evaluated WAPE: {best_wape:.2f}%</div>
        </div>
        """)
    with c2:
        html(f"""
        <div class="alert">
            <div class="card-title">🔴 Critical Attention</div>
            <div class="card-text"><b style="color:#fca5a5;font-size:18px;">{critical_products}</b>
            products are currently classified as Critical.</div>
        </div>
        """)
    with c3:
        html(f"""
        <div class="info">
            <div class="card-title">📅 Forecast Horizon</div>
            <div class="card-text"><b style="color:#93c5fd;font-size:18px;">8 Weeks</b><br>
            {total_forecast_rows} forecast records are available.</div>
        </div>
        """)


# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================
elif page == "📊 Executive Dashboard":
    hero(
        "Executive Dashboard",
        "Demand, Inventory & Risk Command Center",
        "A management-level view of the most important Foresight AI indicators."
    )

    kpi_row([
        ("TOTAL PRODUCTS", f"{total_products}", "Active product set"),
        ("ON-HAND UNITS", f"{total_on_hand:,.0f}", "Current stock"),
        ("ON-ORDER UNITS", f"{total_on_order:,.0f}", "Incoming stock"),
        ("AVERAGE WOS", f"{average_wos:.2f}", "Weeks of supply"),
    ])

    st.markdown("")

    # --------------------------------------------------------
    # TOP ROW: TREEMAP + PRODUCT-LEVEL DONUT
    # --------------------------------------------------------
    c1, c2 = st.columns([1.45, 1])

    with c1:
        inv = final_output[
            ["Product ID", "Inventory_Position"]
        ].sort_values(
            "Inventory_Position",
            ascending=False
        )

        fig = px.treemap(
            inv,
            path=["Product ID"],
            values="Inventory_Position",
            title="Inventory Position by Product",
        )
        plot_theme(fig, 350)
        fig.update_traces(
            textinfo="label",
            marker=dict(
                line=dict(
                    width=2,
                    color="#0b1424"
                )
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Product-level inventory distribution.
        # Risk_Category is intentionally NOT used here because the current
        # project output classifies all monitored products as Critical.
        product_units = final_output[
            ["Product ID", "Inventory_Position"]
        ].sort_values(
            "Inventory_Position",
            ascending=False
        )

        fig = px.pie(
            product_units,
            names="Product ID",
            values="Inventory_Position",
            hole=.55,
            title="Inventory Position Distribution by Product",
        )
        plot_theme(fig, 350)
        fig.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Inventory Position: %{value:,.0f}<br>"
                "Share: %{percent}<extra></extra>"
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

    # --------------------------------------------------------
    # SECOND ROW: RISK + WOS
    # --------------------------------------------------------
    c3, c4 = st.columns(2)

    with c3:
        fig = px.bar(
            risk_counts,
            x="Risk_Category",
            y="Product_Count",
            text="Product_Count",
            title="Product Distribution by Risk Category",
        )
        fig.update_traces(textposition="outside")
        plot_theme(fig, 320)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        wos = final_output[
            ["Product ID", "Weeks_of_Supply"]
        ].sort_values(
            "Weeks_of_Supply"
        )

        fig = px.bar(
            wos,
            x="Weeks_of_Supply",
            y="Product ID",
            orientation="h",
            title="Weeks of Supply by Product",
        )
        fig.add_vline(
            x=1,
            line_dash="dash",
            annotation_text="1 week"
        )
        plot_theme(fig, 320)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# SALES ANALYTICS
# ============================================================
elif page == "📈 Sales Analytics":
    hero(
        "Sales Analytics",
        "Forecast Demand Distribution",
        "Explore the projected demand profile across the monitored products."
    )

    product_sales = final_output[["Product ID", "Forecast_8_Weeks"]].sort_values(
        "Forecast_8_Weeks", ascending=False
    )

    kpi_row([
        ("8-WEEK DEMAND", f"{total_8_week_forecast:,.0f}", "Total forecast"),
        ("AVG WEEKLY DEMAND", f"{final_output['Average_Weekly_Demand'].mean():,.0f}", "Across products"),
        ("PRODUCTS", f"{total_products}", "Forecasted"),
    ])

    fig = px.bar(
        product_sales,
        x="Product ID",
        y="Forecast_8_Weeks",
        text_auto=".2s",
        title="8-Week Forecast by Product",
    )
    plot_theme(fig, 430)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(product_sales, use_container_width=True, hide_index=True)


# ============================================================
# PRODUCT PERFORMANCE
# ============================================================
elif page == "🏷️ Product Performance":
    hero(
        "Product Performance",
        "Product-Level Demand & Inventory Ranking",
        "Compare forecast demand, inventory coverage and risk across products."
    )

    df = final_output[
        ["Product ID", "Forecast_8_Weeks", "Average_Weekly_Demand",
         "Inventory_Position", "Weeks_of_Supply", "Risk_Category"]
    ].sort_values("Forecast_8_Weeks", ascending=False)

    st.dataframe(df, use_container_width=True, hide_index=True)

    fig = px.scatter(
        df,
        x="Average_Weekly_Demand",
        y="Inventory_Position",
        size="Forecast_8_Weeks",
        hover_name="Product ID",
        color="Risk_Category",
        title="Demand vs Inventory Position",
    )
    plot_theme(fig, 430)
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# INVENTORY DASHBOARD
# ============================================================
elif page == "📦 Inventory Dashboard":
    hero(
        "Inventory Dashboard",
        "Inventory Monitoring & Distribution",
        "Monitor inventory position, on-hand stock, incoming stock and weeks of supply."
    )

    kpi_row([
        ("INVENTORY POSITION", f"{total_inventory:,.0f}", "On-hand + on-order"),
        ("ON-HAND", f"{total_on_hand:,.0f}", "Current units"),
        ("ON-ORDER", f"{total_on_order:,.0f}", "Incoming units"),
        ("AVG WOS", f"{average_wos:.2f}", "Average coverage"),
    ])

    st.markdown("")

    # --------------------------------------------------------
    # TOP ROW — INVENTORY POSITION + STOCK COMPOSITION
    # --------------------------------------------------------
    c1, c2 = st.columns([1.35, 1])

    with c1:
        inv = final_output[
            ["Product ID", "Inventory_Position"]
        ].sort_values(
            "Inventory_Position",
            ascending=False
        )

        fig = px.bar(
            inv,
            x="Inventory_Position",
            y="Product ID",
            orientation="h",
            text_auto=".2s",
            title="Inventory Position by Product — Operations",
        )
        plot_theme(fig, 390)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        composition = final_output[
            ["Product ID", "On_Hand_Units", "On_Order_Units"]
        ].sort_values(
            "On_Hand_Units",
            ascending=False
        )

        fig = go.Figure()
        fig.add_bar(
            x=composition["Product ID"],
            y=composition["On_Hand_Units"],
            name="On-Hand Units",
        )
        fig.add_bar(
            x=composition["Product ID"],
            y=composition["On_Order_Units"],
            name="On-Order Units",
        )
        fig.update_layout(
            barmode="stack",
            title="On-Hand vs On-Order Units — Operations",
            xaxis_title="Product ID",
            yaxis_title="Units",
        )
        plot_theme(fig, 390)
        st.plotly_chart(fig, use_container_width=True)

    # --------------------------------------------------------
    # SECOND ROW — STOCK + INCOMING STOCK
    # --------------------------------------------------------
    c3, c4 = st.columns(2)

    with c3:
        stock = final_output[
            ["Product ID", "On_Hand_Units"]
        ].sort_values(
            "On_Hand_Units",
            ascending=False
        )

        fig = px.bar(
            stock,
            x="On_Hand_Units",
            y="Product ID",
            orientation="h",
            text_auto=".2s",
            title="Stock Distribution by Product",
        )
        plot_theme(fig, 340)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        incoming = final_output[
            ["Product ID", "On_Order_Units"]
        ].sort_values(
            "On_Order_Units",
            ascending=False
        )

        fig = px.bar(
            incoming,
            x="On_Order_Units",
            y="Product ID",
            orientation="h",
            text_auto=".2s",
            title="On-Order Distribution by Product",
        )
        plot_theme(fig, 340)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# STOCKOUT RISK
# ============================================================

elif page == "🚨 Stockout Risk":
    hero(
        "Stockout Risk",
        "Products with Low Inventory Coverage",
        "Prioritize products with the lowest Weeks of Supply and review the recommended action."
    )

    risk = final_output.sort_values("Weeks_of_Supply", ascending=True)
    critical = risk[
        risk["Risk_Category"].astype(str).str.lower() == "critical"
    ]

    kpi_row([
        ("CRITICAL PRODUCTS", f"{len(critical)}", "Current classification"),
        ("LOWEST WOS", f"{risk['Weeks_of_Supply'].min():.2f}", "Lowest coverage"),
        ("CRITICAL INVENTORY", f"{critical['Inventory_Position'].sum():,.0f}", "Inventory position"),
        ("AVG WOS", f"{average_wos:.2f}", "Average coverage"),
    ])

    st.markdown("")

    c1, c2 = st.columns([1.35, 1])

    with c1:
        fig = px.bar(
            risk.head(15),
            x="Weeks_of_Supply",
            y="Product ID",
            orientation="h",
            color="Risk_Category",
            title="Stockout Risk — Lowest Weeks of Supply",
        )
        fig.add_vline(
            x=1,
            line_dash="dash",
            annotation_text="Critical threshold: 1 week"
        )
        plot_theme(fig, 430)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        critical_units = critical[
            ["Product ID", "Inventory_Position"]
        ].sort_values(
            "Inventory_Position",
            ascending=True
        ).head(15)

        fig = px.bar(
            critical_units,
            x="Inventory_Position",
            y="Product ID",
            orientation="h",
            text_auto=".2s",
            title="Stockout Risk — Critical Inventory Position",
        )
        plot_theme(fig, 430)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("")

    st.subheader("Critical Product Action List")
    st.dataframe(
        risk[
            [
                "Product ID",
                "Weeks_of_Supply",
                "Inventory_Position",
                "Average_Weekly_Demand",
                "Risk_Category",
                "Recommended_Action",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )




# ============================================================
# OVERSTOCK DASHBOARD
# ============================================================
elif page == "📦 Overstock Dashboard":
    hero(
        "Overstock Dashboard",
        "Inventory Coverage & Excess Stock Candidates",
        "Review products carrying relatively high inventory coverage. This page does not change the project's risk classification."
    )

    high_wos = final_output[
        ["Product ID", "Inventory_Position", "Average_Weekly_Demand", "Weeks_of_Supply"]
    ].sort_values("Weeks_of_Supply", ascending=False)

    kpi_row([
        ("HIGHEST WOS", f"{high_wos['Weeks_of_Supply'].max():.2f}", "Highest inventory coverage"),
        ("TOTAL INVENTORY", f"{total_inventory:,.0f}", "On-hand + on-order"),
        ("AVG WOS", f"{average_wos:.2f}", "Across products"),
        ("PRODUCTS", f"{total_products}", "Monitored products"),
    ])

    st.markdown("")
    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            high_wos.head(10).sort_values("Weeks_of_Supply"),
            x="Weeks_of_Supply",
            y="Product ID",
            orientation="h",
            text_auto=".2f",
            title="Highest Weeks of Supply",
        )
        plot_theme(fig, 400)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.bar(
            high_wos.head(10).sort_values("Inventory_Position"),
            x="Inventory_Position",
            y="Product ID",
            orientation="h",
            text_auto=".2s",
            title="Inventory Position of Highest-WOS Products",
        )
        plot_theme(fig, 400)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    html("""
    <div class="info">
        <div class="card-title">ℹ️ Interpretation</div>
        <div class="card-text">
            The supplied project output does not contain a separate Overstock risk label or
            overstock threshold. Therefore, this page shows high-WOS products as candidates
            for review rather than falsely classifying them as Overstock.
        </div>
    </div>
    """)
    st.dataframe(high_wos, use_container_width=True, hide_index=True)


# ============================================================
# FORECAST DASHBOARD
# ============================================================
elif page == "🔮 Forecast Dashboard":
    hero(
        "Forecast Dashboard",
        "8-Week Demand Forecast",
        "Explore forecast demand across weeks and products."
    )

    weekly = (
        forecast_data.groupby("Week_Start", as_index=False)["Forecast_Units"]
        .sum()
        .sort_values("Week_Start")
    )

    kpi_row([
        ("FORECAST RECORDS", f"{total_forecast_rows}", "Available forecast rows"),
        ("8-WEEK DEMAND", f"{total_8_week_forecast:,.0f}", "Total predicted units"),
        ("PRODUCTS", f"{total_products}", "Forecasted products"),
        ("BEST MODEL", f"{best_model}", f"WAPE {best_wape:.2f}%"),
    ])

    st.markdown("")
    fig = px.line(
        weekly,
        x="Week_Start",
        y="Forecast_Units",
        markers=True,
        title="Total Forecast Demand by Week",
    )
    plot_theme(fig, 400)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        forecast_data.sort_values(["Product ID", "Week_Start"]),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# AI FORECAST
# ============================================================
elif page == "🤖 AI Forecast":
    hero(
        "AI Forecast",
        "Product-Level Machine Learning Forecast",
        "Inspect the eight weekly predictions generated by the forecasting pipeline."
    )

    selected_product = st.selectbox(
        "Select Product",
        sorted(forecast_data["Product ID"].astype(str).unique())
    )

    product_forecast = forecast_data[
        forecast_data["Product ID"].astype(str) == selected_product
    ].sort_values("Week_Start")

    total_product_forecast = product_forecast["Forecast_Units"].sum()

    kpi_row([
        ("PRODUCT", selected_product, "Selected product"),
        ("8-WEEK FORECAST", f"{total_product_forecast:,.0f}", "Predicted units"),
        ("AVG WEEKLY", f"{product_forecast['Forecast_Units'].mean():,.0f}", "Predicted weekly demand"),
        ("WEEKS", f"{len(product_forecast)}", "Forecast records"),
    ])

    st.markdown("")
    fig = px.line(
        product_forecast,
        x="Week_Start",
        y="Forecast_Units",
        markers=True,
        title=f"AI Forecast — {selected_product}",
    )
    plot_theme(fig, 420)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(product_forecast, use_container_width=True, hide_index=True)


# ============================================================
# FORECAST VS ACTUAL
# ============================================================
elif page == "📉 Forecast vs Actual":
    hero(
        "Forecast vs Actual",
        "Forecast Evaluation View",
        "Compare predicted demand with actual demand when actual values are available in the supplied data."
    )

    actual_candidates = [
        "Actual_Units", "Actual_Demand", "Actual", "Demand", "Sales", "Units_Sold"
    ]
    actual_col = next((c for c in actual_candidates if c in forecast_data.columns), None)

    if actual_col is None:
        html("""
        <div class="info">
            <div class="card-title">ℹ️ Actual demand is not available in the exported forecast file.</div>
            <div class="card-text">
                forecast_data.csv contains Product ID, Week_Start and Forecast_Units.
                Therefore this page cannot calculate an Actual-vs-Forecast chart without
                inventing data. The project's model evaluation is shown in ML Performance.
            </div>
        </div>
        """)
        st.dataframe(
            forecast_data.sort_values(["Product ID", "Week_Start"]),
            use_container_width=True,
            hide_index=True,
        )
    else:
        selected_product = st.selectbox(
            "Select Product",
            sorted(forecast_data["Product ID"].astype(str).unique())
        )
        compare = forecast_data[
            forecast_data["Product ID"].astype(str) == selected_product
        ].sort_values("Week_Start")

        long_df = compare[["Week_Start", "Forecast_Units", actual_col]].rename(
            columns={"Forecast_Units": "Forecast", actual_col: "Actual"}
        ).melt(
            id_vars="Week_Start",
            var_name="Series",
            value_name="Units"
        )

        fig = px.line(
            long_df,
            x="Week_Start",
            y="Units",
            color="Series",
            markers=True,
            title=f"Forecast vs Actual — {selected_product}",
        )
        plot_theme(fig, 420)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# RECOMMENDATIONS
# ============================================================
elif page == "💡 Recommendations":
    hero(
        "Recommendations",
        "Inventory Action Center",
        "Review the recommended action generated from the project's inventory-risk output."
    )

    recommendations = final_output[
        [
            "Product ID", "Weeks_of_Supply", "Inventory_Position",
            "Average_Weekly_Demand", "Risk_Category", "Recommended_Action"
        ]
    ].sort_values("Weeks_of_Supply")

    action_counts = (
        recommendations["Recommended_Action"]
        .astype(str)
        .value_counts()
        .rename_axis("Recommended_Action")
        .reset_index(name="Product_Count")
    )

    kpi_row([
        ("PRODUCTS", f"{total_products}", "Products with recommendations"),
        ("CRITICAL", f"{critical_products}", "Current risk classification"),
        ("LOWEST WOS", f"{recommendations['Weeks_of_Supply'].min():.2f}", "Lowest coverage"),
        ("ACTIONS", f"{len(action_counts)}", "Distinct recommended actions"),
    ])

    st.markdown("")
    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            action_counts,
            x="Recommended_Action",
            y="Product_Count",
            text="Product_Count",
            title="Recommended Action Distribution",
        )
        plot_theme(fig, 360)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.bar(
            recommendations.head(10).sort_values("Weeks_of_Supply"),
            x="Weeks_of_Supply",
            y="Product ID",
            orientation="h",
            text_auto=".2f",
            title="Products Requiring Earliest Review",
        )
        plot_theme(fig, 360)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(recommendations, use_container_width=True, hide_index=True)


# ============================================================
# PRODUCT 360
# ============================================================
elif page == "🔎 Product 360":
    hero(
        "Product 360",
        "Complete Product-Level View",
        "Inspect forecast, inventory, coverage, risk and recommended action for one product."
    )

    selected_product = st.selectbox(
        "Select Product",
        sorted(final_output["Product ID"].astype(str).unique())
    )

    row = final_output[
        final_output["Product ID"].astype(str) == selected_product
    ].iloc[0]

    kpi_row([
        ("8-WEEK FORECAST", f"{row['Forecast_8_Weeks']:,.0f}", "Predicted demand"),
        ("INVENTORY POSITION", f"{row['Inventory_Position']:,.0f}", "On-hand + on-order"),
        ("WOS", f"{row['Weeks_of_Supply']:.2f}", "Weeks of supply"),
        ("RISK", f"{row['Risk_Category']}", "Project classification"),
    ])

    st.markdown("")
    c1, c2 = st.columns(2)

    with c1:
        html(f"""
        <div class="panel">
            <div class="card-title">📦 Inventory</div>
            <div class="card-text">
                On-hand units: <b>{row['On_Hand_Units']:,.0f}</b><br>
                On-order units: <b>{row['On_Order_Units']:,.0f}</b><br>
                Inventory position: <b>{row['Inventory_Position']:,.0f}</b>
            </div>
        </div>
        """)

    with c2:
        html(f"""
        <div class="panel">
            <div class="card-title">🚨 Risk & Action</div>
            <div class="card-text">
                Risk category: <b>{row['Risk_Category']}</b><br>
                Weeks of supply: <b>{row['Weeks_of_Supply']:.2f}</b><br>
                Recommended action: <b>{row['Recommended_Action']}</b>
            </div>
        </div>
        """)

    product_forecast = forecast_data[
        forecast_data["Product ID"].astype(str) == selected_product
    ].sort_values("Week_Start")

    if not product_forecast.empty:
        fig = px.line(
            product_forecast,
            x="Week_Start",
            y="Forecast_Units",
            markers=True,
            title=f"8-Week Forecast — {selected_product}",
        )
        plot_theme(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        row.to_frame("Value").reset_index().rename(columns={"index": "Metric"}),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# ML PERFORMANCE
# ============================================================
elif page == "🧠 ML Performance":
    hero(
        "ML Performance",
        "Forecasting Model Comparison",
        "Compare the evaluated models using WAPE and identify the selected model."
    )

    performance = model_comparison.sort_values("WAPE", ascending=True).copy()

    kpi_row([
        ("BEST MODEL", f"{best_model}", "Lowest WAPE"),
        ("BEST WAPE", f"{best_wape:.2f}%", "Evaluation metric"),
        ("MODELS", f"{len(performance)}", "Evaluated models"),
        ("FORECAST HORIZON", "8 Weeks", "Project horizon"),
    ])

    st.markdown("")
    fig = px.bar(
        performance,
        x="Model",
        y="WAPE",
        text="WAPE",
        title="Model Performance — WAPE",
    )
    plot_theme(fig, 400)
    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(performance, use_container_width=True, hide_index=True)

    html(f"""
    <div class="good">
        <div class="card-title">🏆 Selected Model</div>
        <div class="card-text">
            <b style="color:#86efac;font-size:18px;">{best_model}</b>
            achieved the lowest WAPE of <b>{best_wape:.2f}%</b> among the supplied model results.
        </div>
    </div>
    """)




st.markdown("""
<div style="position:fixed;bottom:8px;right:12px;z-index:9999;
color:#536a83;font-size:9px;">FORESIGHT AI • BUILD v10</div>
""", unsafe_allow_html=True)

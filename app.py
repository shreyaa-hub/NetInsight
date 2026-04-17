import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns   # ✅ moved here
from simulation import simulate
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.platypus import KeepTogether
import io

st.set_page_config(page_title="NetInsight Dashboard", layout="wide")

st.title("📡 NetInsight: Network Performance Analysis")
  
# Multi-run averaging
@st.cache_data
def run_multiple(traffic, runs, cycles, queue_size, process_rate, use_priority):
    delays, throughputs, losses, jitters = [], [], [], []

    for _ in range(runs):
        d, t, l, j = simulate(traffic, cycles, queue_size, process_rate, use_priority)
        delays.append(d)
        throughputs.append(t)
        losses.append(l)
        jitters.append(j)

    return (
        sum(delays)/len(delays),
        sum(throughputs)/len(throughputs),
        sum(losses)/len(losses),
        sum(jitters)/len(jitters)
    )

def generate_pdf(df):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    from reportlab.lib.enums import TA_CENTER

    title_style = styles['Title']
    title_style.alignment = TA_CENTER
    content = []
    
    # Paragraph
    content.append(Paragraph("Network Performance Analysis System under Varying Traffic Conditions", title_style))
    content.append(Spacer(1, 10))

    content.append(Paragraph(
        """
        This report presents a comprehensive analysis of network performance under varying traffic conditions.
        The simulation evaluates key performance metrics including delay, throughput, packet loss, and jitter.
        The system models real-world network behavior using stochastic traffic generation and queue-based processing.
        Different traffic intensities (low, medium, and high) are simulated to observe congestion effects and system performance.
        """,
        styles['Normal']
    ))

    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Objectives:</b>", styles['Normal']))
    content.append(Spacer(1, 5))

    content.append(Paragraph("• Evaluate how network delay increases with traffic load", styles['Normal']))
    content.append(Paragraph("• Understand throughput behavior under different conditions", styles['Normal']))
    content.append(Paragraph("• Measure packet loss as an indicator of congestion", styles['Normal']))
    content.append(Paragraph("• Analyze jitter to assess delay variability", styles['Normal']))

    content.append(Spacer(1, 10))

    content.append(Paragraph(
        "The results provide insights into network stability, efficiency, and limitations under varying load conditions.",
        styles['Normal']
    ))

    # 🔹 RESULTS SECTION
    content.append(Paragraph("Results Summary", styles['Heading2']))
    content.append(Spacer(1, 10))

    for index, row in df.iterrows():
        text = f"""
        <b>Traffic:</b> {row['Traffic']}<br/>
        Delay: {row['Delay (ms)']:.2f} ms<br/>
        Throughput: {row['Throughput']:.2f}<br/>
        Packet Loss: {row['Packet Loss %']:.2f}%<br/>
        Jitter: {row['Jitter']:.4f}<br/><br/>
        """
        content.append(Paragraph(text, styles['Normal']))
        content.append(Spacer(1, 10))

    # 🔹 GRAPH 1: Delay
    fig, ax = plt.subplots()
    ax.bar(df["Traffic"], df["Delay (ms)"])
    ax.set_title("Delay (ms)")

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close(fig)
    img_buffer.seek(0)

    # ✅ KEEP TITLE + GRAPH TOGETHER
    delay_section = [
        Paragraph("Delay Analysis", styles['Heading2']),
        Spacer(1, 4),
        Image(img_buffer, width=400, height=250),
        Spacer(1, 20)
    ]

    content.append(KeepTogether(delay_section))

    # 🔹 GRAPH 2: Packet Loss
    fig2, ax2 = plt.subplots()
    ax2.bar(df["Traffic"], df["Packet Loss %"])
    ax2.set_title("Packet Loss %")
    img_buffer2 = io.BytesIO()
    plt.savefig(img_buffer2, format='png')
    plt.close(fig2)
    img_buffer2.seek(0)

    content.append(Paragraph("Packet Loss Analysis", styles['Heading2']))
    content.append(Spacer(1, 10))
    content.append(Image(img_buffer2, width=400, height=250))
    content.append(Spacer(1, 20))

    # 🔹 CONCLUSION
    content.append(Paragraph("Conclusion", styles['Heading2']))
    content.append(Spacer(1, 10))

    content.append(Paragraph(
        "As traffic increases, delay and packet loss increase due to congestion, while throughput stabilizes. This demonstrates typical network performance degradation under heavy load.",
        styles['Normal']
    ))

    doc.build(content)

    buffer.seek(0)
    return buffer

# Sidebar
st.sidebar.header("Configuration")

adaptive = st.sidebar.checkbox("Enable Adaptive Network")

queue_size = st.sidebar.slider("Queue Size", 5, 50, 10)
process_rate = st.sidebar.slider("Processing Rate", 1, 10, 2)
runs = st.sidebar.slider("Number of Runs (Averaging)", 1, 10, 3)
cycles = st.sidebar.slider("Simulation Cycles", 10, 100, 30)

mode = st.sidebar.selectbox("Network Mode", ["Normal", "High Congestion"])
algo = st.sidebar.selectbox("Queue Algorithm", ["Priority", "FIFO"])

dark_mode = st.sidebar.toggle("🌙 Dark Mode")

use_priority = True if algo == "Priority" else False

if mode == "High Congestion":
    queue_size = 5
    process_rate = 1

if adaptive:
    if mode == "High Congestion":
        process_rate += 2

traffic_levels = ["low", "medium", "high"]

if dark_mode:
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

# Run simulation
results = []
for level in traffic_levels:
    delay, throughput, loss, jitter = run_multiple(
        level, runs, cycles, queue_size, process_rate, use_priority
    )

    results.append({
        "Traffic": level.capitalize(),
        "Delay (ms)": delay * 1000,
        "Throughput": throughput,
        "Packet Loss %": loss,
        "Jitter": jitter
    })

df = pd.DataFrame(results)

# =========================
# 🧭 TABS
# =========================
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Graphs", "🧠 Insights"])

# =========================
# 📊 OVERVIEW TAB
# =========================
with tab1:
    st.subheader("Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Avg Delay (ms)", f"{df['Delay (ms)'].mean():.2f}")
    col2.metric("Avg Throughput", f"{df['Throughput'].mean():.2f}")
    col3.metric("Avg Packet Loss %", f"{df['Packet Loss %'].mean():.2f}")
    col4.metric("Avg Jitter", f"{df['Jitter'].mean():.4f}")

    st.subheader("Performance Table")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')

    col1, col2 = st.columns(2)

    with col1:
        pdf = generate_pdf(df)
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf,
            file_name="network_report.pdf",
            mime="application/pdf"
        )

    with col2:
        st.download_button(
            label="📊 Download Results CSV",
            data=csv,
            file_name="network_results.csv"
        )

# =========================
# 📈 GRAPHS TAB
# =========================
with tab2:
    st.subheader("Comparative Analysis")

    col1, col2 = st.columns(2)

    # Bar Chart
    fig1, ax1 = plt.subplots()
    ax1.bar(df["Traffic"], df["Packet Loss %"])
    ax1.set_title("Packet Loss Comparison")
    col1.pyplot(fig1)

    # Line Chart
    fig2, ax2 = plt.subplots()
    ax2.plot(df["Traffic"], df["Delay (ms)"], marker='o')
    ax2.set_title("Delay Trend")
    col2.pyplot(fig2)

    col3, col4 = st.columns(2)

    # 🔹 Throughput (LEFT)
    with col3:
        fig3, ax3 = plt.subplots()
        ax3.plot(df["Traffic"], df["Throughput"], marker='o')
        ax3.set_title("Throughput Trend")
        st.pyplot(fig3)

    # 🔹 Heatmap (RIGHT)
    with col4:
        st.subheader("Heatmap Analysis")

        heat_data = df.set_index("Traffic")[["Delay (ms)", "Throughput", "Packet Loss %"]]

        fig, ax = plt.subplots()
        sns.heatmap(heat_data, annot=True, cmap="coolwarm", ax=ax)

        st.pyplot(fig)

# =========================
# 🧠 INSIGHTS TAB
# =========================
with tab3:
    st.subheader("🚨 Congestion Detection")

    if df["Packet Loss %"].max() > 30:
        st.error("⚠️ High congestion detected in network")

    elif df["Packet Loss %"].max() > 10:
        st.warning("⚠️ Moderate congestion detected")

    else:
        st.success("✅ Network operating normally")

    st.subheader("Observations")

    st.markdown("""
    ### Key Findings:
    - Delay increases as traffic intensity rises due to queue buildup.
    - Throughput initially improves but stabilizes at higher traffic loads.
    - Packet loss increases sharply under high traffic, indicating congestion.
    
    ### Interpretation:
    - The system demonstrates classic congestion behavior in packet-switched networks.
    - Network capacity limits are reached under heavy load conditions.
    """)

    # Comparison over time
    st.subheader("Traffic vs Cycles Impact")

    cycle_range = list(range(10, cycles + 1, 10))

    delay_trend = []
    for c in cycle_range:
        d, _, _, _ = simulate("high", c)
        delay_trend.append(d * 1000)

    col_center = st.columns([1, 2, 1])  # left space | graph | right space

    with col_center[1]:
        fig4, ax4 = plt.subplots(figsize=(6,4))  # ✅ smaller size

        ax4.plot(cycle_range, delay_trend, marker='o')
        ax4.set_title("Delay vs Simulation Cycles (High Traffic)")
        ax4.set_xlabel("Cycles")
        ax4.set_ylabel("Delay (ms)")

        st.pyplot(fig4)
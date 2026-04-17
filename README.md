# 📡 NetInsight: Network Performance Analysis System

## 📌 Overview
NetInsight is a simulation-based network performance analysis system designed to study how packet-switched networks behave under varying traffic conditions. It models real-world network behavior using probabilistic packet generation and queue-based processing.

The system evaluates key performance metrics such as **delay, throughput, packet loss, and jitter**, and presents results through an interactive dashboard and downloadable reports.

---

## 🎯 Objectives
- Analyze network performance under low, medium, and high traffic conditions  
- Study the impact of congestion on packet loss and delay  
- Evaluate throughput limitations and system capacity  
- Measure jitter to understand delay variability  
- Compare FIFO and Priority-based scheduling  
- Provide visual insights using graphs and heatmaps  

---

## ⚙️ Features
- 📊 Interactive dashboard using Streamlit  
- 📈 Graphs: Packet Loss, Delay, Throughput  
- 🔥 Heatmap for comparative analysis  
- 📄 PDF report generation  
- 📥 CSV export option  
- ⚙️ Configurable simulation parameters  
- 🚦 Network modes (Normal / High Congestion)  
- 🔄 Adaptive network handling  
- 🎯 FIFO vs Priority queue scheduling  
- 🌙 Dark mode UI  

---

## 🧠 Technologies Used
- Python  
- Streamlit  
- NumPy  
- Pandas  
- Matplotlib  
- Seaborn  
- ReportLab  

---

## 🏗️ Project Structure
```
NetInsight/
│── app.py              # Streamlit dashboard
│── simulation.py       # Core simulation logic
│── metrics.py          # Performance calculations
│── results.csv         # Generated results
│── README.md           # Project documentation
```

---

## 🔄 How It Works
1. User selects simulation parameters from the dashboard  
2. Packets are generated using Poisson distribution  
3. Packets are queued and processed based on system capacity  
4. Metrics are calculated:
   - Delay  
   - Throughput  
   - Packet Loss  
   - Jitter  
5. Results are visualized using graphs and heatmaps  
6. Reports can be downloaded as PDF or CSV  

---

## 📊 Key Insights
- Packet loss increases sharply under high traffic due to congestion  
- Delay increases gradually due to queue buildup  
- Throughput saturates at system processing capacity  
- Jitter increases with instability in network conditions  

---

## ▶️ How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

---

## 📸 Screenshots
(Add your screenshots here)

---

## 🎓 Conclusion
This project demonstrates how network performance degrades under increasing traffic load and provides insights into congestion behavior, system limits, and optimization strategies.

---

## 🚀 Future Improvements
- Add real-time network simulation  
- Include multiple routers and network topology  
- Implement TCP-like retransmission  
- Deploy as a web application  

---

## 📬 Author
Shreya Singh
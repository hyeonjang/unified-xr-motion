# Latency Analysis for OXRAvatarForge

This directory contains latency measurement data and analysis scripts for the network offloading performance evaluation.

## Files

### Data Files
- `TickLatencyNone_*.csv` - Client-only (no offloading) latency measurements
- `TickLatencyOffload_*.csv` - Server-offload latency measurements  
- `*_histogram_*.csv` - Pre-computed histogram data
- `performance_report_*.txt` - Generated performance reports
- `academic_table_*.txt` - LaTeX table format for papers

### Analysis Scripts
- `plot_latency_analysis.py` - Comprehensive analysis with publication-quality plots
- `quick_plot.py` - Simple plotting for immediate visualization
- `requirements.txt` - Python dependencies

## Usage

### Quick Analysis
```bash
cd paper/data/latency
python quick_plot.py
```

### Full Analysis (Publication Quality)
```bash
cd paper/data/latency
pip install -r requirements.txt
python plot_latency_analysis.py
```

## Generated Figures

The scripts generate the following plots:

1. **Latency Time Series** - Shows latency over time for each configuration
2. **Histogram Comparison** - Probability density comparison between configurations  
3. **Box Plot Comparison** - Statistical distribution comparison
4. **CDF Comparison** - Cumulative distribution functions
5. **LaTeX Table** - Ready-to-use table for academic papers

## Data Format

### Time Series CSV Format
```
Timestamp,LatencyMs,Tick,Configuration
5.629,13.154,246,Oculus Quest_Android
```

### Histogram CSV Format  
```
BinStart,BinEnd,BinCenter,Count,Frequency
7.793,11.239,9.516,214,0.061283
```

## Key Metrics

The analysis calculates:
- **p50 (median)**: 50th percentile latency
- **p95**: 95th percentile latency  
- **p99**: 99th percentile latency
- **Mean/Std**: Average and standard deviation
- **Min/Max**: Range of measured values

## Academic Paper Integration

Use the generated LaTeX table and high-resolution PDF figures directly in your academic paper. The analysis follows standard performance evaluation practices for real-time systems.
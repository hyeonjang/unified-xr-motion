#!/usr/bin/env python3
"""
Quick plotting script for latency data visualization.
Simple script for immediate visualization of network offloading results.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from pathlib import Path

def load_tick_data(tick_type, crop_initial_seconds=0.0, crop_latency_max=200):
    """Load data from a specific tick type folder."""
    folder_path = Path(tick_type)
    if not folder_path.exists():
        print(f"Folder {tick_type} not found, checking current directory...")
        csv_files = glob.glob(f"*{tick_type}*_Android_*.csv")
    else:
        csv_files = glob.glob(str(folder_path / "*_Android_*.csv"))
    
    csv_files = [f for f in csv_files if "histogram" not in f]
    
    data = []
    for file_path in csv_files:
        try:
            df = pd.read_csv(file_path)
            filename = Path(file_path).stem
            
            # Determine configuration
            if "None" in filename:
                config = "Client-only"
            elif "Offload" in filename:
                config = "Server-offload"
            else:
                continue
            
            # Get original data
            original_latencies = df['LatencyMs'].values
            original_timestamps = df['Timestamp'].values if 'Timestamp' in df.columns else np.arange(len(original_latencies))
            original_count = len(original_latencies)
            
            # Crop initial unstable samples based on time
            if 'Timestamp' in df.columns and crop_initial_seconds is not None:
                min_timestamp = np.min(original_timestamps)
                crop_threshold = min_timestamp + crop_initial_seconds
                time_mask = original_timestamps >= crop_threshold
                
                latencies = original_latencies[time_mask]
                timestamps = original_timestamps[time_mask]
            else:
                latencies = original_latencies
                timestamps = original_timestamps
            
            # Crop extreme latency outliers
            if crop_latency_max is not None:
                outlier_mask = latencies <= crop_latency_max
                outlier_removed = len(latencies) - np.sum(outlier_mask)
                latencies = latencies[outlier_mask]
                timestamps = timestamps[outlier_mask]
            
            data.append({
                'config': config,
                'latencies': latencies,
                'timestamps': timestamps,
                'filename': filename,
                'original_count': original_count,
                'final_count': len(latencies)
            })
            
            print(f"  {tick_type} - {config}: {len(latencies)} samples (from {original_count})")
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    return data

def load_all_device_data():
    """Load data from all devices."""
    # Configuration for cropping initial unstable samples
    CROP_INITIAL_SECONDS = 10.0  # Remove first 10 seconds of data (startup/warmup period)
    CROP_LATENCY_MAX = 200       # Maximum allowed latency (ms) to remove extreme outliers
    
    all_data = {}
    
    # Load Quest data
    print("Loading Quest data...")
    quest_data = load_tick_data('quest', CROP_INITIAL_SECONDS, CROP_LATENCY_MAX)
    if quest_data:
        all_data['Quest'] = quest_data
    
    # Load XREAL data
    print("Loading XREAL data...")
    xreal_data = load_tick_data('xreal', CROP_INITIAL_SECONDS, CROP_LATENCY_MAX)
    if xreal_data:
        all_data['XREAL'] = xreal_data
    
    return all_data

def analyze_by_plot_type():
    """Analyze and create plots organized by plot type (time series, histogram) rather than device."""
    
    # Set basic plotting style
    plt.style.use('seaborn-v0_8' if hasattr(plt.style, 'available') and 'seaborn-v0_8' in plt.style.available else 'default')
    plt.rcParams.update({
        'font.size': 16,           # Larger base font size
        'axes.titlesize': 18,      # Larger title size
        'axes.labelsize': 16,      # Larger axis label size
        'xtick.labelsize': 14,     # Larger x-tick labels
        'ytick.labelsize': 14,     # Larger y-tick labels
        'legend.fontsize': 14,     # Larger legend font
        'lines.linewidth': 2       # Thicker lines for visibility
    })
    
    # Load all device data
    all_device_data = load_all_device_data()
    
    if not all_device_data:
        print("No data found for any devices!")
        return
    
    # Define colors for devices and configurations
    device_colors = {'Quest': {'Client-only': '#1f77b4', 'Server-offload': '#ff7f0e'}, 
                    'XREAL': {'Client-only': '#2ca02c', 'Server-offload': '#d62728'}}
    
    # Create time series plot
    create_time_series_plot(all_device_data, device_colors)
    
    # Create histogram plot
    create_histogram_plot(all_device_data, device_colors)
    
    # Print statistics for all devices
    print_all_statistics(all_device_data)

def create_time_series_plot(all_device_data, device_colors):
    """Create time series plots with both devices side by side."""
    output_path = Path("../")
    output_path.mkdir(exist_ok=True)
    
    # Create figure with side-by-side subplots
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    device_names = list(all_device_data.keys())
    
    for i, (device_name, device_data) in enumerate(all_device_data.items()):
        ax = axes[i] if len(device_names) > 1 else axes
        
        for data in device_data:
            config = data['config']
            latencies = data['latencies']
            timestamps = data['timestamps']
            color = device_colors[device_name][config]
            
            # Time series plot for this device
            ax.plot(timestamps, latencies, color=color, alpha=0.7, 
                   label=config, linewidth=2)
        
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Latency (ms)')
        ax.set_title(f'{device_name} Interaction Latency Over Time')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # Handle case where only one device exists
    if len(device_names) == 1:
        axes[1].set_visible(False)
    
    plt.tight_layout()
    
    # Save combined figure
    filename = "figX-time-series-comparison.pdf"
    plt.savefig(output_path / filename, bbox_inches='tight')
    print(f"\nTime series comparison figure saved to: {output_path}/{filename}")
    
    plt.show()

def create_histogram_plot(all_device_data, device_colors):
    """Create histogram plots with both devices side by side."""
    output_path = Path("../")
    output_path.mkdir(exist_ok=True)
    
    # Create figure with side-by-side subplots
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    device_names = list(all_device_data.keys())
    
    for i, (device_name, device_data) in enumerate(all_device_data.items()):
        ax = axes[i] if len(device_names) > 1 else axes
        
        for data in device_data:
            config = data['config']
            latencies = data['latencies']
            color = device_colors[device_name][config]
            
            # Histogram for this device
            ax.hist(latencies, bins=50, alpha=0.6, color=color, 
                   label=config, density=False, edgecolor='black', linewidth=0.5)
        
        ax.set_xlabel('Latency (ms)')
        ax.set_ylabel('Frequency')
        ax.set_title(f'{device_name} Interaction Latency Distribution')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # Handle case where only one device exists
    if len(device_names) == 1:
        axes[1].set_visible(False)
    
    plt.tight_layout()
    
    # Save combined figure
    filename = "figX-histogram-comparison.pdf"
    plt.savefig(output_path / filename, bbox_inches='tight')
    print(f"\nHistogram comparison figure saved to: {output_path}/{filename}")
    
    plt.show()

def print_all_statistics(all_device_data):
    """Print statistics for all devices."""
    for device_name, device_data in all_device_data.items():
        print_tick_statistics(device_data, f"{device_name} Interaction Latency")

def quick_analysis():
    """Quick analysis and plotting - now organized by plot type."""
    analyze_by_plot_type()

def plot_tick_data(tick_data, axes, tick_name, config_colors):
    """Plot time series, histogram, and box plot for a tick type."""
    ax_time, ax_hist = axes
    
    if not tick_data:
        # Handle empty data case
        ax_time.text(0.5, 0.5, f'No {tick_name} data', ha='center', va='center', transform=ax_time.transAxes)
        ax_hist.text(0.5, 0.5, f'No {tick_name} data', ha='center', va='center', transform=ax_hist.transAxes)
        return
    
    box_data = []
    box_labels = []
    
    for data in tick_data:
        config = data['config']
        latencies = data['latencies']
        timestamps = data['timestamps']
        color = config_colors.get(config, '#888888')
        
        # Time series plot
        ax_time.plot(timestamps, latencies, color=color, alpha=0.7, 
                    label=config, linewidth=2)
        
        # Histogram with normalized count instead of density for better readability
        ax_hist.hist(latencies, bins=50, alpha=0.6, color=color, 
                    label=config, density=False, edgecolor='black', linewidth=0.5)
        
        # Collect data for box plot
        box_data.append(latencies)
        box_labels.append(config)
    
    # Configure time series plot
    ax_time.set_xlabel('Time (seconds)')
    ax_time.set_ylabel('Latency (ms)')
    ax_time.set_title(f'{tick_name} - Latency Over Time')
    ax_time.legend()
    ax_time.grid(True, alpha=0.3)
    
    # Configure histogram
    ax_hist.set_xlabel('Latency (ms)')
    ax_hist.set_ylabel('Frequency')
    ax_hist.set_title(f'{tick_name} - Distribution')
    ax_hist.legend()
    ax_hist.grid(True, alpha=0.3)

def print_tick_statistics(tick_data, tick_name):
    """Print detailed statistics for a tick type."""
    print(f"\n=== {tick_name} Statistics ===")
    
    if not tick_data:
        print(f"No {tick_name} data available")
        return
    
    for data in tick_data:
        config = data['config']
        latencies = data['latencies']
        
        if len(latencies) == 0:
            continue
            
        p50 = np.percentile(latencies, 50)
        p95 = np.percentile(latencies, 95)
        p99 = np.percentile(latencies, 99)
        mean_val = np.mean(latencies)
        std_val = np.std(latencies)
        
        print(f"\n{config}:")
        print(f"  Samples: {len(latencies)} (from {data['original_count']} original)")
        print(f"  Mean: {mean_val:.1f}ms ± {std_val:.1f}ms")
        print(f"  p50: {p50:.1f}ms")
        print(f"  p95: {p95:.1f}ms") 
        print(f"  p99: {p99:.1f}ms")
        print(f"  Range: {np.min(latencies):.1f}ms - {np.max(latencies):.1f}ms")

if __name__ == "__main__":
    import sys
    
    # Check for command line arguments to run specific analysis
    if len(sys.argv) > 1:
        analysis_type = sys.argv[1].lower()
        if analysis_type == 'timeseries':
            # Only create time series plot
            all_device_data = load_all_device_data()
            if all_device_data:
                device_colors = {'Quest': {'Client-only': '#1f77b4', 'Server-offload': '#ff7f0e'}, 
                               'XREAL': {'Client-only': '#2ca02c', 'Server-offload': '#d62728'}}
                create_time_series_plot(all_device_data, device_colors)
        elif analysis_type == 'histogram':
            # Only create histogram plot
            all_device_data = load_all_device_data()
            if all_device_data:
                device_colors = {'Quest': {'Client-only': '#1f77b4', 'Server-offload': '#ff7f0e'}, 
                               'XREAL': {'Client-only': '#2ca02c', 'Server-offload': '#d62728'}}
                create_histogram_plot(all_device_data, device_colors)
        elif analysis_type == 'all':
            quick_analysis()
        else:
            print("Usage: python quick_plot.py [timeseries|histogram|all]")
            print("  timeseries - Create only time series plot comparing all devices")
            print("  histogram  - Create only histogram plot comparing all devices") 
            print("  all        - Create both plots (default)")
            sys.exit(1)
    else:
        # Default behavior - create all plots organized by type
        quick_analysis()
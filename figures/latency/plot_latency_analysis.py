#!/usr/bin/env python3
"""
Latency Analysis Plotting Script for OXRAvatarForge Academic Paper
Generates publication-quality figures for network offloading performance analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import glob
import re
from typing import Dict, List, Tuple

# Set publication-quality style
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 12,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14,
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'text.usetex': False,  # Set to True if LaTeX is available
    'figure.figsize': (8, 6),
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1
})

class LatencyAnalyzer:
    def __init__(self, data_dir: str = ".", crop_initial_seconds: float = 10.0, 
                 crop_latency_max: float = 200.0):
        self.data_dir = Path(data_dir)
        self.figures_dir = self.data_dir / "figures"
        self.figures_dir.mkdir(exist_ok=True)
        
        # Cropping configuration
        self.crop_initial_seconds = crop_initial_seconds
        self.crop_latency_max = crop_latency_max
        
        # Tick type folders
        self.tick_folders = {
            'iltick': 'Interaction Tick',
            'systemtick': 'System Tick'
        }
        
    def load_time_series_data(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """Load time series CSV files organized by tick type and configuration."""
        data = {}
        
        for tick_folder, tick_name in self.tick_folders.items():
            data[tick_folder] = {}
            folder_path = self.data_dir / tick_folder
            
            # Try tick folder first, then fallback to current directory
            if folder_path.exists():
                csv_files = glob.glob(str(folder_path / "*_Android_*.csv"))
            else:
                print(f"Folder {tick_folder} not found, checking current directory...")
                csv_files = glob.glob(str(self.data_dir / f"*{tick_folder}*_Android_*.csv"))
            
            csv_files = [f for f in csv_files if "histogram" not in f]
            
            for file_path in csv_files:
                filename = Path(file_path).stem
                
                # Extract configuration from filename
                if "None" in filename:
                    config = "Client-only"
                elif "Offload" in filename:
                    config = "Server-offload"
                else:
                    continue
                    
                try:
                    df = pd.read_csv(file_path)
                    original_count = len(df)
                    
                    # Apply time-based cropping to remove initial unstable samples
                    if 'Timestamp' in df.columns and self.crop_initial_seconds > 0:
                        min_timestamp = df['Timestamp'].min()
                        crop_threshold = min_timestamp + self.crop_initial_seconds
                        df = df[df['Timestamp'] >= crop_threshold]
                        print(f"  {tick_name} time cropping: {original_count} -> {len(df)} samples")
                    
                    # Apply latency outlier cropping
                    if 'LatencyMs' in df.columns and self.crop_latency_max > 0:
                        outlier_count = len(df)
                        df = df[df['LatencyMs'] <= self.crop_latency_max]
                        outlier_removed = outlier_count - len(df)
                        if outlier_removed > 0:
                            print(f"  {tick_name} outlier cropping: removed {outlier_removed} samples > {self.crop_latency_max}ms")
                    
                    df['Configuration'] = config
                    df['Filename'] = filename
                    df['TickType'] = tick_name
                    data[tick_folder][f"{config}_{filename}"] = df
                    print(f"Loaded {tick_name} - {config}: {len(df)} samples (cropped from {original_count})")
                    
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
                    
        return data
    
    def load_histogram_data(self) -> Dict[str, pd.DataFrame]:
        """Load histogram data files."""
        data = {}
        
        hist_files = glob.glob(str(self.data_dir / "*histogram*.csv"))
        
        for file_path in hist_files:
            filename = Path(file_path).stem
            
            # Extract configuration
            if "None" in filename:
                config = "Client-only"
            elif "Offload" in filename:
                config = "Server-offload"
            else:
                config = "Unknown"
                
            try:
                df = pd.read_csv(file_path)
                df['Configuration'] = config
                data[filename] = df
                print(f"Loaded histogram data from {filename}")
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                
        return data
    
    def calculate_percentiles(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Calculate percentiles for each configuration."""
        results = []
        
        for filename, df in data.items():
            if 'LatencyMs' in df.columns:
                latencies = df['LatencyMs'].values
                results.append({
                    'Configuration': df['Configuration'].iloc[0],
                    'Filename': filename,
                    'Count': len(latencies),
                    'Mean': np.mean(latencies),
                    'Std': np.std(latencies),
                    'Min': np.min(latencies),
                    'Max': np.max(latencies),
                    'p50': np.percentile(latencies, 50),
                    'p95': np.percentile(latencies, 95),
                    'p99': np.percentile(latencies, 99)
                })
        
        return pd.DataFrame(results)
    
    def plot_comparison_histogram(self, data: Dict[str, pd.DataFrame]):
        """Create comparison histogram of latency distributions."""
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        
        colors = ['#2E86C1', '#E74C3C', '#28B463', '#F39C12']
        alpha = 0.7
        
        all_latencies = []
        labels = []
        
        for i, (filename, df) in enumerate(data.items()):
            if 'LatencyMs' in df.columns:
                latencies = df['LatencyMs'].values
                config = df['Configuration'].iloc[0]
                
                all_latencies.append(latencies)
                labels.append(f"{config} (n={len(latencies)})")
                
                # Plot histogram
                ax.hist(latencies, bins=50, alpha=alpha, color=colors[i % len(colors)], 
                       label=labels[-1], density=True, edgecolor='black', linewidth=0.5)
        
        ax.set_xlabel('Latency (ms)')
        ax.set_ylabel('Probability Density')
        ax.set_title('Latency Distribution Comparison')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'latency_histogram_comparison.png')
        plt.savefig(self.figures_dir / 'latency_histogram_comparison.pdf')
        print(f"Saved histogram comparison to {self.figures_dir}")
        
    def plot_time_series(self, data: Dict[str, pd.DataFrame]):
        """Plot latency over time for each configuration."""
        fig, axes = plt.subplots(len(data), 1, figsize=(12, 4 * len(data)), sharex=True)
        if len(data) == 1:
            axes = [axes]
            
        colors = ['#2E86C1', '#E74C3C', '#28B463', '#F39C12']
        
        for i, (filename, df) in enumerate(data.items()):
            if 'LatencyMs' in df.columns and 'Timestamp' in df.columns:
                ax = axes[i]
                config = df['Configuration'].iloc[0]
                
                # Plot time series
                ax.plot(df['Timestamp'], df['LatencyMs'], 
                       color=colors[i % len(colors)], alpha=0.7, linewidth=0.8)
                
                # Add rolling mean
                window_size = min(100, len(df) // 10)
                if window_size > 1:
                    rolling_mean = df['LatencyMs'].rolling(window=window_size, center=True).mean()
                    ax.plot(df['Timestamp'], rolling_mean, 
                           color='red', linewidth=2, label=f'Rolling Mean ({window_size} samples)')
                
                ax.set_ylabel('Latency (ms)')
                ax.set_title(f'{config} - Latency Over Time')
                ax.grid(True, alpha=0.3)
                ax.legend()
        
        axes[-1].set_xlabel('Time (seconds)')
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'latency_time_series.png')
        plt.savefig(self.figures_dir / 'latency_time_series.pdf')
        print(f"Saved time series plot to {self.figures_dir}")
        
    def plot_box_comparison(self, data: Dict[str, pd.DataFrame]):
        """Create box plot comparison of configurations."""
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        
        all_data = []
        labels = []
        
        for filename, df in data.items():
            if 'LatencyMs' in df.columns:
                config = df['Configuration'].iloc[0]
                all_data.append(df['LatencyMs'].values)
                labels.append(config)
        
        if all_data:
            box_plot = ax.boxplot(all_data, labels=labels, patch_artist=True,
                                 boxprops=dict(facecolor='lightblue', alpha=0.7),
                                 medianprops=dict(color='red', linewidth=2),
                                 whiskerprops=dict(color='black'),
                                 capprops=dict(color='black'),
                                 flierprops=dict(marker='o', markersize=4, alpha=0.5))
            
            ax.set_ylabel('Latency (ms)')
            ax.set_title('Latency Distribution Comparison (Box Plot)')
            ax.grid(True, alpha=0.3)
            
            # Add statistical annotations
            for i, data_subset in enumerate(all_data):
                p50 = np.percentile(data_subset, 50)
                p99 = np.percentile(data_subset, 99)
                ax.text(i + 1, ax.get_ylim()[1] * 0.9, 
                       f'p50: {p50:.1f}ms\np99: {p99:.1f}ms',
                       ha='center', va='top', fontsize=9,
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'latency_box_comparison.png')
        plt.savefig(self.figures_dir / 'latency_box_comparison.pdf')
        print(f"Saved box plot comparison to {self.figures_dir}")
        
    def plot_cdf_comparison(self, data: Dict[str, pd.DataFrame]):
        """Plot Cumulative Distribution Function comparison."""
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        
        colors = ['#2E86C1', '#E74C3C', '#28B463', '#F39C12']
        
        for i, (filename, df) in enumerate(data.items()):
            if 'LatencyMs' in df.columns:
                latencies = np.sort(df['LatencyMs'].values)
                config = df['Configuration'].iloc[0]
                
                # Calculate CDF
                y = np.arange(1, len(latencies) + 1) / len(latencies)
                
                ax.plot(latencies, y * 100, color=colors[i % len(colors)], 
                       linewidth=2, label=config)
                
                # Mark percentiles
                p50_idx = int(0.5 * len(latencies))
                p99_idx = int(0.99 * len(latencies))
                
                ax.axvline(latencies[p50_idx], color=colors[i % len(colors)], 
                          linestyle='--', alpha=0.7)
                ax.axvline(latencies[p99_idx], color=colors[i % len(colors)], 
                          linestyle=':', alpha=0.7)
        
        ax.set_xlabel('Latency (ms)')
        ax.set_ylabel('Cumulative Probability (%)')
        ax.set_title('Cumulative Distribution Function - Latency')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xlim(left=0)
        
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'latency_cdf_comparison.png')
        plt.savefig(self.figures_dir / 'latency_cdf_comparison.pdf')
        print(f"Saved CDF comparison to {self.figures_dir}")
        
    def generate_performance_table(self, stats_df: pd.DataFrame):
        """Generate LaTeX table for academic paper."""
        latex_table = """
% Network Offloading Performance Results
\\begin{table}[h]
\\centering
\\begin{tabular}{c|c|c}
\\hline
Configuration & p50 (ms) & p99 (ms) \\\\
\\hline
"""
        
        for _, row in stats_df.iterrows():
            config_name = row['Configuration'].replace('_', '\\_')
            latex_table += f"{config_name} & {row['p50']:.1f} & {row['p99']:.1f} \\\\\n"
            
        latex_table += """\\hline
\\end{tabular}
\\caption{Network Offloading Performance Comparison}
\\label{tab:network_offloading}
\\end{table}
"""
        
        with open(self.figures_dir / 'performance_table.tex', 'w') as f:
            f.write(latex_table)
            
        print(f"Generated LaTeX table: {self.figures_dir / 'performance_table.tex'}")
        
    def run_analysis(self):
        """Run complete analysis and generate all plots."""
        print("=== OXRAvatarForge Tick Comparison Analysis ===")
        
        # Load data
        time_series_data = self.load_time_series_data()
        if not time_series_data or not any(time_series_data.values()):
            print("No time series data found!")
            return
            
        # Calculate statistics for each tick type
        all_stats = []
        for tick_folder, tick_data in time_series_data.items():
            if tick_data:
                tick_name = self.tick_folders[tick_folder]
                stats_df = self.calculate_percentiles(tick_data)
                stats_df['TickType'] = tick_name
                all_stats.append(stats_df)
                
        if all_stats:
            combined_stats = pd.concat(all_stats, ignore_index=True)
            print("\nPercentile Statistics:")
            print(combined_stats.to_string(index=False))
            
            # Save statistics
            combined_stats.to_csv(self.figures_dir / 'tick_comparison_statistics.csv', index=False)
            
            # Generate comparison plots
            print("\nGenerating plots...")
            self.plot_tick_comparison(time_series_data)
            self.plot_combined_statistics(combined_stats)
            
            # Generate LaTeX table
            self.generate_tick_comparison_table(combined_stats)
            
            print(f"\nAnalysis complete! All figures saved to: {self.figures_dir}")
            print("Files generated:")
            for file_path in sorted(self.figures_dir.glob('*')):
                print(f"  - {file_path.name}")
        else:
            print("No valid data found for analysis!")
            
    def plot_tick_comparison(self, time_series_data):
        """Create side-by-side comparison plots for interaction vs system tick."""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        colors = {'Client-only': '#2E86C1', 'Server-offload': '#E74C3C'}
        
        # Plot each tick type
        row = 0
        for tick_folder, tick_data in time_series_data.items():
            if not tick_data:
                continue
                
            tick_name = self.tick_folders[tick_folder]
            
            # Time series plot
            ax_time = axes[row, 0]
            for key, df in tick_data.items():
                config = df['Configuration'].iloc[0]
                color = colors.get(config, '#888888')
                ax_time.plot(df['Timestamp'], df['LatencyMs'], 
                           color=color, alpha=0.7, linewidth=1,
                           label=f"{config} (n={len(df)})")
            
            ax_time.set_xlabel('Time (s)')
            ax_time.set_ylabel('Latency (ms)')
            ax_time.set_title(f'{tick_name} - Time Series')
            ax_time.legend()
            ax_time.grid(True, alpha=0.3)
            
            # Histogram plot
            ax_hist = axes[row, 1]
            for key, df in tick_data.items():
                config = df['Configuration'].iloc[0]
                color = colors.get(config, '#888888')
                ax_hist.hist(df['LatencyMs'], bins=30, alpha=0.6, 
                           color=color, label=config, density=True,
                           edgecolor='black', linewidth=0.5)
            
            ax_hist.set_xlabel('Latency (ms)')
            ax_hist.set_ylabel('Density')
            ax_hist.set_title(f'{tick_name} - Distribution')
            ax_hist.legend()
            ax_hist.grid(True, alpha=0.3)
            
            # Box plot
            ax_box = axes[row, 2]
            box_data = []
            box_labels = []
            box_colors = []
            
            for key, df in tick_data.items():
                config = df['Configuration'].iloc[0]
                box_data.append(df['LatencyMs'].values)
                box_labels.append(config)
                box_colors.append(colors.get(config, '#888888'))
            
            if box_data:
                box_plot = ax_box.boxplot(box_data, labels=box_labels, patch_artist=True)
                for patch, color in zip(box_plot['boxes'], box_colors):
                    patch.set_facecolor(color)
                    patch.set_alpha(0.7)
            
            ax_box.set_ylabel('Latency (ms)')
            ax_box.set_title(f'{tick_name} - Box Plot')
            ax_box.grid(True, alpha=0.3)
            
            row += 1
        
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'tick_comparison.png')
        plt.savefig(self.figures_dir / 'tick_comparison.pdf')
        print(f"Saved tick comparison plot")
        
    def plot_combined_statistics(self, stats_df):
        """Create combined statistical comparison plots."""
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Grouped bar plot for p50 and p99
        tick_types = stats_df['TickType'].unique()
        configs = stats_df['Configuration'].unique()
        
        x = np.arange(len(tick_types))
        width = 0.35
        
        colors = {'Client-only': '#2E86C1', 'Server-offload': '#E74C3C'}
        
        # p50 comparison
        ax1 = axes[0]
        for i, config in enumerate(configs):
            config_data = stats_df[stats_df['Configuration'] == config]
            p50_values = []
            for tick_type in tick_types:
                tick_data = config_data[config_data['TickType'] == tick_type]
                p50_values.append(tick_data['p50'].iloc[0] if len(tick_data) > 0 else 0)
            
            ax1.bar(x + i*width, p50_values, width, label=config, 
                   color=colors.get(config, '#888888'), alpha=0.8)
        
        ax1.set_xlabel('Tick Type')
        ax1.set_ylabel('p50 Latency (ms)')
        ax1.set_title('p50 Latency Comparison')
        ax1.set_xticks(x + width/2)
        ax1.set_xticklabels(tick_types)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # p99 comparison
        ax2 = axes[1]
        for i, config in enumerate(configs):
            config_data = stats_df[stats_df['Configuration'] == config]
            p99_values = []
            for tick_type in tick_types:
                tick_data = config_data[config_data['TickType'] == tick_type]
                p99_values.append(tick_data['p99'].iloc[0] if len(tick_data) > 0 else 0)
            
            ax2.bar(x + i*width, p99_values, width, label=config,
                   color=colors.get(config, '#888888'), alpha=0.8)
        
        ax2.set_xlabel('Tick Type')
        ax2.set_ylabel('p99 Latency (ms)')
        ax2.set_title('p99 Latency Comparison')
        ax2.set_xticks(x + width/2)
        ax2.set_xticklabels(tick_types)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'percentile_comparison.png')
        plt.savefig(self.figures_dir / 'percentile_comparison.pdf')
        print(f"Saved percentile comparison plot")
        
    def generate_tick_comparison_table(self, stats_df):
        """Generate LaTeX table comparing tick types."""
        latex_table = """
% Tick Type Performance Comparison
\\begin{table*}
\\centering
\\begin{tabular}{c|c|c|c}
\\hline
Tick Type & Configuration & p50 (ms) & p99 (ms) \\\\
\\hline
"""
        
        for _, row in stats_df.iterrows():
            tick_type = row['TickType'].replace(' ', '\\_')
            config = row['Configuration'].replace('_', '\\_')
            latex_table += f"{tick_type} & {config} & {row['p50']:.1f} & {row['p99']:.1f} \\\\\n"
            
        latex_table += """\\hline
\\end{tabular}
\\caption{Interaction Tick vs System Tick Performance Comparison}
\\label{tab:tick_comparison}
\\end{table*}
"""
        
        with open(self.figures_dir / 'tick_comparison_table.tex', 'w') as f:
            f.write(latex_table)
            
        print(f"Generated LaTeX table: tick_comparison_table.tex")

def main():
    """Main function to run the analysis."""
    analyzer = LatencyAnalyzer(".")
    analyzer.run_analysis()

if __name__ == "__main__":
    main()
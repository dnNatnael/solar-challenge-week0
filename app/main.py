"""
Solar Challenge Interactive Dashboard
10 Academy KAIM Week 0 - Bonus Task

A production-ready Streamlit dashboard for visualizing solar radiation data
from Benin, Sierra Leone, and Togo.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.data_loader import (
    load_solar_data, 
    get_available_metrics, 
    get_date_range,
    filter_by_date_range,
    get_summary_statistics,
    get_top_hours
)
from src.plot_utils import (
    create_boxplot,
    create_time_series,
    create_correlation_heatmap,
    create_scatter_plot,
    create_bubble_chart,
    create_wind_distribution,
    create_hourly_pattern,
    create_monthly_pattern,
    create_distribution_plot
)

# Page configuration
st.set_page_config(
    page_title="Solar Challenge Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data
def load_data_cached(file_path: str):
    """Cache data loading for better performance"""
    try:
        return load_solar_data(file_path)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None


def main():
    """Main application function"""
    
    # Header
    st.markdown('<div class="main-header">☀️ Solar Challenge Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Interactive Analysis of Solar Radiation Data from West Africa</div>', unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.title("⚙️ Dashboard Configuration")
    st.sidebar.markdown("---")
    
    # Country/Dataset selection
    st.sidebar.subheader("📍 Select Dataset")
    
    # Option to upload file or use local path
    data_source = st.sidebar.radio(
        "Data Source:",
        ["Upload CSV File", "Use Local Path"],
        help="Choose how to load your dataset"
    )
    
    df = None
    
    if data_source == "Upload CSV File":
        uploaded_file = st.sidebar.file_uploader(
            "Upload cleaned CSV file",
            type=['csv'],
            help="Upload your cleaned solar dataset CSV file"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if 'Timestamp' in df.columns:
                    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
                st.sidebar.success("✅ File loaded successfully!")
            except Exception as e:
                st.sidebar.error(f"❌ Error loading file: {str(e)}")
    
    else:  # Use Local Path
        # Predefined country paths (user can modify)
        country = st.sidebar.selectbox(
            "Select Country:",
            ["Benin", "Sierra Leone", "Togo", "Custom Path"],
            help="Select a predefined country or use a custom path"
        )
        
        # Default paths (users should update these)
        default_paths = {
            "Benin": "data/benin-malanville.csv",
            "Sierra Leone": "data/sierraleone-bumbuna.csv",
            "Togo": "data/togo-dapaong_qc.csv"
        }
        
        if country == "Custom Path":
            file_path = st.sidebar.text_input(
                "Enter file path:",
                placeholder="path/to/your/file.csv",
                help="Enter the full or relative path to your CSV file"
            )
        else:
            file_path = st.sidebar.text_input(
                f"File path for {country}:",
                value=default_paths.get(country, ""),
                help="Update this path to match your local file location"
            )
        
        if file_path:
            if st.sidebar.button("📂 Load Data"):
                df = load_data_cached(file_path)
                if df is not None:
                    st.sidebar.success("✅ Data loaded successfully!")
    
    # Main content area
    if df is None:
        st.info("👈 Please load a dataset using the sidebar to get started!")
        
        # Display instructions
        with st.expander("📖 How to Use This Dashboard", expanded=True):
            st.markdown("""
            ### Getting Started
            
            1. **Load Your Data**: Use the sidebar to either:
               - Upload a CSV file directly, or
               - Specify a local file path to your cleaned dataset
            
            2. **Configure Filters**: Once data is loaded, you can:
               - Select metrics to analyze (GHI, DNI, DHI, etc.)
               - Filter by date range
               - Choose visualization options
            
            3. **Explore Visualizations**: Navigate through different tabs to view:
               - Boxplot comparisons
               - Time series analysis
               - Statistical summaries
               - Correlation patterns
               - And much more!
            
            ### Expected Data Format
            Your CSV file should contain columns such as:
            - `Timestamp`: Date and time of measurements
            - `GHI`: Global Horizontal Irradiance
            - `DNI`: Direct Normal Irradiance
            - `DHI`: Diffuse Horizontal Irradiance
            - `Tamb`: Ambient Temperature
            - `RH`: Relative Humidity
            - `WS`: Wind Speed
            - `WSgust`: Wind Gust Speed
            
            ### Note
            This dashboard is designed for the 10 Academy KAIM Week 0 Solar Challenge.
            It supports analysis of solar radiation data from Benin, Sierra Leone, and Togo.
            """)
        
        return
    
    # Data loaded successfully - show metrics selector
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Select Metrics")
    
    available_metrics = get_available_metrics(df)
    
    if not available_metrics:
        st.error("❌ No valid metrics found in the dataset!")
        return
    
    # Multi-select for metrics
    selected_metrics = st.sidebar.multiselect(
        "Choose metrics to analyze:",
        available_metrics,
        default=available_metrics[:3] if len(available_metrics) >= 3 else available_metrics,
        help="Select one or more metrics for analysis"
    )
    
    # Date range filter
    st.sidebar.markdown("---")
    st.sidebar.subheader("📅 Date Range Filter")
    
    min_date, max_date = get_date_range(df)
    
    if min_date and max_date:
        use_date_filter = st.sidebar.checkbox("Enable date filter", value=False)
        
        if use_date_filter:
            date_range = st.sidebar.date_input(
                "Select date range:",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            
            if len(date_range) == 2:
                df = filter_by_date_range(df, date_range[0], date_range[1])
                st.sidebar.info(f"📊 Filtered to {len(df):,} records")
    
    # Display basic dataset info
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ Dataset Info")
    st.sidebar.write(f"**Records**: {len(df):,}")
    st.sidebar.write(f"**Columns**: {len(df.columns)}")
    if min_date and max_date:
        st.sidebar.write(f"**Date Range**: {min_date.date()} to {max_date.date()}")
    
    # Main dashboard content with tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview", 
        "📈 Time Series", 
        "🔍 Detailed Analysis",
        "🌡️ Patterns",
        "🔗 Correlations",
        "📋 Data Table"
    ])
    
    with tab1:
        st.header("📊 Overview & Summary Statistics")
        
        if not selected_metrics:
            st.warning("⚠️ Please select at least one metric from the sidebar.")
        else:
            # Summary statistics
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Statistical Summary")
                summary_df = get_summary_statistics(df, selected_metrics)
                st.dataframe(summary_df.style.format("{:.2f}"), use_container_width=True)
            
            with col2:
                st.subheader("Quick Metrics")
                for metric in selected_metrics[:3]:  # Show top 3
                    if metric in df.columns:
                        mean_val = df[metric].mean()
                        st.metric(
                            label=f"Avg {metric}",
                            value=f"{mean_val:.2f}",
                            delta=f"±{df[metric].std():.2f}"
                        )
            
            # Boxplot comparison
            st.subheader("Distribution Comparison (Boxplot)")
            fig_box = create_boxplot(df, selected_metrics, "Metric Distribution Comparison")
            st.plotly_chart(fig_box, use_container_width=True)
    
    with tab2:
        st.header("📈 Time Series Analysis")
        
        if not selected_metrics:
            st.warning("⚠️ Please select at least one metric from the sidebar.")
        else:
            # Metric selector for time series
            metric_for_ts = st.selectbox(
                "Select metric for time series:",
                selected_metrics,
                help="Choose which metric to display over time"
            )
            
            if metric_for_ts:
                # Time series plot
                fig_ts = create_time_series(df, metric_for_ts)
                st.plotly_chart(fig_ts, use_container_width=True)
                
                # Top/Peak hours
                st.subheader(f"🏆 Top 10 Peak Hours for {metric_for_ts}")
                top_df = get_top_hours(df, metric_for_ts, top_n=10)
                if not top_df.empty:
                    st.dataframe(top_df.style.format({metric_for_ts: "{:.2f}"}), use_container_width=True)
                else:
                    st.info("No timestamp data available for peak hours analysis.")
    
    with tab3:
        st.header("🔍 Detailed Analysis")
        
        if not selected_metrics:
            st.warning("⚠️ Please select at least one metric from the sidebar.")
        else:
            analysis_type = st.selectbox(
                "Select analysis type:",
                ["Distribution", "Scatter Plot", "Bubble Chart", "Wind Analysis"]
            )
            
            if analysis_type == "Distribution":
                metric = st.selectbox("Select metric:", selected_metrics, key="dist_metric")
                fig = create_distribution_plot(df, metric)
                st.plotly_chart(fig, use_container_width=True)
            
            elif analysis_type == "Scatter Plot":
                col1, col2, col3 = st.columns(3)
                with col1:
                    x_metric = st.selectbox("X-axis:", selected_metrics, key="scatter_x")
                with col2:
                    y_metric = st.selectbox("Y-axis:", selected_metrics, index=min(1, len(selected_metrics)-1), key="scatter_y")
                with col3:
                    color_option = st.selectbox("Color by:", ["None"] + selected_metrics, key="scatter_color")
                
                color_metric = None if color_option == "None" else color_option
                fig = create_scatter_plot(df, x_metric, y_metric, color_metric)
                st.plotly_chart(fig, use_container_width=True)
            
            elif analysis_type == "Bubble Chart":
                if len(selected_metrics) < 3:
                    st.warning("⚠️ Please select at least 3 metrics for bubble chart.")
                else:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        x_metric = st.selectbox("X-axis:", selected_metrics, key="bubble_x")
                    with col2:
                        y_metric = st.selectbox("Y-axis:", selected_metrics, index=min(1, len(selected_metrics)-1), key="bubble_y")
                    with col3:
                        size_metric = st.selectbox("Size:", selected_metrics, index=min(2, len(selected_metrics)-1), key="bubble_size")
                    
                    color_option = st.selectbox("Color by:", ["None"] + selected_metrics, key="bubble_color")
                    color_metric = None if color_option == "None" else color_option
                    
                    fig = create_bubble_chart(df, x_metric, y_metric, size_metric, color_metric)
                    st.plotly_chart(fig, use_container_width=True)
            
            elif analysis_type == "Wind Analysis":
                if 'WS' in df.columns:
                    fig = create_wind_distribution(df)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ Wind speed data (WS) not available in the dataset.")
    
    with tab4:
        st.header("🌡️ Temporal Patterns")
        
        if not selected_metrics:
            st.warning("⚠️ Please select at least one metric from the sidebar.")
        elif 'Timestamp' not in df.columns:
            st.warning("⚠️ Timestamp column not found in the dataset.")
        else:
            metric = st.selectbox("Select metric for pattern analysis:", selected_metrics, key="pattern_metric")
            
            pattern_type = st.radio(
                "Pattern type:",
                ["Hourly Pattern", "Monthly Pattern"],
                horizontal=True
            )
            
            if pattern_type == "Hourly Pattern":
                fig = create_hourly_pattern(df, metric)
                st.plotly_chart(fig, use_container_width=True)
                
                st.info("💡 This chart shows the average values across all days for each hour of the day.")
            
            else:  # Monthly Pattern
                fig = create_monthly_pattern(df, metric)
                st.plotly_chart(fig, use_container_width=True)
                
                st.info("💡 This chart shows the average values for each month in the dataset.")
    
    with tab5:
        st.header("🔗 Correlation Analysis")
        
        if len(selected_metrics) < 2:
            st.warning("⚠️ Please select at least 2 metrics for correlation analysis.")
        else:
            st.subheader("Correlation Heatmap")
            fig_corr = create_correlation_heatmap(df, selected_metrics)
            st.plotly_chart(fig_corr, use_container_width=True)
            
            st.info("💡 Correlation values range from -1 to 1. Values closer to 1 indicate strong positive correlation, while values closer to -1 indicate strong negative correlation.")
    
    with tab6:
        st.header("📋 Raw Data Table")
        
        st.subheader("Dataset Preview")
        
        # Display controls
        col1, col2 = st.columns([1, 1])
        with col1:
            num_rows = st.slider("Number of rows to display:", 5, 100, 20)
        with col2:
            show_all_cols = st.checkbox("Show all columns", value=False)
        
        # Display data
        if show_all_cols:
            st.dataframe(df.head(num_rows), use_container_width=True)
        else:
            display_cols = ['Timestamp'] + selected_metrics if 'Timestamp' in df.columns else selected_metrics
            display_cols = [col for col in display_cols if col in df.columns]
            st.dataframe(df[display_cols].head(num_rows), use_container_width=True)
        
        # Download option
        st.subheader("📥 Download Data")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download filtered data as CSV",
            data=csv,
            file_name="solar_data_filtered.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888; padding: 1rem;'>
        <p>☀️ Solar Challenge Dashboard | 10 Academy KAIM Week 0 | Built with Streamlit</p>
        <p>Data sources: Benin, Sierra Leone, and Togo Solar Radiation Measurements</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

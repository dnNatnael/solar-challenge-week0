# 🏗️ Dashboard Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    SOLAR CHALLENGE DASHBOARD                     │
│                   Streamlit Web Application                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────────────────────┐   │
│  │    SIDEBAR       │  │         MAIN CONTENT             │   │
│  ├──────────────────┤  ├──────────────────────────────────┤   │
│  │ • Data Source    │  │  Tab 1: Overview                 │   │
│  │ • Country Select │  │  Tab 2: Time Series              │   │
│  │ • Metric Select  │  │  Tab 3: Detailed Analysis        │   │
│  │ • Date Filter    │  │  Tab 4: Patterns                 │   │
│  │ • Dataset Info   │  │  Tab 5: Correlations             │   │
│  └──────────────────┘  │  Tab 6: Data Table               │   │
│                        └──────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                           │
│                        app/main.py                               │
├─────────────────────────────────────────────────────────────────┤
│  • Page Configuration                                            │
│  • State Management                                              │
│  • Widget Handlers                                               │
│  • Layout Orchestration                                          │
│  • Caching (@st.cache_data)                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
┌──────────────────────────┐      ┌──────────────────────────┐
│    DATA LAYER            │      │   VISUALIZATION LAYER    │
│  src/data_loader.py      │      │   src/plot_utils.py      │
├──────────────────────────┤      ├──────────────────────────┤
│ • validate_file_path()   │      │ • create_boxplot()       │
│ • load_solar_data()      │      │ • create_time_series()   │
│ • get_available_metrics()│      │ • create_correlation()   │
│ • get_date_range()       │      │ • create_scatter_plot()  │
│ • filter_by_date_range() │      │ • create_bubble_chart()  │
│ • get_summary_stats()    │      │ • create_wind_dist()     │
│ • get_top_hours()        │      │ • create_hourly_pattern()│
└──────────────────────────┘      │ • create_monthly_pattern()│
            │                      │ • create_distribution()  │
            ▼                      └──────────────────────────┘
┌──────────────────────────┐                  │
│     DATA SOURCES         │                  ▼
├──────────────────────────┤      ┌──────────────────────────┐
│ • File Upload            │      │   PLOTTING LIBRARIES     │
│ • Local File Path        │      ├──────────────────────────┤
│ • CSV Format             │      │ • Plotly Express         │
└──────────────────────────┘      │ • Plotly Graph Objects   │
                                  │ • Matplotlib             │
                                  │ • Seaborn                │
                                  └──────────────────────────┘
```

---

## Component Interaction Flow

### 1. Data Loading Flow

```
User Action (Upload/Path)
         │
         ▼
    [Sidebar Widget]
         │
         ▼
    validate_file_path()  ◄─── src/data_loader.py
         │
         ▼
    load_solar_data()     ◄─── src/data_loader.py
         │
         ▼
    [@st.cache_data]      ◄─── Cached for performance
         │
         ▼
    [DataFrame Ready]
         │
         └──────┐
                ▼
        Update UI with data
```

### 2. Visualization Flow

```
User Selects Metric
         │
         ▼
    [Widget State Change]
         │
         ▼
    Filter DataFrame
         │
         ▼
    Call plot_utils function  ◄─── src/plot_utils.py
         │
         ▼
    Generate Plotly Figure
         │
         ▼
    st.plotly_chart()
         │
         ▼
    [Interactive Plot Displayed]
```

### 3. Filter Application Flow

```
User Adjusts Filters
         │
         ├─── Select Metrics
         │         │
         │         ▼
         │    Update metric list
         │
         ├─── Date Range
         │         │
         │         ▼
         │    filter_by_date_range()
         │
         └─── Country
                   │
                   ▼
              Load new file
         │
         ▼
    Re-render all visualizations
```

---

## Module Dependencies

```
app/main.py
    │
    ├─── streamlit (UI framework)
    ├─── pandas (data manipulation)
    ├─── sys, pathlib (path management)
    │
    ├─── src/data_loader
    │        │
    │        ├─── pandas
    │        ├─── os
    │        └─── pathlib
    │
    └─── src/plot_utils
             │
             ├─── pandas
             ├─── matplotlib
             ├─── seaborn
             ├─── plotly.express
             ├─── plotly.graph_objects
             └─── numpy
```

---

## Data Flow Diagram

```
┌──────────────┐
│  CSV File    │
│  (External)  │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  File Validation │ ◄─── validate_file_path()
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Load & Parse    │ ◄─── load_solar_data()
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  DataFrame       │
│  - Timestamp     │
│  - GHI, DNI, DHI │
│  - Tamb, RH, WS  │
└──────┬───────────┘
       │
       ├──────────────────┐
       │                  │
       ▼                  ▼
┌──────────────┐   ┌─────────────────┐
│  Filtering   │   │  Aggregation    │
│  - Date      │   │  - Statistics   │
│  - Metrics   │   │  - Grouping     │
└──────┬───────┘   └────────┬────────┘
       │                    │
       └─────────┬──────────┘
                 │
                 ▼
         ┌───────────────┐
         │ Visualization │
         │  Functions    │
         └───────┬───────┘
                 │
                 ▼
         ┌───────────────┐
         │ Plotly Charts │
         └───────┬───────┘
                 │
                 ▼
         ┌───────────────┐
         │  User Display │
         └───────────────┘
```

---

## State Management

### Streamlit Session State

```python
# Streamlit automatically manages state through:

# 1. Widget State
selected_metrics = st.multiselect(...)  # Auto-persisted
date_range = st.date_input(...)         # Auto-persisted

# 2. Cache State
@st.cache_data
def load_data_cached(file_path):
    # Cached by file_path parameter
    return dataframe

# 3. Page State
# Maintained through reruns
# Widgets retain values across reruns
```

### Data Cache Strategy

```
┌─────────────────────────────────────┐
│         Cache Key: file_path         │
├─────────────────────────────────────┤
│                                      │
│  First Load:                         │
│  1. Read CSV from disk               │
│  2. Parse dates                      │
│  3. Store in cache                   │
│                                      │
│  Subsequent Loads:                   │
│  1. Check cache by file_path         │
│  2. Return cached DataFrame          │
│  3. No disk I/O needed              │
│                                      │
│  Cache Invalidation:                 │
│  • File path changes                 │
│  • Manual cache clear                │
│  • App restart                       │
└─────────────────────────────────────┘
```

---

## Performance Optimization

### 1. Data Loading
- ✅ Cache with `@st.cache_data`
- ✅ Parse dates only once
- ✅ Validate before loading

### 2. Visualization
- ✅ Sample large datasets (>1000 rows for bubble)
- ✅ Use Plotly for GPU acceleration
- ✅ Lazy render (tab-based)

### 3. Memory Management
- ✅ Load data on-demand
- ✅ Clear cache when needed
- ✅ Filter before visualization

---

## Security Considerations

### Input Validation

```python
# File path validation
def validate_file_path(file_path):
    # 1. Check existence
    # 2. Verify file type
    # 3. Prevent path traversal
    return is_valid, error_message
```

### Data Handling

```python
# Safe CSV loading
df = pd.read_csv(file_path)
# No SQL injection risk (CSV only)
# No arbitrary code execution
```

### Deployment Security

```toml
# .streamlit/config.toml
[server]
enableXsrfProtection = true  # CSRF protection
enableCORS = false            # Restrict origins
```

---

## Scalability

### Current Limitations
- CSV files up to 200MB
- In-memory processing
- Single-threaded

### Scaling Strategies

#### For Larger Datasets
```python
# 1. Chunked reading
chunks = pd.read_csv(file_path, chunksize=10000)
df = pd.concat(chunks)

# 2. Sampling
df_sample = df.sample(n=100000)

# 3. Database backend
# Replace CSV with SQL queries
```

#### For Multiple Users
```
Current: Streamlit Cloud (single instance)
         ↓
Scale: Multi-instance deployment
       Load balancer
       Shared cache (Redis)
```

---

## Error Handling Strategy

```
┌─────────────────────────────────┐
│     User Action                  │
└────────────┬────────────────────┘
             │
             ▼
    ┌────────────────────┐
    │  Try Operation     │
    └────────┬───────────┘
             │
        ┌────┴────┐
        │ Success │
        └────┬────┘
             │
             ▼
    ┌─────────────────┐
    │  Display Result │
    └─────────────────┘

    ┌────┴────┐
    │ Error   │
    └────┬────┘
         │
         ├─── File Not Found
         │         │
         │         ▼
         │    st.error("File not found")
         │
         ├─── Parse Error
         │         │
         │         ▼
         │    st.error("Invalid CSV format")
         │
         ├─── Missing Column
         │         │
         │         ▼
         │    st.warning("Metric not available")
         │
         └─── Other Error
                   │
                   ▼
              st.error(str(exception))
```

---

## Deployment Architecture

### Local Development

```
Developer Machine
    │
    ├── Python 3.8+
    ├── Virtual Environment
    ├── Source Code
    ├── Local Data Files
    │
    └── Run: streamlit run app/main.py
        │
        └── http://localhost:8501
```

### Streamlit Community Cloud

```
GitHub Repository
    │
    ├── app/main.py
    ├── src/
    ├── requirements.txt
    ├── .streamlit/config.toml
    │
    └── Connected to Streamlit Cloud
        │
        ├── Auto-deploy on push
        ├── Container instance
        ├── Public URL
        │
        └── https://yourapp.streamlit.app
```

---

## Technology Stack

```
┌──────────────────────────────────────┐
│         Presentation Layer            │
│  • Streamlit (Web Framework)         │
│  • HTML/CSS (via Streamlit)          │
└──────────────┬───────────────────────┘
               │
┌──────────────▼───────────────────────┐
│         Application Layer             │
│  • Python 3.8+                       │
│  • Streamlit Runtime                 │
└──────────────┬───────────────────────┘
               │
┌──────────────▼───────────────────────┐
│         Data Processing Layer         │
│  • Pandas (DataFrames)               │
│  • NumPy (Numerical ops)             │
└──────────────┬───────────────────────┘
               │
┌──────────────▼───────────────────────┐
│         Visualization Layer           │
│  • Plotly Express                    │
│  • Plotly Graph Objects              │
│  • Matplotlib                        │
│  • Seaborn                           │
└──────────────┬───────────────────────┘
               │
┌──────────────▼───────────────────────┐
│         Storage Layer                 │
│  • CSV Files (local/uploaded)        │
│  • In-memory cache                   │
└──────────────────────────────────────┘
```

---

## Extension Points

### Adding New Features

#### 1. New Visualization Type
```python
# In src/plot_utils.py
def create_new_chart(df, params):
    fig = go.Figure()
    # Chart logic
    return fig

# In app/main.py
with new_tab:
    fig = create_new_chart(df, params)
    st.plotly_chart(fig)
```

#### 2. New Data Source
```python
# In src/data_loader.py
def load_from_api(url):
    response = requests.get(url)
    df = pd.DataFrame(response.json())
    return df
```

#### 3. New Analysis
```python
# In src/data_loader.py
def calculate_solar_efficiency(df):
    # Analysis logic
    return results

# In app/main.py
efficiency = calculate_solar_efficiency(df)
st.metric("Efficiency", f"{efficiency}%")
```

---

## Testing Strategy

```
Unit Tests
    │
    ├── test_data_loader.py
    │   ├── test_validate_file_path()
    │   ├── test_load_solar_data()
    │   └── test_get_summary_statistics()
    │
    └── test_plot_utils.py
        ├── test_create_boxplot()
        ├── test_create_time_series()
        └── test_create_heatmap()

Integration Tests
    │
    └── test_dashboard.py
        ├── test_file_upload()
        ├── test_metric_selection()
        └── test_visualization_rendering()

E2E Tests
    │
    └── test_user_workflows.py
        ├── test_complete_analysis_workflow()
        └── test_data_export_workflow()
```

---

## Monitoring & Logging

### Current Implementation
```python
# Error display to user
st.error(f"Error: {message}")
st.warning("Warning message")
st.info("Info message")
```

### Production Enhancement
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log critical events
logger.info(f"Data loaded: {len(df)} records")
logger.error(f"Load failed: {error}")
```

---

**Last Updated:** November 2024  
**Version:** 1.0.0  
**Architecture Type:** Modular Monolith  
**Deployment Model:** Cloud-Native (Streamlit Cloud)

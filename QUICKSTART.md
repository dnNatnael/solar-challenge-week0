# 🚀 Quick Start Guide - Solar Challenge Dashboard

Get your dashboard up and running in under 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (optional, for cloning)

## Installation (3 Steps)

### Step 1: Setup Environment

```bash
# Navigate to project directory
cd solar-challenge-week0

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run Dashboard

```bash
streamlit run app/main.py
```

That's it! Your dashboard will open automatically at `http://localhost:8501`

## First Time Usage

### Option A: Upload Your Data (Recommended for first try)

1. Launch the dashboard
2. In the sidebar, select **"Upload CSV File"**
3. Click **"Browse files"** and select your cleaned CSV
4. Dashboard will automatically load and display your data

### Option B: Use Local File Path

1. Launch the dashboard
2. In the sidebar, select **"Use Local Path"**
3. Choose a country or select **"Custom Path"**
4. Update the file path to match your local file location
5. Click **"Load Data"**

## Test with Sample Data

Don't have data yet? Create a test file:

```python
# test_data_generator.py
import pandas as pd
import numpy as np

# Generate sample data
dates = pd.date_range('2024-01-01', periods=1000, freq='H')
data = pd.DataFrame({
    'Timestamp': dates,
    'GHI': np.random.uniform(0, 1000, 1000),
    'DNI': np.random.uniform(0, 900, 1000),
    'DHI': np.random.uniform(0, 500, 1000),
    'Tamb': np.random.uniform(20, 35, 1000),
    'RH': np.random.uniform(30, 90, 1000),
    'WS': np.random.uniform(0, 15, 1000),
    'WSgust': np.random.uniform(0, 20, 1000)
})

# Save to CSV
data.to_csv('data/test_sample.csv', index=False)
print("✅ Test data created at data/test_sample.csv")
```

Run the generator:
```bash
python test_data_generator.py
```

Then load `data/test_sample.csv` in the dashboard.

## Dashboard Navigation

### Sidebar (Left)
- **Data Source**: Choose how to load data
- **Select Metrics**: Pick which variables to analyze
- **Date Filter**: Filter data by date range
- **Dataset Info**: View record counts and ranges

### Main Tabs (Top)
1. **📊 Overview**: Summary statistics and boxplots
2. **📈 Time Series**: Temporal analysis and peak hours
3. **🔍 Detailed Analysis**: Distributions, scatter plots, bubbles
4. **🌡️ Patterns**: Hourly and monthly patterns
5. **🔗 Correlations**: Correlation heatmap
6. **📋 Data Table**: View and download data

## Common Workflows

### Workflow 1: Quick Overview
```
1. Load data (upload or path)
2. Go to Overview tab
3. View summary statistics
4. Check boxplot distribution
```

### Workflow 2: Time Series Analysis
```
1. Load data
2. Select metrics (e.g., GHI, DNI, DHI)
3. Go to Time Series tab
4. Choose metric to visualize
5. View peak hours table
```

### Workflow 3: Correlation Study
```
1. Load data
2. Select at least 2 metrics
3. Go to Correlations tab
4. Analyze heatmap for relationships
```

### Workflow 4: Pattern Discovery
```
1. Load data
2. Go to Patterns tab
3. Select metric
4. Switch between Hourly/Monthly
5. Identify daily or seasonal trends
```

## Tips for Best Experience

### ✅ Do's
- Select 3-5 metrics for optimal visualization
- Use date filter for large datasets
- Download filtered data for offline analysis
- Explore all tabs for comprehensive insights

### ❌ Don'ts
- Don't upload files larger than 200MB
- Don't select too many metrics at once (performance)
- Don't forget to check data quality first
- Don't use production data in cloud deployments (unless secure)

## Keyboard Shortcuts

- `Ctrl + R` (or `Cmd + R`): Rerun the app
- `Ctrl + Shift + R`: Clear cache and rerun
- `Ctrl + K`: Focus on sidebar
- `Esc`: Close modals/dialogs

## Troubleshooting Quick Fixes

### Dashboard won't start
```bash
# Check if Streamlit is installed
streamlit version

# Reinstall if needed
pip install --upgrade streamlit
```

### Import errors
```bash
# Install all dependencies fresh
pip install -r requirements.txt --upgrade
```

### Data won't load
- Check CSV format (must have headers)
- Verify Timestamp column exists
- Ensure file path is correct
- Try uploading instead of path

### Visualization not showing
- Check if metric names match column names
- Ensure at least one metric is selected
- Verify data is not empty
- Try refreshing the browser

## Next Steps

### For Development
- Read `DASHBOARD.md` for technical details
- Explore `src/plot_utils.py` for plotting functions
- Check `src/data_loader.py` for data utilities

### For Deployment
- See README.md section "Deploying to Streamlit Community Cloud"
- Push code to GitHub
- Deploy on [share.streamlit.io](https://share.streamlit.io)

### For Customization
- Edit `.streamlit/config.toml` for theme changes
- Add new tabs in `app/main.py`
- Create custom plots in `src/plot_utils.py`

## Getting Help

### Resources
- 📖 Full documentation: `README.md`
- 🔧 Technical details: `DASHBOARD.md`
- 💬 Streamlit docs: [docs.streamlit.io](https://docs.streamlit.io)

### Community
- [Streamlit Forum](https://discuss.streamlit.io)
- [GitHub Issues](https://github.com/your-username/solar-challenge-week0/issues)

## Example Session

```bash
# Start fresh session
cd solar-challenge-week0
source venv/bin/activate  # or venv\Scripts\activate on Windows
streamlit run app/main.py

# Dashboard opens in browser
# 1. Upload data/benin-malanville.csv
# 2. Select metrics: GHI, DNI, DHI, Tamb
# 3. Explore Overview tab
# 4. Check Time Series for GHI
# 5. View Correlations heatmap
# 6. Download filtered data if needed
```

## Success Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed from requirements.txt
- [ ] Dashboard launches without errors
- [ ] Data loads successfully (upload or path)
- [ ] Metrics are selectable
- [ ] Visualizations render correctly
- [ ] All tabs are functional
- [ ] Download feature works

## Ready to Deploy?

Once everything works locally:

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy with `app/main.py`
5. Share your dashboard URL!

---

**Need more help?** Check `README.md` for detailed documentation or `DASHBOARD.md` for technical specifics.

**Happy Analyzing! 📊☀️**

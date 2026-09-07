import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from arch import arch_model
from scipy.optimize import minimize
import numpy as np
import tensorflow as tf 
from tensorflow.keras import regularizers
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense,Input, Dropout, Bidirectional



import pandas as pd
import plotly.graph_objs as go
from arch import arch_model
import numpy as np

# Function to calculate GARCH volatility
def calculate_garch_volatility(data: pd.Series, p=1, q=1):
    data = data.sort_index()
    returns = data.pct_change().dropna()
    scaled_returns = returns * 100
    model = arch_model(scaled_returns, vol='Garch', p=p, q=q)
    garch_fit = model.fit(disp="off")
    volatility = garch_fit.conditional_volatility
    return volatility

# Function to calculate simple moving averages
def calculate_moving_averages(data: pd.Series, window=30):
    return data.rolling(window=window).mean()

# Function to calculate exponential moving averages
def calculate_ema(data: pd.Series, span=30):
    return data.ewm(span=span, adjust=False).mean()

# Function to add Bollinger Bands calculation
def calculate_bollinger_bands(data: pd.Series, window=30, num_of_std=2):
    rolling_mean = data.rolling(window=window).mean()
    rolling_std = data.rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_of_std)
    lower_band = rolling_mean - (rolling_std * num_of_std)
    return rolling_mean, upper_band, lower_band

# Function to generate individual plots
def market_trends(data: pd.Series):
    # Calculate indicators
    volatility = calculate_garch_volatility(data)
    moving_averages = calculate_moving_averages(data)
    ema = calculate_ema(data)
    bollinger_mean, upper_band, lower_band = calculate_bollinger_bands(data)

    # Create individual plots
    volatility_fig = go.Figure()
    volatility_fig.add_trace(go.Scatter(x=data.index, y=volatility, mode='lines', name='Volatility', line=dict(color='orange')))
    volatility_fig.update_layout(title='Volatility', xaxis_title='Date', yaxis_title='Value', width=1200, height=600)

    price_ma_fig = go.Figure()
    price_ma_fig.add_trace(go.Scatter(x=data.index, y=data, mode='lines', name='Price', line=dict(color='red')))
    price_ma_fig.add_trace(go.Scatter(x=data.index, y=moving_averages, mode='lines', name='Moving Average', line=dict(color='green')))
    price_ma_fig.update_layout(title='Price & Moving Averages', xaxis_title='Date', yaxis_title='Value', width=1200, height=600)

    ema_fig = go.Figure()
    ema_fig.add_trace(go.Scatter(x=data.index, y=ema, mode='lines', name='EMA', line=dict(color='blue')))
    ema_fig.update_layout(title='Exponential Moving Average (EMA)', xaxis_title='Date', yaxis_title='Value', width=1200, height=600)

    bollinger_fig = go.Figure()
    bollinger_fig.add_trace(go.Scatter(x=data.index, y=bollinger_mean, mode='lines', name='Bollinger Mean', line=dict(color='purple')))
    bollinger_fig.add_trace(go.Scatter(x=data.index, y=upper_band, mode='lines', name='Upper Band', line=dict(color='gray')))
    bollinger_fig.add_trace(go.Scatter(x=data.index, y=lower_band, mode='lines', name='Lower Band', line=dict(color='gray')))
    bollinger_fig.update_layout(title='Bollinger Bands', xaxis_title='Date', yaxis_title='Value', width=1200, height=600)

    return volatility_fig, price_ma_fig, ema_fig, bollinger_fig







import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def calculate_var(data: pd.Series, confidence_level=0.95):
    returns = data.pct_change().dropna()
    var = np.percentile(returns, (1 - confidence_level) * 100)
    return var

def calculate_es(data: pd.Series, confidence_levels=[0.95, 0.99]):
    returns = data.pct_change().dropna()
    es_values = {}
    
    for confidence_level in confidence_levels:
        var = np.percentile(returns, (1 - confidence_level) * 100)
        es = returns[returns <= var].mean()
        es_values[confidence_level] = es
    
    return es_values

def calculate_sharpe_ratio(data: pd.Series, risk_free_rate=0.01):
    returns = data.pct_change().dropna()
    excess_return = returns.mean() - risk_free_rate
    sharpe_ratio = excess_return / returns.std()
    return sharpe_ratio

def calculate_risk_matrix(data: pd.Series):
    returns = data.pct_change().dropna()
    mean_return = returns.mean()
    std_return = returns.std()
    probabilities = np.linspace(0, 1, num=5)
    impacts = np.linspace(0, std_return * 3, num=5)
    risk_levels = np.zeros((len(probabilities), len(impacts)))
    
    for i, prob in enumerate(probabilities):
        for j, impact in enumerate(impacts):
            risk_levels[i, j] = np.mean(np.abs(returns) <= impact)
    
    return probabilities, impacts, risk_levels

def plot_monte_carlo_simulation(data: pd.Series, num_simulations=1000, num_days=252):
    returns = data.pct_change().dropna()
    mean_return = returns.mean()
    std_return = returns.std()
    simulations = np.zeros((num_simulations, num_days))
    
    for i in range(num_simulations):
        simulated_returns = np.random.normal(loc=mean_return, scale=std_return, size=num_days)
        simulations[i, :] = np.cumprod(1 + simulated_returns)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=np.arange(num_days),
        y=simulations.mean(axis=0),
        mode='lines',
        line=dict(color='red', width=2),
        name='Average Simulation'
    ))
    fig.add_trace(go.Scatter(
        x=np.arange(num_days),
        y=simulations.min(axis=0),
        mode='lines',
        line=dict(color='blue', width=1, dash='dash'),
        name='Min Simulation'
    ))
    fig.add_trace(go.Scatter(
        x=np.arange(num_days),
        y=simulations.max(axis=0),
        mode='lines',
        line=dict(color='green', width=1, dash='dash'),
        name='Max Simulation'
    ))

    fig.update_layout(
        title='Monte Carlo Simulation',
        xaxis_title='Days',
        yaxis_title='Simulated Portfolio Value',
        width=1200,
        height=600
    )

    return fig

def plot_cumulative_return(data: pd.Series):
    cumulative_return = (1 + data.pct_change().dropna()).cumprod() - 1
    fig = px.line(cumulative_return, labels={'value': 'Cumulative Return', 'index': 'Date'})
    fig.update_layout(
        title='Cumulative Return Over Time',
        xaxis_title='Date',
        yaxis_title='Cumulative Return',
        xaxis=dict(
            tickformat='%Y',
        ),
        width=1200,
        height=600
    )
    return fig

def plot_drawdown(data: pd.Series):
    cumulative_return = (1 + data.pct_change().dropna()).cumprod()
    drawdown = (cumulative_return / cumulative_return.cummax()) - 1
    fig = px.line(drawdown, labels={'value': 'Drawdown', 'index': 'Date'})
    fig.update_layout(
        title='Drawdown Over Time',
        xaxis_title='Date',
        yaxis_title='Drawdown',
        xaxis=dict(
            tickformat='%Y',
        ),
        width=1200,
        height=600
    )
    return fig

def plot_risk_matrix_heatmap(probabilities, impacts, risk_levels):
    likelihood_labels = ['Very Unlikely', 'Unlikely', 'Possible', 'Likely', 'Very Likely']
    severity_labels = ['Negligible', 'Minor', 'Moderate', 'Significant', 'Severe']
    
    fig = go.Figure(data=go.Heatmap(
        z=risk_levels,
        x=severity_labels,
        y=likelihood_labels,
        colorscale='Viridis'
    ))
    fig.update_layout(
        title='Risk Matrix Heatmap',
        xaxis=dict(title='Severity', tickvals=np.arange(len(severity_labels)), ticktext=severity_labels),
        yaxis=dict(title='Likelihood', tickvals=np.arange(len(likelihood_labels)), ticktext=likelihood_labels),
        width=1200,
        height=600
    )
    return fig


def plot_risk_metrics_half_donut(var, es, max_drawdown, sharpe_ratio):
    # Handle NaN or invalid values
    var = var if pd.notna(var) and var != 0 else 0.01  # Default small value
    es = es if pd.notna(es) and es != 0 else 0.01
    max_drawdown = max_drawdown if pd.notna(max_drawdown) and max_drawdown != 0 else 0.01
    sharpe_ratio = sharpe_ratio if pd.notna(sharpe_ratio) and sharpe_ratio != 0 else 0.01

    labels = ['VaR', 'ES', 'Max Drawdown', 'Sharpe Ratio']
    values = [abs(var), abs(es), abs(max_drawdown), abs(sharpe_ratio)]  # Ensure positive values
    colors = ['#FF6347', '#4682B4', '#32CD32', '#FFD700']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,  # Creates the doughnut shape
        rotation=90,  # Adjust start angle
        direction='clockwise',
        marker=dict(colors=colors),
        textinfo='label+percent',
        textfont_size=14,
        domain={'x': [0, 1], 'y': [0, 0.6]}  # Controls the size to make it half-doughnut
    )])

    fig.update_layout(
        title='Risk Metrics Overview',
        annotations=[dict(text='Risk Metrics', x=0.5, y=0.35, font_size=20, showarrow=False)],
        showlegend=True,
        width=1200,
        height=600
    )

    return fig









import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Stress Test Scenario Function with Industry-Specific, Cumulative, and Realistic Financial Indicators
def stress_test_scenario(data: pd.Series, shock_percentage: float, stress_factor: str, severity_level: str, duration: int, sector: str = None, inflation_rate: float = 0.02) -> pd.Series:
    """
    Apply non-linear stress to the data based on the specified factors and industry.

    Parameters:
    - data: Stock or portfolio data (as pandas Series)
    - shock_percentage: Percentage of shock (e.g., 10% drop)
    - stress_factor: Type of stress factor (e.g., 'economic-downturn', 'market-volatility')
    - severity_level: The severity level ('mild', 'moderate', 'severe')
    - duration: Duration of stress (in days)
    - sector: Optional, to apply sector-specific stress.
    - inflation_rate: Optional, default is 2% inflation rate.
    
    Returns:
    - Stressed data (as pandas Series)
    """
    baseline_data = data.copy()
    n = len(data)
    time_index = np.arange(n)

    # Apply sector-specific adjustments if any
    
    if stress_factor == 'economic-downturn':
        stress = np.exp(-shock_percentage / 100 * time_index / n)  # Exponential decay
    elif stress_factor == 'market-volatility':
        stress = 1 + (shock_percentage / 100) * np.sin(np.linspace(0, np.pi, n))  # Sinusoidal volatility
    elif stress_factor == 'high-interest-rates':
        stress = np.power(1 - shock_percentage / 100, np.linspace(1, 10, n))  # Compounding effect
    elif stress_factor == 'regulatory-changes':
        stress = np.linspace(1, 1 - shock_percentage / 100, n)  # Linear decay
    else:
        stress = np.ones(n)  # No stress if factor is unknown

    # Apply severity level adjustment
    if severity_level == 'severe':
        stress *= 1.3
    elif severity_level == 'moderate':
        stress *= 1.2
    elif severity_level == 'mild':
        stress *= 1.1

    # Apply inflation adjustment
    inflation_effect = 1 + inflation_rate * np.random.normal(0, 0.1, n)
    stress *= inflation_effect  # Incorporating inflation into stress

    # Apply stress and duration
    stressed_data = baseline_data.copy()
    stressed_data.iloc[:duration] = baseline_data.iloc[:duration] * stress[:duration]
    stressed_data.iloc[duration:] = baseline_data.iloc[duration:] * stress[duration:]

    return stressed_data

# Function to apply multiple stress factors over different time durations
def apply_stress_tests(data: pd.Series, shock_percentage: float, stress_factors: list, severity_level: str, stress_durations: list, sector: str = None, inflation_rate: float = 0.02) -> go.Figure:
    """
    Apply multiple stress tests over different durations and factors.
    
    Parameters:
    - data: Stock or portfolio data (as pandas Series)
    - shock_percentage: Percentage of shock
    - stress_factors: List of stress factors
    - severity_level: Severity level of the stress
    - stress_durations: List of durations for stress
    - sector: Sector for specific adjustments
    - inflation_rate: Inflation rate
    
    Returns:
    - Plotly figure showing original and stressed data for different factors and durations
    """
    fig = go.Figure()

    # Original Data Plot
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data,
        mode='lines',
        name='Original Data',
        line=dict(color='blue')
    ))
    
    colors = ['red', 'green', 'purple', 'orange', 'yellow']
    heatmap_data = []
    
    for duration in stress_durations:
        for idx, stress_factor in enumerate(stress_factors):
            stressed_data = stress_test_scenario(data, shock_percentage, stress_factor, severity_level, duration, sector, inflation_rate)
            fig.add_trace(go.Scatter(
                x=stressed_data.index,
                y=stressed_data,
                mode='lines',
                name=f'Stressed Data ({stress_factor}, {duration} days)',
                line=dict(color=colors[idx % len(colors)])
            ))
            
            # Prepare data for heatmap
            stress_effect = stressed_data - data
            heatmap_data.append(stress_effect)
    
    # Combine heatmap data for plotting
    if heatmap_data:
        heatmap_df = pd.DataFrame(heatmap_data, index=[f'{sf} ({d} days)' for d in stress_durations for sf in stress_factors]).T
        heatmap_fig = px.imshow(heatmap_df.T, color_continuous_scale='RdYlBu', labels={'x': 'Stress Factor & Duration', 'y': 'Date', 'color': 'Stress Impact'})
        heatmap_fig.update_layout(
            title='Stress Impact Heatmap',
            xaxis_title='Stress Factor & Duration',
            yaxis_title='Date',
            height=400,
            width=800
        )
        # Add heatmap to the main figure
        fig.add_trace(heatmap_fig.data[0])
    
    # Adjust layout for the main plot
    fig.update_layout(
        title='Original vs Stressed Data Over Multiple Time Frames',
        xaxis_title='Date',
        yaxis_title='Value',
        legend_title='Legend',
        legend=dict(
            x=1.1,  # Move the legend to the right
            y=1,     # Position at the top
            traceorder='normal',
            orientation='v'  # Vertical orientation
        ),
        height=600,  # Increase height
        width=1200,  # Increase width
        hovermode='closest'  # Show closest data points on hover
    )

    return fig

# Scenario-Based Weighted Stress Test
def weighted_stress_test(data: pd.Series, shock_percentage: float, stress_factors: list, probabilities: list, severity_level: str, duration: int, sector: str = None) -> pd.Series:
    """
    Apply weighted stress test scenarios based on the probability of each stress factor occurring.
    
    Parameters:
    - data: Stock or portfolio data (as pandas Series)
    - shock_percentage: Percentage of shock
    - stress_factors: List of stress factors
    - probabilities: List of probabilities associated with each stress factor
    - severity_level: Severity level of stress
    - duration: Duration of stress
    - sector: Sector for specific adjustments
    
    Returns:
    - Weighted stressed data as pandas Series
    """
    combined_stress = np.zeros(len(data))
    
    for stress_factor, probability in zip(stress_factors, probabilities):
        stress = stress_test_scenario(data, shock_percentage, stress_factor, severity_level, duration, sector)
        combined_stress += stress * probability  # Weight each stress by its probability

    return combined_stress


import pandas as pd
import plotly.express as px

# Generate heatmap for stress impact
def generate_stress_heatmap(data: pd.Series, stress_factors: list, shock_percentage: float, severity_level: str, stress_duration: int):
    heatmap_data = []
    for factor in stress_factors:
        # Apply the stress test to get stressed data
        stress_effect = weighted_stress_test(data, shock_percentage, [factor], [1], severity_level, stress_duration)
        heatmap_data.append(stress_effect - data)

    # Convert heatmap data to DataFrame for visualization
    heatmap_df = pd.DataFrame(heatmap_data, index=stress_factors).T
    
    # Plot the heatmap
    heatmap_fig = px.imshow(
        heatmap_df.T,
        color_continuous_scale='RdYlBu',
        labels={'x': 'Date', 'y': 'Stress Factor', 'color': 'Impact'},
        title='Stress Impact Heatmap'
    )
    heatmap_fig.update_layout(
        height=600,
        width=1200
    )

    return heatmap_fig




import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional, Input
from tensorflow.keras import regularizers
from tensorflow.keras.callbacks import EarlyStopping
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Data preprocessing function
def preprocess_data(data, window_size=60):
    data = np.array(data)  # Convert data to a NumPy array
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data.reshape(-1, 1))  # Ensure data is 2D
    
    x_train, y_train = [], []
    for i in range(window_size, len(scaled_data)):
        x_train.append(scaled_data[i-window_size:i, 0])
        y_train.append(scaled_data[i, 0])
    
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    
    return x_train, y_train, scaler

# LSTM model creation function
def create_lstm_model(input_shape):
    model = Sequential()
    model.add(Input(shape=input_shape))
    model.add(Bidirectional(LSTM(units=150, return_sequences=True, kernel_regularizer=regularizers.l2(0.01))))
    model.add(Dropout(0.2))
    model.add(Bidirectional(LSTM(units=150, return_sequences=False, kernel_regularizer=regularizers.l2(0.01))))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# LSTM model fitting function
def fit_lstm_model(data, window_size=60, epochs=20, batch_size=64):
    x_train, y_train, scaler = preprocess_data(data, window_size)
    model = create_lstm_model((x_train.shape[1], 1))
    
    # Early stopping
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    
    history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2, verbose=2, callbacks=[early_stopping])
    return model, scaler
# LSTM prediction function for prices
def predict_with_lstm(model, scaler, data, duration, window_size=60):
    data = np.array(data)  # Convert data to a NumPy array
    scaled_data = scaler.transform(data.reshape(-1, 1))  # Ensure data is 2D
    predictions = []

    for _ in range(duration):
        last_window = scaled_data[-window_size:]
        last_window = last_window.reshape(1, last_window.shape[0], 1)
        
        pred_price = model.predict(last_window)
        noise = np.random.normal(0, 0.02)  # Adding Gaussian noise
        predictions.append(pred_price[0, 0] + noise)
        
        # Append prediction to the data
        scaled_data = np.append(scaled_data, [[pred_price[0, 0]]], axis=0)
    
    predictions = np.array(predictions).reshape(-1, 1)
    predictions = scaler.inverse_transform(predictions)
    
    return predictions

# Function to evaluate model performance
def evaluate_model(model, scaler, data, window_size=60):
    x_train, y_train, _ = preprocess_data(data, window_size)
    y_pred = model.predict(x_train)

    # Rescale predictions
    y_train_rescaled = scaler.inverse_transform(y_train.reshape(-1, 1))
    y_pred_rescaled = scaler.inverse_transform(y_pred)
    
    # Calculate metrics
    mse = mean_squared_error(y_train_rescaled, y_pred_rescaled)
    r2 = r2_score(y_train_rescaled, y_pred_rescaled)
    
    return mse, r2
    
    mse, r2 = evaluate_model(model, scaler, data)
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")



# Plot forecasted values
def plot_forecast(predictions, start_date, duration, investment_amount):
    if isinstance(predictions, pd.Series):
        predictions = predictions.values
    
    future_dates = pd.date_range(start=start_date, periods=duration)
    
    forecast_df = pd.DataFrame({
        'Date': future_dates,
        'Open': predictions.flatten() * (1 + np.random.uniform(-0.01, 0.01, size=duration)),
        'High': predictions.flatten() * (1 + np.random.uniform(0, 0.02, size=duration)),
        'Low': predictions.flatten() * (1 - np.random.uniform(0, 0.02, size=duration)),
        'Close': predictions.flatten()
    })

    forecast_df['High'] = forecast_df[['Open', 'High']].max(axis=1)
    forecast_df['Low'] = forecast_df[['Open', 'Low']].min(axis=1)
    
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=forecast_df['Date'],
        open=forecast_df['Open'],
        high=forecast_df['High'],
        low=forecast_df['Low'],
        close=forecast_df['Close'],
        name='Predicted Prices'
    ))

    fig.add_annotation(
        x=future_dates[0], 
        y=forecast_df['Close'].iloc[0], 
        text=f'Initial Investment: ${investment_amount}',
        showarrow=True,
        arrowhead=1
    )

    fig.update_layout(
        title='Forecasted Prices',
        xaxis_title='Date',
        yaxis_title='Predicted Value',
        yaxis_showticklabels=True,
        
        height=600,
        width=1200,
        xaxis_rangeslider_visible=True
    )
    
    return fig
def calculate_returns(predictions, initial_investment):
    if predictions.size == 0:
        return np.array([]), initial_investment
    
    initial_price = predictions[0]
    if initial_price == 0:
        return np.array([]), initial_investment
    
    returns = (predictions - initial_price) / initial_price
    total_returns = (1 + returns).prod() - 1
    total_value = initial_investment * (1 + total_returns)
    
    return returns, total_value

def plot_returns(predictions, investment_amount):
    # Calculate returns and total returns
    initial_value = predictions.flatten()[0]
    returns = (predictions.flatten() - initial_value) / initial_value
    total_returns = (returns + 1).prod() - 1
    total_investment = investment_amount * (1 + total_returns)
    profit_or_loss = total_investment - investment_amount

    # Plot returns
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(range(len(returns))),
        y=returns,
        mode='lines+markers',
        name='Returns',
        line=dict(color='blue')
    ))

    fig.add_annotation(
        x=len(returns) - 1,
        y=returns[-1],
        text=f'Total Return Amount: ${profit_or_loss:.2f}',
        showarrow=True,
        arrowhead=1
    )

    fig.update_layout(
        title='Investment Returns Over Time',
        xaxis_title='Time',
        yaxis_title='Returns',
        height=600,
        width=1200
    )

    return fig



"""

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
import plotly.express as px
import plotly.io as pio
import logging

def calculate_technical_indicators(df):
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
    df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
    
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['Bollinger_High'] = df['SMA_20'] + 2 * df['Close'].rolling(window=20).std()
    df['Bollinger_Low'] = df['SMA_20'] - 2 * df['Close'].rolling(window=20).std()
    
    df['VWAP'] = (df['Volume'] * df['Close']).cumsum() / df['Volume'].cumsum()

    return df

def filter_data_by_selection(sectors, companies, file_paths):
    combined_data = []
    for sector in sectors:
        for company in companies:
            if company in file_paths.get(sector, {}):
                file_path = file_paths[sector][company]
                df = pd.read_csv(file_path)
                df = calculate_technical_indicators(df)
                df['Company'] = company
                df['Sector'] = sector
                combined_data.append(df)
            else:
                logging.warning(f"File path missing for sector: {sector}, company: {company}")
                
    if not combined_data:
        logging.error("No data combined; check file paths and filters.")
    
    result = pd.concat(combined_data, ignore_index=True)
    
    logging.debug(f"Filtered Data Head: {result.head()}")
    logging.debug(f"Filtered Data Columns: {result.columns}")
    
    return result

def calculate_standard_deviation(filtered_data):
    filtered_data['Return'] = filtered_data['Close'].pct_change()
    filtered_data['Standard_Deviation'] = filtered_data['Return'].rolling(window=20).std()  # 20-period rolling standard deviation
    
    # Drop NaN values that result from the rolling operation
    filtered_data = filtered_data.dropna(subset=['Standard_Deviation'])
    return filtered_data

def calculate_optimal_portfolio(df, sectors, companies, amount, risk_tolerance, investment_objective):
    features = ['SMA_10', 'SMA_50', 'EMA_10', 'EMA_50', 'RSI', 'MACD', 'Bollinger_High', 'Bollinger_Low', 'VWAP']
    
    df = df.dropna(subset=features)
    
    X = df[features]
    y = df['Close'].pct_change().shift(-1).dropna()
    
    X = X.iloc[:len(y)]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = xgb.XGBRegressor()
    model.fit(X_train, y_train)  # Train the model
    
    y_pred = model.predict(X_test)
    
    # Use predictions (y_pred) as returns
    df_pred = X_test.copy()
    df_pred['Predicted_Return'] = y_pred
    df_pred = df_pred.reset_index(drop=True)
    
    logging.debug(f"Predicted Returns Head: {df_pred.head()}")
    
    portfolio = {
        'Sectors': sectors,
        'Companies': companies,
        'Investment Amount': amount,
        'Risk Tolerance': risk_tolerance,
        'Investment Objective': investment_objective
    }
    
    return portfolio, model

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio

# Calculate covariance matrix
def calculate_covariance_matrix(df):
    return df.pivot_table(index='Date', columns='Company', values='Predicted_Return').cov()

# Plot efficient frontier
def plot_efficient_frontier(predicted_returns, cov_matrix):
    num_portfolios = 5000
    results = np.zeros((3, num_portfolios))

    for i in range(num_portfolios):
        weights = np.random.random(len(predicted_returns))
        weights /= np.sum(weights)
        portfolio_return = np.sum(weights * predicted_returns) * 252
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 252, weights)))
        sharpe_ratio = (portfolio_return - 0.01) / portfolio_volatility
        results[0, i] = portfolio_return
        results[1, i] = portfolio_volatility
        results[2, i] = sharpe_ratio

    results_df = pd.DataFrame(results.T, columns=['Return', 'Volatility', 'Sharpe Ratio'])
    
    fig = px.scatter(
        results_df,
        x='Volatility',
        y='Return',
        color='Sharpe Ratio',
        title='Efficient Frontier',
        labels={'Sharpe Ratio': 'Sharpe Ratio'},
        color_continuous_scale='Viridis'
    )
    fig.update_layout(width=1200, height=600)
    return fig

# Plot risk-return quadrant
def plot_risk_return_quadrant(df):
    if 'Standard_Deviation' not in df.columns or 'Predicted_Return' not in df.columns:
        raise ValueError("The DataFrame must contain 'Standard_Deviation' and 'Predicted_Return' columns.")
    
    fig = px.scatter(
        df,
        x='Standard_Deviation',
        y='Predicted_Return',
        color='Sector',
        size='Close',
        title='Sector Risk-Return Quadrant',
        labels={'Standard_Deviation': 'Risk (Standard Deviation)', 'Predicted_Return': 'Predicted Return'}
    )
    fig.update_layout(width=1200, height=600)
    return fig

# Plot optimization surface
def plot_optimization_surface(predicted_returns, cov_matrix):
    num_portfolios = 5000
    results = np.zeros((3, num_portfolios))

    for i in range(num_portfolios):
        weights = np.random.random(len(predicted_returns))
        weights /= np.sum(weights)
        portfolio_return = np.sum(weights * predicted_returns) * 252
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 252, weights)))
        sharpe_ratio = (portfolio_return - 0.01) / portfolio_volatility
        results[0, i] = portfolio_return
        results[1, i] = portfolio_volatility
        results[2, i] = sharpe_ratio

    results_df = pd.DataFrame(results.T, columns=['Return', 'Volatility', 'Sharpe Ratio'])

    fig = px.scatter_3d(
        results_df,
        x='Volatility',
        y='Return',
        z='Sharpe Ratio',
        color='Sharpe Ratio',
        title='Optimization Surface',
        labels={'Sharpe Ratio': 'Sharpe Ratio'},
        color_continuous_scale='Viridis'
    )
    fig.update_layout(width=1200, height=600)
    return fig

# Create risk-return table
def create_risk_return_table(df, amount):
    # Filter the dataframe to include only unique companies
    companies = df['Company'].unique()
    
    if len(companies) == 0:
        return '<p>No data available for the selected companies.</p>'
    
    num_companies = len(companies)
    investment_per_company = amount / num_companies
    
    df_unique = df.drop_duplicates(subset=['Company'])
    df_unique['Investment'] = investment_per_company
    df_unique['Profit/Loss'] = df_unique['Close'] - df_unique['Investment']
    df_unique['Percentage Change'] = (df_unique['Profit/Loss'] / df_unique['Investment']) * 100
    
    table_html = (
        '<table class="table table-bordered">'
        '<thead>'
        '<tr><th>Company</th><th>Investment</th><th>Close</th><th>Profit/Loss</th><th>Percentage Change</th></tr>'
        '</thead>'
        '<tbody>'
    )

    for i, row in df_unique.iterrows():
        table_html += f"<tr><td>{row['Company']}</td><td>{row['Investment']:.2f}</td><td>{row['Close']:.2f}</td><td>{row['Profit/Loss']:.2f}</td><td>{row['Percentage Change']:.2f}%</td></tr>"

    table_html += '</tbody></table>'
    
    return table_html

def create_dashboard(filtered_data, optimal_portfolio, model, amount):
    
    response = {'pie_chart': '', 'scatter_plot': '', 'efficient_frontier': '', 'risk_return_quadrant': '', 'optimization_surface': '', 'risk_return_table': ''}
    
    if filtered_data.empty:
        response['error'] = "No data available for the selected operation."
        return response
    
    # Ensure 'Predicted_Return' is present
    if 'Predicted_Return' not in filtered_data.columns:
        logging.debug("Predicted_Return not found, generating predictions...")
        features = ['SMA_10', 'SMA_50', 'EMA_10', 'EMA_50', 'RSI', 'MACD', 'Bollinger_High', 'Bollinger_Low', 'VWAP']
        X = filtered_data[features]
        
        # Use the trained model to generate predictions
        filtered_data['Predicted_Return'] = model.predict(X)
        
        logging.debug("Generated Predicted_Return:")
        logging.debug(filtered_data['Predicted_Return'].head())
    
    # Add standard deviation calculation
    filtered_data = calculate_standard_deviation(filtered_data)
    
    # Pie chart visualization based on predicted returns
    pie_chart = px.pie(filtered_data, names='Company', values='Predicted_Return', title='Portfolio Composition')
    response['pie_chart'] = pio.to_html(pie_chart, full_html=False)
    
    # Scatter plot visualization for risk-return analysis
    filtered_data['Return_Color'] = np.where(filtered_data['Predicted_Return'] >= 0, 'green', 'red')
    
    scatter_plot = px.scatter(
        filtered_data,
        x='Standard_Deviation',  # Now 'Standard_Deviation' exists in the data
        y='Predicted_Return',
        color='Return_Color',
        title='Risk-Return Analysis',
        labels={'Return_Color': 'Return Indicator'}
    )
    response['scatter_plot'] = pio.to_html(scatter_plot, full_html=False)

    # Covariance matrix for portfolio optimization
    cov_matrix = calculate_covariance_matrix(filtered_data)
    predicted_returns = filtered_data.groupby('Company')['Predicted_Return'].mean().values
    
    # Plot efficient frontier
    efficient_frontier = plot_efficient_frontier(predicted_returns, cov_matrix)
    response['efficient_frontier'] = pio.to_html(efficient_frontier, full_html=False)
    
    # Plot risk-return quadrant
    risk_return_quadrant = plot_risk_return_quadrant(filtered_data)
    response['risk_return_quadrant'] = pio.to_html(risk_return_quadrant, full_html=False)
    
    # Plot optimization surface
    optimization_surface = plot_optimization_surface(predicted_returns, cov_matrix)
    response['optimization_surface'] = pio.to_html(optimization_surface, full_html=False)
    
    # Create risk-return table
    risk_return_table = create_risk_return_table(filtered_data, amount)
    response['risk_return_table'] = risk_return_table
    
    return response
    
    """
    
"""    
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import plotly.express as px
import plotly.io as pio

# Function to calculate technical indicators
def calculate_technical_indicators(df):
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
    df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
    
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['Bollinger_High'] = df['SMA_20'] + 2 * df['Close'].rolling(window=20).std()
    df['Bollinger_Low'] = df['SMA_20'] - 2 * df['Close'].rolling(window=20).std()
    
    df['VWAP'] = (df['Volume'] * df['Close']).cumsum() / df['Volume'].cumsum()

    return df

# Function to filter and combine data based on selected sectors and companies
def filter_data_by_selection(sectors, companies, file_paths):
    combined_data = []
    for sector in sectors:
        for company in companies:
            if company in file_paths.get(sector, {}):
                file_path = file_paths[sector][company]
                df = pd.read_csv(file_path)
                df = calculate_technical_indicators(df)
                df['Company'] = company
                df['Sector'] = sector
                combined_data.append(df)
            else:
                print(f"File path missing for sector: {sector}, company: {company}")
                
    if not combined_data:
        raise ValueError("No data combined; check file paths and filters.")
    
    result = pd.concat(combined_data, ignore_index=True)
    
    # Print lengths for debugging
    print(f"Number of rows in combined data: {len(result)}")
    
    return result

# Function to calculate returns and covariance matrix
def calculate_returns_and_covariance(data):
    data['Return'] = data['Close'].pct_change()
    
    # Pivot data to have companies as columns
    returns_pivot = data.pivot_table(index='Date', columns='Company', values='Return')
    
    # Check if there are missing values in the pivoted DataFrame
    if returns_pivot.isnull().any().any():
        print("Warning: Pivoted returns data contains missing values")
        returns_pivot = returns_pivot.fillna(0)  # or use returns_pivot.ffill() for forward-fill
    
    returns_mean = returns_pivot.mean()
    cov_matrix = returns_pivot.cov()
    
    return returns_mean, cov_matrix

# Mean-Variance Optimization
def mean_variance_optimization(expected_returns, cov_matrix, maximize_return=False):
    def objective(weights):
        if maximize_return:
            return -np.dot(weights, expected_returns)  # Maximize return
        return np.dot(weights.T, np.dot(cov_matrix, weights))  # Minimize risk
    
    def constraint(weights):
        return np.sum(weights) - 1
    
    num_assets = len(expected_returns)
    bounds = [(0, 1) for _ in range(num_assets)]
    constraints = [{'type': 'eq', 'fun': constraint}]
    
    result = minimize(objective, num_assets * [1./num_assets], bounds=bounds, constraints=constraints)
    return result.x

# Risk Parity Optimization
def risk_parity_optimization(cov_matrix):
    def risk_contribution(weights):
        port_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
        marginal_contribution = np.dot(cov_matrix, weights)
        risk_contribution = weights * marginal_contribution
        return risk_contribution / np.sqrt(port_variance)
    
    def objective(weights):
        risk_contributions = risk_contribution(weights)
        return np.sum((risk_contributions - np.mean(risk_contributions))**2)
    
    num_assets = cov_matrix.shape[0]
    bounds = [(0, 1) for _ in range(num_assets)]
    constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
    
    result = minimize(objective, num_assets * [1./num_assets], bounds=bounds, constraints=constraints)
    return result.x

# Minimum Variance Optimization
def minimum_variance_optimization(cov_matrix):
    def objective(weights):
        return np.dot(weights.T, np.dot(cov_matrix, weights))
    
    num_assets = cov_matrix.shape[0]
    bounds = [(0, 1) for _ in range(num_assets)]
    constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
    
    result = minimize(objective, num_assets * [1./num_assets], bounds=bounds, constraints=constraints)
    return result.x

# Select and perform the optimization model based on the investment objective
def select_optimization_model(objective_type, expected_returns, cov_matrix):
    if objective_type == 'Balanced Risk and Return':
        return mean_variance_optimization(expected_returns, cov_matrix)
    elif objective_type == 'Minimize Risk':
        return risk_parity_optimization(cov_matrix)
    elif objective_type == 'Maximize Return':
        return mean_variance_optimization(expected_returns, cov_matrix, maximize_return=True)
    else:
        raise ValueError("Invalid investment objective. Choose from 'Balanced Risk and Return', 'Minimize Risk', or 'Maximize Return'.")


# Function to calculate technical indicators
def calculate_technical_indicators(df):
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
    df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
    
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['Bollinger_High'] = df['SMA_20'] + 2 * df['Close'].rolling(window=20).std()
    df['Bollinger_Low'] = df['SMA_20'] - 2 * df['Close'].rolling(window=20).std()
    
    df['VWAP'] = (df['Volume'] * df['Close']).cumsum() / df['Volume'].cumsum()

    return df


import numpy as np
import pandas as pd
from scipy.optimize import minimize
import plotly.express as px

# Function to filter and combine data based on selected sectors and companies
def filter_data_by_selection(sectors, companies, file_paths):
    combined_data = []
    for sector in sectors:
        for company in companies:
            if company in file_paths.get(sector, {}):
                file_path = file_paths[sector][company]
                df = pd.read_csv(file_path)
                df = calculate_technical_indicators(df)
                df['Company'] = company
                df['Sector'] = sector
                combined_data.append(df)
                
    result = pd.concat(combined_data, ignore_index=True)
    return result

# Function to calculate returns and covariance matrix
def calculate_returns_and_covariance(data):
    data['Return'] = data.groupby('Company')['Close'].pct_change()
    
    returns_pivot = data.pivot_table(index='Date', columns='Company', values='Return')
    returns_pivot = returns_pivot.dropna()  # Remove any rows with NaN values

    returns_mean = returns_pivot.mean()
    cov_matrix = returns_pivot.cov()
    
    return returns_mean, cov_matrix

# Mean-Variance Optimization
def mean_variance_optimization(expected_returns, cov_matrix, maximize_return=False):
    def objective(weights):
        portfolio_return = np.dot(weights, expected_returns)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        if maximize_return:
            return -portfolio_return
        else:
            return portfolio_volatility - 0.01 * portfolio_return  # Balance risk and return

    def constraint(weights):
        return np.sum(weights) - 1

    num_assets = len(expected_returns)
    bounds = [(0, 1) for _ in range(num_assets)]
    constraints = [{'type': 'eq', 'fun': constraint}]
    
    initial_weights = np.array([1.0 / num_assets] * num_assets)
    result = minimize(objective, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    
    return result.x

# Convert Weights to Investment

def convert_weights_to_investment(weights, companies, amount, sectors):
    # Ensure lengths of all inputs match
    if len(weights) != len(companies):
        raise ValueError("Lengths of weights and companies do not match.")
    
    # Assuming weights are for companies only
    investment_amount = amount / len(weights)
    
    allocation_data = {
        'Company': companies,
        'Sector': [sector for sector in sectors for _ in range(len(weights)//len(sectors))],  # Adjust based on how sectors are assigned
        'Weight': weights,
        'Investment': [investment_amount * weight for weight in weights]
    }

    allocation_df = pd.DataFrame(allocation_data)
    
    return allocation_df

# Plot Risk-Return Scatter
def plot_risk_return_scatter(returns, risk, labels, title):
    df = pd.DataFrame({
        'Return': returns,
        'Risk': risk,
        'Label': labels
    })
    fig = px.scatter(df, x='Risk', y='Return', text='Label', title=title,
                     labels={'Return': 'Expected Return', 'Risk': 'Risk (Std Dev)'},
                     template='plotly_white')
    fig.update_traces(textposition='top center')
    return fig

# Plot Sector Performance
def plot_sector_performance(allocation_df, title):
    sector_performance = allocation_df.groupby('Sector')['Investment'].sum().reset_index()
    sector_performance['Performance'] = sector_performance['Investment']
    
    print(f"Sector Performance Data: {sector_performance}")  # Debugging output
    
    fig = px.bar(sector_performance, x='Sector', y='Performance', title=title,
                 labels={'Performance': 'Investment Amount'},
                 template='plotly_white')
    
    return fig

# Plot Pie Charts for Allocation
def plot_pie_charts(allocation_df, title):
    allocation_df = allocation_df[allocation_df['Investment'] > 0]
    sector_allocation = allocation_df.groupby('Sector')['Investment'].sum().reset_index()

    # Company allocation
    if allocation_df['Investment'].nunique() > 1:
        fig_company_allocation = px.pie(allocation_df, names='Company', values='Investment', title=f'{title} - Company Allocation')
    else:
        fig_company_allocation = px.bar(allocation_df, x='Company', y='Investment', title=f'{title} - Company Allocation')

    # Sector allocation
    if sector_allocation['Investment'].nunique() > 1:
        fig_sector_allocation = px.pie(sector_allocation, names='Sector', values='Investment', title=f'{title} - Sector Allocation')
    else:
        fig_sector_allocation = px.bar(sector_allocation, x='Sector', y='Investment', title=f'{title} - Sector Allocation')

    return fig_company_allocation, fig_sector_allocation

# Create Performance Metrics Dashboard
def create_performance_metrics_dashboard(return_metric, risk_metric, top_performers):
    dashboard = f""""""
    <div>
        <h3>Performance Metrics</h3>
        <p><strong>Total Return:</strong> {return_metric:.2f}%</p>
        <p><strong>Total Risk:</strong> {risk_metric:.2f}%</p>
    </div>
    <div>
        <h3>Top Performers</h3>
        <ul>
    """"""
    for performer in top_performers:
        dashboard += f"<li>{performer}</li>"
    
    dashboard += "</ul></div>"
    return dashboard

# Create Investment Breakdown
def create_investment_breakdown(investments, labels, sectors):
    total_investment = sum(investments)
    breakdown_df = pd.DataFrame({
        'Label': labels,
        'Investment': investments,
        'Percentage': [(x / total_investment) * 100 for x in investments],
        'Sector': sectors
    })
    return breakdown_df

def select_optimization_model(objective_type, expected_returns, cov_matrix):
    if objective_type == 'Balanced Risk and Return':
        weights = mean_variance_optimization(expected_returns, cov_matrix)
    
    elif objective_type == 'Minimize Risk':
        weights = mean_variance_optimization(expected_returns, cov_matrix, maximize_return=False)
    
    elif objective_type == 'Maximize Return':
        weights = mean_variance_optimization(expected_returns, cov_matrix, maximize_return=True)
    
    else:
        raise ValueError("Invalid investment objective.")
    
    # Normalize weights to ensure they sum to 1
    weights = np.maximum(weights, 0.01)  # Ensure no weight is exactly zero
    weights /= np.sum(weights)
    
    return weights
"""
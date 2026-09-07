from flask import Blueprint, request, render_template, jsonify
import pandas as pd
import os
from app.models import (
    calculate_garch_volatility,
    calculate_moving_averages,
    calculate_ema,
    
    market_trends,
    
    stress_test_scenario,
    apply_stress_tests,
    fit_lstm_model,
    predict_with_lstm,
    plot_forecast,calculate_var, calculate_es, calculate_sharpe_ratio,
    calculate_risk_matrix, plot_monte_carlo_simulation,
    plot_cumulative_return, plot_drawdown, plot_risk_matrix_heatmap,
    plot_risk_metrics_half_donut,
    plot_returns,
    calculate_returns,
    
    
    generate_stress_heatmap,
    apply_stress_tests
)

# Define the Blueprint
main = Blueprint('main', __name__)

# Define file paths
file_paths = {
    'IT': {
        'Google': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/IT/google.csv",
        'Apple': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/IT/apple.csv",
        'Intel': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/IT/intel.csv",
        'Microsoft': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/IT/microsoft.csv",
        'Nvidia': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/IT/nvidia.csv"
    },
    'Finance': {
        'Bank of America': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Finance/Bank_of_America.csv",
        'Berkshire Hathaway': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Finance/Berkshire_Hathaway.csv",
        'Goldman Sachs': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Finance/Goldman_Sachs.csv",
        'JPMorgan': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Finance/JPMorgan.csv",
        'Wells Fargo': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Finance/Wells_Fargo.csv"
    },
    'Healthcare': {
        'Abbvie': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Health_care/AbbVie.csv",
        'Johnson & Johnson': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Health_care/J&J.csv",
        'Merck': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Health_care/Merck.csv",
        'Pfizer': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Health_care/Pfizer.csv",
        'UnitedHealth': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Health_care/UnitedHealth.csv"
    },
    'Real Estate': {
        'AvalonBay': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Real_Estate/AvalonBay.csv",
        'Prologis Inc': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Real_Estate/Prologis_Inc.csv",
        'Public Storage': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Real_Estate/Public_Storage.csv",
        'Realty Income': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Real_Estate/Realty_Income.csv",
        'Simon Property': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Real_Estate/Simon_Property.csv"
    },
    'Energy': {
        'Chevron Corporation': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Energy/Chevron_Corporation.csv",
        'ConocoPhillips': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Energy/ConocoPhillips.csv",
        'Exxon Mobil': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Energy/Exxon_Mobil.csv",
        'NextEra': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Energy/NextEra.csv",
        'TotalEnergies': "C:/Users/hp/OneDrive/Documents/Christ University/Trimester_4/Project_Lab/datasets/Energy/TotalEnergies.csv"
    }
}
import os
# Define routes
from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)

# Route for the services page
@main.route('/service')
def service():
    return render_template('service.html')

# Route for the model page
@main.route('/model')
def model():
    return render_template('index.html')

# Route for the team page
@main.route('/team')
def team():
    return render_template('team.html')

# Route for the about page
@main.route('/about')
def about():
    return render_template('about.html')

# Route for the blog page
@main.route('/blog')
def blog():
    return render_template('blog.html')

# Route for the why page
@main.route('/why')
def why():
    return render_template('why.html')

# Home route (index1.html)
@main.route('/')
def home():
    return render_template('index1.html')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/market_trends', methods=['GET', 'POST'])
def market_trends_form():
    if request.method == 'POST':
        sector = request.form.get('sector')
        company = request.form.get('company')
        
        # Move file_path inside the POST block
        file_path = file_paths.get(sector, {}).get(company)
        if file_path:
            data = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
            volatility_fig, price_ma_fig, ema_fig, bollinger_fig = market_trends(data['Close'])
            return render_template(
                'solution1.html',
                operation='market_trends',
                sector=sector,
                company=company,
                market_trends_plot_volatility=volatility_fig.to_html(full_html=False),
                market_trends_plot_price_ma=price_ma_fig.to_html(full_html=False),
                market_trends_plot_ema=ema_fig.to_html(full_html=False),
                market_trends_plot_bollinger=bollinger_fig.to_html(full_html=False)
            )
        else:
            return "Error: Invalid sector or company", 400

    # Handle GET requests, possibly by rendering the form
    return render_template('market_trends.html')


# Define file paths and other functions here...

def index():
    return render_template('index1.html')

"""
from flask import render_template, request
import pandas as pd
from app.models import (
    calculate_var, calculate_es, calculate_sharpe_ratio, plot_monte_carlo_simulation, 
    plot_cumulative_return, plot_drawdown, calculate_risk_matrix, 
    plot_risk_matrix_heatmap, plot_risk_metrics_half_donut
)

@main.route('/risk_assessment', methods=['GET', 'POST'])
def risk_assessment_form():
    if request.method == 'POST':
        sector = request.form.get('sector')
        company = request.form.get('company')
        duration = request.form.get('duration')

        # Retrieve the file path for the company and sector
        file_path = file_paths.get(sector, {}).get(company)
        if file_path:
            data = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')

            # Generate plots for risk assessment
            probabilities, impacts, risk_levels = calculate_risk_matrix(data['Close'])
            risk_fig = plot_risk_matrix_heatmap(probabilities, impacts, risk_levels)
            monte_carlo_fig = plot_monte_carlo_simulation(data['Close'])
            cumulative_return_fig = plot_cumulative_return(data['Close'])
            drawdown_fig = plot_drawdown(data['Close'])

            # Calculate risk metrics
            var = calculate_var(data['Close'])
            es_values = calculate_es(data['Close'])  # ES at different confidence levels
            sharpe_ratio = calculate_sharpe_ratio(data['Close'])
            max_drawdown = plot_drawdown(data['Close']).data[0].y.min()  # Extract the max drawdown

            # Generate half-donut chart for risk metrics
            risk_metrics_half_donut_fig = plot_risk_metrics_half_donut(
                var, es_values[0.95], max_drawdown, sharpe_ratio
            )

            # Render the results in the solution2 template
            return render_template(
                'solution2.html',
                operation='risk_assessment',
                risk_plot=risk_fig.to_html(full_html=False),
                monte_carlo_plot=monte_carlo_fig.to_html(full_html=False),
                cumulative_return_plot=cumulative_return_fig.to_html(full_html=False),
                drawdown_plot=drawdown_fig.to_html(full_html=False),
                risk_metrics_plot=risk_metrics_half_donut_fig.to_html(full_html=False)
            )
        else:
            return "File not found", 404

    return render_template('risk_assessment.html')

    
    """
    
    
from flask import render_template, request
import pandas as pd
from app.models import (
    calculate_var, calculate_es, calculate_sharpe_ratio, plot_monte_carlo_simulation, 
    plot_cumulative_return, plot_drawdown, calculate_risk_matrix, 
    plot_risk_matrix_heatmap, plot_risk_metrics_half_donut
)

@main.route('/risk_assessment', methods=['GET', 'POST'])
def risk_assessment_form():
    if request.method == 'POST':
        sector = request.form.get('sector')
        company = request.form.get('company')
        duration = request.form.get('duration')

        # Retrieve the file path for the company and sector
        file_path = file_paths.get(sector, {}).get(company)
        if file_path:
            data = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')

            # Generate plots for risk assessment
            probabilities, impacts, risk_levels = calculate_risk_matrix(data['Close'])
            risk_fig = plot_risk_matrix_heatmap(probabilities, impacts, risk_levels)
            monte_carlo_fig = plot_monte_carlo_simulation(data['Close'])
            cumulative_return_fig = plot_cumulative_return(data['Close'])
            drawdown_fig = plot_drawdown(data['Close'])

            # Calculate risk metrics
            var = calculate_var(data['Close'])
            es_values = calculate_es(data['Close'])  # ES at different confidence levels
            sharpe_ratio = calculate_sharpe_ratio(data['Close'])

            # Calculate max drawdown directly from cumulative return
            cumulative_return = (1 + data['Close'].pct_change().dropna()).cumprod()
            max_drawdown = (cumulative_return / cumulative_return.cummax() - 1).min()

            # Generate half-donut chart for risk metrics
            risk_metrics_half_donut_fig = plot_risk_metrics_half_donut(
                var, es_values[0.95], max_drawdown, sharpe_ratio
            )

            # Render the results in the solution2 template
            return render_template(
                'solution2.html',
                operation='risk_assessment',
                risk_plot=risk_fig.to_html(full_html=False),
                monte_carlo_plot=monte_carlo_fig.to_html(full_html=False),
                cumulative_return_plot=cumulative_return_fig.to_html(full_html=False),
                drawdown_plot=drawdown_fig.to_html(full_html=False),
                risk_metrics_plot=risk_metrics_half_donut_fig.to_html(full_html=False)
            )
        else:
            return "File not found", 404

    return render_template('risk_assessment.html')


def index():
    return render_template('index1.html')

@main.route('/forecast', methods=['GET', 'POST'])
def forecast_form():
    if request.method == 'POST':
        sector = request.form.get('sector')
        company = request.form.get('company')
        duration = request.form.get('duration')
        investment_amount = request.form.get('investment_amount')

        if not sector or not company or not duration or not investment_amount:
            return jsonify({"error": "All fields are required"}), 400

        try:
            if 'm' in duration:
                duration = int(duration.replace('m', '')) * 30
            else:
                duration = int(duration) * 365
            investment_amount = float(investment_amount)
        except ValueError:
            return jsonify({"error": "Invalid duration or investment amount"}), 400

        file_path = file_paths.get(sector, {}).get(company)
        if file_path:
            data = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
            future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=duration)
            model, scaler = fit_lstm_model(data['Close'].values)
            predictions = predict_with_lstm(model, scaler, data['Close'].values, duration)

            # Plot forecasts and returns
            forecast_fig = plot_forecast(predictions, start_date=future_dates[0], duration=duration, investment_amount=investment_amount)
            returns_fig = plot_returns(predictions, investment_amount)

            forecast_plot = forecast_fig.to_html(full_html=False)
            returns_plot = returns_fig.to_html(full_html=False)

            return render_template('solution4.html', 
                                   operation='forecast',
                                   sector=sector,
                                   company=company,
                                   duration=duration,
                                   investment_amount=investment_amount,
                                   forecast_plot=forecast_plot,
                                   returns_plot=returns_plot)
        else:
            return jsonify({"error": "File path not found for the selected sector and company"}), 404
    
    return render_template('forecast.html')







@main.route('/stress_testing', methods=['GET', 'POST'])
def stress_test_form():
    if request.method == 'POST':
        # Extract form inputs
        sector = request.form.get('sector')
        company = request.form.get('company')
        shock_percentage = float(request.form.get('shock_percentage'))
        stress_factors = request.form.getlist('stress_factors')
        severity_level = request.form.get('severity_level')
        stress_duration = int(request.form.get('stress_duration'))

        # Fetch the file path based on sector and company
        file_path = file_paths.get(sector, {}).get(company)
        if file_path:
            # Load data from the file
            data = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')

            # Generate the stress test plot (Main stress test visualization)
            fig = apply_stress_tests(data['Close'], shock_percentage, stress_factors, severity_level, [stress_duration])

            # Generate the heatmap for stress impact (Uses function from models.py)
            heatmap_fig = generate_stress_heatmap(data['Close'], stress_factors, shock_percentage, severity_level, stress_duration)

            # Convert the plots to HTML for rendering
            stress_testing_plot = fig.to_html(full_html=False)
            heatmap_plot = heatmap_fig.to_html(full_html=False)

            # Render the template with the plots
            return render_template('solution3.html',
                                   operation='stress_testing',
                                   sector=sector,
                                   company=company,
                                   shock_percentage=shock_percentage,
                                   stress_factors=stress_factors,
                                   severity_level=severity_level,
                                   stress_duration=stress_duration,
                                   stress_testing_plot=stress_testing_plot,
                                   heatmap_plot=heatmap_plot)
        else:
            # Handle case where file path is not found
            return "File path not found for the selected sector and company", 404

    # If GET request, render the form page
    return render_template('stress_testing.html')


        
      
"""  
import logging
from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import logging
import plotly.io as pio  # Import Plotly IO for HTML conversion
from app.models import (
    filter_data_by_selection, 
    calculate_optimal_portfolio, 
    calculate_covariance_matrix, 
    plot_efficient_frontier, 
    plot_risk_return_quadrant, 
    plot_optimization_surface, 
    create_risk_return_table, 
    create_dashboard
)
import logging

logging.basicConfig(level=logging.DEBUG)
import traceback


@main.route('/optimal_portfolio', methods=['GET', 'POST'])
def optimal_portfolio_form():
    if request.method == 'POST':
        try:
            # Get data from the form submission
            sectors = request.form.getlist('sectors')
            companies = request.form.getlist('companies')
            amount = float(request.form['amount'])  # Capture the user-provided investment amount
            risk_tolerance = request.form['risk_tolerance']
            investment_objective = request.form['investment_objective']
            
            logging.debug(f"Sectors: {sectors}")
            logging.debug(f"Companies: {companies}")
            logging.debug(f"Amount: {amount}")
            logging.debug(f"Risk Tolerance: {risk_tolerance}")
            logging.debug(f"Investment Objective: {investment_objective}")
            
            # Ensure file_paths is defined
            if 'file_paths' not in globals():
                raise ValueError("File paths configuration is missing.")
            
            # Filter data based on selected sectors and companies
            filtered_data = filter_data_by_selection(sectors, companies, file_paths)
            
            # Calculate optimal portfolio and get the trained model
            optimal_portfolio, model = calculate_optimal_portfolio(filtered_data, sectors, companies, amount, risk_tolerance, investment_objective)
            
            # Pass the user-provided investment amount to the dashboard
            dashboard = create_dashboard(filtered_data, optimal_portfolio, model, amount=amount)  # Use the captured 'amount'
            
            # Check for errors
            if 'error' in dashboard:
                return render_template('solution5.html', error=dashboard['error'])
            
            # Pass the HTML components to the template
            return render_template(
                'solution5.html',
                pie_chart_html=dashboard.get('pie_chart', ''),
                scatter_plot_html=dashboard.get('scatter_plot', ''),
                efficient_frontier_html=dashboard.get('efficient_frontier', ''),
                risk_return_quadrant_html=dashboard.get('risk_return_quadrant', ''),
                optimization_surface_html=dashboard.get('optimization_surface', ''),
                risk_return_table=dashboard.get('risk_return_table', '')
            )
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            logging.error(traceback.format_exc())  # Log the full stack trace
            return render_template('solution5.html', error="An error occurred while processing your request.")
    else:
        # Render the form page for GET requests
        return render_template('optimal_portfolio.html')




import numpy as np
from flask import Blueprint, request, render_template, jsonify
import pandas as pd
from app.models import (filter_data_by_selection, calculate_returns_and_covariance,
                   select_optimization_model, plot_risk_return_scatter, 
                   plot_sector_performance, plot_pie_charts, 
                   create_performance_metrics_dashboard, create_investment_breakdown, 
                   convert_weights_to_investment,)

import logging

logging.basicConfig(level=logging.DEBUG)
import traceback
from flask import render_template, request
import pandas as pd
import numpy as np

















@main.route('/optimal_portfolio', methods=['GET', 'POST'])
def optimal_portfolio_form():
    if request.method == 'POST':
        sectors = request.form.getlist('sectors')
        companies = request.form.getlist('companies')
        amount = float(request.form['amount'])
        investment_objective = request.form['investment_objective']

        # Filter data
        filtered_data = filter_data_by_selection(sectors, companies, file_paths)

        # Calculate returns and covariance
        returns, cov_matrix = calculate_returns_and_covariance(filtered_data)

        # Perform optimization
        weights = select_optimization_model(investment_objective, returns, cov_matrix)

        # Make sure companies, sectors, and weights are aligned
        company_sector_dict = {company: sector for sector in sectors for company in companies if company in filtered_data['Company'].unique()}
        companies = list(company_sector_dict.keys())
        sectors = list(company_sector_dict.values())

        # Ensure weights correspond to the companies
        weights = [weight for company, weight in zip(returns.index, weights) if company in companies]

        # Convert weights to investment amounts
        allocation_df = convert_weights_to_investment(weights, companies, amount, sectors)
        # Generate visualizations and metrics
        risk_return_plot = plot_risk_return_scatter(returns[companies], np.sqrt(np.diag(cov_matrix.loc[companies, companies])), companies, 'Risk-Return Analysis')
        sector_performance_plot = plot_sector_performance(allocation_df, 'Sector Performance')
        company_allocation_pie, sector_allocation_pie = plot_pie_charts(allocation_df, 'Portfolio Allocation')

        return_metric = np.dot(returns[companies], weights) * 100
        risk_metric = np.sqrt(np.dot(weights, np.dot(cov_matrix.loc[companies, companies], weights))) * 100
        top_performers = allocation_df.nlargest(5, 'Investment')['Company'].tolist()
        performance_dashboard = create_performance_metrics_dashboard(return_metric, risk_metric, top_performers)

        breakdown_df = create_investment_breakdown(allocation_df['Investment'], allocation_df['Company'], allocation_df['Sector'])

        # Render template with results
        return render_template('solution5.html',
                               risk_return_plot=risk_return_plot.to_html(full_html=False),
                               sector_performance_plot=sector_performance_plot.to_html(full_html=False),
                               company_allocation_pie=company_allocation_pie.to_html(full_html=False),
                               sector_allocation_pie=sector_allocation_pie.to_html(full_html=False),
                               performance_dashboard=performance_dashboard,
                               breakdown_table=breakdown_df.to_html(classes='table table-striped'))

    # If GET request, render the form
    return render_template('optimal_portfolio.html')
    
    


@main.route('/optimal_portfolio', methods=['GET', 'POST'])
def optimal_portfolio_form():
    if request.method == 'POST':
        sectors = request.form.getlist('sectors')
        companies = request.form.getlist('companies')
        amount = request.form['amount']
        investment_objective = request.form['investment_objective']
        risk_tolerance = request.form['risk_tolerance']
        
        data = filter_data_by_selection(sectors, companies, file_paths)
        expected_returns, cov_matrix = calculate_returns_and_covariance(data)
        weights = select_optimization_model(investment_objective, expected_returns, cov_matrix)
        allocation_df = convert_weights_to_investment(weights, companies, amount, sectors)
        
        returns = expected_returns[companies].values
        risk = np.sqrt(np.diag(cov_matrix))
        risk_return_fig = plot_risk_return_scatter(returns, risk, companies, 'Risk-Return Scatter')
        sector_performance_fig = plot_sector_performance(allocation_df, 'Sector Performance')
        company_pie, sector_pie = plot_pie_charts(allocation_df, 'Allocation')
        
        performance_metrics = create_performance_metrics_dashboard(
            return_metric=np.sum(returns * weights),
            risk_metric=np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))),
            top_performers=companies
        )
        
        investment_breakdown_df = create_investment_breakdown(
            allocation_df['Investment'].values,
            allocation_df['Company'].values,
            allocation_df['Sector'].values
        )
        
        return render_template('solution5.html',
                               risk_return_scatter=risk_return_fig.to_html(full_html=False),
                               sector_performance=sector_performance_fig.to_html(full_html=False),
                               company_pie=company_pie.to_html(full_html=False),
                               sector_pie=sector_pie.to_html(full_html=False),
                               performance_metrics=performance_metrics,
                               investment_breakdown=investment_breakdown_df.to_html(index=False))

    return render_template('optimal_portfolio.html')
"""

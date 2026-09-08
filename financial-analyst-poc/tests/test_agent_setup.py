import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_agent_model_import_without_api_key():
    import importlib

    # Ensure no key is set for the test environment.
    os.environ.pop('GROQ_API_KEY', None)

    module = importlib.import_module('agent.agent_model')
    assert hasattr(module, 'AgentModel')
    model = module.AgentModel()
    assert model is not None


def test_financial_agent_can_answer_query():
    from agent.financial_agent import FinancialAgent

    agent = FinancialAgent()
    result = agent.run('Price of INFY')
    assert result['type'] in {'tool', 'llm'}


def test_financial_agent_resolves_us_and_indian_tickers_without_network_lookup():
    from agent.financial_agent import FinancialAgent

    agent = FinancialAgent()

    assert agent.extract_tickers('What is the current value of AAPL?') == ['AAPL']
    assert agent.extract_tickers('What is the TCS ticker value?') == ['TCS.NS']


def test_financials_request_works_without_live_yahoo_data():
    from backend.utils.yf_utils import YFinanceHelper

    result = YFinanceHelper.get_financials('RELIANCE.NS')
    assert isinstance(result, dict)
    assert 'income_statement' in result
    assert 'balance_sheet' in result
    assert 'cash_flow' in result

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_alert_backend_defaults_to_fastapi(monkeypatch):
    import ui.components.alert_config as alert_config

    monkeypatch.delenv('BACKEND_URL', raising=False)
    assert alert_config.get_backend_url() == 'http://localhost:8000'


def test_send_alert_config_uses_backend_alert_endpoint(monkeypatch):
    import ui.components.alert_config as alert_config

    captured = {}

    def fake_post(url, json=None, timeout=None):
        captured['url'] = url
        captured['json'] = json
        captured['timeout'] = timeout

        class Response:
            status_code = 200

            def json(self):
                return {'alert': {'alert_status': 'SAFE', 'message': 'ok'}}

        return Response()

    monkeypatch.setattr(alert_config.requests, 'post', fake_post)
    monkeypatch.setenv('BACKEND_URL', 'http://localhost:8000/')

    success, message = alert_config.send_alert_config(
        'user@example.com', 'AAPL', 'Percentage Drop', 5.0
    )

    assert success is True
    assert captured['url'] == 'http://localhost:8000/run_NAV_Alert_Trigger'
    assert captured['json'] == {
        'ticker': 'AAPL',
        'threshold': 5.0,
        'email': 'user@example.com',
    }
    assert 'ok' in message

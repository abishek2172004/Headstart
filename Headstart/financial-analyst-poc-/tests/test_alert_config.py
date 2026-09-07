import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_alert_webhook_defaults_to_n8n_test_webhook(monkeypatch):
    import ui.components.alert_config as alert_config

    monkeypatch.delenv('N8N_WEBHOOK_URL', raising=False)
    assert alert_config.get_webhook_url() == 'http://localhost:5678/webhook-test/alert'


def test_send_alert_config_uses_configured_webhook(monkeypatch):
    import ui.components.alert_config as alert_config

    captured = {}

    def fake_post(url, json=None, timeout=None):
        captured['url'] = url
        captured['json'] = json
        captured['timeout'] = timeout

        class Response:
            status_code = 200

            def json(self):
                return {'message': 'ok'}

        return Response()

    monkeypatch.setattr(alert_config.requests, 'post', fake_post)
    monkeypatch.setenv('N8N_WEBHOOK_URL', 'http://localhost:5678/webhook-test/alert')

    success, message = alert_config.send_alert_config(
        'user@example.com', 'AAPL', 'Percentage Drop', 5.0
    )

    assert success is True
    assert captured['url'] == 'http://localhost:5678/webhook-test/alert'
    assert captured['json']['threshold_value'] == 5.0
    assert 'ok' in message

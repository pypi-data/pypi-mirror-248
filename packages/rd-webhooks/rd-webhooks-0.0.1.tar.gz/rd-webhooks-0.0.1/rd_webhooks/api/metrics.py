""" /api/metrics endpoint

files: rd_webhooks/api/metrics.py
       rd_webhooks/api/metrics.yml
       tests/api/test_metrics.py
"""


def get(**_kwargs):
    """/api/metrics endpoint"""
    # Not returning anything is actually enough to at least have an up{job} metric
    return """
# HELP rd_webhooks_api_service_status Static value to imply service is up
# TYPE rd_webhooks_api_service_status gauge
rd_webhooks_api_service_status 1
"""

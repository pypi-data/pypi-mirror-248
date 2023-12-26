""" /api/status endpoint

files: rd_webhooks/api/status.py
       rd_webhooks/api/status.yml
       tests/api/test_status.py
"""


def get(**_kwargs):
    """/api/status endpoint"""
    return {"status": "ok"}

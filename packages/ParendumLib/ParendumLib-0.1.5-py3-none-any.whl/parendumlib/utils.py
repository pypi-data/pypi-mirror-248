from uuid import uuid4
import re
import os


def all_required(model: dict, required_args: list):
    for _req_arg in required_args:
        if model.get(_req_arg) is None:
            return False, _req_arg
    return True, None


def detect_browser(user_agent: str):
    browsers = {
        'brave': r'Brave',
        'firefox': r'Firefox',
        'edge': r'Edg',
        'safari': r'Safari',
        'opera': r'Opera|OPR',
        'internet_explorer': r'MSIE|Trident',
        'chrome': r'Chrome',
    }

    for browser, pattern in browsers.items():
        if re.search(pattern, user_agent):
            if browser == 'chrome':
                if 'Edg' not in user_agent and 'Brave' not in user_agent:
                    return browser
            elif browser == 'safari':
                if 'Chrome' not in user_agent and 'Brave' not in user_agent:
                    return browser
            else:
                return browser
    return 'unknown'


def format_user_agent(user_agent: str):
    _browser = detect_browser(user_agent).capitalize()
    return " - ".join(user_agent.split('(')[1].split(')')[0].split('; '))

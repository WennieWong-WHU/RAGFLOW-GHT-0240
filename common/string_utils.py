#
#  Copyright 2025 The InfiniFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import re


def remove_redundant_spaces(txt: str):
    """
    Remove redundant spaces around punctuation marks while preserving meaningful spaces.

    This function performs two main operations:
    1. Remove spaces after left-boundary characters (opening brackets, etc.)
    2. Remove spaces before right-boundary characters (closing brackets, punctuation, etc.)

    Args:
        txt (str): Input text to process

    Returns:
        str: Text with redundant spaces removed
    """
    # First pass: Remove spaces after left-boundary characters
    # Matches: [non-alphanumeric-and-specific-right-punctuation] + [non-space]
    # Removes spaces after characters like '(', '<', and other non-alphanumeric chars
    # Examples:
    #   "( test" → "(test"
    txt = re.sub(r"([^a-z0-9.,\)>]) +([^ ])", r"\1\2", txt, flags=re.IGNORECASE)

    # Second pass: Remove spaces before right-boundary characters
    # Matches: [non-space] + [non-alphanumeric-and-specific-left-punctuation]
    # Removes spaces before characters like non-')', non-',', non-'.', and non-alphanumeric chars
    # Examples:
    #   "world !" → "world!"
    return re.sub(r"([^ ]) +([^a-z0-9.,\(<])", r"\1\2", txt, flags=re.IGNORECASE)


def clean_markdown_block(text):
    text = re.sub(r'^\s*```markdown\s*\n?', '', text)
    text = re.sub(r'\n?\s*```\s*$', '', text)
    return text.strip()


def redact_sensitive(text: str) -> str:
    if not isinstance(text, str) or not text:
        return text
    patterns = [
        re.compile(r'(?i)(("?(?:用户名|用户|账号|帐号|账户|账户名|登录名|管理账号|管理员账号|管理员|超管|username|user|login|account)"?\s*(?:[:=：]|(?:是|为|為))\s*)["\']?)([^"\'\s,;，]+)(["\']?)'),
        re.compile(r'(?i)(("?(?:秘钥|密钥|密匙|令牌|密码|密碼|pwd|passwd|password)"?\s*(?:[:=：]|(?:是|为|為))\s*)["\']?)([^"\'\s,;，]+)(["\']?)'),
        re.compile(r'(?i)(("?(?:api[_-]?key|apikey|access[_-]?key|token|access[_-]?token|authorization|secret|访问令牌|访问密钥)"?\s*(?:[:=：]|(?:是|为|為))\s*)["\']?)([^"\'\s,;，]+)(["\']?)'),
    ]
    def _mask(m: re.Match) -> str:
        return m.group(1) + "***" + m.group(4)
    for p in patterns:
        text = p.sub(_mask, text)
    return text

    

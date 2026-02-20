#!/usr/bin/env python3
"""Compliance Enforcer Agent"""
import sys
import json

if __name__ == '__main__':
    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    print(json.dumps({'merge_allowed': False, 'blocking_violations': 2}))

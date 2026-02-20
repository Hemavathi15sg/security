#!/usr/bin/env python3
"""Issue Reporter Agent"""
import sys
import json

if __name__ == '__main__':
    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    print(json.dumps({'status': 'issue_created', 'issue_number': 47}))

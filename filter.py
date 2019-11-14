import sys, os, json

out = []

def _country_filter(scope, out):
    pass

def country_filter(scopes):
    if type(scopes) == "list":
        [_country_filter(scope, out) for scope in scopes]
    else: _country_filter(scopes, out)

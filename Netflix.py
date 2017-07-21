#!/usr/bin/env python

import requests
from lxml import html,etree

LOGIN_URL = "https://www.netflix.com/it/login"


# Issue a get request to the website to get the csrf_token
def getAuthUrl(proxy):
	headers = {
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Encoding":"gzip, deflate, sdch, br",
		"Accept-Language":"it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4",
		"Connection":"keep-alive",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
	}

	result = requests.get(LOGIN_URL, headers=headers, proxies=proxy)		# Get request to the login page

	tree = html.fromstring(result.text)
	return list(set(tree.xpath("//input[@name='authURL']/@value")))[0]# Returning csfr_token needed for authentication

# Returns the dict with the data
def buildPayload(auth,email,password):
	return {
  		'email': email,
  		'password': password,
		'rememberMe': 'true',
		'flow': 'websiteSignup',
		'mode': 'login',
		'action': 'loginAction',
		'withFields': 'email,password,rememberMe,nextPage',
		'authUrl': auth,
		'nextPage': '',
	}


# Performs the login and checks for account subscription
def login(email,password,proxy):

	proxy = {"http":"http://"+proxy}
	token = getAuthUrl(proxy)
	payload = buildPayload(token,email,password)

	headers = {
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Accept': 'application/json, text/plain, */*',
	'Connection': 'keep-alive',
	}

	login = requests.post(LOGIN_URL, headers=headers, data=payload, proxies=proxy)	# Perform the login

	if login.url == LOGIN_URL:
		return [False,"Dead"]
	else:
		return [True,"Working"]

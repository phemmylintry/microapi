from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from user_dashboard.models import Api
import requests
import json
# Create your views here.

# Views to docs
def docs(request, slug):
	try:
		docs = get_object_or_404(Api, slug=slug)
		if docs.docs_url == "":
			messages.info(request, 'Sorry, no documentation was provided for this API')
			return redirect("index")
		api_docs = docs.docs_url
		response = requests.get(api_docs)
		documentation = response.json()
		info = documentation['data']['info']
		servers = documentation['data']['servers']
		paths = documentation['data']['paths']
		components = documentation['data']['components']
		server_url = servers[0]['url']
		return render(request, 'api_docs/api_doc_page.html',
			{'info' : info,'servers' : servers,
				'paths' : paths,'components' : components, 'time' :docs.updated_on, 'url' : server_url})
	except KeyError as e:
		messages.info(request, 'Sorry, Documentation Format is Invalid')
		return redirect("index")
	
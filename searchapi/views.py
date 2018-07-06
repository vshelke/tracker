from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from searchapi.models import User
from searchapi.serializers import UserSerializer
import requests, json

auth = '?client_id=676cb6d3e33c3bed8831&client_secret=0e1b5515a3e2b8e52b470616f28249eababe9718'
url = 'https://api.github.com/search/users' + auth + '&q='
# Create your views here.
def get_user_details(raw):
    r_user = json.loads(requests.get(raw['url'] + auth).text)
    r_repo = json.loads(requests.get(raw['repos_url'] + auth).text)
    user = {}
    repos = []
    user['uid'] = raw['id']
    user['login'] = raw['login']
    user['thumbnail'] = raw['avatar_url']
    user['user_type'] = raw['type']
    user['fullname'] = r_user['name']
    user['email'] = r_user['email']
    user['location'] = r_user['location']
    user['created'] = r_user['created_at']
    user['followers'] = r_user['followers']
    user['languages'] = []
    for i in r_repo:
        user['languages'].append(i['language'])
    return user

def query_parser(q):
    tokens = q.split(' ')
    query = ''
    filters = []
    for token in tokens:
        if not ':' in token:
            query = token
        else:
            filters.append(token.split(':'))
    filter_query = {}
    for filter in filters:
        if filter[0] == 'type':
            filter_query['user_type__icontains'] = filter[1]
        elif filter[0] == 'location':
            filter_query['location__icontains'] = filter[1]
        elif filter[0] == 'language':
            filter_query['languages__in'] = filter[1]
        elif filter[0] == 'in' and not query == '':
            filter_query[filter[1] + '__icontains'] = query
        # elif filter[0] == 'repos':
        #     if filter[1].startswith('>')
        # elif filter[0] == 'created':
        # elif filter[0] == 'followers':
    return User.objects.filter(**filter_query)

def index(request):
    q = request.GET.get('q', '')
    return HttpResponse(query_parser(q))

    # r = requests.get(url + q)
    # data = json.loads(r.text)
    # res = []
    # for i in data['items']:
    #     user = get_user_details(i)
    #     res.append(user)
    #     u = User(**user)
    #     u.save()
    # return JsonResponse(res, safe=False)

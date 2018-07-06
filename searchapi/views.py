from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from searchapi.models import User
from searchapi.serializers import UserSerializer
import requests, json
from django.conf import settings
import dateutil.parser

API_SCORE_THRESHOLD = settings.API_SCORE_THRESHOLD
API_AUTH = settings.API_AUTH
API_HOST = settings.API_HOST

def filter_user_details(raw):
    r_user = json.loads(requests.get(raw['url'] + API_AUTH).text)
    r_repo = json.loads(requests.get(raw['repos_url'] + API_AUTH).text)
    user = {}
    repos = []
    user['uid'] = raw['id']
    user['login'] = raw['login']
    user['thumbnail'] = raw['avatar_url']
    user['user_type'] = raw['type']
    user['fullname'] = r_user['name']
    user['email'] = r_user['email']
    user['location'] = r_user['location']
    user['created'] = dateutil.parser.parse(r_user['created_at'])
    user['followers'] = r_user['followers']
    user['languages'] = []
    for i in r_repo:
        user['languages'].append(i['language'])
    return user

def search_db(q):
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
        # add filters for repos, created and followers
    if not query == '':
        filter_query['login__icontains'] = query
    res = User.objects.filter(**filter_query)
    return res

def search_github(q):
    r = requests.get(API_HOST + q)
    data = json.loads(r.text)
    res = []
    for i in data['items']:
        if i['score'] > API_SCORE_THRESHOLD:
            user = filter_user_details(i)
            res.append(user)
            u = UserSerializer(data=user)
            if u.is_valid():
                print ('here')
                u.save()
    return res

def index(request):
    q = request.GET.get('q', '')
    db_res = search_db(q)
    if db_res:
        serializer = UserSerializer(db_res, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        api_res = search_github(q)
        return JsonResponse(api_res, safe=False)

def fetch_all(request):
    res = User.objects.all()
    serialised = UserSerializer(res, many=True)
    return JsonResponse(serialised.data, safe=False)

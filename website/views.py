# coding: utf-8

import json

from django.conf import settings
from django.shortcuts import render
from django.utils.datastructures import SortedDict

from urllib2 import urlopen, Request, HTTPError

from common.auth.backends.bratabase import BratabaseAuth


def get_request(url, token):
    request = Request(url, headers={
        'Authorization': 'bearer %s' % token
    })
    return request


def get_user_bras(token):
    request = get_request(BratabaseAuth.ME_URL, token)
    body = json.load(urlopen(request))
    bras_url = body['links']['bras']
    request = get_request(bras_url, token)
    bras = json.load(urlopen(request))
    return bras


def get_avatar(token):
    request = get_request(BratabaseAuth.ME_URL, token)
    body = json.load(urlopen(request))
    return body['body']['avatar']['medium']


def sort_bras(bras):
    result = {}
    for bra in bras['collection']:
        brand_url = bra['brand']['bratabase_url']
        if brand_url not in result:
            result[brand_url] = {
                'name': bra['brand']['name'],
                'bras': [],
                'total': 0
            }

        result[brand_url]['bras'].append(bra)
        result[brand_url]['total'] += 1

    return SortedDict(sorted(list(result.items()),
        key=lambda b: -b[1]['total']))


def get_top_brand(brands):
    return max(brands.values(), key=lambda b: b['total'])['name']

def sort_sizes(bras):
    result = {}
    for bra in bras['collection']:
        size = bra['size']['size']
        if size not in result:
            result[size] = 0

        result[size] += 1

    return SortedDict(sorted(list(result.items()), key=lambda b: -b[1]))


def error_page(request, err):
    return render(request, 'home/error.html', {
        'user': request.user,
        'err': err,
    })


def home(request):
    if not request.user.is_authenticated():
        return render(request, 'home/anon.html')
    access_token = request.user.social_auth.all()[0].extra_data['access_token']
    try:
        user_bras = get_user_bras(access_token)
    except HTTPError, err:
        return error_page(request, err)

    brands = sort_bras(user_bras)
    top_brand = get_top_brand(brands)
    sizes = sort_sizes(user_bras)

    return render(request, 'home/welcome.html', {
        'bras': user_bras['collection'],
        'brands': brands,
        'top_brand': top_brand,
        'top_size': sizes.keys()[0],
        'avatar': get_avatar(access_token),
    })



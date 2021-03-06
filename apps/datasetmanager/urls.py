"""
Defines all routes of the Dataset Manager
"""

from django.conf.urls import patterns, url, include

from .api import *

dataset_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', DatasetDetail.as_view(), name='dataset-detail'),
    url(r'^$', DatasetList.as_view(), name='dataset-list')
)

converter_urls = patterns(
    '',
    url(r'^$', Converter.as_view(), name='converter')

)

urlpatterns = patterns(
    '',
    url(r'^datasets', include(dataset_urls)),
    url(r'^converter', include(converter_urls)),
    url(r'^', Base.as_view(), name="dataset-manager-base")
)


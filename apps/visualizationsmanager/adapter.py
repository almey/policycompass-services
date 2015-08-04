"""
Collection of adapters to the Visualisation
"""

__author__ = 'mmilparat'
from apps.common.serviceadapters.base_adapter import BaseAdapter
from django.conf import settings

import logging

#class MetricsAdapter(BaseAdapter):
#    """
#    Adapter for metrics
#    """
#    def __init__(self):
#        metric_url = settings.PC_SERVICES['references']['base_url'] + settings.PC_SERVICES['references']['metricsInvisualizations']               
#        logging.warning(metric_url)
#        self.url = metric_url
#        self.url_entity = metric_url + '/%s'
#        super(MetricsAdapter, self).__init__()


class DatasetsAdapter(BaseAdapter):
    """
    Adapter for datasets
    """
    def __init__(self):
        dataset_url = settings.PC_SERVICES['references']['base_url'] + settings.PC_SERVICES['references']['datasetsInvisualizations']               
        logging.warning(dataset_url)
        self.url = dataset_url
        self.url_entity = dataset_url + '/%s'
        super(DatasetsAdapter, self).__init__()

class HistoricalEventsAdapter(BaseAdapter):
    """
    Adapter for historical events
    """
    def __init__(self):
        historical_events_url = settings.PC_SERVICES['references']['base_url'] + settings.PC_SERVICES['references']['eventsInVisualizations']
        self.url = historical_events_url
        self.url_entity = historical_events_url + '/%s'
        super(HistoricalEventsAdapter, self).__init__()
#!/usr/bin/env python

import unittest
import xml.etree.ElementTree as ET
from xml.dom import minidom

import requests
from opensearch import Client as OpenSearchClient


class OpenSearchUnitTestCase(unittest.TestCase):
    DESCRIPTION_URL = 'http://fedeo.esa.int/opensearch/description.xml'

    def setUp(self):
        self.clnt = OpenSearchClient(self.DESCRIPTION_URL)

    def test01_query(self):
        results = self.clnt.search('sentinel', startRecord=1, 
                                   maximumRecords=2)
        print('Number of results: {}'.format(len(results)))
        for result in results:
            print('+'*80)
            print(result.title)
            description_url = None
            for link in result.links:
                if link.type == u'application/opensearchdescription+xml':
                    description_url = link.href
                
                elif link.type == u'application/vnd.iso.19115-3+xml':
                    print('Title: ' + link.title)
                    print('Link: ' + link.href)
                    
                    response = requests.get(link.href)
                    if response.text:
                        resp_elem = ET.fromstring(response.content)
                        xml_s = minidom.parseString(
                            ET.tostring(resp_elem)).toprettyxml(indent="   ")
                        print(xml_s)
                
            if description_url:
                ds_clnt = OpenSearchClient(description_url)
                ds_result = ds_clnt.search('')
                for item in ds_result.items:
                    for link in item.links:
                        if link.type == u'application/x-binary':
                            print('+'*80)
                            print('Title: ' + link.title)
                            print('Link: ' + link.href)
                            
                        if link.type.startswith('application/gml+xml'):
                            print('+'*80)
                            print('Title: ' + link.title)
                            print('Link: ' + link.href)
                            

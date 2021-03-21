from elasticsearch import Elasticsearch
from odoo import _, api, fields, models

es = Elasticsearch(["elasticsearch:9200"])


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'elasticsearch.mixin']

    def prepare_elasticseach_data(self):
        """ Method to be overridden to return data """
        return {
            "id": self.id,
            "name": self.name,
            "customer_full_name": self.partner_id.name,
        }

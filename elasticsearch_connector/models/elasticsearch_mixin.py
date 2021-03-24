""" Initialize Sqs Mixin """

from elasticsearch import Elasticsearch
from odoo import _, api, fields, models


class ElasticsearchMixin(models.AbstractModel):
    """
    Initialize Elasticsearch Mixin:
    """

    _name = 'elasticsearch.mixin'
    _description = 'Elasticsearch Mixin'

    def prepare_elasticseach_data(self):
        """ Method to be overridden to return data """
        raise NotImplementedError(
            "Please Implement this prepare_elasticseach_data"
        )

    def _get_elasticsearch_client(self):
        """Get Elasticsearch client """

        ICP = self.env["ir.config_parameter"].sudo()
        hosts = ICP.get_param("elasticsearch.hosts")
        hosts = hosts.split(",")
        es = Elasticsearch(hosts)
        return es

    def index(self, index=None, document_id=None):
        """index document in Elasticsearch

        :param index: name of index
        :param document_id: Integer that define a document in Elasticsearch
                            use it when update update document
        :return: values of document
        """
        if index is None:
            index = self._name
        body = self.prepare_elasticseach_data()
        es = self._get_elasticsearch_client()
        document = es.index(index=index, id=document_id, body=body)
        return document

    def delete(self, index=None, document_id=None):
        """delete document in Elasticsearch

        :param document_id: Integer that define a document in Elasticsearch
        """
        if index is None:
            index = self._name
        es = self._get_elasticsearch_client()
        document = es.delete(index=index, id=document_id)
        return document

    def perform_index(self, document_id=None):
        self.index(document_id=document_id)

    def perform_delete(self, document_id=None):
        self.delete(document_id=document_id)

    @api.model
    def create(self, vals):
        res = super(ElasticsearchMixin, self).create(vals)
        res.perform_index(res.id)
        return res

    def write(self, values):
        res = super(ElasticsearchMixin, self).write(values)
        self.perform_index(self.id)
        return res

    def unlink(self):
        res = super(ElasticsearchMixin, self).unlink()
        for _id in self.ids:
            self.perform_delete(_id)
        return res

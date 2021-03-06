# Elasticsearch Odoo Connector
Elasticsearch is awesome tools in searching saving document, plus visualize data using `kibana`.

Elasticsearch Odoo Connector is a powerful and flexible toolkit for connecting Odoo with elasticsearch.

# Example
Let's take a look at a quick example of using Elasticsearch Odoo Connector to Create/update/delete a document of model `sale.order` 

``` Python
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
```
when a record created in Odoo you should find the document of this record in index 'sale.order'
you should override the method `prepare_elasticseach_data` which data be prepared to be created in elasticsearch

# Try it with docker
``` Shell
docker-compose up -d
```

- go to `localhost:8069` create a new DB and install module `sale_elasticsearch_example` create a new record
- go to `localhost:5601` find you record in index `sale.order` 

# what is next?
- be configurable
  - hosts
  - Auth
  - Multi nodes
- prepare data of sales modules and create Kibana dashboard
- prepate data of invoice modules and create Kibana dashboard

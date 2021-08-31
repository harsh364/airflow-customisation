from json import dumps

from airflow.models import BaseOperator
from plugins.adhoc_download.hooks.custom_bq_hooq import BigQueryHook
from airflow.utils.decorators import apply_defaults

def handle_row(row_dict):
    for rows in row_dict:
        print(rows[0])


class BigQueryReturnOperator(BaseOperator):
    template_fields = ['sql']
    ui_color = '#ffffff'

    @apply_defaults
    def __init__(
            self,
            sql,
            keys,
            bigquery_conn_id='bigquery_default',
            delegate_to=None,
            location='asia-southeast1',
            *args,
            **kwargs):
        super(BigQueryReturnOperator, self).__init__(*args, **kwargs)
        self.sql = sql
        self.keys = keys # A list of keys for the columns in the result set of sql
        self.bigquery_conn_id = bigquery_conn_id
        self.delegate_to = delegate_to
        self.location = location

    def execute(self, context):
        """
        Run query and handle results row by row.
        """
        cursor = self._query_bigquery()
        row_dict=[]
        self.log.info('Retrieving return value')
        for row in cursor.fetchall():
            # Zip keys and row together because the cursor returns a list of list (not list of dicts)
            # row_dict = dumps(dict(zip(row))).encode('utf-8')
            self.log.info('Calling handling function')
            # Do what you want with the row...
            row_dict.append(row)
            handle_row(row_dict)


    def _query_bigquery(self):
        """
        Queries BigQuery and returns a cursor to the results.
        """
        bq = BigQueryHook(bigquery_conn_id=self.bigquery_conn_id,
                          use_legacy_sql=False,
                          location=self.location,
                          delegate_to=self.delegate_to)
        conn = bq.get_conn()
        cursor = conn.cursor()
        self.log.info('Executing sql')
        cursor.execute(self.sql)

        return cursor
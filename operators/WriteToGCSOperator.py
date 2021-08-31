import warnings

from utils.hooks.custom_gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from google.cloud import storage

class WriteToGoogleCloudStorageOperator(BaseOperator):
    _conn = None

    def get_conn(self):
        """
        Returns a Google Cloud Storage service object.
        """
        if not self._conn:
            self._conn = storage.Client(credentials=self._get_credentials(),
                                        project=self.project_id)

        return self._conn

    # template_fields = ('src', 'bucket')

    @apply_defaults
    def __init__(self,
                 src,
                 bucket,
                 write_string,
                 gcp_conn_id='google_cloud_default',
                 google_cloud_storage_conn_id=None,
                 mime_type='application/octet-stream',
                 delegate_to=None,
                 gzip=False,
                 *args,
                 **kwargs):
        super(WriteToGoogleCloudStorageOperator,self).__init__(*args, **kwargs)

        if google_cloud_storage_conn_id:
            warnings.warn(
                "The google_cloud_storage_conn_id parameter has been deprecated. You should pass "
                "the gcp_conn_id parameter.", DeprecationWarning, stacklevel=3)
            gcp_conn_id = google_cloud_storage_conn_id

        self.src = src
        self.bucket = bucket
        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to
        self.write_string = write_string

    def execute(self, context):
        """
        Creates new file in Google cloud storage
        """
        # hook = GoogleCloudStorageHook(
        #     google_cloud_storage_conn_id=self.gcp_conn_id,
        #     delegate_to=self.delegate_to,
        #
        #
        # )
        #
        # hook.write_to_gcs(
        #     bucket_name=self.bucket,
        #     filename=self.src,
        #     write_string = self.write_string
        #
        # )
        #
        client = storage.Client()
        bucket = client.get_bucket(self.bucket)

        print (self.src)
        print(bucket.name)
        nfile = bucket.blob(self.src)
        # for fls in bucket.list_blobs():
        #     print(fls.name)
        nfile.upload_from_string(self.write_string)
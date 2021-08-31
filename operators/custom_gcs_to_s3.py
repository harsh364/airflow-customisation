# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
This module contains Google Cloud Storage to S3 operator.
"""
import warnings

from utils.hooks.custom_gcs_hook import GoogleCloudStorageHook
from airflow.contrib.operators.gcs_list_operator import GoogleCloudStorageListOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.S3_hook import S3Hook


class GoogleCloudStorageToS3Operator(GoogleCloudStorageListOperator):
    """
    Synchronizes a Google Cloud Storage bucket with an S3 bucket.

    :param bucket: The Google Cloud Storage bucket to find the objects. (templated)
    :type bucket: str
    :param prefix: Prefix string which filters objects whose name begin with
        this prefix. (templated)
    :type prefix: str
    :param delimiter: The delimiter by which you want to filter the objects. (templated)
        For e.g to lists the CSV files from in a directory in GCS you would use
        delimiter='.csv'.
    :type delimiter: str
    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.
    :type gcp_conn_id: str
    :param google_cloud_storage_conn_id: (Deprecated) The connection ID used to connect to Google Cloud
        Platform. This parameter has been deprecated. You should pass the gcp_conn_id parameter instead.
    :type google_cloud_storage_conn_id: str
    :param delegate_to: The account to impersonate, if any.
        For this to work, the service account making the request must have
        domain-wide delegation enabled.
    :type delegate_to: str
    :param dest_aws_conn_id: The destination S3 connection
    :type dest_aws_conn_id: str
    :param dest_s3_key: The base S3 key to be used to store the files. (templated)
    :type dest_s3_key: str
    :param dest_verify: Whether or not to verify SSL certificates for S3 connection.
        By default SSL certificates are verified.
        You can provide the following values:

        - ``False``: do not validate SSL certificates. SSL will still be used
                 (unless use_ssl is False), but SSL certificates will not be
                 verified.
        - ``path/to/cert/bundle.pem``: A filename of the CA cert bundle to uses.
                 You can specify this argument if you want to use a different
                 CA cert bundle than the one used by botocore.

    :type dest_verify: bool or str
    :param replace: Whether or not to verify the existence of the files in the
        destination bucket.
        By default is set to False
        If set to True, will upload all the files replacing the existing ones in
        the destination bucket.
        If set to False, will upload only the files that are in the origin but not
        in the destination bucket.
    :type replace: bool
    """
    template_fields = ('bucket', 'prefix', 'delimiter', 'dest_s3_key')
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self,  # pylint: disable=too-many-arguments
                 bucket,
                 file = None,
                 prefix=None,
                 delimiter=None,
                 gcp_conn_id='google_cloud_default',
                 google_cloud_storage_conn_id=None,
                 delegate_to=None,
                 dest_aws_conn_id='aws_default',
                 dest_s3_key=None,
                 dest_verify=None,
                 replace=False,
                 *args,
                 **kwargs):

        if google_cloud_storage_conn_id:
            warnings.warn(
                "The google_cloud_storage_conn_id parameter has been deprecated. You should pass "
                "the gcp_conn_id parameter.", DeprecationWarning, stacklevel=3)
            gcp_conn_id = google_cloud_storage_conn_id

        super().__init__(
            bucket=bucket,
            prefix=prefix,
            delimiter=delimiter,

            delegate_to=delegate_to,

            *args,
            **kwargs
        )
        self.file = file
        self.dest_aws_conn_id = dest_aws_conn_id
        self.dest_s3_key = dest_s3_key
        self.dest_verify = dest_verify
        self.replace = replace
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        # use the super to list all files in an Google Cloud Storage bucket
        # files = super().execute(context)
        s3_hook = S3Hook(aws_conn_id=self.dest_aws_conn_id, verify=self.dest_verify)


        hook = GoogleCloudStorageHook(
            google_cloud_storage_conn_id=self.gcp_conn_id,
            delegate_to=self.delegate_to
        )


        file_bytes = hook.download(self.bucket,self.file)

        dest_key = self.dest_s3_key + self.file
        self.log.info("Saving file to %s", dest_key)

        s3_hook.load_bytes(file_bytes,
                           key=dest_key,
                           replace=self.replace)

        self.log.info("All done, uploaded %d files to S3", len(self.file))

        return self.file
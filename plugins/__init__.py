from airflow.plugins_manager import AirflowPlugin
import deploy_dag
from documentation import Documentation, DOCUMENTATION_VIEW

class DeployDagPlugin(AirflowPlugin):
    name = "deploy_dag_plugin"
    flask_blueprints = [deploy_dag.DeployDag]
    admin_views = [deploy_dag.DEPLOY_VIEW]


class DocumentationPlugin(AirflowPlugin):
    name = "documentation_plugin"
    flask_blueprints = [Documentation]
    admin_views = [DOCUMENTATION_VIEW]
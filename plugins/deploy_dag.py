import os
from flask import Blueprint, flash, redirect, url_for
from flask_admin import BaseView, expose
from flask import request
from airflow.www.app import csrf

DeployDag = Blueprint('deploy_dag', __name__, url_prefix='/deploy_dag')

class Deploy(BaseView):
    @csrf.exempt
    @expose('/', methods=['GET', 'POST'])
    def deploy_dag(self):
        if request.method=='GET':
            return self.render('deploy_dag.html')
        else:
            print("Executing custom 'deploy_dag' function")
            print("Dag_file:")
            dag_file = request.files['dag_file']
            print(dag_file.filename)
            airflow_dags_folder = os.getcwd()+"/logs/dynamicdags"
            print(airflow_dags_folder)
            if dag_file and dag_file.filename.endswith(".py"):
                save_file_path = os.path.join(airflow_dags_folder, dag_file.filename)

            print("Saving file to '" + save_file_path + "'")
            dag_file.save(save_file_path)

            flash("Dag Deployed Successfully at "+airflow_dags_folder)
            return self.render('deploy_dag.html')

    @DeployDag.route('/test', methods=['POST'])
    @csrf.exempt
    def check(self):
        print("Health Check")
        return "Running"


DEPLOY_VIEW = Deploy(category="Deploy Dag", name="Deploy New Dag")
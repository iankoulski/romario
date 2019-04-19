# Main imports
import kfp
import kfp.dsl as dsl
from kfp.gcp import use_gcp_secret
from kubernetes import client as k8s_client
from flask import Flask, request
from werkzeug.utils import secure_filename
import datetime

app = Flask(__name__)

def create_rom_client():
	# Defining a client
	# client = kfp.Client()
	return kfp.Client()

def create_rom_experiment(experiment_name = 'romario_test',client=None):
	# Creating Experiment
	# exp = client.create_experiment(name=EXPERIMENT_NAME)
	nowStr = str(datetime.datetime.now())
	try:
		exp = client.create_experiment(name=experiment_name + nowStr)
	except:
		exp = None
		raise Exception('Client { } not defined'.format(client))


	return exp

def run_rom_pipeline(pipeline_name='romario_pipeline_run_1',
					pipeline_path=None,
					client=None,
					experiment=None,
					timeout=None):
	# Run
	# run = client.run_pipeline(exp.id, 'hypertune-arun1', 'hypertune.tar.gz',
	#                          params={'arch': ARCH})
	# Checking for pipeline path
	if not pipeline_path:
		raise Exception('Pipeline TAR file path not defined!')
	if not experiment:
		raise Exception('Exeriment not defined!')
	if not client:
		raise Exception('Client not defined!')
	# Running the pipeline
	nowStr = str(datetime.datetime.now())
	try:
		run = client.run_pipeline(experiment.id, pipeline_name + nowStr, pipeline_path)
		#if not timeout:
		#	results = client.wait_for_run_completion(run.id, timeout=timeout)
	except:
		run = None
		raise Exception('Client { } not defined'.format(client))

	return run

# Tar-ing an ARGO YAML
# TODO: implement a tar for a given YAML

# Compile
# TODO: Provide a server to compile an python script pipeline
"""
hypertune_loops_dag is a relative import...
So the pipeline would need to be a function... not an instance of a python objec.

It would record it locally

CMD: compiler.Compiler().compile(hypertune_loops_dag,  'hypertune.tar.gz')

"""
@app.route("/")
def hello_world():
	return "Hello World"

@app.route("/print_filename", methods=['POST','PUT'])
def print_filename():
	file = request.files['file']
	filename=secure_filename(file.filename)
	file.save(filename)
	with open(filename, 'r') as fin:
		returning = fin.read()
	return returning

@app.route("/test_create_client", methods=['POST','PUT'])
def test_create_client():
	file = request.files['file']
	filename=secure_filename(file.filename)
	file.save(filename)
	with open(filename, 'r') as fin:
		returning = fin.read()
	try:
		client = create_rom_client()
		returning = 'Success!!'
	except:
		returning = 'Failed: Client creation not working!\n\n'
		raise Exception(returning)

	return returning

@app.route("/test_create_exp", methods=['POST','PUT'])
def test_create_exp():
	file = request.files['file']
	filename=secure_filename(file.filename)
	file.save(filename)
	with open(filename, 'r') as fin:
		returning = fin.read()
	try:
		client = create_rom_client()
		returning = 'Success!!'
	except:
		returning = 'Failed: Client creation not working!\n\n'
		raise Exception(returning)
	try:
		exp = create_rom_experiment(client=client)
		returning = 'Success!!'
	except:
		returning = 'Failed: Experiment creation Failed!\n\n'
		raise Exception(returning)

	return returning

@app.route("/test_run_pipeline", methods=['POST','PUT'])
def test_run_pipeline():
	file = request.files['file']
	filename=secure_filename(file.filename)
	file.save(filename)
	try:
		client = create_rom_client()
		returning = 'Success!!'
	except:
		returning = 'Failed: Client creation not working!\n\n'
		raise Exception(returning)
	try:
		exp = create_rom_experiment(client=client)
		returning = 'Success!!'
	except:
		returning = 'Failed: Experiment creation Failed!\n\n'
		raise Exception(returning)

	try:
		ran = run_rom_pipeline(pipeline_path=filename,
			client=client,
			experiment=exp)
		returning = 'Success!! - your pipeline should be runing by now!\n\n'
	except:
		returning = 'Failed: Run creation failed!\n\n'
		raise Exception(returning)

	return returning


if __name__ == '__main__':
	app.run(port=6966, debug=True, host='0.0.0.0')
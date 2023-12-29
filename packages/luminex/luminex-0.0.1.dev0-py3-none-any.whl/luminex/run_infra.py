import sys
import subprocess
import requests
import json
import time
import boto3

from validation import IAMRoleValidator

# get repo root level
root_path = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=False
).stdout.rstrip("\n")
# add repo path to use all libraries
sys.path.append(root_path)

from configs import Config

# Declare Global Variable
cfg = Config('../configs/config.yaml')

def get_stack_outputs(stack_name, region, aws_access_key_id, aws_secret_access_key, aws_session_token):
    """
    Returns the EMR cluster ID.

            Parameters:
                    stack_name (str): The name of the cloudformation stack
                    region (str): The aws region from where the output has to be fetched
                    aws_access_key_id (str): AWS Temp Credentials: Access Key ID
                    aws_secret_access_key (str): AWS Temp Credentials: Secret Access Key
                    aws_session_token (str): AWS Temp Credentials: Session Token

            Returns:
                    EMR Cluster ID (str): It returns the output of the stack i.e.
                    EMR Cluster ID to the trigger_workflow function
    """
    client = boto3.client('cloudformation', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

    try:
        stack = client.describe_stacks(StackName=stack_name)
        outputs = stack['Stacks'][0]['Outputs']

        return {output['OutputKey']: output['OutputValue'] for output in outputs}

    except client.exceptions.ClientError as e:
        print(f"Error getting stack outputs: {e}")
        return {}


def fetch_stack_status_with_retry(stack_name, aws_region, aws_access_key_id, aws_secret_access_key, aws_session_token, max_retries=15, retry_delay=60, initial_delay=120):
    """
    Returns the EMR cluster ID.

            Parameters:
                    stack_name (str): The name of the cloudformation stack
                    aws_region (str): The aws region from where the output has to be fetched
                    aws_access_key_id (str): AWS Temp Credentials: Access Key ID
                    aws_secret_access_key (str): AWS Temp Credentials: Secret Access Key
                    aws_session_token (str): AWS Temp Credentials: Session Token
                    max_retries (int): Max retries to trigger the AWS to check if the stack deployment is complete
                    retry_delay (int): Delay seconds between each retry
                    initial_delay (int): The initial delay in seconds before checking on the stack creation

            Returns:
                    If the stack creation has been successful or not
    """
    # Initial waiting period before starting retries
    print(f"Waiting for stack {stack_name} to be created...")
    time.sleep(initial_delay)
    client = boto3.client('cloudformation', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

    # Retry fetching the EMR Cluster ID with a delay in case of 404 errors
    for retry_count in range(max_retries):
        try:
            stack_resources = client.list_stack_resources(StackName=stack_name)
            stack_resources = stack_resources['StackResourceSummaries']
            print("Resources:")
            for resource in stack_resources:
                print("| {} | {} | {} | {} |".format(resource['LogicalResourceId'], resource['PhysicalResourceId'], resource['ResourceType'], resource['ResourceStatus']))

            stack = client.describe_stacks(StackName=stack_name)
            status = stack['Stacks'][0]['StackStatus']

            if status.endswith('COMPLETE'):
                print(f"Stack {stack_name} creation complete.")
                return True

            elif status.endswith('ROLLBACK'):
                print(f"Stack {stack_name} creation failed.")
                return False
        
        except client.exceptions.ClientError as e:
            if 'does not exist' in str(e):
                pass  # Stack doesn't exist yet, continue waiting
            else:
                raise

        print(f'Retry {retry_count + 1}/{max_retries}. EMR Cluster creation in progress, waiting {retry_delay} seconds before fetching more details...')
        time.sleep(retry_delay)

    print(f'Exceeded maximum retries. Failed to retrieve EMR Cluster ID. Please check the logs for more information.')
    return None


def read_config(file_path='../config/infra_config.json'):

    """
    Returns the static parameters to run_infra from the config file.

            Parameters:
                    file_path (str): The path of the config file

            Returns:
                    config_data (dict): Represents the data in the config file
    """

    with open(file_path, 'r') as config_file:
        config_data = json.load(config_file)
    return config_data
#


def trigger_workflow(organization, repository, workflow_name, event_type, aws_region, token, inputs=None):

    """
    Triggers the GitHub actions to create the AWS infrastructure for Luminex.

            Parameters:
                    organization (str): The name of the organization which the Repo belongs to
                    repository (str): The name of the Repo
                    workflow_name (str): The GitHub action that needs to be triggered to deploy the infra
                    event_type (str): The type of the event to trigger
                    aws_region (str): The aws region from where the emr creation status has to be fetched
                    token (str): The personal access token need to trigger the GitHub action
                    inputs (dict): The inputs variables that needs to be passed to the GitHub action

            Returns:
                    Returns the EMR Cluster ID
    """

    url = f'https://api.github.com/repos/{organization}/{repository}/dispatches'
    stack_name = inputs['stack-name']
    aws_access_key_id = inputs['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = inputs['AWS_SECRET_ACCESS_KEY']
    aws_session_token = inputs['AWS_SESSION_TOKEN']
    headers = {
        'Accept': 'application/vnd.github.everest-preview+json',
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    payload = {
        'event_type': event_type,
        'client_payload': {
            'workflow': workflow_name,
            'inputs': inputs or {},
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)

    if response.status_code == 204:
        print(f'Response status code: {response.status_code}, Workflow triggered successfully.')
    else:
        print(f'Failed to trigger the GitHub Actions workflow. Status code: {response.status_code}, Content: {response.text}')
        return None

    if fetch_stack_status_with_retry(stack_name, aws_region, aws_access_key_id, aws_secret_access_key, aws_session_token):
        outputs = get_stack_outputs(stack_name, aws_region, aws_access_key_id, aws_secret_access_key, aws_session_token)
        for key, value in outputs.items():
            print(f"Infra has been set.{key}: {value} ")
    else:
        print("Failed to create the stack.")

    return None
#


def run_infra(pat, stack_name):

    """
    Retrieves values from different sources and finally triggers the function to run the github action

            Parameters:
                    pat (str): Personal Access token to trigger github action.
                    stack_name (str): Name of the stack that manages Luminex infra resources.
                    ENV: AWS_ACCESS_KEY_ID (str): AWS Temp Credentials: Access Key ID
                    ENV: AWS_SECRET_ACCESS_KEY (str): AWS Temp Credentials: Secret Access Key
                    ENV: AWS_SESSION_TOKEN (str): AWS Temp Credentials: Session Token

            Returns:
                    Calls the trigger workflow function with required parameters (From config file: organization_name, repository_name
                    workflow_name, event_type, From user: personal_access_token, workflow_inputs)
    """
    # Access AWS config
    aws_access_key_id = cfg.get('aws/access_key_id')
    aws_secret_access_key = cfg.get('aws/secret_access_key')
    aws_session_token = cfg.get('aws/session_token')

    if not aws_access_key_id or not aws_secret_access_key or not aws_session_token:
        print("Please set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and AWS_SESSION_TOKEN environment variables.")
        return

    # Validation logic
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # config_path = os.path.join(script_dir, 'validation', 'config.json')
    permissions_validator = IAMRoleValidator(cfg)
    permissions_validator.validate_roles()

    organization_name = cfg.get('infra/github_organization')
    repository_name = cfg.get('infra/github_repository')
    workflow_name = cfg.get('infra/github_workflow')
    event_type = cfg.get('infra/github_event_type')
    aws_region = cfg.get('aws/region')
    personal_access_token = pat


    workflow_inputs = {
        'stack-name': stack_name,
        'AWS_ACCESS_KEY_ID': aws_access_key_id,
        'AWS_SECRET_ACCESS_KEY': aws_secret_access_key,
        'AWS_SESSION_TOKEN': aws_session_token
    }

    trigger_workflow(organization_name, repository_name, workflow_name, event_type, aws_region, personal_access_token, workflow_inputs)

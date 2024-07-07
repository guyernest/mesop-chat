import json
from typing import Dict, Any
import boto3


import mesop as me
import mesop.labs as mel

ssm = boto3.client('ssm')

bedrock_agent_runtime_client = boto3.client('bedrock-agent-runtime')
agent_id = ssm.get_parameter(Name='/bedrock-agent-data/Bedrock-agent-id')['Parameter']['Value']
agent_alias_id = ssm.get_parameter(Name='/bedrock-agent-data/Bedrock-agent-alias-id')['Parameter']['Value']

@me.page(
  path="/chat",
  title="Bedrock Agent Demo Chat",
)

def page():
  mel.chat(transform, title="Bedrock Agent Demo Chat", bot_user="Baseball Bot")

# Extract the SQL query and reply as it was sent to the Lambda in the orchestration phase.
def extract_sql(trace_dict: Dict[str, Any]) -> Dict[str, Any]:
    trace = {}

    orchestration_trace = trace_dict.get('orchestrationTrace', {})
    invocation_input = orchestration_trace.get('invocationInput', {})
    action_group_input = invocation_input.get('actionGroupInvocationInput', {})

    if action_group_input.get('apiPath') == '/querydatabase':
        parameters = action_group_input.get('parameters', [])
        for param in parameters:
            if param.get('name') == 'query':
                trace['sql'] = param.get('value')

    observation = orchestration_trace.get('observation', {})
    action_group_output = observation.get('actionGroupInvocationOutput', {})
    query_response = action_group_output.get('text')

    if query_response:
        trace['table'] = json.loads(query_response)

    return trace

def transform(input: str, history: list[mel.ChatMessage]):
    print(input)
    response = bedrock_agent_runtime_client.invoke_agent(
        agentAliasId=agent_alias_id,
        agentId=agent_id,
        inputText=input,
        enableTrace=True,
        sessionId="42",
    )
    completion = ""

    for event in response.get("completion"):
        chunk = event.get("chunk", {})
        completion = completion + chunk.get("bytes", b'').decode('utf-8')
        trace_chunk = event.get("trace", {}).get("trace", {})
        trace_chunk = extract_sql(trace_chunk)
        if trace_chunk:
          if 'sql' in trace_chunk:
            yield trace_chunk['sql']
          # elif 'table' in trace_chunk:
          #   yield trace_chunk['table']        
        if completion:
          yield completion

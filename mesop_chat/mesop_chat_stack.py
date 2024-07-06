
from aws_cdk import (
    Stack,
    CfnOutput,
    Duration,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_apprunner_alpha as apprunner,
    aws_logs as logs,
)

from constructs import Construct

class MesopChatStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

                # Create the role for the UI backend
        ui_backend_role = iam.Role(self, "Mesop UI Backend Role",
            role_name=f"AppRunnerMesopChatUIRole-{self.region}",
            assumed_by=iam.ServicePrincipal("tasks.apprunner.amazonaws.com"),
        )

        # Adding the permission to write to the X-Ray Daemon
        ui_backend_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AWSXRayDaemonWriteAccess"
            )
        )

        # Adding the permission to read from the parameter store
        ui_backend_role.add_to_policy(iam.PolicyStatement(
            sid="ReadSSM",
            effect=iam.Effect.ALLOW,
            actions=[
                "ssm:GetParameter",
                "ssm:GetParameters",
                "ssm:GetParametersByPath",
            ],
            resources=[
                f"arn:aws:ssm:{self.region}:{self.account}:parameter/bedrock-agent-data/*"
            ]
        ))

        # Adding the permission to invoke the agent in Bedrock
        ui_backend_role.add_to_policy(iam.PolicyStatement(
            sid="InvokeBedrockAgent",
            effect=iam.Effect.ALLOW,
            actions=[
                "bedrock:InvokeAgent",
            ],
            resources=[
                "*"
            ]
        ))

        github_connection_arn = ssm.StringParameter.value_for_string_parameter(
            self, 
            "/bedrock-agent-data/GitHubConnection"
        )

        repository_url = ssm.StringParameter.value_for_string_parameter(
            self, 
            "/mesop-chat/GitHubRepositoryURL"
        )


        # Create the UI backend using App Runner
        ui_hosting_service = apprunner.Service(
            self, 
            'MesopChatUIService', 
            source=apprunner.Source.from_git_hub(
                configuration_source= apprunner.ConfigurationSourceType.REPOSITORY,
                repository_url= repository_url,
                branch= 'master',
                connection= apprunner.GitHubConnection.from_connection_arn(github_connection_arn),
            ),
            service_name= "mesop-chat-ui",
            auto_deployments_enabled= True,
            instance_role=ui_backend_role,
        )

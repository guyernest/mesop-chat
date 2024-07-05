import aws_cdk as core
import aws_cdk.assertions as assertions

from mesop_chat.mesop_chat_stack import MesopChatStack

# example tests. To run these tests, uncomment this file along with the example
# resource in mesop_chat/mesop_chat_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MesopChatStack(app, "mesop-chat")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

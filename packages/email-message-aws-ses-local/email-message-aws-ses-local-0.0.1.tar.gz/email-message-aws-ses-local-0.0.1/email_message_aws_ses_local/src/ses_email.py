import os
import boto3
from botocore.exceptions import ClientError
from typing import List
from dotenv import load_dotenv
from logger_local.Logger import Logger
from message_local.MessageImportance import MessageImportance
from message_local.MessageLocal import MessageLocal
from message_local.Recipient import Recipient 



load_dotenv()

EMAIL_MESSAGE_AWS_SES_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 208
EMAIL_MESSAGE_AWS_SES_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = "email_message_aws_ses_local_python_package"
DEVELOPER_EMAIL = "emad.a@circ.zone"

logger = Logger.create_logger(object={
    "component_id": EMAIL_MESSAGE_AWS_SES_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    "component_name": EMAIL_MESSAGE_AWS_SES_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    "component_category": "Code",
    "developer_email": DEVELOPER_EMAIL
})

class EmailMessageAwsSesLocal(MessageLocal):
    def __init__(self, subject: str, body: str, importance: MessageImportance, to_recipients: List[Recipient],
                 ses_resource=None):
        self.ses_resource = ses_resource if ses_resource else boto3.client('ses', region_name=os.getenv('AWS_DEFAULT_REGION', 'us-west-2'))
        self.subject = subject
        super().__init__(original_body=body, importance=importance, to_recipients=to_recipients,
                         )

    def __send_email(self, recipient_email: str, body: str):
        try:
            response = self.ses_resource.send_email(
                Destination={'ToAddresses': [recipient_email]},
                Message={
                    'Body': {
                        'Text': {
                            'Charset': 'UTF-8',
                            'Data': body,
                        },
                    },
                    'Subject': {
                        'Charset': 'UTF-8',
                        'Data': self.subject,
                    },
                },
                Source=os.getenv('FROM_EMAIL', 'info@circ.zone'),  # Use provided or default sender email
                ConfigurationSetName=os.getenv('CONFIGURATION_SET', None)  # Set Configuration Set if provided
            )
            message_id = response['MessageId']
            logger.info(f"Email sent to {recipient_email} with message ID: {message_id}")
        except ClientError as e:
            logger.exception(f"Couldn't send email to {recipient_email}. Error: {e}")
            raise
        return message_id

    def send(self, body: str = None, recipients: List[Recipient] = None) -> List[str]:
        if body or recipients:
            self._set_body_after_text_template(body=body, to_recipients=recipients)
        recipients = self.get_recipients()
        logger.start(object={"body": body, "recipients": recipients})
        messages_ids = []
        for recipient in recipients:
            message_body = body or self.get_body_after_text_template(recipient)
            recipient_email = recipient.get_email()
            if recipient_email is not None:
                if os.getenv("REALLY_SEND_EMAIL") == '1':
                    message_id = self.__send_email(recipient_email, message_body)
                else:
                    print(f"EmailMessageAwsSesLocal.send REALLY_SEND_EMAIL is off: "
                          f"supposed to send email to {recipient_email} with body {message_body}")
                    message_id = '0'
            else:
                logger.warn(f"recipient.get_email() is None: {recipient}")
                message_id = '0'
            messages_ids.append(message_id)
        return messages_ids

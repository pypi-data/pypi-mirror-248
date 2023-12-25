import os
from typing import List

import boto3
from botocore.exceptions import ClientError
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

MAIL_TYPE_ID = 1
AWS_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-west-2')
FROM_EMAIL = os.getenv('FROM_EMAIL', 'info@circ.zone')


class EmailMessageAwsSesLocal(MessageLocal):
    def __init__(self, subject: str, body: str, importance: MessageImportance, to_recipients: List[Recipient],
                 ses_resource=None, api_type_id=MAIL_TYPE_ID, from_email=FROM_EMAIL,
                 configuration_set=os.getenv('CONFIGURATION_SET', None)):
        self.ses_resource = ses_resource or boto3.client('ses', region_name=AWS_REGION)
        self.subject = subject
        self.api_type_id = api_type_id  # Set API Type ID to 1 for Email Message AWS SES
        self.from_email = from_email
        self.configuration_set = configuration_set
        super().__init__(original_body=body, importance=importance, to_recipients=to_recipients,
                         api_type_id=api_type_id)

    def __send_email(self, recipient_email: str, body: str) -> str:
        """Returns the message ID of the email sent and the message ID of the email saved in the database"""
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
            # Example MessageId: '0100018c9e7552b1-b8932399-7049-492d-ae47-8f60967f49f1-000000'
            message_id = response['MessageId']
            logger.info(f"Email sent to {recipient_email} with message ID: {message_id}",
                        object={"message_id": message_id, "destination_emails": recipient_email})

        except ClientError as e:
            logger.exception(f"Couldn't send email to {recipient_email}. Error: {e}")
            raise
        return message_id

    def send(self, body: str = None, recipients: List[Recipient] = None) -> List[int]:
        if body or recipients:
            self._set_body_after_text_template(body=body, to_recipients=recipients)
        recipients = self.get_recipients()
        logger.start(object={"body": body, "recipients": recipients})
        messages_ids = []
        for recipient in recipients:
            message_body = body or self.get_body_after_text_template(recipient)
            recipient_email = recipient.get_email_address()
            if recipient_email is not None:
                if os.getenv("REALLY_SEND_EMAIL") == '1':
                    # TODO: call can_send and after_send_attempt with the proper parameters
                    if 1: #self.can_send(sender_profile_id=, api_data=, outgoing_body=):
                        email_messageid = self.__send_email(recipient_email, message_body)
                        # TODO: subject and body should be inside ml table
                        message_id = self.insert(data_json={"email_messageid": email_messageid,
                                                            "body": body,
                                                            "subject": self.subject,
                                                            "to_profile_id": recipient.get_profile_id(),
                                                            "to_email": recipient_email,
                                                            })
                        # self.after_send_attempt(sender_profile_id=, outgoing_body=, incoming_message=,
                        #                         http_status_code=, response_body=)
                else:
                    logger.info(f"EmailMessageAwsSesLocal.send REALLY_SEND_EMAIL is off: "
                                f"supposed to send email to {recipient_email} with body {message_body}")
                    message_id = 0  
            else:
                logger.warn(f"recipient.get_email() is None: {recipient}")
                message_id = 0  
            messages_ids.append(message_id)
        return messages_ids
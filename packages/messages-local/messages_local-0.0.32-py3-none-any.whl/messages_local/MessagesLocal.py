from datetime import datetime
from typing import List, Union

from dotenv import load_dotenv
from email_message_aws_ses_local.ses_email import (MAIL_TYPE_ID,
                                                   EmailMessageAwsSesLocal)
from label_message_local.LabelConstants import LabelsLocalConstants
from label_message_local.LabelMessage import LabelsMessageLocal
from logger_local.Logger import Logger
from message_local.MessageConstants import (AWS_EMAIL,
                                            AWS_SMS_MESSAGE_PROVIDER_ID,
                                            INFORU_MESSAGE_PROVIDER_ID)
from message_local.MessageImportance import MessageImportance
from message_local.MessageLocal import MessageLocal
from message_local.MessageType import MessageType
from message_local.Recipient import Recipient
from queue_worker_local.queue_worker import QueueWorker
from sms_message_aws_sns_local.sms_message_aws_sns import (
    SMS_MESSAGE_AWS_SNS_API_TYPE_ID, SmsMessageAwsSnsLocal)
# from whatsapp_message_local.whatsappmessage import WhatsAppMessage, WHATSAPP_MESSAGE_VONAGE_API_TYPE_ID
from whataspp_inforu_local.WhatsAppMessageInforuLocal import (
    WHATSAPP_MESSAGE_INFORU_API_TYPE_ID, WhatsAppMessageInforuLocal)

from .MessagesLocalConstants import (MESSAGE_ACTION_ID, MESSAGES_API_TYPE_ID,
                                     logger_object_message)

load_dotenv()

logger = Logger.create_logger(object=logger_object_message)


class MessagesLocal:
    # no classes type, so the worker can init it with json.
    def __init__(self, default_original_body: str = None, default_subject: str = None,
                 default_importance: int = MessageImportance.MEDIUM.value, to_recipients: List[dict] = None):
        self.to_recipients = to_recipients

        self.default_original_body = default_original_body
        self.default_subject = default_subject
        self.default_importance = default_importance
        self.label_crud = LabelsMessageLocal()
        self.queue_worker = QueueWorker(schema_name="message", table_name="message_table",
                                        view_name="message_outbox_view", id_column_name="message_id")

    # This method should be used by Queue Worker
    def send_sync(self, to_recipients: List[dict] = None, cc_recipients: List[dict] = None,
                  bcc_recipients: List[dict] = None,
                  original_body: str = None, importance: int = None,
                  sender_profile_id: int = None, original_subject: str = None,
                  template_id: int = None, user_external_id: int = None, campaign_id: int = None) -> None:
        """send method"""
        to_recipients = to_recipients or self.to_recipients
        original_body = original_body or self.default_original_body
        original_subject = original_subject or self.default_subject
        importance = MessageImportance(importance or self.default_importance)

        details = {
            "original_body": original_body,
            "to_recipients": to_recipients,
            "cc_recipients": cc_recipients,
            "bcc_recipients": bcc_recipients,
            "sender_profile_id": sender_profile_id,
            "original_subject": original_subject,
            "template_id": template_id,
            "user_external_id": user_external_id,
            "importance": importance,
            "campaign_id": campaign_id
        }
        logger.start("MessagesLocal send_sync()", object=details)
        to_recipients = self._get_recipients(to_recipients)
        cc_recipients = self._get_recipients(cc_recipients)
        bcc_recipients = self._get_recipients(bcc_recipients)

        for recipient in to_recipients:
            # the __class__ can be set only once, but for different recipients we might want different classes
            message_local = MessageLocal(original_body=original_body, original_subject=original_subject,
                                         to_recipients=to_recipients,
                                         api_type_id=MESSAGES_API_TYPE_ID)
            body = message_local.get_body_after_text_template(recipient)
            message_recipient_channel_id = message_local.get_message_channel_id(recipient)
            message_recipient_provider_id = message_local.get_message_provider_id(
                message_recipient_channel_id, recipient)
            if message_recipient_channel_id == MessageType.SMS.value and \
                    message_recipient_provider_id == AWS_SMS_MESSAGE_PROVIDER_ID:
                message_local.__class__ = SmsMessageAwsSnsLocal
                message_local._api_type_id = SMS_MESSAGE_AWS_SNS_API_TYPE_ID
            elif message_recipient_channel_id == MessageType.WHATSAPP.value and \
                    message_recipient_provider_id == INFORU_MESSAGE_PROVIDER_ID:
                message_local.__class__ = WhatsAppMessageInforuLocal
                message_local._api_type_id = WHATSAPP_MESSAGE_INFORU_API_TYPE_ID
                print("Sending WhatsApp message to recipient: ", recipient, "with body: ", body)
            elif message_recipient_channel_id == MessageType.EMAIL.value and \
                    message_recipient_provider_id == AWS_EMAIL:
                message_local.__class__ = EmailMessageAwsSesLocal
                message_local._api_type_id = MAIL_TYPE_ID
            else:
                # TODO We need to add to the message Recipient country, message plain text length after template,
                #  message HTML length after template, number of attachments, attachments' types and sizes.
                data = {"channel_id": message_recipient_channel_id,
                        "provider_id": message_recipient_provider_id,
                        "recipient": recipient,
                        "body": body,
                        "body_length": len(body),
                        "importance": importance,
                        "sender_profile_id": sender_profile_id,
                        "original_subject": original_subject,
                        "template_id": template_id,
                        "user_external_id": user_external_id,
                        "campaign_id": campaign_id
                        }
                error_message = "Don't know which MessageLocal class to use."
                logger.error(error_message, object=data)
                raise Exception(error_message + " Data: " + str(data))
            message_local.__init__(original_body=body, importance=importance, to_recipients=[recipient])
            message_local.send()

        logger.end()

    # This method will push the messages to the queue in message_outbox_table
    def send_scheduled(self, to_recipients: List[Recipient] = None, cc_recipients: List[Recipient] = None,
                       bcc_recipients: List[Recipient] = None,
                       start_timestamp: Union[str, datetime] = None, end_timestamp: Union[str, datetime] = None,
                       importance: MessageImportance = None,
                       sender_profile_id: int = None, original_subject: str = None, original_body: str = None,
                       template_id: int = None, user_external_id: int = None, campaign_id: int = None) -> int:
        """The message will be sent any time between start_timestamp and end_timestamp"""
        if not start_timestamp:
            start_timestamp = datetime.now()
        importance = importance or MessageImportance(self.default_importance)
        message_json = {
            "to_recipients": self._recipients_to_json(to_recipients),
            "cc_recipients": self._recipients_to_json(cc_recipients),
            "bcc_recipients": self._recipients_to_json(bcc_recipients),
            "sender_profile_id": sender_profile_id,
            "original_subject": original_subject,
            "original_body": original_body,
            "template_id": template_id,
            "user_external_id": user_external_id,
            "importance": importance.value,
            "campaign_id": campaign_id

        }
        class_json = {"default_original_body": self.default_original_body,
                      "default_subject": self.default_subject,
                      "default_importance": self.default_importance,
                      "to_recipients": self.to_recipients
                      }
        queue_id = self.queue_worker.push({"function_parameters_json": message_json,
                                           "class_parameters_json": class_json,
                                           "action_id": MESSAGE_ACTION_ID,
                                           "start_timestamp": start_timestamp,
                                           "end_timestamp": end_timestamp})
        try:
            self.label_crud.add_label(label_id=LabelsLocalConstants.MESSAGE_OUTBOX_LABEL_ID, message_id=queue_id)
        except Exception as e:
            logger.exception("Failed to add label to message", object=e)
        logger.info("Message pushed to the queue successfully", object={"queue_id": queue_id})
        return queue_id

    @staticmethod
    def _get_recipients(recipients: List[dict]) -> List[Recipient] | List | None:
        """get recipients"""
        if not recipients:
            return recipients  # None or []
        return [Recipient(**recipient) for recipient in recipients]

    @staticmethod
    def _recipients_to_json(recipients: List[Recipient]) -> List[dict] | List | None:
        """recipients to json"""
        if not recipients:
            return recipients
        return [recipient.to_json() for recipient in recipients]

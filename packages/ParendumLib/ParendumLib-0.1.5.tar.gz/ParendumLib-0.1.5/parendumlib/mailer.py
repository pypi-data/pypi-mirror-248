from typing import Tuple, Dict, List, Optional, Union
import imaplib
import email

from .logger import Logger


class GMailer:

    def __init__(self, email_address: str, password: str, logger: Logger = None, imap_server: str = 'imap.gmail.com'):
        self.email = email_address
        self.password = password
        self.imap_server = imap_server
        self.logger = logger
        self._mail = None

    def find_emails(self, target_email: str, search_flag: str = 'FROM', target_folder: str = 'inbox') -> list:
        if search_flag not in ['TO', 'FROM']:
            raise ValueError("search_flag must be 'TO' or 'FROM'")
        self._connect(target_folder)
        _search = f'({search_flag} "{target_email}")'
        result, data = self._mail.search(None, _search)
        if result != "OK":
            self.logger.info(f"Could not found emails {_search}")
            return []
        if not (email_ids := data[0].split()):
            self.logger.info(f"Could not found emails {_search}")
            return []
        return email_ids

    def read_email(self, email_id: str) -> Dict[str, Optional[Union[str, List[Tuple[str, str]]]]]:
        _, email_data = self._mail.fetch(email_id, '(RFC822)')
        raw_email = email_data[0][1]
        email_message = email.message_from_bytes(raw_email)

        result = {
            "text": None,
            "html": None,
            "headers": self._get_headers(email_message),
            "attachments": self._get_attachments(email_message)
        }

        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" in content_disposition:
                continue
            elif content_type == "text/plain" and not result["text"]:
                result["text"] = part.get_payload(decode=True).decode()
            elif content_type == "text/html" and not result["html"]:
                result["html"] = part.get_payload(decode=True).decode()

        return result

    def delete_emails(self, target_email: str, search_flag: str = 'FROM', target_folder: str = 'inbox'):
        self._connect(target_folder)
        for e_id in self.find_emails(target_email, search_flag, target_folder):
            self._delete_email(e_id)
        self._mail.expunge()
        self._mail.close()
        self._mail.logout()
        self.logger.info(f"All mails sent to {target_email} were removed successfully")

    def _connect(self, target_folder: str = 'inbox'):
        self._mail = imaplib.IMAP4_SSL(self.imap_server)
        self._mail.login(self.email, self.password)
        self._mail.select(target_folder)

    def _delete_email(self, email_id: str):
        self._mail.store(email_id, '+FLAGS', '\\Deleted')

    @staticmethod
    def _get_headers(email_message) -> Dict[str, str]:
        return {key: value for key, value in email_message.items()}

    @staticmethod
    def _get_attachments(email_message) -> List[Tuple[str, str]]:
        attachments = []
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if filename:
                payload = part.get_payload(decode=True)
                attachments.append((filename, payload))
        return attachments


if __name__ == '__main__':
    my_logger = Logger("localhost", api_key="183d96c0-0965-44fa-b7d7-d4fcf10610a5", api_secret="e4882d22-9d35-4f85-b32d-f497e8c08979", port=5626)
    mailer = GMailer("parendumou@gmail.com", "laeujjrdrxhwqnjo", my_logger)

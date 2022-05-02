from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pprint import pprint

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://mail.google.com/"]


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        results = {
            "labels": service.users().labels().list(userId="me").execute(),
            "messages": service.users().messages().list(userId="me").execute(),
            "threads": service.users()
            .threads()
            .list(userId="me", labelIds=["Label_6316554527288637446"])
            .execute(),
        }
        labels = results["labels"].get("labels", [])
        messages = results["messages"].get("messages", [])
        threads = results["threads"].get("threads", [])
        if not labels:
            print("No labels found.")
            return
        print("Labels:")
        for label in labels:
            print(label["name"], label["id"])
        # print("labels[0]", labels)
        # print("messages[0]", messages[0])
        print("threads[0]", threads[0])
        print('results["threads"]', results["threads"])
        # print(
        #     "kljhasdlkjahsdf",
        #     service.users()
        #     .messages()
        #     .get(userId="me", id="1808337e916a3656")
        #     .execute(),
        # )

        # my_messages = []
        # for mess in messages[:10000]:
        #     if hasattr(mess, "labelIds"):
        #         if "Label_3" in mess["labelIds"]:
        #             my_messages.append(mess)
        print("my_messages", messages[0])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()

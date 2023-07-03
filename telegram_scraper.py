import requests
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, ChatWriteForbiddenError, \
    InviteHashExpiredError, ChannelPrivateError, UserAlreadyParticipantError
from telethon.errors import FloodWaitError
from telethon.errors import MultiError

from telethon.tl.types import ContactStatus, UserStatusOnline, UserStatusOffline, UserStatusRecently, UserStatusLastWeek, UserStatusLastMonth, UserStatusEmpty

from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import types
from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantAdmin
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon import events
import sys
import csv
import os
import subprocess
import configparser
import traceback
import time

import sys
import csv
import traceback
from datetime import date, datetime, timedelta

# Subscribe to Solve4You Channel for more free script

api_id = 13029151
api_hash = '74d4448ff146eb7a9b9b003fcae17fdf'
phone = '+201503888316'

client = TelegramClient(str(phone), api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input(
        'Enter the code recieved to your Telegram messenger: '))


chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print('Choose a group to scrape members from:')
i = 0
for g in groups:
    print(str(i) + '- ' + g.title)
    i += 1

g_index = input("Enter a Number: ")
target_group = groups[int(g_index)]

print('Fetching Members...')
all_participants = []
all_participants = client.iter_participants(
    target_group, limit=None, filter=None, aggressive=True)

with open("data.csv", "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['sr. no.', 'username', 'user id',
                    'access hash', 'name', 'group', 'group id', 'last seen'])
    i = 0
    try:
        for user in all_participants:
            accept = True

            try:
                lastDate = user.status.was_online
                num_months = (datetime.now().year - lastDate.year) * \
                    12 + (datetime.now().month - lastDate.month)
                if (num_months > 1):
                    accept = False
            except:
                continue
            if (accept):
                i += 1
                if user.username:
                    username = user.username
                else:
                    username = ""
                if user.first_name:
                    first_name = user.first_name
                else:
                    first_name = ""
                if user.last_name:
                    last_name = user.last_name
                else:
                    last_name = ""
                name = (first_name + ' ' + last_name).strip()

                if isinstance(user.status, types.UserStatusOffline):
                    last_name = ""

                writer.writerow([username, user.id, user.access_hash, name,
                                target_group.title, target_group.id, user.status.was_online])
                time.sleep(0.1)

    except MultiError as e:
        # The first and third requests worked.
        first = e.results[0]
        second = e.exceptions[1]
        third = e.results[2]
        # The second request failed.

print('Members scraped successfully.')

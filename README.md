#fbmdown - Facebook Message Downloader
This is my small pet project but it might be useful for someone.
It does what is in its name: downloads whole conversation threads from your Facebook inbox folder!

Run `fbmdown-cli.py` and follow the help.

##How to get an Access Token?
- Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer)
- Click on `Get Access Token`
- Deselect all except the `read_mailbox` under `Extended Permissions`
- Click `Allow` in the pop-up. This will allow the `Graph API Explorer` app to access your inbox
- Select and copy the text from `Access Token` and insert it into `fbmdown.py` where it is needed
- Enjoy!


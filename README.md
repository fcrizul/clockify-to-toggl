# clockify2toggl.py
Import CSV from Clockify to Toggl via API

## Steps

1. Export CSV from Clockify with ```Start Date```, ```Start Time```, ```Duration (h)```, ```Description```, ```Project columns```

2. Obtain Toggl API access token.
Each user in Toggl.com has an API token. They can find it under "My Profile" in their Toggl account.

3. Run command

```
python3 clockify2toggl.py <API_TOKEN> <CSV_FILE>
```
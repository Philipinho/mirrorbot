
### MirrorBot
Rapidsave client for the Central Mirrorbot API [u/a-mirror-bot](https://np.reddit.com/user/a-mirror-bot).  

create a .env file with the following content:  

```
REDDIT_USERNAME=xxxxxxxxxxx
REDDIT_PASSWORD='xxxxxxxxxxxxxxxx'
REDDIT_CLIENT_ID='xxxxxxxxxxxxxxxx'
REDDIT_CLIENT_SECRET='xxxxxxxxxxxxxxxx'
USER_AGENT='centralized mirror for r/publicfreakout'
SUB_REDDIT_NAME='xxxxxxxxxxxxxxxx'
MIRROR_BOT_ACCESS_TOKEN='Key xxxxxxxxxxxxxxxx'
```

then run the container with:  
docker run -d --name mirrorbot --env-file=.env ghcr.io/philipinho/mirrorbot:latest  


# usage: python3 rd.py out.txt SUBREDDIT "phrase" ["phrase"...]  — Reddit search via OAuth
# Creds from ~/.config/gaphunt/reddit.env (never committed): REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET
# Untested: Reddit ended self-service app creation 2025-11-11, so no credential exists to run this.
import base64, json, os, pathlib, sys, time, urllib.parse, urllib.request

env = {}
for line in pathlib.Path.home().joinpath(".config/gaphunt/reddit.env").read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()

UA = "gaphunt/0.1 by u/" + env.get("REDDIT_USERNAME", "anon")
auth = base64.b64encode(
    f"{env['REDDIT_CLIENT_ID']}:{env['REDDIT_CLIENT_SECRET']}".encode()).decode()
req = urllib.request.Request(
    "https://www.reddit.com/api/v1/access_token",
    data=b"grant_type=client_credentials",
    headers={"Authorization": f"Basic {auth}", "User-Agent": UA})
token = json.load(urllib.request.urlopen(req))["access_token"]

out, sub, phrases = sys.argv[1], sys.argv[2], sys.argv[3:]
with open(out, "w") as f:
    for p in phrases:
        url = (f"https://oauth.reddit.com/r/{sub}/search?q={urllib.parse.quote(p)}"
               "&restrict_sr=1&sort=relevance&t=year&limit=25")
        r = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {token}", "User-Agent": UA})
        children = json.load(urllib.request.urlopen(r))["data"]["children"]
        f.write(f"\n### r/{sub} :: {p} ({len(children)} hits)\n")
        for c in children:
            d = c["data"]
            body = (d.get("selftext") or "").replace("\n", " ")
            f.write(f"{time.strftime('%Y-%m-%d', time.gmtime(d['created_utc']))} | "
                    f"{d.get('score')} | {d.get('title','')} | {body[:400]}\n")
        time.sleep(1)
print("wrote", out)

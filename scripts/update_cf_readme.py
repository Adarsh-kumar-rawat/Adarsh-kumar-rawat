#!/usr/bin/env python3
import requests, re

HANDLE = "isanz"
README = "README.md"
START = "<!-- CF-STATS:START -->"
END = "<!-- CF-STATS:END -->"

def fetch_user(handle):
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    if data["status"] != "OK":
        raise RuntimeError(f"Codeforces API error: {data}")
    return data["result"][0]

def make_card(u):
    name = u["handle"]
    rating = u.get("rating", "Unrated")
    maxRating = u.get("maxRating", "—")
    rank = u.get("rank", "—").title()
    maxRank = u.get("maxRank", "—").title()
    contrib = u.get("contribution", 0)
    avatar = u.get("titlePhoto", "https://sta.codeforces.com/s/59454/images/codeforces-telegram.png")

    return f"""
<table>
<tr>
<td>
**[{name}](https://codeforces.com/profile/{name})**  
🏆 **Rating:** {rating}  
🔥 **Max Rating:** {maxRating}  
🎖️ **Rank:** {rank}  
⚡ **Max Rank:** {maxRank}  
💬 **Contributions:** {contrib}
</td>
<td><img src="{avatar}" width="100" height="100" /></td>
</tr>
</table>
"""

def replace_section(content, start, end, new):
    pattern = re.compile(re.escape(start) + ".*?" + re.escape(end), re.DOTALL)
    return pattern.sub(f"{start}\n{new}\n{end}", content)

def main():
    user = fetch_user(HANDLE)
    card = make_card(user)
    with open(README, encoding="utf-8") as f:
        text = f.read()
    new_text = replace_section(text, START, END, card)
    if new_text != text:
        with open(README, "w", encoding="utf-8") as f:
            f.write(new_text)
        print("✅ README updated.")
    else:
        print("ℹ️ No changes needed.")

if __name__ == "__main__":
    main()

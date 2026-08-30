import os
import re
import urllib.request
import json

USERNAME = "xeeshan-zs"
API_URL = f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&per_page=15"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github.v3+json"
}

token = os.environ.get("GITHUB_TOKEN")
if token:
    headers["Authorization"] = f"Bearer {token}"

req = urllib.request.Request(API_URL, headers=headers)

repos = []
try:
    with urllib.request.urlopen(req) as response:
        repos = json.loads(response.read().decode())
except Exception as e:
    print(f"API notice: {e}")

filtered_repos = []
for repo in repos:
    name = repo.get("name")
    if repo.get("fork") or name == USERNAME or name == "xeeshan-zs":
        continue
    filtered_repos.append(repo)

top_repos = filtered_repos[:3]

if top_repos:
    primary = top_repos[0]
    p_name = primary.get("name")
    p_url = primary.get("html_url")
    p_desc = primary.get("description")
    p_home = primary.get("homepage")
    
    home_str = f" -> [{p_home}]({p_home})" if p_home else ""
    desc_str = f" - *{p_desc}*" if p_desc else ""
    
    current_lines = [f"- :telescope: Currently grinding on **[{p_name}]({p_url})**{desc_str}{home_str}"]
    
    if len(top_repos) > 1:
        other_lines = []
        for r in top_repos[1:]:
            r_name = r.get("name")
            r_url = r.get("html_url")
            r_desc = r.get("description")
            r_desc_str = f" - {r_desc}" if r_desc else ""
            other_lines.append(f"  - :zap: **[{r_name}]({r_url})**{r_desc_str}")
        
        current_lines.append("- :crossed_swords: **Recent Quests & Dungeons:**")
        current_lines.extend(other_lines)
    
    new_content = "\n".join(current_lines)

    readme_path = "README.md"
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        pattern = r"(<!-- RECENT_REPOS:START -->)(.*?)(<!-- RECENT_REPOS:END -->)"
        replacement = f"\\1\n{new_content}\n\\3"
        
        if re.search(pattern, content, flags=re.DOTALL):
            updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print("README.md updated with latest active repos!")
else:
    print("No new repo data fetched or rate limited, keeping existing entries.")
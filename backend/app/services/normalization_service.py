from collections import Counter


def normalize_profile(github_username: str, leetcode_data: dict, github_data: dict) -> dict:
    matched = leetcode_data["matchedUser"]
    solved_counts = {x["difficulty"]: x["count"] for x in matched["submitStats"]["acSubmissionNum"]}
    repos = github_data["repos"]

    language_counter = Counter([repo.get("language") for repo in repos if repo.get("language")])
    skills = [lang for lang, _ in language_counter.most_common(6)]

    return {
        "username": github_username,
        "platform": ["github", "leetcode"],
        "problems_solved": solved_counts.get("All", 0),
        "repos": [
            {
                "name": repo["name"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "language": repo.get("language") or "Unknown",
                "commits_proxy": repo["size"],
                "url": repo["html_url"],
                "description": repo.get("description") or "",
            }
            for repo in repos
        ],
        "skills": skills,
        "languages": dict(language_counter),
        "activity": {
            "public_repos": github_data["user"].get("public_repos", 0),
            "followers": github_data["user"].get("followers", 0),
            "leetcode_reputation": matched["profile"].get("reputation", 0),
        },
        "rank": str(matched["profile"].get("ranking") or "Unranked"),
    }

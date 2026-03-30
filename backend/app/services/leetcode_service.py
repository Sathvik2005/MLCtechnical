import httpx

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"


async def fetch_leetcode_user(username: str) -> dict:
    query = """
    query getUserProfile($username: String!) {
      allQuestionsCount { difficulty count }
      matchedUser(username: $username) {
        username
        profile { ranking reputation }
        submitStats {
          acSubmissionNum { difficulty count }
        }
      }
    }
    """
    payload = {"query": query, "variables": {"username": username}}
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(LEETCODE_GRAPHQL_URL, json=payload)
        response.raise_for_status()
        data = response.json()

    user = data.get("data", {}).get("matchedUser")
    if not user:
        raise ValueError(f"LeetCode user '{username}' not found")

    return data["data"]

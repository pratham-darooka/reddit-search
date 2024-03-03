from googleapiclient.discovery import build
import praw
from file_handling import save_post_to_file, reset_directory
from query_rewriting import rewrite_query
from rag import search_posts
from globals import DIRECTORY, GOOGLE_DEV_KEY, REDDIT_USER_AGENT, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, GOOGLE_CUSTOM_SEARCH_ENGINE_KEY
from logger import logger

def get_reddit_posts(query: str) -> dict:
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    service = build(
        "customsearch", "v1", developerKey=GOOGLE_DEV_KEY
    )
    logger.info(f"Fetching Reddit Posts for: {query}")
    res = (
        service.cse()
        .list(
            q=query,
            cx=GOOGLE_CUSTOM_SEARCH_ENGINE_KEY,
        )
        .execute()
    )
    logger.info(f"Successfully fetched posts!")
    logger.debug("Results Obtained:")
    logger.debug(res)
    return res

def get_post_content_and_comments(url: str) -> tuple:
    # Initialize the Reddit API wrapper
    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                         client_secret=REDDIT_CLIENT_SECRET,
                         user_agent=REDDIT_USER_AGENT)

    # Extract submission ID from the URL
    submission_id = url.split('/')[-3]
    # Fetch the submission (post)
    submission = reddit.submission(id=submission_id)
    # Extract post content
    post_title = url.split('/')[-2]
    post_content = submission.selftext

    # Extract comments
    comments = []
    submission.comments.replace_more(limit=None)  # Retrieve all comments
    for comment in submission.comments.list():
        comments.append(comment.body)

    return post_title, post_content, comments

def get_relevant_reddit_posts(user_request: str) -> None:
    logger.info(f"User Request: {user_request}")

    query = rewrite_query(user_request)

    search_results = get_reddit_posts(query=query)['items']
    reset_directory(directory=DIRECTORY)

    for search_result in search_results:
        url = search_result['link']

        post_title, post_content, comments = get_post_content_and_comments(url)
        logger.debug(f"--> {post_title}")

        save_post_to_file(url, post_title, post_content, comments, directory=DIRECTORY)

def search_reddit(user_request: str, directory: str) -> str:
    get_relevant_reddit_posts(user_request)
    return search_posts(user_request)

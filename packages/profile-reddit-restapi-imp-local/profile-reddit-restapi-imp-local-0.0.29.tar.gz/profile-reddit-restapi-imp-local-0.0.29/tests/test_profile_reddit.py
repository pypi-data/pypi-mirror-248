from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum

import praw
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Add the parent directory to the path so we can import the script
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))
from profile_reddit_restapi_imp_python_package.search_reddit import Reddit                            # noqa: E402
from profile_reddit_restapi_imp_python_package.handler import RedditImporter                          # noqa: E402
from profile_reddit_restapi_imp_python_package.ProfileRedditConstants import (                        # noqa: E402
    PROFILE_REDDIT_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    PROFILE_REDDIT_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME
)

object_to_insert = {
    'component_id': PROFILE_REDDIT_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': PROFILE_REDDIT_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
    'developer_email': 'yoav.e@circ.zone'
}

logger = Logger.create_logger(object=object_to_insert)


def test_authenticate_reddit():
    logger.start()
    reddit = Reddit()._authenticate_reddit()

    result = isinstance(reddit, praw.Reddit)
    logger.end(object={'result': result})
    assert result


def test_get_subreddit_and_query():
    FUNNY = "funny"
    USER_COUNT = 10
    logger.start()
    request = {"subreddit_name": FUNNY, "user_count": USER_COUNT}
    reddit_object = Reddit()
    subreddit_name, num = reddit_object.get_subreddit_and_query(request=request)
    logger.info(f"subreddit_name {subreddit_name}")
    logger.info(f"num {num}")
    assert subreddit_name == "funny"
    assert num == 10
    logger.end()


def test_handle():
    logger.start()
    event_json = {
                    "subreddit_name": "funny",
                    "user_count": 1
                 }
    reddit_object = RedditImporter()
    reddit_object.handle(event_json)
    logger.end()

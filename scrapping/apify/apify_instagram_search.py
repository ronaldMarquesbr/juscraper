from apify_actors_constants import INSTAGRAM_HASHTAG_SCRAPER
from apify_support import get_dataset_items

def get_hashtag_posts(
    client,
    hashtags,
    results_type = "posts",
    results_limit = 20
):
    params = {
        "hashtags": hashtags,
        "results_type": results_type,
        "resultsLimit": results_limit
    }

    run = client.actor(INSTAGRAM_HASHTAG_SCRAPER).call(run_input=params)

    return get_dataset_items(client, run["defaultDatasetId"])
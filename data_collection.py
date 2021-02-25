import os
import yaml

config = dict(
    search_tweets_api = dict(
        account_type = 'premium',
        endpoint = 'https://api.twitter.com/1.1/tweets/search/fullarchive/DEV.json',
        consumer_key =  os.environ.get('TWITTER_API_KEY'),
        consumer_secret =  os.environ.get('TWITTER_API_SECRET')
    )
)

with open('twitter_keys_fullarchive.yaml', 'w') as config_file:
    yaml.dump(config, config_file, default_flow_style=False)

from searchtweets import load_credentials

premium_search_args = load_credentials("twitter_keys_fullarchive.yaml",
                                       yaml_key="search_tweets_api",
                                       env_overwrite=False)
print(premium_search_args)

from searchtweets import gen_rule_payload 
query = "(#COVID19 OR rules OR rule) (lockdown OR curfew 0R #curfew OR #lockdown) point_radius:[-1.133849 52.630847 35km]"
rule = gen_rule_payload(query, results_per_call=100, from_date="2020-03-20", to_date="2020-06-20", )

from searchtweets import ResultStream

rs = ResultStream(rule_payload=rule,
                  max_results=3000,
                  **premium_search_args)
print(rs)

import json
with open('tweetsData.jsonl', 'a', encoding='utf-8') as f:
    for tweet in rs.stream():
        json.dump(tweet, f)
        print(tweet)
        f.write('\n')
print('done')
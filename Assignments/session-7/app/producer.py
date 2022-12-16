#!/usr/bin/env python
import sys
import time
import logging
import json
import twint
import nest_asyncio
from datetime import datetime
from argparse import ArgumentParser
from confluent_kafka import Producer

# Optional per-message delivery callback (triggered by poll() or flush())
# when a message has been successfully delivered or permanently
# failed delivery (after retries).
def delivery_callback(err, msg) -> None:
    if err:
        print(f'ERROR: Message failed delivery: {err}')
    else:
        message = '{} Produced message on topic {} with value of {}\n'.format(
            msg.key(),msg.topic(), msg.value())
        logger.info(message)
        print(message)

def retrieve_tweet(topic: str, limit_search: int) -> None:
    # tweets_as_objects = []
    nest_asyncio.apply()
    # Configure Intelligent Tool
    ct = twint.Config()
    ct.Search = topic
    ct.Lang = "en"
    ct.Since = '2022-01-01'
    ct.Limit = limit_search
    ct.Hide_output = True
    ct.Store_object = True
    ct.Store_json = True
    ct.Output = f"data/search-{topic}-tweets.json"
    # ct.Store_object_tweets_list = tweets_as_objects

    # Run
    twint.run.Search(ct)

    tweets_as_objects = twint.output.tweets_list

    for tweet in tweets_as_objects:
        get_tweet={
                'id': tweet.id,
                'conversation_id': tweet.conversation_id,
                'datetime': str(tweet.datestamp) + ' ' + str(tweet.timestamp) + ' ' + str(tweet.timezone),
                'user_id':tweet.user_id,
                'tweet':tweet.tweet
                
            }
        msg = json.dumps(get_tweet)
        print(msg)
        prd.poll(1)
        prd.produce('twitter_streaming', msg.encode('utf-8'), callback=delivery_callback)
        prd.flush()
        time.sleep(3)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S',
                        filename=f'data/{datetime.now().strftime("%Y-%m-%d_%H.%M.%S"}-producer.log',
                        filemode='w')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    ####################
    # Create Producer instance
    prd = Producer({'bootstrap.servers':'localhost:9092'})
    print('Kafka Producer has been initiated...')
    ####################

    parser = ArgumentParser(description='> Kafka Streaming Twitter Custom Search Topic <')
    parser.add_argument('-S', '--topic_search_term', type=str, metavar='Twitter Search',
    help='Type what you want to search for the Tweet', default='Musk')
    parser.add_argument('-L', '--limit_search', type=int, metavar='Tweet Get Limit Number',
    help='Twitter get Tweet limit', default=1000)
    args = parser.parse_args()

    retrieve_tweet(args.topic_search_term, args.limit_search)
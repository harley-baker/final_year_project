import csv
import json
from datetime import datetime, timezone

DATE_FORMAT = '%a %b %d %H:%M:%S %z %Y'


def parse(input_tsv, input_json, output_file):
    print('Starting %s' % input_tsv)
    with open(input_tsv, 'r') as tsv:
        reader = [line.strip().split('\t') for line in tsv]
        with open(input_json) as f:
            data = json.load(f)
            with open(output_file, mode='a', newline='') as out:
                out_writer = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                user_exists = 'user' in data[0]
                for line in reader:
                    account_id = int(line[0])
                    account_class = line[1]
                    for account in data:
                        # Write to file
                        data = parse_json_to_data(account, user_exists, account_id)
                        out_writer.writerow([
                            float(account_id),
                            data['status_count'],
                            data['follower_count'],
                            data['friends_count'],
                            data['favourites_count'],
                            data['listed_count'],
                            data['default_profile'],
                            data['profile_use_background_image'],
                            data['verified'],
                            float(data['tweet_freq']),
                            float(data['follower_growth_rate']),
                            float(data['friend_growth_rate']),
                            float(data['favourites_growth_rate']),
                            float(data['listed_growth_rate']),
                            float(data['followers_friends_ratio']),
                            data['screen_name_length'],
                            data['num_digits_in_screen_name'],
                            data['name_length'],
                            data['num_digits_in_name'],
                            data['description_length'],
                            account_class
                        ])

    print('Done with %s' % input_tsv)


def parse_json_to_data(json_obj, user_exists, account_id=None):
    if user_exists:
        user = json_obj['user']
        created_at = json_obj['created_at']
        user_id = user['id']
        user_age = datetime.now(timezone.utc) - datetime.strptime(created_at,
                                                                  '%a %b %d %H:%M:%S %z %Y')
    else:
        user = json_obj
        created_at = json_obj['user_created_at']
        user_id = user['user_id']
        user_age = datetime.now() - datetime.strptime(created_at, '%a %b %d %H:%M:%S %Y')
    if user_id == account_id or account_id is None:
        # Get feature data
        data = {}
        # Metadata features
        data['status_count'] = user['statuses_count']
        data['follower_count'] = user['followers_count']
        data['friends_count'] = user['friends_count']
        data['favourites_count'] = user['favourites_count']
        data['listed_count'] = user['listed_count']
        data['default_profile'] = user['default_profile']
        data['profile_use_background_image'] = user['profile_use_background_image']
        data['verified'] = user['verified']
        data['screen_name'] = user['screen_name']
        data['name'] = user['name']
        data['description'] = user['description']

        # Derived features
        data['tweet_freq'] = user['statuses_count'] / user_age.seconds
        data['follower_growth_rate'] = data['follower_count'] / user_age.seconds
        data['friend_growth_rate'] = data['friends_count'] / user_age.seconds
        data['favourites_growth_rate'] = data['favourites_count'] / user_age.seconds
        data['listed_growth_rate'] = data['favourites_count'] / user_age.seconds
        data['followers_friends_ratio'] = data['follower_count'] / data['friends_count'] if\
            data['friends_count'] > 0 else 0
        data['screen_name_length'] = len(data['screen_name'])
        data['num_digits_in_screen_name'] = sum(c.isdigit() for c in data['screen_name'])
        data['name_length'] = len(data['name'])
        data['num_digits_in_name'] = sum(c.isdigit() for c in data['name'])
        data['description_length'] = len(data['description']) if data['description'] else 0
        return data

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
                        if user_exists:
                            user = account['user']
                            created_at = account['created_at']
                            user_id = user['id']
                            user_age = datetime.now(timezone.utc) - datetime.strptime(created_at,
                                                                                      '%a %b %d %H:%M:%S %z %Y')
                        else:
                            user = account
                            created_at = account['user_created_at']
                            user_id = user['user_id']
                            user_age = datetime.now() - datetime.strptime(created_at, '%a %b %d %H:%M:%S %Y')
                        if user_id == account_id:
                            # Get feature data

                            # Metadata features
                            status_count = user['statuses_count']
                            follower_count = user['followers_count']
                            friends_count = user['friends_count']
                            favourites_count = user['favourites_count']
                            listed_count = user['listed_count']
                            default_profile = user['default_profile']
                            profile_use_background_image = user['profile_use_background_image']
                            verified = user['verified']
                            screen_name = user['screen_name']
                            name = user['name']
                            description = user['description']

                            # Derived features
                            tweet_freq = user['statuses_count'] / user_age.seconds
                            follower_growth_rate = follower_count / user_age.seconds
                            friend_growth_rate = friends_count / user_age.seconds
                            favourites_growth_rate = favourites_count / user_age.seconds
                            listed_growth_rate = favourites_count / user_age.seconds
                            followers_friends_ratio = follower_count / friends_count if friends_count > 0 else 0
                            screen_name_length = len(screen_name)
                            num_digits_in_screen_name = sum(c.isdigit() for c in screen_name)
                            name_length = len(name)
                            num_digits_in_name = sum(c.isdigit() for c in name)
                            description_length = len(description) if description else 0

                            # Write to file
                            out_writer.writerow([
                                float(account_id),
                                status_count,
                                follower_count,
                                friends_count,
                                favourites_count,
                                listed_count,
                                default_profile,
                                profile_use_background_image,
                                verified,
                                float(tweet_freq),
                                float(follower_growth_rate),
                                float(friend_growth_rate),
                                float(favourites_growth_rate),
                                float(listed_growth_rate),
                                float(followers_friends_ratio),
                                screen_name_length,
                                num_digits_in_screen_name,
                                name_length,
                                num_digits_in_name,
                                description_length,
                                account_class
                            ])

    print('Done with %s' % input_tsv)

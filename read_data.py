from pandas import DataFrame
import json

# TODO HH: Work in progress. Ez Way to access data. May switch to python generator. 
def get_data():
    user_following = DataFrame.from_csv(
        './data/output_user_follow_pl_partial.csv', sep='\t')
    track_features = DataFrame.from_csv(
        './data/track_features_info_partial.csv')
    track_features.set_index("id", inplace=True)

    track_lists = json.loads(
        open('./data/creator_pl_partial.json', 'r').read())

    big_dict = {}

    for user in track_lists:
        for playlist in track_lists[user]:
            big_dict[playlist] = {}
            for track in track_lists[user][playlist]:
                big_dict[playlist][track] = {}
                print track_features.loc[track]


def main():
    user_following = DataFrame.from_csv(
        './data/output_user_follow_pl_partial.csv', sep='\t')
    track_features = DataFrame.from_csv(
        './data/track_features_info_partial.csv')
    # get_data()

if __name__ == '__main__':

    main()

import argparse
import duolingo
import inspect
import glob
import json

# Update data from base.md to README.md
def update_reademe(streak_num, total_dis):
    with open('base.md', 'r') as f:
        base_md = f.read()
    readme_md = base_md.replace('STREAK-NUM', str(streak_num)).replace('TOTAL-DIS', str(round(total_dis, 1)))
    with open('README.md', 'w') as f:
        f.write(readme_md)

# Fetch 'Duolingo' streak number
def get_duolingo_streak(DUOLINGO_USERNAME, DUOLINGO_JWT):
    source = inspect.getsource(duolingo)
    new_source = source.replace('jwt=None', 'jwt')
    new_source = source.replace('self.jwt = None', ' ')
    exec(new_source, duolingo.__dict__)

    lingo = duolingo.Duolingo(username = DUOLINGO_USERNAME, jwt = DUOLINGO_JWT)
    data = lingo.get_streak_info()
    streak_num = data.get('site_streak')
    return streak_num

# Parse 'Nike Run Club' activity log
def parse_nrc_activity():
    for file in glob.glob('activities/*.json'):
        with open(file, 'r') as f:
            json_data = json.loads(f.read())
            summaries = json_data['summaries']
            for summary in summaries:
                if summary['metric'] == 'distance':
                    total_dis += summary['value']
    return total_dis


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("duolingo_username", help = "usename for Duolingo")
    parser.add_argument("duolingo_jwt", help = "API access token for Duolingo")
    options = parser.parse_args()
    streak_num = get_duolingo_streak(options.duolingo_username, options.duolingo_jwt)
    total_dis = parse_nrc_activity()
    update_reademe(streak_num, total_dis)

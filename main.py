import duolingo
import os
from dotenv import load_dotenv
import glob
import json

load_dotenv()

# Parse 'Nike Run Club' activity log
total_dis = 0.0
for file in glob.glob('activities/*.json'):
    with open(file, 'r') as f:
        json_data = json.loads(f.read())
        summaries = json_data['summaries']
        for summary in summaries:
            if summary['metric'] == 'distance':
                total_dis += summary['value']

# Fetch 'Duolingo' streak number
lingo = duolingo.Duolingo(os.environ['DUOLINGO_ID'], os.environ['DUOLINGO_PW'])
data = lingo.get_streak_info()
streak_num = data.get('site_streak')

# Update data from base.md to README.md
with open('base.md', 'r') as f:
    base_md = f.read()
readme_md = base_md.replace('STREAK-NUM', str(streak_num)).replace('TOTAL-DIS', str(round(total_dis, 1)))
with open('README.md', 'w') as f:
    f.write(readme_md)

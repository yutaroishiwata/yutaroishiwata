import duolingo
import inspect
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
source = inspect.getsource(duolingo)
new_source = source.replace('jwt=None', 'jwt')
new_source = source.replace('self.jwt = None', ' ')
exec(new_source, duolingo.__dict__)

lingo = duolingo.Duolingo(username = os.environ['DUOLINGO_USERNAME'], jwt = os.environ['DUOLINGO_JWT'])
data = lingo.get_streak_info()
streak_num = data.get('site_streak')

# Update data from base.md to README.md
with open('base.md', 'r') as f:
    base_md = f.read()
readme_md = base_md.replace('STREAK-NUM', str(streak_num)).replace('TOTAL-DIS', str(round(total_dis, 1)))
with open('README.md', 'w') as f:
    f.write(readme_md)

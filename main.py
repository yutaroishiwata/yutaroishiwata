import duolingo
import os
from dotenv import load_dotenv

load_dotenv()

# Get 'Duolingo' streak number
lingo  = duolingo.Duolingo(os.environ['DUOLINGO_ID'], os.environ['DUOLINGO_PW'])
data = lingo.get_streak_info()
streak_num = data.get('site_streak')

# Update data from base.md to README.md
with open('base.md', 'r') as f:
    base_md = f.read()
readme_md = base_md.replace('STREAK-NUM', str(streak_num))
with open('README.md', 'w') as f:
    f.write(readme_md)

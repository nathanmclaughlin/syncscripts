"""Testing dataset. Scratchpad"""

import ConfigParser, dataset

ini = 'config.ini'
config = ConfigParser.SafeConfigParser()
config.read(ini)

db = dataset.connect(config.get('StudentDB','dsn'))



table = db['REG']


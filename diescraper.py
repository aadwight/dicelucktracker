import re

rollbot_name = 'Dr QuantumBOT'
filename = 'die_raw.txt'

class DieScraper:

    def __init__(self):
        self.rollbot_name = rollbot_name
        self.columns = {'name', 'roll_type', 'result'}

    def extract_rolls(self, filename):
        rolls = []
        line_num = 0
        try:
            for line in open(filename):
                line_num += 1
                line = line.strip()
                markers = {'Today'}
                roll_marker = '!roll'

                for marker in markers:
                    if marker in line:
                        name = line[0:line.find(marker)]
                        if name != rollbot_name:
                            person = name
                if roll_marker in line:
                    die_roll = line[len(roll_marker):].strip()
                    if('+' in die_roll):
                        die_roll = die_roll[0:die_roll.find('+')].strip()
                rolled_marker = person + ' rolled'
                if rolled_marker in line:
                    result = line[len(rolled_marker):].strip()
                    if ' ' in result:
                        result = result[0:result.find(' ') + 1]
                    roll_data = [person, die_roll, result]
                    self.validate_roll_data(*roll_data)
                    rolls.append(roll_data)
            return rolls
        except AssertionError as e:
            raise ValueError('Input error on line %s -- %s' % (line_num, e))

    def validate_roll_data(self, person, die_roll, result):
        assert re.search(r'[0-9]+d[0-9]+.*', die_roll), "bad die roll: %s" % (die_roll)
        assert re.search(r'\[[0-9]+\]', result), "bad result: %s" % (result)


if __name__ == '__main__':
    scraper = DieScraper()
    rolls = scraper.extract_rolls(filename)
    print(rolls)

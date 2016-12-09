import MySQLdb
import json
from collections import defaultdict


class QuestionSet(dict):
    def __init__(self, host, user, password, db_name):
        self._dups = defaultdict(list)

        db = MySQLdb.connect(host=host, user=user, passwd=password, db=db_name)
        self._load_all_questions(db)

        for q, v in self.iteritems():
            try:
                self._dups[v['Id']] += map(str, v['dups'])
                for d in v['dups']:
                    self._dups[str(d)].append(v['Id'])
            except KeyError:
                pass
        db.close()

    def _load_all_questions(self, db):
        cur = db.cursor()
        cur.execute('SELECT * FROM dup_questions')

        for row in cur:
            try:
                self[row[0]] = json.loads(row[1], strict=False)
            except ValueError:
                pass

    def get_dup(self, qid):
        return self._dups[qid]


if __name__ == '__main__':
    questions = QuestionSet('ec2-52-91-216-34.compute-1.amazonaws.com', 'root', '123456', 'pds_team')
    print questions.values()[18:19]
    print len(questions)
    for i in questions.values():
        print i['Tags']

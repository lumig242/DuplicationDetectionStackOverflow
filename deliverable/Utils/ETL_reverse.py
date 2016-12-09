import json
import MySQLdb

fp_dup = open("duped_questions", "w")
cnx = MySQLdb.connect(user='root', password='123456',
                              host='ec2-52-91-216-34.compute-1.amazonaws.com',
                              database='pds_team')

all_questions = MySQLdb.connect(user='root', password='123456',
                              host='ec2-52-91-216-34.compute-1.amazonaws.com',
                              database='pds_team')
no_dup = []
cnx.query("SELECT * FROM dup_questions")
res = cnx.use_result()
count = 0
while True:
    result = res.fetch_row(maxrows=100)
    if len(result) == 0:
        break
    count += 100
    print str(count) + " items is completed"
    for id, post_json in result:
        try:
            print post_json
            post = json.loads(post_json)
            if len(post['dups']) == 0:
                no_dup.append(id)
            else:
                for dup_id in post["dups"]:
                    all_questions.query("SELECT * FROM all_questions WHERE id=" + str(dup_id))
                    all_res = all_questions.store_result()
                    for _, item in all_res.fetch_row():
                        fp_dup.write(str(dup_id) + "wcyz666SQL" + item + "\n")
        except:
            pass
fp_dup.close()
cnx.close()
print no_dup
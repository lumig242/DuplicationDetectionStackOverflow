import re
import sys
import json

regex = re.compile('([a-z0-9]+)="([^"]+)"', re.I)
dup_id = re.compile("stackoverflow.com/questions/(\d+)/")

fp_all = open("all_questions", "w")
fp_dup = open("dup_questions", "w")
with open(sys.argv[1], "r") as fp:
    for line in fp:
        try:
            line = line.strip()
            post = dict(re.findall(regex, line))
            if "Id" not in post:
                continue

            if "has already been answered" in post["Body"] or ("Title" in post and "[duplicate]" in post["Title"]):
                post["dups"] = [int(num) for num in re.findall(dup_id, post["Body"])]
                fp_dup.write(post["Id"] + "wcyz666SQL" + json.dumps(post) + "\n")

            fp_all.write(post["Id"] + "wcyz666SQL" + json.dumps(post) + "\n")
        except:
            pass
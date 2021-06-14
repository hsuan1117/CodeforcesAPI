import CodeforcesAPI

cf = CodeforcesAPI.Codeforces()
data = cf.contest().list()
print(data)

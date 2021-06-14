import CodeforcesAPI

cf = CodeforcesAPI.Codeforces()
data = cf.contest().users()[0].blogs()
print(data)
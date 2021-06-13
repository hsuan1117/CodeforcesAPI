import CodeforcesAPI

cf = CodeforcesAPI.Codeforces()
data = cf.contest().submissions(with_subtasks=True,with_simple_handle=True,with_simple_problem=True)
print(data)
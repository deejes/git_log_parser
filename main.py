# Script to get total commits by contributor, and commits that contained specific keywords from commit logs 

# generate commit files with ->
# git log --no-merges --stat --pretty=format:'{%n  "sanitized_subject_line": "%f" ,%n "name": "%aN",%n  "date": "%aD"%n %n}' > log.txt

filename = "git_logs.txt"
file = open(filename, "r")

def break_file_into_commits(input_file):
    # returns an array of commits in a file
    result = []
    commit_body = ''
    mapper = {}
    for line in input_file:
        if len(line) > 1:
            commit_body += line
        if len(line) == 1:
            if commit_body.find("san") > 1: # excludes empty lines
                result.append(commit_body)
                commit_body = ''
    return result

array_of_commits = break_file_into_commits(file)

def get_name_of_committer(commit_body):
    # returns string of committer name
    indexOfName = commit_body.find('"name"')
    if indexOfName >  1:
        startOfDevName = commit_body.find('"',indexOfName + 6)
        endOfDevName = commit_body.find('"',startOfDevName + 1)
        return commit_body[startOfDevName + 1:endOfDevName]    

def dict_of_commits_by_committer(commit_messages):
    # returns dict, with K:V -> committer: [...commits]
    result = {}
    for commit_message in commit_messages:
        committer = get_name_of_committer(commit_message)
        if committer  in  result.keys():
            result[committer].append(commit_message)
        else:
             result[committer] = [commit_message]
    return result

commits_by_committer =  dict_of_commits_by_committer(array_of_commits) # committerName : [committs...]


def get_month_of_commit(commit_body):
    # returns string of month in which commit was made
    indexOfName = commit_body.find('"date"')
    if indexOfName >  1:
        startOfDate = commit_body.find('"',indexOfName + 6)
        return commit_body[startOfDate + 8 : startOfDate+12].strip()


def split_commits_into_months(array_of_commits):
    # takes an array of commits, returns an array of 12 arrays, with each 
    # array containing commits from corrosponding month (0-jan, 1-march, ... 11 -> dec)
    result = [[] for _ in range(12)]
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for commit in array_of_commits:
        index = months.index(get_month_of_commit(commit))
        result[index].append(commit)
    return result


def print_total_committs_by_committer_by_month(commits_by_committer):
    for committer in commits_by_committer:
        arr_of_all_committer_commits = commits_by_committer[committer]
        arr_of_monthwise_array_of_commits = split_commits_into_months(arr_of_all_committer_commits)
        print committer + " , " , [len(x) for x in  arr_of_monthwise_array_of_commits]


def print_filtered_committs_by_committer_by_month(commits_by_committer):
    # counts number of commits per engineer per month based on keywords in the commit
    for committer in commits_by_committer:
        arr_of_all_committer_commits = commits_by_committer[committer] # 
        arr_of_monthwise_array_of_commits = split_commits_into_months(arr_of_all_committer_commits)
        result = [ 0 for _ in range(12)]

        i = 0
        while i < 12: 
            monthly_commits = arr_of_monthwise_array_of_commits[i]
            for commit in monthly_commits:
                # specify keyword(s) on the line below
                if commit.find('rule') > 1 or commit.find('predicate') > 1 or commit.find('action') > 1 or commit.find('mlang') > 1:
                    result[i] += 1
            i += 1

        print committer + " , " , result

# print_committs_by_committer_by_month(commits_by_committer)
print_filtered_committs_by_committer_by_month(commits_by_committer)
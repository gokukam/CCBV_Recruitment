# Dictionaries to store count
api_requests = {}
endpoints = {}
batches = {}
algos = {"Heuristic Backtracking": 0, "Iterative Random Sampling": 0}

# A set to store unique user IDs
users = set()

# TT Gen related variables
tts = 0
ttgencalls = 0


# Incrementing count in a given dict for given key
def inc_ctr(key, d):
    if key in d:
        d[key] += 1
    else:
        d[key] = 1


# Reading in the logfile
with open("timetable.log", "r") as f:
    lines = f.read().split("\n")

# Parsing the data line by line
for line in lines:
    words = line.split()

    # Getting status code and endpoint info from request lines
    if len(words) == 7 and words[3] in ("POST", "GET"):
        endp = words[4]
        status = words[5]
        resptime = float(words[-1][:-2])

        # Adding status codes and incrementing count
        inc_ctr(status, api_requests)

        # Adding endpoints with count and response time info
        # Each key has value as [No. of accesses, MaxTime, TotalTime]
        if endp in endpoints:
            endpoints[endp][0] += 1
            endpoints[endp][-1] += resptime
            if resptime > endpoints[endp][1]:
                endpoints[endp][1] = resptime
        else:
            endpoints[endp] = [1, resptime, resptime]

    # Getting all unique user IDs (check last word's format)
    if len(words) == 6 and words[-1][:4] == "[202":
        userid = words[-1][1:-1]
        users.add(userid)

    # Getting algo usage count
    if len(words) in (12, 13):
        if words[5] == "Heuristic":
            algos["Heuristic Backtracking"] += 1
        if words[5] == "Iterative":
            algos["Iterative Random Sampling"] += 1

    # Getting TT Gen data
    if len(words) == 14 and words[4] == "Generation":
        ttgencalls += 1
        tts += int(words[7])

# Populating batches dict with user count
for userid in users:  # Traversing the set 'users'
    year = userid[:4]
    inc_ctr(year, batches)

# Creating a sep for reuse
sep = "-" * 30

# Displaying the report
print(f"Traffic & Usage Analysis\n{sep}")
print(f"Total API Requests Logged: {sum(api_requests.values())}")
print("\nEndpoint Popularity:")
for end in endpoints:
    vals = endpoints[end]
    perc = (vals[0] / sum(api_requests.values())) * 100
    print(f"- {end}: {vals[0]} requests ({perc}%)")

print("\nHTTP Status Codes:")
for code in api_requests:
    print(f"- {code}: {api_requests[code]} times")
print(sep)

print(f"Performance Metrics\n{sep}")
for end in endpoints:
    vals = endpoints[end]
    print(f"Endpoint: {end}")
    print(f"- Average Response Time: {vals[-1] / vals[0]} ms")
    print(f"- Max Response Time: {vals[1]} ms")
print(sep)

print(f"Application-Specific Insights\n{sep}")
print("Timetable Generation Strategy Usage:")
for algo in algos:
    print(f"- {algo}: {algos[algo]} times")

print(f"\nAverage Timetables Found per /generate call: {tts / ttgencalls}")
print(f"Total number of timetables generated: {tts}")
print(f"{sep}\nUnique ID Analysis\n{sep}")
print(f"Total Unique IDs found: {len(users)}")
for batch in batches:
    print(f"Batch of {batch}: {batches[batch]} unique IDs")

# End of Code

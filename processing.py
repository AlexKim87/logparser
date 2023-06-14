import re
import json


def processing(*files):
    counter = 0
    for file in files:
        total_stat = {"GET": 0, "POST": 0, "HEAD": 0, "PUT": 0, "OPTIONS": 0, "DELETE": 0, "UPDATE": 0, "PATCH": 0}
        total_requests = 0
        top_longest = []
        top_ips = {}
        filename = f'RESULT{counter}.json'

        with open(file) as f:
            for line in f:

                temp_dict = {"ip": 0, "date": 0, "method": 0, "url": 0, "duration": 0}

                ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
                ip = ip_match.group()
                method_match = re.search(r"\] \"(GET|POST|HEAD|PUT|OPTIONS|DELETE|UPDATE|PATCH)", line)
                method = method_match.group(1)
                date_match = re.search(r"\[\d{2}/[A-z]{3}/(\d{4}:\d\d:\d\d:\d\d) \+\d{4}]", line)
                date = date_match.group()
                url_match = re.search(r"(GET|POST|HEAD|PUT|OPTIONS|DELETE|UPDATE|PATCH) (\S+) +(HTTP)", line)
                url = url_match.group(2)
                duration_match = re.search(r"(\") +(\d+)$", line)
                duration = duration_match.group(2)

                if ip in top_ips:
                    top_ips[ip] += 1
                else:
                    top_ips[ip] = 1
                total_stat[method] += 1
                total_requests += 1

                temp_dict["ip"] = ip
                temp_dict["date"] = date
                temp_dict["method"] = method
                temp_dict["url"] = url
                temp_dict["duration"] = duration

                if len(top_longest) < 3:
                    top_longest.append(temp_dict)
                if len(top_longest) == 3:
                    for i in top_longest:
                        if int(duration) > int(i["duration"]):
                            top_longest[top_longest.index(i)] = temp_dict
                            break
                        else:
                            pass

            top_ips = dict(sorted(top_ips.items(), key=lambda item: item[1], reverse=True)[0:3])

        result = {"top_ips": top_ips, "top_longest": top_longest, "total_stat": total_stat, "total_requests": total_requests}
        print(f"RESULT_{counter}__________________________________________________________________________________________________________")
        print(json.dumps(result, indent=4))

        with open(filename, 'w') as file_object:
            json.dump(result, file_object)
        counter += 1




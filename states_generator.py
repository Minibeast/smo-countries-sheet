import urllib
import urllib.request
import urllib.error
import json
import datetime


def generate():
    leaderboard = json.loads(urllib.request.urlopen("https://www.speedrun.com/api/v1/leaderboards/76r55vd8/category/w20w1lzd?var-68km3w4l=zqoyz021&embed=players").read())

    country_data = []

    for x in leaderboard["data"]["runs"]:
        new_country = True
        if x["run"]["players"][0]["rel"] == "guest":
            continue

        for i in leaderboard["data"]["players"]["data"]:
            try:
                error = i["location"]
            except KeyError:
                continue

            if i["location"] is None or len(i["location"]) > 2:
                continue

            if i["rel"] != "guest" and x["run"]["players"][0]["id"] == i["id"]:
                try:
                    for c in country_data:
                        if i["location"]["region"]["code"][0:5] == c["code"] and i["location"]["country"]["code"] == "us":
                            c["players"].append({"name": i["names"]["international"],
                                                 "time": str(datetime.timedelta(seconds=int(x["run"]["times"]["primary_t"])))})
                            new_country = False
                    if new_country and i["location"]["country"]["code"] == "us":
                        country_data.append({"code": i["location"]["region"]["code"][0:5],
                                             "name": i["location"]["region"]["names"]["international"],
                                             "players": [{"name": i["names"]["international"],
                                                          "time": str(
                                                              datetime.timedelta(seconds=int(x["run"]["times"]["primary_t"])))}
                                                         ]})
                except KeyError:
                    continue

    result = ""

    for x in country_data:
        result += str(x["name"]) + "\t"
    result += "\n"

    longest_runs = 0
    for x in country_data:
        if len(x["players"]) > longest_runs:
            longest_runs = len(x["players"])
    i = 0
    while i <= longest_runs:
        for x in country_data:
            try:
                result += str(x["players"][i]["name"] + " : " + x["players"][i]["time"]) + "\t"
            except LookupError:
                result += "\t"
                continue
        result += "\n"
        i += 1

    with open("states.tsv", "w+") as output:
        result = result.replace("\u200b", "")
        output.write(result)
        output.close()


if __name__ == "__main__":
    generate()

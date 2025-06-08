import json

if __name__ == "__main__":
    with open("GameParams-0.json", "r") as params:
        raw_data = params.read()
    json_data = json.loads(raw_data)
    for key in json_data:
        current = json_data[key]
        if "typeinfo" in current:
            # Ohio
            if current["id"] == 3760142320:
                # find A_Hull
                hull = current["A_Hull"]
                # sum up volume of the hull
                volume = 0
                for part in hull:
                    hull_part = hull[part]
                    # make sure it's a dict
                    if isinstance(hull_part, dict) and "volume" in hull_part:
                        volume += hull_part["volume"]
                print(f"Volume of {current['id']} is {volume}")

                # dump current out
                # with open(f"{current['id']}.json", "w") as dump:
                #     dump.write(json.dumps(current, indent=4))
                #     exit(0)

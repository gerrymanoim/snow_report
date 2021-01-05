import json

import requests
from jinja2 import Template

BASE_URL = "http://feeds.snocountry.net/getSnowReport.php?apiKey=SnoCountry.example&ids="

MOUNTAIN_IDS = [
    802019,  # stratton
    802007,  # killington
    802023,  # sugarbush
    304001,  # snowshoe
    207009,  # sunday river
    207008,  # sugar loaf
    603014,  # loon
    518009,  # windham
]

SITE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Snow Status</title>
</head>
<body>
    <div id="content">
        <table>
            <tr>
                <th>Resort</th>
                <th>Snow</th>
                <th>Open Percent</th>
                <th>Lifts</th>
                <th>Trails</th>
                <th>Acres</th>
                <th>Snow (24h)</th>
                <th>Snow (48h)</th>
                <th>Base Depth</th>
                <th>Surface Conditions</th>
                <th>Covid</th>
        {% for m in mountains %}
            <tr>
                <td>{{m.resortName}}, {{m.state}}</td>
                <td>{{m.snowComments}}</td>
                <td>{{m.openDownHillPercent}}%</td>
                <td>{{m.openDownHillLifts}} of {{m.maxOpenDownHillLifts}}</td>
                <td>{{m.openDownHillTrails}} of {{m.maxOpenDownHillTrails}}</td>
                <td>{{m.openDownHillAcres}} of {{m.maxOpenDownHillAcres}}</td>
                <td>{{m.newSnowMin or 0}}-{{m.newSnowMax or 0}}</td>
                <td>{{m.snowLast48Hours or 0}}</td>
                <td>{{m.avgBaseDepthMin}}-{{m.avgBaseDepthMax}}</td>
                <td>{{m.primarySurfaceCondition}}</td>
                <td><a href="{{m.resortCovidPage}}">click</a></td>
            </tr>
        {% endfor %}
        </table>
    </div>
</body>
</html>

"""


output = list()
for mid in MOUNTAIN_IDS:
    r = requests.get(BASE_URL + str(mid))
    if r.ok:
        output.append(r.json()["items"][0])
    else:
        print(f"Error getting {mid=}")

with open("data.json", "w") as f:
    json.dump(output, f, indent=4)

with open("index.html", "w") as f:
    f.write(Template(SITE_TEMPLATE).render(mountains=output))

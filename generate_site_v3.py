import os

os.makedirs("site", exist_ok=True)

# homepage
index = """
<!DOCTYPE html>
<html>
<head>
<title>Can I Throw This Away?</title>
</head>
<body>

<h1>Can I Throw This Away?</h1>

<ul>
<li><a href="states.html">States</a></li>
<li><a href="items.html">Items</a></li>
</ul>

</body>
</html>
"""

with open("site/index.html","w") as f:
    f.write(index)

# states page
states = [
"alabama","alaska","arizona","arkansas","california","colorado","connecticut",
"delaware","florida","georgia","hawaii","idaho","illinois","indiana","iowa",
"kansas","kentucky","louisiana","maine","maryland","massachusetts","michigan",
"minnesota","mississippi","missouri","montana","nebraska","nevada",
"new-hampshire","new-jersey","new-mexico","new-york","north-carolina",
"north-dakota","ohio","oklahoma","oregon","pennsylvania","rhode-island",
"south-carolina","south-dakota","tennessee","texas","utah","vermont",
"virginia","washington","west-virginia","wisconsin","wyoming"
]

states_html = "<h1>States</h1>"

for s in states:
    states_html += f"<p><a href='{s}.html'>{s.title()}</a></p>"

with open("site/states.html","w") as f:
    f.write(states_html)

# individual state pages
for s in states:
    page = f"""
<h1>{s.title()}</h1>
<p>Recycling and disposal rules for {s.title()}.</p>
<a href='index.html'>Home</a>
"""
    with open(f"site/{s}.html","w") as f:
        f.write(page)

import requests, csv, json, os
from datetime import datetime, timedelta
from google.transit import gtfs_realtime_pb2

# -------------------------------------------------
# CONFIG
# -------------------------------------------------

AC_API_KEY = os.environ.get("AC_TRANSIT_API_KEY")
TRMNL_WEBHOOK_URL = os.environ.get("TRMNL_WEBHOOK_URL")
BART_GTFS_RT = "https://api.bart.gov/gtfsrt/tripupdate.aspx"

# walking + offsets
WALK_51A = 7
BUS_51A = 13

WALK_NL = 18
BUS_NL = 6

WALK_19TH = 20
POWELL_TO_METREON = 15
SIXTEENTH_TO_ALAMO = 15

# stop prefixes
NINETEENTH = "K20"
POWELL = "M30"
SIXTEENTH = "M50"

# route compression
ROUTE_CODES = {
    "Yellow-S – Antioch to SF Int'l Airport SFO/Millbrae": "Y",
    "Red-S – Richmond to SF Int'l Airport SFO/Millbrae": "R",
}

ROUTE_NAMES = {
    "Y": "Yellow Antioch → SFO",
    "R": "Red Richmond → SFO"
}

# -------------------------------------------------
# UTILS
# -------------------------------------------------

def hhmm(dt): return dt.strftime("%H:%M")
def mins(td): return int(td.total_seconds() // 60)

# -------------------------------------------------
# AC TRANSIT (BUS)
# -------------------------------------------------

def get_bus_json(stop_id, walk_min, ride_min, route_filter):
    url = f"https://api.actransit.org/transit/actrealtime/prediction?stpid={stop_id}&token={AC_API_KEY}"
    r = requests.get(url, timeout=10)

    out = []
    now = datetime.now()

    prds = r.json().get("bustime-response", {}).get("prd", [])

    for p in prds:
        if not route_filter(p["rt"]):
            continue

        board = datetime.strptime(p["prdtm"], "%Y%m%d %H:%M")
        leave = board - timedelta(minutes=walk_min)

        if leave < now:
            continue

        arrive = board + timedelta(minutes=ride_min)

        out.append({
            "lh": hhmm(leave),
            "b": hhmm(board),
            "a": hhmm(arrive),
            "t": mins(arrive - leave),
            "r": p["rt"]
        })

    return out[:5]
SHUTTLE_SCHEDULE = [

# ---------------- WEEKDAY ----------------
{"day":"Weekday","depart":"6:00 AM","arrive":"6:08 AM"},
{"day":"Weekday","depart":"6:15 AM","arrive":"6:23 AM"},
{"day":"Weekday","depart":"6:30 AM","arrive":"6:38 AM"},
{"day":"Weekday","depart":"6:45 AM","arrive":"6:53 AM"},
{"day":"Weekday","depart":"7:00 AM","arrive":"7:08 AM"},
{"day":"Weekday","depart":"7:15 AM","arrive":"7:23 AM"},
{"day":"Weekday","depart":"7:30 AM","arrive":"7:38 AM"},
{"day":"Weekday","depart":"7:45 AM","arrive":"7:55 AM"},
{"day":"Weekday","depart":"8:00 AM","arrive":"8:10 AM"},
{"day":"Weekday","depart":"8:15 AM","arrive":"8:25 AM"},
{"day":"Weekday","depart":"8:30 AM","arrive":"8:40 AM"},
{"day":"Weekday","depart":"8:45 AM","arrive":"8:55 AM"},
{"day":"Weekday","depart":"9:00 AM","arrive":"9:10 AM"},
{"day":"Weekday","depart":"9:15 AM","arrive":"9:25 AM"},
{"day":"Weekday","depart":"9:30 AM","arrive":"9:40 AM"},
{"day":"Weekday","depart":"9:45 AM","arrive":"9:55 AM"},
{"day":"Weekday","depart":"10:00 AM","arrive":"10:10 AM"},
{"day":"Weekday","depart":"10:15 AM","arrive":"10:25 AM"},
{"day":"Weekday","depart":"10:30 AM","arrive":"10:40 AM"},
{"day":"Weekday","depart":"10:45 AM","arrive":"10:55 AM"},
{"day":"Weekday","depart":"11:00 AM","arrive":"11:10 AM"},
{"day":"Weekday","depart":"11:15 AM","arrive":"11:25 AM"},
{"day":"Weekday","depart":"11:30 AM","arrive":"11:40 AM"},
{"day":"Weekday","depart":"11:45 AM","arrive":"11:55 AM"},
{"day":"Weekday","depart":"12:00 PM","arrive":"12:10 PM"},
{"day":"Weekday","depart":"12:15 PM","arrive":"12:25 PM"},
{"day":"Weekday","depart":"12:30 PM","arrive":"12:40 PM"},
{"day":"Weekday","depart":"12:45 PM","arrive":"12:55 PM"},
{"day":"Weekday","depart":"1:00 PM","arrive":"1:10 PM"},
{"day":"Weekday","depart":"1:15 PM","arrive":"1:25 PM"},
{"day":"Weekday","depart":"1:30 PM","arrive":"1:40 PM"},
{"day":"Weekday","depart":"1:45 PM","arrive":"1:55 PM"},
{"day":"Weekday","depart":"2:00 PM","arrive":"2:10 PM"},
{"day":"Weekday","depart":"2:15 PM","arrive":"2:25 PM"},
{"day":"Weekday","depart":"2:30 PM","arrive":"2:40 PM"},
{"day":"Weekday","depart":"2:45 PM","arrive":"2:55 PM"},
{"day":"Weekday","depart":"3:00 PM","arrive":"3:10 PM"},
{"day":"Weekday","depart":"3:15 PM","arrive":"3:25 PM"},
{"day":"Weekday","depart":"3:30 PM","arrive":"3:40 PM"},
{"day":"Weekday","depart":"3:45 PM","arrive":"3:55 PM"},
{"day":"Weekday","depart":"4:00 PM","arrive":"4:10 PM"},
{"day":"Weekday","depart":"4:15 PM","arrive":"4:25 PM"},
{"day":"Weekday","depart":"4:30 PM","arrive":"4:40 PM"},
{"day":"Weekday","depart":"4:45 PM","arrive":"4:55 PM"},
{"day":"Weekday","depart":"5:00 PM","arrive":"5:10 PM"},
{"day":"Weekday","depart":"5:15 PM","arrive":"5:25 PM"},
{"day":"Weekday","depart":"5:30 PM","arrive":"5:40 PM"},
{"day":"Weekday","depart":"5:45 PM","arrive":"5:55 PM"},
{"day":"Weekday","depart":"6:00 PM","arrive":"6:10 PM"},
{"day":"Weekday","depart":"6:15 PM","arrive":"6:25 PM"},
{"day":"Weekday","depart":"6:30 PM","arrive":"6:40 PM"},
{"day":"Weekday","depart":"6:45 PM","arrive":"6:55 PM"},
{"day":"Weekday","depart":"7:00 PM","arrive":"7:10 PM"},
{"day":"Weekday","depart":"7:15 PM","arrive":"7:25 PM"},
{"day":"Weekday","depart":"7:30 PM","arrive":"7:38 PM"},
{"day":"Weekday","depart":"7:45 PM","arrive":"7:53 PM"},
{"day":"Weekday","depart":"8:00 PM","arrive":"8:08 PM"},
{"day":"Weekday","depart":"8:15 PM","arrive":"8:23 PM"},
{"day":"Weekday","depart":"8:30 PM","arrive":"8:38 PM"},
{"day":"Weekday","depart":"8:45 PM","arrive":"8:53 PM"},
{"day":"Weekday","depart":"9:00 PM","arrive":"9:08 PM"},
{"day":"Weekday","depart":"9:15 PM","arrive":"9:23 PM"},
{"day":"Weekday","depart":"9:30 PM","arrive":"9:38 PM"},
{"day":"Weekday","depart":"9:45 PM","arrive":"9:53 PM"},
{"day":"Weekday","depart":"10:00 PM","arrive":"10:08 PM"},

# ---------------- SATURDAY ----------------
{"day":"Saturday","depart":"8:20 AM","arrive":"8:29 AM"},
{"day":"Saturday","depart":"8:40 AM","arrive":"8:49 AM"},
{"day":"Saturday","depart":"9:00 AM","arrive":"9:09 AM"},
{"day":"Saturday","depart":"9:20 AM","arrive":"9:29 AM"},
{"day":"Saturday","depart":"9:40 AM","arrive":"9:49 AM"},
{"day":"Saturday","depart":"10:00 AM","arrive":"10:09 AM"},
{"day":"Saturday","depart":"10:20 AM","arrive":"10:29 AM"},
{"day":"Saturday","depart":"10:40 AM","arrive":"10:49 AM"},
{"day":"Saturday","depart":"11:00 AM","arrive":"11:11 AM"},
{"day":"Saturday","depart":"11:20 AM","arrive":"11:31 AM"},
{"day":"Saturday","depart":"11:40 AM","arrive":"11:51 AM"},
{"day":"Saturday","depart":"12:00 PM","arrive":"12:11 PM"},
{"day":"Saturday","depart":"12:20 PM","arrive":"12:31 PM"},
{"day":"Saturday","depart":"12:40 PM","arrive":"12:51 PM"},
{"day":"Saturday","depart":"1:00 PM","arrive":"1:11 PM"},
{"day":"Saturday","depart":"1:20 PM","arrive":"1:31 PM"},
{"day":"Saturday","depart":"1:40 PM","arrive":"1:51 PM"},
{"day":"Saturday","depart":"2:00 PM","arrive":"2:11 PM"},
{"day":"Saturday","depart":"2:20 PM","arrive":"2:31 PM"},
{"day":"Saturday","depart":"2:30 PM","arrive":"2:41 PM"},
{"day":"Saturday","depart":"2:40 PM","arrive":"2:51 PM"},
{"day":"Saturday","depart":"3:00 PM","arrive":"3:11 PM"},
{"day":"Saturday","depart":"3:20 PM","arrive":"3:31 PM"},
{"day":"Saturday","depart":"3:30 PM","arrive":"3:41 PM"},
{"day":"Saturday","depart":"3:40 PM","arrive":"3:51 PM"},
{"day":"Saturday","depart":"4:00 PM","arrive":"4:11 PM"},
{"day":"Saturday","depart":"4:20 PM","arrive":"4:31 PM"},
{"day":"Saturday","depart":"4:40 PM","arrive":"4:51 PM"},
{"day":"Saturday","depart":"5:00 PM","arrive":"5:11 PM"},
{"day":"Saturday","depart":"5:20 PM","arrive":"5:31 PM"},
{"day":"Saturday","depart":"5:40 PM","arrive":"5:51 PM"},
{"day":"Saturday","depart":"6:00 PM","arrive":"6:11 PM"},
{"day":"Saturday","depart":"6:20 PM","arrive":"6:31 PM"},
{"day":"Saturday","depart":"6:40 PM","arrive":"6:51 PM"},
{"day":"Saturday","depart":"7:00 PM","arrive":"7:09 PM"},
{"day":"Saturday","depart":"7:20 PM","arrive":"7:29 PM"},
{"day":"Saturday","depart":"7:40 PM","arrive":"7:49 PM"},
{"day":"Saturday","depart":"8:00 PM","arrive":"8:09 PM"},
{"day":"Saturday","depart":"8:20 PM","arrive":"8:29 PM"},
{"day":"Saturday","depart":"8:40 PM","arrive":"8:49 PM"},
{"day":"Saturday","depart":"9:00 PM","arrive":"9:09 PM"},
{"day":"Saturday","depart":"9:20 PM","arrive":"9:29 PM"},
{"day":"Saturday","depart":"9:40 PM","arrive":"9:49 PM"},
{"day":"Saturday","depart":"10:00 PM","arrive":"10:09 PM"},

# ---------------- SUNDAY ----------------
{"day":"Sunday","depart":"9:00 AM","arrive":"9:05 AM"},
{"day":"Sunday","depart":"9:20 AM","arrive":"9:25 AM"},
{"day":"Sunday","depart":"9:40 AM","arrive":"9:45 AM"},
{"day":"Sunday","depart":"10:00 AM","arrive":"10:05 AM"},
{"day":"Sunday","depart":"10:20 AM","arrive":"10:25 AM"},
{"day":"Sunday","depart":"10:40 AM","arrive":"10:45 AM"},
{"day":"Sunday","depart":"11:00 AM","arrive":"11:06 AM"},
{"day":"Sunday","depart":"11:20 AM","arrive":"11:26 AM"},
{"day":"Sunday","depart":"11:40 AM","arrive":"11:46 AM"},
{"day":"Sunday","depart":"12:00 PM","arrive":"12:06 PM"},
{"day":"Sunday","depart":"12:10 PM","arrive":"12:16 PM"},
{"day":"Sunday","depart":"12:20 PM","arrive":"12:26 PM"},
{"day":"Sunday","depart":"12:40 PM","arrive":"12:46 PM"},
{"day":"Sunday","depart":"1:00 PM","arrive":"1:06 PM"},
{"day":"Sunday","depart":"1:20 PM","arrive":"1:26 PM"},
{"day":"Sunday","depart":"1:40 PM","arrive":"1:46 PM"},
{"day":"Sunday","depart":"2:00 PM","arrive":"2:06 PM"},
{"day":"Sunday","depart":"2:20 PM","arrive":"2:26 PM"},
{"day":"Sunday","depart":"2:40 PM","arrive":"2:46 PM"},
{"day":"Sunday","depart":"3:00 PM","arrive":"3:06 PM"},
{"day":"Sunday","depart":"3:20 PM","arrive":"3:26 PM"},
{"day":"Sunday","depart":"3:40 PM","arrive":"3:46 PM"},
{"day":"Sunday","depart":"4:00 PM","arrive":"4:06 PM"},
{"day":"Sunday","depart":"4:20 PM","arrive":"4:26 PM"},
{"day":"Sunday","depart":"4:40 PM","arrive":"4:46 PM"},
{"day":"Sunday","depart":"5:00 PM","arrive":"5:06 PM"},
{"day":"Sunday","depart":"5:20 PM","arrive":"5:26 PM"},
{"day":"Sunday","depart":"5:40 PM","arrive":"5:46 PM"},
{"day":"Sunday","depart":"6:00 PM","arrive":"6:06 PM"},
{"day":"Sunday","depart":"6:20 PM","arrive":"6:26 PM"},
{"day":"Sunday","depart":"6:40 PM","arrive":"6:46 PM"},
]

def next_shuttle():
    now = datetime.now()
    day = "Weekday" if now.weekday() < 5 else "Saturday" if now.weekday()==5 else "Sunday"
    out = []

    for s in SHUTTLE_SCHEDULE:
        if s["day"] != day:
            continue

        d = datetime.strptime(f"{now.date()} {s['depart']}", "%Y-%m-%d %I:%M %p")
        a = datetime.strptime(f"{now.date()} {s['arrive']}", "%Y-%m-%d %I:%M %p")

        leave = d - timedelta(minutes=30)
        arrive = a + timedelta(minutes=5)

        if leave > now:
            out.append({
                "lh": hhmm(leave),
                "b": hhmm(d),
                "a": hhmm(arrive),
                "t": mins(arrive - leave)
            })

    return out[:3]

# -------------------------------------------------
# BART
# -------------------------------------------------

def load_csv(path, key):
    d = {}
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            d[r[key]] = r
    return d

def get_bart():
    trips = load_csv("trips.txt", "trip_id")
    routes = load_csv("routes.txt", "route_id")

    r = requests.get(BART_GTFS_RT, timeout=15)
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(r.content)

    now = datetime.now()
    arrival_19 = now + timedelta(minutes=WALK_19TH)

    metreon, alamo = [], []

    for e in feed.entity:
        if not e.HasField("trip_update"):
            continue

        tu = e.trip_update
        trip = trips.get(tu.trip.trip_id, {})
        route = routes.get(trip.get("route_id"), {})

        stops = [{
            "id": s.stop_id,
            "t": datetime.fromtimestamp(s.arrival.time)
        } for s in tu.stop_time_update if s.HasField("arrival")]

        i19 = next((i for i,s in enumerate(stops) if s["id"].startswith(NINETEENTH)), None)
        if i19 is None:
            continue

        board = stops[i19]["t"]
        if board < arrival_19:
            continue

        leave = board - timedelta(minutes=WALK_19TH)
        line = f"{route.get('route_short_name')} – {route.get('route_long_name')}"

        ip = next((i for i,s in enumerate(stops) if s["id"].startswith(POWELL)), None)
        i16 = next((i for i,s in enumerate(stops) if s["id"].startswith(SIXTEENTH)), None)

        if ip and ip > i19:
            metreon.append((leave, board, stops[ip]["t"] + timedelta(minutes=POWELL_TO_METREON), line))

        if i16 and i16 > i19:
            alamo.append((leave, board, stops[i16]["t"] + timedelta(minutes=SIXTEENTH_TO_ALAMO), line))

    return metreon[:5], alamo[:5]

def pack_bart(rows):
    out = []
    for l,b,a,line in rows:
        code = ROUTE_CODES.get(line, line[:1])
        out.append({
            "lh": hhmm(l),
            "b": hhmm(b),
            "a": hhmm(a),
            "t": mins(a-l),
            "r": code
        })
    return out

# -------------------------------------------------
# BUILD PAYLOAD
# -------------------------------------------------

now = datetime.now()

payload = {
    "d": now.strftime("%Y-%m-%d"),
    "g": now.strftime("%H:%M"),

    "routes": ROUTE_NAMES,

    "cape": {
        "m": {"d":"Cape & Cowl","on":"28th/Broadway","off":"17th/Broadway"},
        "r": get_bus_json("57771", WALK_51A, BUS_51A, lambda r: r=="51A")
    },

    "grand": {
        "m": {"d":"Grand Lake Theater","on":"Grand/Harrison","off":"Grand Lake Theater"},
        "r": get_bus_json("51099", WALK_NL, BUS_NL, lambda r: r.startswith("NL"))
    },

    "shuttle": {
        "m": {"d":"AMC Bay Street","on":"Shellmound Pickup","off":"AMC Bay Street"},
        "r": next_shuttle()
    }
}

m,a = get_bart()
payload["bart_m"] = {
    "m": {"d":"AMC Metreon","on":"19th Street","off":"Powell Street"},
    "r": pack_bart(m)
}
payload["bart_a"] = {
    "m": {"d":"Alamo Drafthouse","on":"19th Street","off":"16th/Mission"},
    "r": pack_bart(a)
}

# -------------------------------------------------
# EMIT — POST TO WEBHOOK
# -------------------------------------------------

json_payload = json.dumps(payload, separators=(",", ":"))

response = requests.post(
    TRMNL_WEBHOOK_URL,
    data=json_payload,
    headers={"Content-Type": "application/json"},
    timeout=30
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

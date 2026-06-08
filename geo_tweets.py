import os

from projects.common import Project

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
BY_EMOJI_DIR = os.path.join(STATIC_DIR, "by_emoji")
BY_EMOJI_URL = "/static/projects/geo_tweets/by_emoji"
UNBALANCED_PATH = os.path.join(STATIC_DIR, "unbalanced.txt")
UNBALANCED = {
    l.split(":")[0] for l in open(UNBALANCED_PATH, encoding="utf8").readlines()
}


class GeoTweets(Project):
    def fill_dict(self, request, d):
        emojis = [k for k in request.GET if request.GET.get(k)]
        if not emojis:
            emojis = ["zzz", "beer_mug", "hot_beverage"]
        paths = [os.path.join(BY_EMOJI_URL, e) + ".json" for e in emojis]
        paths = [p for p in paths if os.path.isfile(os.path.join(BY_EMOJI_DIR, os.path.basename(p)))]
        d["emojis"] = paths

        seen = 0
        unbalanced = 0
        too_long = 0
        cells = []
        for em in sorted(os.listdir(BY_EMOJI_DIR), key=lambda x: x.lower()):
            if em.endswith(".png"):
                seen += 1
                em_id = em.rsplit(".", 1)[0]
                if not em_id in UNBALANCED:
                    unbalanced += 1
                    continue
                txt = em_id.replace("_", " ")
                cell = {
                    "txt": txt,
                    "selected": em_id in emojis,
                    "img": os.path.join(BY_EMOJI_URL, em),
                    "id": em_id,
                }

                if len(txt) < 15 and not txt == "clinking beer mugs":
                    cells.append(cell)
                else:
                    too_long += 1
        print(seen, unbalanced, too_long)
        d["cells"] = cells

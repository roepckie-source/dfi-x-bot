import json
import os


LANG_PATH = "languages"


base_file = os.path.join(
    LANG_PATH,
    "en.json"
)


with open(
    base_file,
    "r",
    encoding="utf-8"
) as f:

    base = json.load(f)



base_keys = set(base.keys())



for file in os.listdir(LANG_PATH):

    if file.endswith(".json"):

        path = os.path.join(
            LANG_PATH,
            file
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            lang = json.load(f)



        missing = base_keys - set(lang.keys())


        if missing:

            print(
                f"⚠️ {file} fehlt:"
            )

            for key in missing:
                print(
                    "   ",
                    key
                )


        else:

            print(
                f"✅ {file} vollständig"
            )

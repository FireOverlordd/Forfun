from dotenv import load_dotenv
load_dotenv()

import os
from forfun_app.factory import create_app

env = os.environ.get("FLASK_ENV", "dev")

app = create_app("uno_app.config.%sConfig" % env.capitalize())

if __name__ == "__main__":
    app.run()
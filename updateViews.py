import os
import sys
import logging

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from time import sleep

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

logging.basicConfig(
    filename="Logs.log", format="%(asctime)s %(message)s", filemode="w"
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "auth/secret.json"  # insert
    if len(sys.argv) < 2:
        print("Provide Path to secret.json")
        exit()
    client_secrets_file = sys.argv[1]

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes
    )
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )

    vid = "U3ZsUfjdwDQ"
    count = 0

    while True:
        try:
            request = youtube.videos().list(part="snippet,statistics", id=vid)
            response = request.execute()

            # print(response)

            video = response["items"][0]
            title = video["snippet"]["title"]
            views = str(video["statistics"]["viewCount"])
            likes = str(video["statistics"]["likeCount"])
            logger.info(msg=f"Title: {title}")
            logger.info(msg=f"Views: {views}")
            logger.info(msg=f"Likes: {likes}")

            changed = (views not in title) or (likes not in title)

            if changed:
                new_title = (
                    "Avatar: Korra | Do It Like A Dude | Views: "
                    + views
                    + ", Likes: "
                    + likes
                )
                video["snippet"]["title"] = new_title

                request = youtube.videos().update(
                    part="snippet", body={"id": vid, "snippet": video["snippet"]}
                )
                response = request.execute()

                logger.info(msg="Title Changed successfully")

        except Exception as e:
            logger.error(msg="Unable to Change Title")
            logger.error(e)
            if count > 5:
                break

        count += 1
        logger.info(msg=f"Count: {count}\n\n")
        sleep(600)


if __name__ == "__main__":
    main()

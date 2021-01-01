import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from time import sleep

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "auth/secret.json"  # insert

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    vid = "U3ZsUfjdwDQ"
    count = 0

    while (True):
        try:
            request = youtube.videos().list(
                part="snippet,statistics",
                id=vid
            )
            response = request.execute()

            # print(response)

            video = response["items"][0]
            title = video["snippet"]["title"]
            views = str(video["statistics"]["viewCount"])
            likes = str(video["statistics"]["likeCount"])
            print("Title: ", title)
            print("views:", views)
            print("likes:", likes)

            changed = (views not in title) or (likes not in title)

            if(changed):
                new_title = "Avatar: Korra | Do It Like A Dude | Views: " + \
                    views + ", Likes: " + likes
                video["snippet"]["title"] = new_title

                request = youtube.videos().update(
                    part="snippet",
                    body={
                        "id": vid,
                        "snippet": video["snippet"]
                    }
                )
                response = request.execute()

                print("Changed")

        except:
            print("Error, try again")
            if count > 5:
                break

        count += 1
        print("\ncount: " + str(count) + "\n")
        sleep(600)


if __name__ == "__main__":
    main()

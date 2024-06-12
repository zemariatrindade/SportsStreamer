import os
import dotenv
import socket
import json
import praw
import time


env_file = 'creds.sh'
dotenv.load_dotenv(env_file, override=True)

CLIENT_ID = os.environ['CLIENT_ID']
SECRET_TOKEN = os.environ['SECRET_TOKEN']
USER_AGENT = 'MyBot/0.0.1'

host = "127.0.0.1"
port = 9998


def send_data_to_socket(data, conn):
    json_encoded = json.dumps(data)
    conn.sendall(
        json_encoded.encode("utf-8") + b"\n"
    )

def stream_json(subreddit):
    c, addr = s.accept()
    print(f"Connection from: {addr}")

    for comment in subreddit.stream.comments():
        try:
            post = comment.submission
            parent_id = str(comment.parent())
            prev_comment = reddit.comment(parent_id)

            prev_body = prev_comment.body
            comment_body = comment.body

            my_object = {
                "comment": comment_body,
                "prev_comment": prev_body,
                "post": post.selftext,
                "author": str(comment.author),
                "created_utc": comment.created_utc,
            }
            send_data_to_socket(my_object, c)
            time.sleep(1)

        except praw.exceptions.PRAWException as ex:
            print(f"Reddit API exception: {ex}")
            continue
        except Exception as ex:
            print(f"Unexpected exception: {ex}")
            continue

    c.close()



if __name__ == "__main__":

    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=SECRET_TOKEN,
                         user_agent=USER_AGENT)

    subred_name\
        = "euro2024+nba+tennis+CopaAmerica"

    # Socket prep
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    print("Listening on port: %s" % str(port))
    s.listen()

    subreddit = reddit.subreddit(subred_name)
    stream_json(subreddit)
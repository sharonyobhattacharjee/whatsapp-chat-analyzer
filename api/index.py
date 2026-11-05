import os
import sys
import io
import base64

from flask import Flask, jsonify, render_template, request

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

import preprocessor
import helper


app = Flask(
    __name__,
    template_folder=os.path.join(ROOT_DIR, "templates")
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/health")
def health():
    return jsonify({
        "status": "success",
        "message": "WhatsApp Chat Analyzer API is running on Vercel"
    })


def wordcloud_to_base64(wordcloud):
    buffer = io.BytesIO()

    wordcloud.to_image().save(
        buffer,
        format="PNG"
    )

    return base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")


def safe_int_list(values):
    return [
        int(value)
        for value in values
    ]


def safe_float_list(values):
    return [
        float(value)
        for value in values
    ]


@app.route("/api/analyze", methods=["POST"])
def analyze():

    # --------------------------------------------------
    # Validate upload
    # --------------------------------------------------

    if "chat" not in request.files:
        return jsonify({
            "error": "No chat file uploaded."
        }), 400

    uploaded_file = request.files["chat"]

    if not uploaded_file.filename:
        return jsonify({
            "error": "No chat file selected."
        }), 400

    # Vercel request payload limit is 4.5 MB.
    # Keep a little safety margin.
    uploaded_file.seek(0, os.SEEK_END)
    file_size = uploaded_file.tell()
    uploaded_file.seek(0)

    if file_size > 4 * 1024 * 1024:
        return jsonify({
            "error": (
                "This chat export is too large for the current Vercel "
                "upload limit. Please export the chat without media."
            )
        }), 413

    try:

        # --------------------------------------------------
        # Read chat
        # --------------------------------------------------

        data = uploaded_file.read().decode(
            "utf-8-sig",
            errors="replace"
        )

        if not data.strip():
            return jsonify({
                "error": "The uploaded chat file is empty."
            }), 400

        # --------------------------------------------------
        # Process chat
        # --------------------------------------------------

        df = preprocessor.preprocess(data)

        if df.empty:
            return jsonify({
                "error": (
                    "No WhatsApp messages were detected. "
                    "Please upload a valid WhatsApp exported .txt file."
                )
            }), 400

        # --------------------------------------------------
        # Users
        # --------------------------------------------------

        users = [
            str(user)
            for user in df["user"].dropna().unique().tolist()
            if user != "group_notification"
        ]

        users.sort(
            key=lambda x: x.lower()
        )

        selected_user = request.form.get(
            "user",
            "Overall"
        )

        if (
            selected_user != "Overall"
            and selected_user not in users
        ):
            selected_user = "Overall"

        # --------------------------------------------------
        # Statistics
        # --------------------------------------------------

        (
            num_messages,
            words,
            num_media_messages,
            num_links
        ) = helper.fetch_stats(
            selected_user,
            df
        )

        # --------------------------------------------------
        # Monthly timeline
        # --------------------------------------------------

        monthly = helper.monthly_timeline(
            selected_user,
            df
        )

        monthly_data = {
            "time": [
                str(x)
                for x in monthly["time"].tolist()
            ],
            "message": safe_int_list(
                monthly["message"].tolist()
            )
        }

        # --------------------------------------------------
        # Daily timeline
        # --------------------------------------------------

        daily = helper.daily_timeline(
            selected_user,
            df
        )

        daily_data = {
            "date": [
                str(x)
                for x in daily["only_date"].tolist()
            ],
            "message": safe_int_list(
                daily["message"].tolist()
            )
        }

        # --------------------------------------------------
        # Busy days
        # --------------------------------------------------

        busy_day = helper.week_activity_map(
            selected_user,
            df
        )

        busy_day_data = {
            "days": [
                str(x)
                for x in busy_day.index.tolist()
            ],
            "messages": safe_int_list(
                busy_day.values.tolist()
            )
        }

        # --------------------------------------------------
        # Heatmap
        # --------------------------------------------------

        heatmap = helper.activity_heatmap(
            selected_user,
            df
        )

        heatmap_data = {
            "days": [
                str(x)
                for x in heatmap.index.tolist()
            ],
            "periods": [
                str(x)
                for x in heatmap.columns.tolist()
            ],
            "values": [
                safe_int_list(row)
                for row in heatmap.values.tolist()
            ]
        }

        # --------------------------------------------------
        # Most busy users
        # --------------------------------------------------

        busy_users_data = {
            "names": [],
            "messages": []
        }

        user_percent_data = {
            "names": [],
            "percent": []
        }

        if selected_user == "Overall":

            busy_users, user_percent = (
                helper.most_busy_users(df)
            )

            busy_users_data = {
                "names": [
                    str(x)
                    for x in busy_users.index.tolist()
                ],
                "messages": safe_int_list(
                    busy_users.values.tolist()
                )
            }

            if not user_percent.empty:

                user_percent_data = {
                    "names": [
                        str(x)
                        for x in user_percent["name"].tolist()
                    ],
                    "percent": safe_float_list(
                        user_percent["percent"].tolist()
                    )
                }

        # --------------------------------------------------
        # Word cloud
        # --------------------------------------------------

        wordcloud_image = ""

        try:
            wc = helper.create_wordcloud(
                selected_user,
                df
            )

            if wc:
                wordcloud_image = (
                    wordcloud_to_base64(wc)
                )

        except Exception:
            # Wordcloud should never break
            # the entire dashboard.
            wordcloud_image = ""

        # --------------------------------------------------
        # Emoji analysis
        # --------------------------------------------------

        emoji_data = {
            "emojis": [],
            "counts": []
        }

        try:

            emoji_df = helper.emoji_helper(
                selected_user,
                df
            )

            if (
                emoji_df is not None
                and not emoji_df.empty
                and len(emoji_df.columns) >= 2
            ):

                emoji_data = {
                    "emojis": [
                        str(x)
                        for x in emoji_df.iloc[:, 0].tolist()
                    ],
                    "counts": safe_int_list(
                        emoji_df.iloc[:, 1].tolist()
                    )
                }

        except Exception:
            # Emoji analysis is optional.
            # Never crash the complete analysis.
            emoji_data = {
                "emojis": [],
                "counts": []
            }

        # --------------------------------------------------
        # Final response
        # --------------------------------------------------

        return jsonify({

            "status": "success",

            "users": users,

            "selected_user": selected_user,

            "statistics": {

                "messages": int(
                    num_messages
                ),

                "words": int(
                    words
                ),

                "media": int(
                    num_media_messages
                ),

                "links": int(
                    num_links
                )
            },

            "monthly_timeline":
                monthly_data,

            "daily_timeline":
                daily_data,

            "busy_days":
                busy_day_data,

            "heatmap":
                heatmap_data,

            "busy_users":
                busy_users_data,

            "user_percent":
                user_percent_data,

            "wordcloud":
                wordcloud_image,

            "emoji":
                emoji_data
        })

    except Exception as e:

        import traceback

        print(
            "ANALYSIS ERROR:",
            str(e)
        )

        traceback.print_exc()

        return jsonify({
            "status": "error",
            "error": (
                "Could not analyze this WhatsApp chat. "
                "Please make sure it is an exported WhatsApp "
                "chat .txt file."
            ),
            "details": str(e)
        }), 500

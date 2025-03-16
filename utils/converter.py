def convert_to_html(feedback, main_language):
    """Converts feedback into structured HTML format with RTL or LTR direction."""

    dir_attr = "rtl" if main_language == "ar" else "ltr"
    lang_attr = "ar" if main_language == "ar" else "en"

    html_template = f"""
    <!DOCTYPE html>
    <html lang="{lang_attr}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Feedback Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 20px;
                background-color: #f4f4f4;
            }}
            .container {{
                direction: {dir_attr};
                text-align: {'right' if dir_attr == 'rtl' else 'left'};
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }}
            h1, h2, h3 {{
                color: #333;
            }}
            p {{
                font-size: 16px;
                line-height: 1.6;
            }}
            ul {{
                padding-left: 20px;
            }}
            li {{
                margin-bottom: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {feedback}
        </div>
    </body>
    </html>
    """

    return html_template

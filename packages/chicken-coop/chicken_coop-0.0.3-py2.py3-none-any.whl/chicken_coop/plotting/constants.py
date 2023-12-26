from __future__ import annotations

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SVG Centered</title>
    <style>
        body, html {{
            height: 100%;
            margin: 0;
            background-color: white;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        svg {{
            max-height: 100%;
            max-width: 100%;
            width: 100%;
            height: 100%;
        }}
    </style>
</head>
<body>
    <svg viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
        {}
    </svg>
</body>
</html>
'''

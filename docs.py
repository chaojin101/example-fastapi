from starlette.responses import HTMLResponse

from fastapi import APIRouter

router = APIRouter()


def get_custom_redoc_html(
    *,
    openapi_url: str,
    title: str,
    redoc_favicon_url: str = "https://fastapi.tiangolo.com/img/favicon.png",
    with_google_fonts: bool = True,
) -> HTMLResponse:
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{title}</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    """
    if with_google_fonts:
        html += """
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    """
    html += f"""
        <link rel="shortcut icon" href="{redoc_favicon_url}">
        <!--
        ReDoc doesn't change outer page styles
        -->
        <style>
          body {{
            margin: 0;
            padding: 0;
          }}
        </style>
        </head>
        <body>
            <div id="redoc-container"></div>
              <script src="https://cdn.jsdelivr.net/npm/redoc@2.0.0-rc.55/bundles/redoc.standalone.min.js"> </script>
              <script src="https://cdn.jsdelivr.net/gh/wll8/redoc-try@1.4.1/dist/try.js"></script>
              <script>
                initTry({{
                openApi: `{openapi_url}`,
                  redocOptions: {{scrollYOffset: 50}},
                }})
              </script>
        </body>
        </html>
        """
    return HTMLResponse(html)


@router.get("/redoc", include_in_schema=False)
async def redoc_with_try_it_out():
    print(1)
    return get_custom_redoc_html(
        openapi_url="/openapi.json",
        title="Custom Redoc",
        redoc_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        with_google_fonts=True,
    )

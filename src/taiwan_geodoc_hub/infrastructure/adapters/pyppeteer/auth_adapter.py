from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware

from taiwan_geodoc_hub.modules.cli.access_managing.domain.ports.auth_service import (
    AuthService,
)
from taiwan_geodoc_hub.modules.cli.access_managing.dtos.credentials import Credentials
from os import getenv
from uvicorn import Config, Server
from asyncio import create_task, get_running_loop, wait_for, CancelledError
from pyppeteer import launch
from json import loads


class AuthAdapter(AuthService):
    async def render_sign_in_page(self, request):
        config = getenv("FIREBASE_CONFIG")
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <title>Login</title>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <script src="https://www.gstatic.com/firebasejs/10.12.0/firebase-app-compat.js"></script>
          <script src="https://www.gstatic.com/firebasejs/10.12.0/firebase-auth-compat.js"></script>
        </head>
        <body>
          <div id="status">正在初始化...</div>
          <script>
            async function performAuth() {{
              try {{
                document.getElementById('status').textContent = '正在初始化 Firebase...';
                firebase.initializeApp({config});
                
                document.getElementById('status').textContent = '請選擇 Google 帳號進行登入...';
                const provider = new firebase.auth.GoogleAuthProvider();
                provider.addScope('email');
                provider.addScope('profile');
                
                const result = await firebase.auth().signInWithPopup(provider);
                const user = result.user;
                
                document.getElementById('status').textContent = '正在取得認證令牌...';
                const id_token = await user.getIdToken();
                const refresh_token = user.refreshToken;
                
                document.getElementById('status').textContent = '登入成功！';
                
                // 呼叫 Python 暴露的函數
                if (window.resolve) {{
                  window.resolve(JSON.stringify({{
                    id_token: id_token,
                    refresh_token: refresh_token
                  }}));
                }} else {{
                  console.error('resolve function not found');
                }}
              }} catch (error) {{
                console.error('Auth error:', error);
                document.getElementById('status').textContent = '登入失敗: ' + error.message;
                if (window.reject) {{
                  window.reject(error.message);
                }} else {{
                  console.error('reject function not found');
                }}
              }}
            }}
            
            // 等待頁面完全載入後執行
            if (document.readyState === 'loading') {{
              document.addEventListener('DOMContentLoaded', performAuth);
            }} else {{
              performAuth();
            }}
          </script>
        </body>
        </html>
        """
        return HTMLResponse(html.strip())

    def create_app(self):
        app = Starlette(
            debug=False,
            routes=[
                Route("/auth/sign-in", self.render_sign_in_page),
            ],
        )
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
        return app

    async def auth(self) -> Credentials:
        future = get_running_loop().create_future()
        port = int(getenv("AUTH_SERVICE_PORT", "3000"))
        server = Server(
            Config(
                app=self.create_app(),
                host="0.0.0.0",
                port=port,
                log_level="error",
            )
        )
        server_task = create_task(server.serve())
        browser = await launch(
            headless=False,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process",
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
                "--no-first-run",
                "--no-default-browser-check",
            ],
        )
        try:
            [page] = await browser.pages()

            # 暴露函數到瀏覽器環境
            await page.exposeFunction(
                "resolve",
                lambda json_str: (
                    future.set_result(json_str) if not future.done() else None
                ),
            )
            await page.exposeFunction(
                "reject",
                lambda error: (
                    future.set_exception(Exception(error))
                    if not future.done()
                    else None
                ),
            )

            def on_close():
                if not future.done():
                    future.set_exception(Exception(""))

            page.on("close", on_close)
            await page.goto(
                f"http://localhost:{port}/auth/sign-in", waitUntil="networkidle0"
            )
            json_str = await wait_for(future, timeout=300)  # 增加到 5 分鐘
            credentials_data = loads(json_str)
            return Credentials(**credentials_data)
        except Exception:
            raise
        finally:
            await browser.close()

            server.should_exit = True
            await server.shutdown()
            if not server_task.done():
                server_task.cancel()
                try:
                    await server_task
                except CancelledError:
                    pass

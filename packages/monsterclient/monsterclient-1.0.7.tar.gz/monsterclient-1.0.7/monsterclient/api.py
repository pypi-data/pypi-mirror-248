
import os
import json
import requests
import json
import curlify
import warnings
from pathlib import Path
from urllib.parse import urlparse
from pygments import highlight, lexers, formatters
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)


def convert_to_curl(curl_command):
    unwanted_headers = [
        "-H 'Accept: */*'",
        "-H 'Accept-Encoding: gzip, deflate'",
        "-H 'Connection: keep-alive'",
        "-H 'Content-Length: 0'",
        "-H 'User-Agent: python-requests/2.31.0'",
    ]

    curl = curlify.to_curl(curl_command)

    for header in unwanted_headers:
        curl = curl.replace(header, "")
    curl_parts = curl.split()
    curl_parts.insert(1, "-v")
    return " ".join(curl_parts)


class Response:
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def repr(self, **kwargs):
        ans = ""
        for key, value in vars(self).items():
            if key in kwargs and kwargs[key] == False:
                continue
            elif value is not None:
                tmp = self.prettify(value)
                try:
                    soup = BeautifulSoup(tmp, "html.parser")
                    beautified_html = soup.prettify()
                    tmp = beautified_html
                except:
                    pass
                ans += tmp + "\n"

        ans = ans.replace("\n\n", "\n")
        ans = ans.removesuffix("\n")
        return ans

    def prettify(self, inp):
        res = str(inp).replace("'", '"')
        try:
            data = json.loads(res)
            tmp = json.dumps(data, indent=4)
            colorized_json = highlight(
                tmp, lexers.JsonLexer(), formatters.TerminalFormatter()
            )
            return colorized_json
        except:
            return res


class Token:
    def __init__(self) -> None:
        self.auth_endpoint = ""
        self.url_endpoint = ""
        self.username = ""
        self.password = ""

    def get_token(self):
        pass


class TokenV3(Token):
    def __init__(self) -> None:
        self.monster_endpoint = os.getenv("OS_MONSTER_URL", "http://127.0.0.1:8080")
        self.auth_endpoint_postfix = "/v3/auth/tokens"
        self.auth_endpoint = os.getenv("OS_AUTH_URL", "http://127.0.0.1:5000")
        self.url_endpoint = ""
        self.user_domain_id = os.getenv("OS_USER_DOMAIN", "default")
        self.project_domain_id = os.getenv("OS_PROJ_DOMAIN", "default")
        self.username = os.getenv("OS_USERNAME", "tester")
        self.password = os.getenv("OS_PASSWORD", "testing")
        self.project_name = os.getenv("OS_PROJECT_NAME", "test")

    def get_token(self):
        payload = json.dumps(
            {
                "auth": {
                    "identity": {
                        "methods": ["password"],
                        "password": {
                            "user": {
                                "name": f"{self.username}",
                                "domain": {"id": f"{self.user_domain_id}"},
                                "password": f"{self.password}",
                            }
                        },
                    },
                    "scope": {
                        "project": {
                            "domain": {"id": f"{self.project_domain_id}"},
                            "name": f"{self.project_name}",
                        }
                    },
                }
            }
        )
        headers = {"Content-Type": "application/json"}
        url = self.auth_endpoint + self.auth_endpoint_postfix
        response = requests.post(url=url, headers=headers, data=payload)
        project_id = response.json()["token"]["project"]["id"]
        storage_path = self.monster_endpoint + "/v1/AUTH_" + project_id
        self.url_endpoint = storage_path
        token = response.headers["X-Subject-Token"]
        return token, self.url_endpoint, response


class TokenV1(Token):
    def get_token(self):
        auth_endpoint = os.getenv("ST_AUTH", "http://127.0.0.1:8080/auth/v1.0")
        url_endpoint = os.getenv("ST_URL", "http://127.0.0.1:8080/v1/AUTH_test")
        username = os.getenv("ST_USER", "test:tester")
        password = os.getenv("ST_KEY", "testing")

        headers = {"X-Storage-User": username, "X-Storage-Pass": password}
        response = requests.get(url=auth_endpoint, headers=headers)
        token = response.headers["X-Auth-Token"]
        return token, url_endpoint, response


class AuthAPI:
    def __init__(self) -> None:
        self.path = os.path.join(Path.home(), ".monster")

    def write_monster_connection(self, token: Token):
        path = self.path
        token, monster_endpoint, response = token.get_token()
        token_json = {"token": token, "monster": monster_endpoint}
        with open(path, "w") as data:
            json.dump(token_json, data)

        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            token=token,
            curl=modified_curl,
        )

    def read_monster_connection(self):
        path = self.path
        try:
            with open(path, "r") as data:
                jdata = json.load(data)
            return jdata
        except:
            return {"token": None, "monster": "http://127.0.0.1:8080/v1/AUTH_test"}


class MonsterAPI:
    def __init__(self) -> None:
        auth = AuthAPI()
        connection = auth.read_monster_connection()
        self.monster_endpoint = connection["monster"]
        self.token = connection["token"]
        self.headers = {"X-Auth-Token": self.token}

    # Create
    def create_container(self, container_name):
        url = self.monster_endpoint
        response = requests.put(f"{url}/{container_name}", headers=self.headers)
        modified_curl = convert_to_curl(response.request)

        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    def upload_object(self, container_name, object_name):
        url = self.monster_endpoint

        with open(object_name, "rb") as f:
            data = f.read()
        response = requests.put(
            f"{url}/{container_name}/{object_name}", headers=self.headers, data=data
        )
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    # Delete
    def delete_container(self, container_name):
        url = self.monster_endpoint
        response = requests.delete(f"{url}/{container_name}", headers=self.headers)
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    def delete_object(self, container_name, object_name):
        url = self.monster_endpoint

        response = requests.delete(
            f"{url}/{container_name}/{object_name}", headers=self.headers
        )
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    # Head
    def head_account(self):
        url = self.monster_endpoint

        response = requests.head(f"{url}", headers=self.headers)
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            headers=response.headers,
            curl=modified_curl,
        )

    def head_container(self, container_name):
        url = self.monster_endpoint

        response = requests.head(f"{url}/{container_name}", headers=self.headers)
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            headers=response.headers,
            curl=modified_curl,
        )

    def head_object(self, container_name, object_name):
        url = self.monster_endpoint

        response = requests.head(
            f"{url}/{container_name}/{object_name}", headers=self.headers
        )
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            headers=response.headers,
            curl=modified_curl,
        )

    # Get
    def get_account(self):
        url = self.monster_endpoint

        response = requests.get(f"{url}", headers=self.headers)
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    def get_container(self, container_name):
        url = self.monster_endpoint

        response = requests.get(f"{url}/{container_name}", headers=self.headers)
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    def get_object(self, container_name, object_name):
        url = self.monster_endpoint

        response = requests.get(
            f"{url}/{container_name}/{object_name}", headers=self.headers
        )
        modified_curl = convert_to_curl(response.request)
        with open(f"{object_name}", "wb") as data:
            data.write(response.content)

        try:
            return Response(
                status_code=response.status_code,
                content=response.content.decode(),
                curl=modified_curl,
            )
        except:
            return Response(
                status_code=response.status_code,
                curl=modified_curl,
            )

    # Metadata
    def post_account(self, kv):
        url = self.monster_endpoint
        key, value = kv.split(":")[0], kv.split(":")[1]
        headers = self.headers
        headers |= {f"{key}": f"{value}"}

        response = requests.post(f"{url}", headers=headers)
        modified_curl = convert_to_curl(response.request)

        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    def post_container(self, container_name, kv):
        url = self.monster_endpoint
        key, value = kv.split(":")[0], kv.split(":")[1]
        headers = self.headers
        headers |= {f"{key}": f"{value}"}

        response = requests.post(f"{url}/{container_name}", headers=headers)
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    def post_object(self, container_name, object_name, kv):
        url = self.monster_endpoint
        key, value = kv.split(":")[0], kv.split(":")[1]
        headers = self.headers
        headers |= {f"{key}": f"{value}"}

        response = requests.post(
            f"{url}/{container_name}/{object_name}", headers=headers
        )
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

    # Info
    def get_info(self):
        url = self.monster_endpoint

        parsed_url = urlparse(url)
        base_url = parsed_url.scheme + "://" + parsed_url.netloc
        response = requests.get(f"{base_url}/info")
        modified_curl = convert_to_curl(response.request)
        return Response(
            status_code=response.status_code,
            content=response.content.decode(),
            curl=modified_curl,
        )

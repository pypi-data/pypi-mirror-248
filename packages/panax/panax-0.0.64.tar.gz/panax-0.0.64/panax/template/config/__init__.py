# 全局配置


APP_SETTING = {
    # 数据库链接
    "db": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "passwd": "",
        "database": ""
    },
    "static": "",
    # jwt 配置
    "jwt": {
        # jwt中 包含的用户列, 至少包含["id", "username", "name", "role"]，可以按需增加其他列
        "column": ["id", "username", "name", "role"],
        # jwt加密解密使用的密钥串
        "secret": "123!@#"
    },
    "file": {
        # 配置文件上传接口 可以上传的文件类型，调用方式：/api/file/image, /api/file/video
        "image": ["jpg", "jpeg", "bmp", "gif", "png"],
        "video": ["mp4"],
        "doc": ["doc", "docx"],
        "pdf": ["pdf"],
        "txt": ["txt"],
    },
    "request": {
        "secret": True,
        "key": {
            "public": b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApTE9r3m0xUhm+i5JsONo\nVNVax5IKdIhLIei2U+7BfwQECPV2UpV/L7CAzq9hBJKm6wjHRRm1avEo2YjqvYjT\niCs1NG85UjaTb42iSbLCzGxdB/S6FFWk0c/i4VT8PcNdh5Dg5U/p8chp5WYlPYjk\n9WPz66z6Imf1TW9NoShwYYGFqeoZTS6uz7oU93kpOFWRLgPizysamF4AWbD7dosT\nZpYjHJEk5yqvFC/wlgNGpBMShvKcUa+ogg7VYcJu3HbLggAqrSuCrUp/ZX9F2gyR\nmNbiOyvC5QXdz7lpFqMWu7ZEJeGF+SVycknWb2O8OCzk0Padq0CNXUjtdzHy8rV/\n/QIDAQAB\n-----END PUBLIC KEY-----',
            "private": b'-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEApTE9r3m0xUhm+i5JsONoVNVax5IKdIhLIei2U+7BfwQECPV2\nUpV/L7CAzq9hBJKm6wjHRRm1avEo2YjqvYjTiCs1NG85UjaTb42iSbLCzGxdB/S6\nFFWk0c/i4VT8PcNdh5Dg5U/p8chp5WYlPYjk9WPz66z6Imf1TW9NoShwYYGFqeoZ\nTS6uz7oU93kpOFWRLgPizysamF4AWbD7dosTZpYjHJEk5yqvFC/wlgNGpBMShvKc\nUa+ogg7VYcJu3HbLggAqrSuCrUp/ZX9F2gyRmNbiOyvC5QXdz7lpFqMWu7ZEJeGF\n+SVycknWb2O8OCzk0Padq0CNXUjtdzHy8rV//QIDAQABAoIBAAajz00vmOzKH3uE\nY0llJqMsTUES1XFALjbvde6zPNtYY7ohda9Vm35k+5RzN7TZmTR+zpWwNhrVlTUD\nPB5AsvH4/KM+KkFr+Kql+IU6Vnqli2q/s0AQfjbBwqaYhigMY4TItcV53BcwHVOP\ncsVBrKRRb3NEaWx7HcDOTcJB0ByXKd2wwxLxcnykMxPtlNJXuYrAYX96K/RZozei\n9l8BbDznbp26y55XFgENz7ON7KigLFQl5W+EvClTrlXpPh2t8pfnoW9CORgrDvMB\nDIp2xfnNtL0GgrZ7NS6IkayDX7Fzj1+qkfH8qTt8luOlWZsRQMCusY2x8XSbjsY5\nC5d00IkCgYEAvlnaL43nUEp4TTu1VDYGnKkvS0uyorR8RbnQUOG8OY/v3MWbMvU0\n9m+vcj+nFIpXl8YfrgdL7oPNYH+QuieI3JiGMb+u/RgX1C/lPgyzKuXOICm0CdmG\nV9kWVh/4TPMJdDr8ORmN65YgQQjbGTVASVSupUrkHE0HZJbSAV2bLfUCgYEA3iof\n7BuyOhfceLyl/1bBJ4qYjuDSMpkE1EcuoRv1bry1uYIX8vPPi0s8B1oQqkKpeyjJ\nQM5L8r234W0beRfzeGnndnjzXVYD44tQ2ToKU2CIq0G341HRCuiLror8TabU0b30\nbOnVjkevx2ChihFxOpPgi9wlbCBpPqa3FbWefOkCgYEAp3+fe/sNkdyF8chZrol/\n1fkWMdahkYTqWdzBT3rjy286LXYBNJ0LBtOOeiVC29NEcryXgebPzUlTvtdhvj0t\ntJfOdhZrYDEEPuYKfkhknJntgOXRlF1CVyki+5RURToTlqCU85XmCWloZnHpgkwW\njrCioba99Z1epQgGMcdx1sUCgYEAkCtj9dNvUDWl1BAP5OhGhkNxht6saTtVn+/l\neZVsKwV5JD4hDn9bgrg650ZyJBsIYqzwFQcK0CZ/imFEf8ukKtMG6qHIxBwKgAIr\nYBxDESJG7mPCUlkIv/xykL0Ox9FosAeF85u3AxLQJiE2EyQIh4vpHrmo60cJJSgJ\nDaSDiekCgYEAgbrrmbBzcYmRfu0vx8cdAYeIT97qQPnMFsN0VMJGXOpYnVG0acA7\nrQ+a05wrmSRGqyRcGhaAAo4SEEeZ+isAAkkfL5k3+8ANM2MWz4AEUitDVoN03lqP\ndXRAk8Tgn2xVnpo3crbGYhSDjMYnlIuNHcspGkCCwxX+efwu0WyV190=\n-----END RSA PRIVATE KEY-----'
        }
    }
}

# anymore 所有用户，包含匿名用户
# all 所有用户（登录）
# 角色
# 用户字段__表字段

# 权限配置
API_PERMISSION = {
    "__default": {
        "list": ["all"],
        "get": ["all"],
        "post": ["all"],
        "put": ["all"],
        "delete": ["all"],
        "drop": [],
        "__other": []
    },
    "file": {
        "image": ["anymore"],
        "video": ["anymore"],
        "doc": ["anymore"],
        "pdf": ["anymore"],
        "txt": ["anymore"],
    },
    "users": {
        "post": ["admin", "teacher"],
        "put": ["admin", "teacher", "id__id"],
        "delete": ["admin"],
        "login": ["anymore"]
    },
    # 权限示例，并没有创建experiment表
    "experiment": {
        "post": ["admin", "teacher"],
        # 管理员、 教师、 负责人、 所属组织的用户、 教学团队中的用户
        "put": ["admin", "teacher", "id__master_id", "org_id__org_id", "org_id__team_id"],
        "delete": ["admin", ],
        "pub": ["admin", ],
        "cancel": ["admin", ]
    }
}

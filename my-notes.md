# 常用命令

## 查看端口占用
```bash
netstat -tulpn | grep :3000 # 查看3000端口是否被占用
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 127.0.0.1:3000          0.0.0.0:*               LISTEN      127893/node
```
上面这个127893就是pid

```bash
lsof -i :3000
```
这个更直接

## 启动backend

```bash
# 启动开发服务器（支持热重载）
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
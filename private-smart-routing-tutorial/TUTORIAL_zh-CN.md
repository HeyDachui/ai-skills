# 用一台海外 VPS 搭建“国内直连、国际服务走海外”的私人智能分流

版本：V1  
适用对象：有基础 Linux 和 Windows 运维能力的个人用户  
定位：少量具名设备的私人网络基础设施，不是公开代理或商业 VPN

## 1. 最终效果

```text
你的 Windows 电脑
  ├─ 国内网站、局域网、打印机 → 本地宽带
  └─ Google、OpenAI、Codex、GitHub 等 → 海外 VPS
```

这套方案使用：

- Ubuntu VPS 作为海外出口；
- WireGuard 作为电脑到 VPS 的加密通道；
- Windows TUN 规则引擎自动区分国内和国际流量；
- 每台电脑使用独立密钥和独立地址。

它不会开放公网 HTTP/SOCKS 代理，也不需要给 Codex 设置 `HTTP_PROXY`。

## 2. 适用与不适用

适合：

- 个人或极少量具名用户；
- 希望国内网站保持本地速度；
- 希望浏览器、Codex、CLI 和部分 UDP 应用统一分流；
- 能维护一台 Ubuntu VPS。

不适合：

- 公开招募用户；
- 出售代理账号；
- 多租户商业服务；
- 规避服务商条款或目标平台规则；
- 要求零维护、绝对稳定或保证 IP 永不触发风控。

实施前请核对 VPS 服务商的最新条款、所在地法律和目标平台规则。

## 3. 准备材料

- 一台 Ubuntu 22.04 或相近版本的海外 VPS；
- 独立公网 IPv4；
- UDP 可用；
- Windows 10/11 x64；
- 一套经过验证的 Windows TUN 管理器发布包；
- 服务商控制台恢复入口；
- SSH 密钥。

如果没有具备“中国直连、其余公网经 WireGuard”规则和 DNS 分流能力的 TUN
客户端，本文的服务端部分只能得到普通 WireGuard 出口，不能自动实现本文所述的
智能分流效果。

先定义自己的变量：

```text
<VPS_PUBLIC_IP>   VPS 公网地址
<SSH_PORT>        SSH 管理端口
<WG_PORT>         WireGuard UDP 端口
<WAN_IF>          VPS 公网网卡
<WG_SUBNET>       WireGuard 私网，例如自选 RFC1918 /24
<WG_SERVER_ADDR>  服务端私网地址
<ADMIN_USER>      日常管理账号
<SERVER_PRIVATE_KEY>  服务端本地生成的 WireGuard 私钥
<DEVICE_PUBLIC_KEY>   某台 Windows 电脑生成的 WireGuard 公钥
<DEVICE_UNIQUE_ADDRESS>  该电脑独享的 WireGuard /32 地址
```

任何仍含 `<...>` 的命令都不能直接执行。

## 4. 配置 Ubuntu VPS

### 4.1 更新和安装软件

```bash
sudo apt update
sudo apt full-upgrade -y
sudo apt install -y wireguard ufw fail2ban vnstat curl
```

### 4.2 建立密钥管理账号

```bash
sudo adduser <ADMIN_USER>
sudo usermod -aG sudo <ADMIN_USER>
sudo install -d -m 700 -o <ADMIN_USER> -g <ADMIN_USER> /home/<ADMIN_USER>/.ssh
sudoedit /home/<ADMIN_USER>/.ssh/authorized_keys
sudo chown <ADMIN_USER>:<ADMIN_USER> /home/<ADMIN_USER>/.ssh/authorized_keys
sudo chmod 600 /home/<ADMIN_USER>/.ssh/authorized_keys
```

在 `sudoedit` 打开的文件中粘贴管理电脑生成的 SSH 公钥。先确认新账号可以用密钥登录，再关闭密码登录。

### 4.3 加固 SSH

在 `/etc/ssh/sshd_config.d/` 新建配置：

```text
Port <SSH_PORT>
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
PermitRootLogin prohibit-password
AllowUsers <ADMIN_USER>
```

先放行端口，然后检查配置：

```bash
sudo ufw allow <SSH_PORT>/tcp
sudo sshd -t
sudo systemctl reload ssh
```

必须保留当前 SSH 会话，并用第二个终端验证新入口。不要在无法使用服务商控制台时冒险修改 SSH。

### 4.4 生成 WireGuard 服务端密钥

```bash
sudo install -d -m 700 /etc/wireguard
sudo sh -c 'umask 077; wg genkey > /etc/wireguard/server_private.key'
sudo sh -c 'wg pubkey < /etc/wireguard/server_private.key > /etc/wireguard/server_public.key'
sudo chmod 600 /etc/wireguard/server_private.key
```

私钥只保存在服务器。不要截图或分享。

### 4.5 开启 IPv4 转发

创建 `/etc/sysctl.d/99-private-wireguard.conf`：

```text
net.ipv4.ip_forward=1
net.ipv4.conf.all.rp_filter=2
net.ipv4.conf.default.rp_filter=2
```

应用：

```bash
sudo sysctl --system
```

### 4.6 创建 WireGuard 接口

先用下面命令确认公网网卡：

```bash
ip route get 1.1.1.1
```

创建 `/etc/wireguard/wg0.conf`：

```ini
[Interface]
Address = <WG_SERVER_ADDR>
ListenPort = <WG_PORT>
PrivateKey = <SERVER_PRIVATE_KEY>

PostUp = iptables -A FORWARD -i %i -o <WAN_IF> -s <WG_SUBNET> -j ACCEPT; iptables -A FORWARD -i <WAN_IF> -o %i -d <WG_SUBNET> -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT; iptables -t nat -A POSTROUTING -s <WG_SUBNET> -o <WAN_IF> -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -o <WAN_IF> -s <WG_SUBNET> -j ACCEPT; iptables -D FORWARD -i <WAN_IF> -o %i -d <WG_SUBNET> -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT; iptables -t nat -D POSTROUTING -s <WG_SUBNET> -o <WAN_IF> -j MASQUERADE
```

然后：

```bash
sudo chmod 600 /etc/wireguard/wg0.conf
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw default deny routed
sudo ufw allow <SSH_PORT>/tcp
sudo ufw allow <WG_PORT>/udp
sudo ufw route allow in on wg0 out on <WAN_IF> from <WG_SUBNET>
sudo ufw enable
sudo systemctl enable --now wg-quick@wg0
sudo wg show
```

服务启动只证明 WireGuard 接口存在，还不代表 Windows 或 AI 平台已经可用。

## 5. 为每台电脑登记独立身份

每台 Windows 电脑都必须：

1. 在本机生成自己的 WireGuard 密钥；
2. 只把公钥交给服务器管理员；
3. 获得唯一 `/32` 私网地址；
4. 使用自己的 Profile；
5. 不与第二台电脑复制密钥或 Profile。

服务端为设备添加：

```ini
[Peer]
PublicKey = <DEVICE_PUBLIC_KEY>
AllowedIPs = <DEVICE_UNIQUE_ADDRESS>/32
```

修改前备份 `/etc/wireguard/wg0.conf`，再加载：

```bash
sudo bash -c 'wg syncconf wg0 <(wg-quick strip wg0)'
sudo wg show wg0
```

客户端 Profile 只应包含端点、服务端公钥、设备地址和分流规则，不应包含客户端私钥。客户端私钥应在 Windows 本地加密保存。

## 6. Windows 智能分流

### 6.1 正确的规则模型

推荐规则：

1. 环回、局域网、RFC1918 私网直连；
2. 中国域名和中国 IP 直连；
3. 手工指定的国内例外直连；
4. 其他公网默认经海外 WireGuard。

不要只列出几个国际域名然后让其余流量默认直连。现代网页包含缓存 IP、CDN 和多个附属域名，很容易出现“检测通过，但网页打不开”。

### 6.2 DNS 必须一起分流

- 国内域名使用本地 DNS；
- 国际域名使用可信远端 DNS；
- 远端 DNS 的连接本身要走海外 WireGuard；
- 如果 VPS 只支持 IPv4 出口，国际解析优先使用 IPv4；
- 中国域名/IP规则集应随客户端提供并定期更新。

只把流量送入 WireGuard、却让国际域名继续走错误的本地解析，是常见失败原因。

### 6.3 安装

1. 解压经过验证的 Windows 发布包；
2. 运行 `Install.cmd`；
3. 接受管理员权限；
4. 打开桌面管理器；
5. 生成设备申请；
6. 让服务器管理员登记公钥并返回 Profile；
7. 导入 Profile；
8. 关闭正在接管网络的 Clash、其他 VPN/TUN 或旧系统代理；
9. 点击“一键启动”。

新工具不应自动修改或清除其他代理。切换前要记录旧设置，以便回滚。

### 6.4 不要设置代理环境变量

TUN 已在系统网络层处理分流，因此通常不需要：

```text
HTTP_PROXY
HTTPS_PROXY
ALL_PROXY
```

WireGuard 的 UDP 端口也不是 HTTP/SOCKS 代理端口，不能填入这些变量。

## 7. 验收

由实际使用者完成：

1. 打开一个国内网站，确认可用；
2. 确认国内出口不是 VPS；
3. 打开 Google 和 ChatGPT 的完整网页；
4. 确认国际出口等于 VPS 公网 IP；
5. 使用 Codex 完成连续收发；
6. 点击“停止并恢复”，确认网络恢复；
7. 再次启动后，点击窗口“×”，确认程序留在托盘且连接继续；
8. 双击托盘图标恢复窗口。

一次成功只能证明基本路径可用。建议继续观察 7—14 天，包括晚高峰、睡眠唤醒、Windows 重启、VPS 重启和平台风控。

## 8. 常见问题

### 日本出口正常，但 ChatGPT 不通

检查国际 DNS 是否经 WireGuard，检查是否错误返回不可用 IPv6，检查目标平台是否拒绝该 IP。

### 检测显示正常，但浏览器打不开

通常是国际白名单过窄。改用“中国域名/IP直连，其余公网默认海外”，再测试完整网页。

### 退出 Clash 后完全没网

Windows 系统代理或环境变量可能仍指向已经停止的本地代理端口。恢复 Clash，或在明确记录后关闭旧代理设置。不要随意填写新环境变量。

### 安装提示文件被占用

升级器应先停止旧管理器和它所属的引擎、等待文件释放、重试复制并校验哈希。不要全局结束所有同名进程。

### 安装窗口乱码

使用 ASCII 的 CMD/PowerShell 安装入口，把中文说明放在 Markdown 中，并保留安装日志。

### Codex 偶发 WebSocket 中断

先重试。再对照时间检查 TUN 是否刚重启、是否只有单个任务失败。不要因为一次长连接中断就设置代理环境变量。

## 9. 回滚和吊销

Windows：

1. 点击“停止并恢复”；
2. 确认 TUN 和引擎退出；
3. 运行 `Uninstall.cmd`；
4. 按切换前记录恢复旧代理。

服务器吊销单台设备：

1. 从 `wg0.conf` 删除该设备的 `[Peer]`；
2. 重新执行 `wg syncconf`；
3. 确认其他设备仍能握手；
4. 被吊销的旧密钥不再复用。

停止全部 WireGuard：

```bash
sudo systemctl disable --now wg-quick@wg0
```

## 10. 安全底线

- 不共享私钥或 Profile；
- 不开放公网 HTTP/SOCKS；
- 不记录访问正文、Cookie 或 API Key；
- 每台设备独立公钥和 `/32`；
- 不再使用的设备立即吊销；
- 定期更新系统和中国规则集；
- 控制月流量与账单；
- 不把独立 IPv4 宣称为高信誉 IP；
- 不把一次连接成功宣称为长期稳定或平台允许。

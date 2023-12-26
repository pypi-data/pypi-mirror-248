## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for details.

让爬虫更简单，让爬虫更高效，让爬虫更智能

## 快速开始

### 1 命令行

aioSpider 系统语法：aioSpider [action] [-argv] [--option]

#### 1.1 查看帮助

```bash
aioSpider -h
```

#### 1.2 查看版本

```bash
aioSpider -v
```

#### 1.3 创建项目

```bash
aioSpider create -p <project>
```

#### 1.4 创建爬虫

```bash
aioSpider create -s <name> --u <url> --en <spider_en_name> --s <source> --t <target> --h <help>
```

#### 1.5 `sql` 表结构转 `model`

```bash
aioSpider make -m --i <path> [--o <path>]
```

#### 1.6 生成爬虫 `bat` 启动脚本

```bash
aioSpider make -b [--i <path>] [--o <path>]
```

#### 1.7 启动 `aioSpider Server`

```bash
aioSpider server run
```

#### 1.8 停止 `aioSpider Server`

```bash
aioSpider server stop
```

#### 1.9 测试 `IP` 带宽 

```bash
aioSpider test proxy [-p <proxy>] [--d <timeout>]
```

### 1.10 适配浏览器环境

```bash
aioSpider install
```

### 1.11 启动redis服务器

```bash
aioSpider redis start
```

### 1.12 关闭redis服务器

```bash
aioSpider redis stop [-p <port>]
```

### 2 使用步骤

（1）创建项目

```bash
aioSpider create -p myproject
```

（2）进入项目根路径

```bash
cd myproject
```


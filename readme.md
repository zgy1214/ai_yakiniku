想要一键烤肉吗？快来下载ai_yakiniku

安装依赖：

```python
pip install -r requirements.txt
```

(如果文件上没有的依赖麻烦手动安一下）

本模型需要用到whisper，请先去将whisper模型下载，并放入本地/models/whisper目录下，以下是模型下载链接（注意，不要下载.en结尾的，因为它可能只支持英文）

```shell
"tiny.en": "https://openaipublic.azureedge.net/main/whisper/models/d3dd57d32accea0b295c96e26691aa14d8822fac7d9d27d5dc00b4ca2826dd03/tiny.en.pt",
"tiny": "https://openaipublic.azureedge.net/main/whisper/models/65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9/tiny.pt",
"base.en": "https://openaipublic.azureedge.net/main/whisper/models/25a8566e1d0c1e2231d1c762132cd20e0f96a85d16145c3a00adf5d1ac670ead/base.en.pt",
"base": "https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt",
"small.en": "https://openaipublic.azureedge.net/main/whisper/models/f953ad0fd29cacd07d5a9eda5624af0f6bcf2258be67c92b79389873d91e0872/small.en.pt",
"small": "https://openaipublic.azureedge.net/main/whisper/models/9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794/small.pt",
"medium.en": "https://openaipublic.azureedge.net/main/whisper/models/d7440d1dc186f76616474e0ff0b3b6b879abc9d1a4926b7adfa41db2d497ab4f/medium.en.pt",
"medium": "https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt",
"large-v1": "https://openaipublic.azureedge.net/main/whisper/models/e4b87e7e0bf463eb8e6956e646f1e277e901512310def2c24bf0e11bd3c28e9a/large-v1.pt",
"large-v2": "https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt",
"large-v3": "https://openaipublic.azureedge.net/main/whisper/models/e5b1a55b89c1367dacf97e3e19bfd829a01529dbfdeefa8caeb59b3f1b81dadb/large-v3.pt",
"large": "https://openaipublic.azureedge.net/main/whisper/models/e5b1a55b89c1367dacf97e3e19bfd829a01529dbfdeefa8caeb59b3f1b81dadb/large-v3.pt",
"large-v3-turbo": "https://openaipublic.azureedge.net/main/whisper/models/aff26ae408abcba5fbf8813c21e62b0941638c5f6eebfb145be0c9839262a19a/large-v3-turbo.pt",
"turbo": "https://openaipublic.azureedge.net/main/whisper/models/aff26ae408abcba5fbf8813c21e62b0941638c5f6eebfb145be0c9839262a19a/large-v3-turbo.pt",
```

如果想用到显卡加速，请配置好本地的torch，关于torch的教程，在此不再赘述。

**在烤肉前，你要把音频文件放到/input目录下，**

下一步就可以开始烤肉

**烤肉命令：(需要在项目目录中）**

```shell
python run main.py -a 你的音频文件名
```

除了`-a`是必选之外，还有以下参数：

+ `-l`目标语言，默认为`bi`（中日双语），其他可选包括`jp`（仅输出日语），`zh`（仅输出中文）
+ `-b`节目代码，用于大模型prompt校队，输入正确的节目代码可以提供给大模型正确的信息，增加正确率。关于节目代码与节目信息，请参考这个网站[http://47.114.217.240/](http://47.114.217.240/)，例如如果正在烤声优桑拿部的节目则输入`snb`,欢迎大家补充（不要恶意攻击网站0
+ `-m`转录模型，默认为`large-v2`如果自己显存不够或者想尝试别的模型可以输入，一定要与上述的名称一致

如果一切顺利，烤好的文件位于/output/output.ass




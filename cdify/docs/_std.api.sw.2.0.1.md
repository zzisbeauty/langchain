```shell
title: AI数字助手
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
code_clipboard: true
highlight_theme: darkula
headingLevel: 2
generator: "@tarslib/widdershins v4.0.30"
```


# 说明

1. 该接口文档基于 yjy 1.0 版本补充，得到的 api 2.0 版本，当前完全向下兼容 1.0 版本。
2. 公共参数 / API 路由和 yjy-1.0版本统一
3. 此版本任意接口新增的参数在每个接口中单独说明，且均具备默认值
4. 响应无法完全对齐，因为确实有当前版本的响应字段并没有在1.0中出现，或者1.0的字段未在当前2.0版本的response中出现。针对这种情况，1.0的reponse中未对齐的字段均采用默认值填充，以保证当前服务无需改动，进替换baseurl后即可快速完成切换。

> **_MORE:🚩正在添加新的图谱等功能也尽可能实现向下兼容_**


# 接口基础信息

## Base URLs
http://10.0.15.21:5627/hanwei/v1


## Authentication

### dify

认证模块在网关进行控制；程序内部不涉及认证操作


### neo4j server

- neo4j base64 密钥信息 `bmVvNGo6OU5WODR0TFRjQkxvVnQ=`
- Authorization: Basic bmVvNGo6OU5WODR0TFRjQkxvVnQ=

#### 图数据库服务状态快速测试

```shell
curl -H "Authorization: Basic bmVvNGo6OU5WODR0TFRjQkxvVnQ=" \
     -H "Content-Type: application/json" \
     -d '{"statements":[{"statement":"MATCH (n) RETURN n LIMIT 1"}]}' \
     http://10.0.15.21:7474/db/neo4j/tx/commit
```


# 接口服务健康检查

- GET /hello

## 返回示例

```json
{
	"code": 0,
	"data": "",
	"elapsed_ms": 0.0403,  // 接口耗时记录，方便后续性能优化
	"message": "Healthy check successful!"
}
```



# 研究院知识库/知识库管理


## GET 获取知识库列表 （已兼容）

GET /kb/list

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|page|query|string| 否 |none|
|page_size|query|string| 否 |none|
|keywords|query|string| 否 |none|
|Username|header|string| 否 |none|

1. 没有 Username 参数，因为这里不做权限管理 

### 返回示例

```json
{
  "code": 0,
  "data": {
    "kbs": [
      {
        "avatar": "",
        "chunk_num": 5657,
        "description": "",
        "doc_num": 5965,
        "embd_id": "BAAI/bge-large-zh-v1.5@BAAI",
        "id": "c63752aa2edf11f09ce41a5a51635fdb",
        "language": "English",
        "name": "数据支撑平台-保密",
        "parser_id": "naive",
        "permission": "team",
        "token_num": 1181410,
        "update_time": 1747733392127
      },
      ...
    ],
    "total": 10
  },
  "message": "success"
}
```





## POST 新增知识库（已兼容）

POST /kb/create

### 请求参数

```json
{
  "name": "testApi"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|name|query|string| 否 |none|
|Username|header|string| 否 |none|
|body|body|object| 否 |none|

#### 前版本新增参数

**_新增：均已设置默认值，以向下兼容 1.0_**

- description：知识库描述
- indexing_technique：索引方案
- search_method：检索方法
- score_threshold_enabled：语义检索阈值开关，建议设置为 false，否则可能会影响召回
- embedding_model：目前写定为本地模型
- reranking_enable：目前默认False，本地无rerank model，且非必需为 True
- score_threshold: 语义检索召回阈值
- top_k：默认召回的片段数量
- weights：混合检索，语义权重

### 返回示例

```json
{
  "code": 0,
  "message": "string"
}
```





## GET 获取单个知识库详情（已兼容）

GET /v1/kb/detail

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|kb_id|query|string| 否 |none|
|Username|header|string| 否 |none|

### 返回示例
```json
{
  "code": 0,
  "data": {
    "auth_list": [
      "string"
    ],
    "avatar": "string",
    "chunk_num": 0,
    "description": "string",
    "doc_num": 0,
    "embd_id": "string",
    "id": "string",
    "language": "string",
    "manager_list": [
      "string"
    ],
    "name": "string",
    "pagerank": 0,
    "parser_config": {
      "graphrag": {
        "community": true,
        "entity_types": [
          "string"
        ],
        "method": "string",
        "resolution": true,
        "use_graphrag": true
      },
      "layout_recognize": "string"
    },
    "parser_id": "string",
    "permission": "string",
    "token_num": 0
  },
  "message": "string"
}
```

### 返回数据结构

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|object|true|none||none|
|»» auth_list|[string]|true|none||none|
|»» avatar|string|true|none||none|
|»» chunk_num|integer|true|none||none|
|»» description|string|true|none||none|
|»» doc_num|integer|true|none||none|
|»» embd_id|string|true|none||none|
|»» id|string|true|none||none|
|»» language|string|true|none||none|
|»» manager_list|[string]|true|none||none|
|»» name|string|true|none||none|
|»» pagerank|integer|true|none||none|
|»» parser_config|object|true|none||none|
|»»» graphrag|object|true|none||none|
|»»»» community|boolean|true|none||none|
|»»»» entity_types|[string]|true|none||none|
|»»»» method|string|true|none||none|
|»»»» resolution|boolean|true|none||none|
|»»»» use_graphrag|boolean|true|none||none|
|»»» layout_recognize|string|true|none||none|
|»» parser_id|string|true|none||none|
|»» permission|string|true|none||none|
|»» token_num|integer|true|none||none|
|» message|string|true|none||none|





## POST 知识库更新（已兼容）

POST /v1/kb/update

### 请求参数

```json
{
  "avatar": "",
  "description": null,
  "embd_id": "BAAI/bge-large-zh-v1.5@BAAI",
  "kb_id": "998ff43836a911f09aaca68d932eca9a",
  "name": "test_0411",
  "pagerank": 100,
  "parser_config": {
    "layout_recognize": "DeepDOC",
    "auto_keywords": 0,
    "auto_questions": 0,
    "raptor": {
      "use_raptor": false
    },
    "graphrag": {
      "use_graphrag": true,
      "entity_types": [
        "organization",
        "person",
        "geo",
        "event",
        "category"
      ],
      "resolution": true,
      "method": "light"
    }
  },
  "parser_id": "manual",
  "permission": "team",
  "manager_list": [
    "H05583"
  ],
  "auth_list": [
    "2122"
  ]
}
```

### 新增参数 ----> **_均设置默认值向下兼容_**

- weights：检索语义权重
- top_k：召回文档片段数量
- indexing_technique：索引方案
- score_threshold_enabled：召回阈值开关启用，默认 False，建议保持关闭，否则可能会出现很难召回的情况
- score_threshold：召回阈值，不建议设置过高，rag领域，超过0.35就容易出现难以召回的情况，该值默认 0.25，非必要可无需调整

### 返回示例

```json
{
  "code": 0,
  "data": {
    "avatar": "string",
    "chunk_num": 0,
    "create_date": "string",
    "create_time": 0,
    "created_by": "string",
    "description": null,
    "doc_num": 0,
    "embd_id": "string",
    "id": "string",
    "language": "string",
    "name": "string",
    "pagerank": 0,
    "parser_config": {
      "auto_keywords": 0,
      "auto_questions": 0,
      "graphrag": {
        "entity_types": [
          "string"
        ],
        "method": "string",
        "resolution": true,
        "use_graphrag": true
      },
      "layout_recognize": "string",
      "raptor": {
        "use_raptor": true
      }
    },
    "parser_id": "string",
    "permission": "string",
    "similarity_threshold": 0,
    "status": "string",
    "tenant_id": "string",
    "token_num": 0,
    "update_date": "string",
    "update_time": 0,
    "vector_similarity_weight": 0
  },
  "message": "string"
}
```

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|object|true|none||none|
|»» avatar|string|true|none||none|
|»» chunk_num|integer|true|none||none|
|»» create_date|string|true|none||none|
|»» create_time|integer|true|none||none|
|»» created_by|string|true|none||none|
|»» description|null|true|none||none|
|»» doc_num|integer|true|none||none|
|»» embd_id|string|true|none||none|
|»» id|string|true|none||none|
|»» language|string|true|none||none|
|»» name|string|true|none||none|
|»» pagerank|integer|true|none||none|
|»» parser_config|object|true|none||none|
|»»» auto_keywords|integer|true|none||none|
|»»» auto_questions|integer|true|none||none|
|»»» graphrag|object|true|none||none|
|»»»» entity_types|[string]|true|none||none|
|»»»» method|string|true|none||none|
|»»»» resolution|boolean|true|none||none|
|»»»» use_graphrag|boolean|true|none||none|
|»»» layout_recognize|string|true|none||none|
|»»» raptor|object|true|none||none|
|»»»» use_raptor|boolean|true|none||none|
|»» parser_id|string|true|none||none|
|»» permission|string|true|none||none|
|»» similarity_threshold|number|true|none||none|
|»» status|string|true|none||none|
|»» tenant_id|string|true|none||none|
|»» token_num|integer|true|none||none|
|»» update_date|string|true|none||none|
|»» update_time|integer|true|none||none|
|»» vector_similarity_weight|number|true|none||none|
|» message|string|true|none||none|







## POST 知识库删除（已兼容）

POST /v1/kb/rm

### 请求参数

```json
{
  "kb_id": "998ff43836a911f09aaca68d932eca9a"
}
```

### 返回示例(v-1.0)

```json
{}
```

### 返回示例(v-2.0) ----> **_新增示例说明_**

- code = 0: 表示删除成功
- code = -1：表示删除失败

```json
{
	"code": 0,
	"data": "delete DB f3338b4c-d710-4f10-a651-ad75a7df5511 true",
	"message": "Delete DB successful!"
}
```








## POST 召回测试（已兼容）

POST /v1/chunk/retrieval_test

### 请求参数

```json
{
  "similarity_threshold": 0.2,  // 不建议过高（超过0.35），0.2 是合适的
  "vector_similarity_weight": 0.30000000000000004,
  "use_kg": false,
  "question": "一级",
  "doc_ids": [],
  "kb_id": "226c7cd63ad311f0aa52360cd0cdbb30",
  "page": 1,
  "size": 10
}
```

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Username|header|string| 否 |none|
|authentication|header|string| 否 |none|
|timestamp|header|string| 否 |none|
|body|body|object| 否 |none|

### 新增参数 ----> **_新增参数_**

- top_k：召回的片段数量
- score_threshold_enabled：召回阈值开关；默认 false,否则很难召回

### 返回示例

#### 502 Response

```
{}
```

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|502|[Bad Gateway](https://tools.ietf.org/html/rfc7231#section-6.6.3)|none|Inline|

#### 正常响应 ----> **_新增响应示例_**

```json
{
	"code": 0,
	"data": {
		"query": "文章主旨是什么, 是宝黛爱情吗？",
		"records": [
			{
				"answer": "贾宝玉与林黛质的爱情是《红楼梦》的核心线索，贯穿全书并推动情节发展。他们的爱情从初见的朦胧情愫到后来的深切相知，既体现了封建礼教对自由恋爱的压抑，也映射出人物命运的悲剧性。黛玉的早逝与宝玉的出家直接导致贾府由盛转衰，其爱情悲剧成为整个故事的高潮和结局，同时揭示了\"千红一哭，万艳同悲\"的主题。",
				"content": "贾宝玉和林黛玉的爱情在《红楼梦》中如何作为故事的推进主线？",
				"document": {
					"id": "59f95774-31fc-4e05-a691-eb89f1b5be22",
					"name": "红楼梦解析"
				},
				"score": 0.668397
			},
			{
				"answer": "他们的爱情既是个体命运的悲剧，也是社会制度的缩影。黛玉的多愁善感与宝玉的痴情反映了封建社会对人性的压抑，而他们最终未能在一起的结局则揭示了封建礼教对自由恋爱的残酷打击。这种爱情悲剧既是对个人情感的哀悼，也是对整个封建社会的批判，体现了曹雪芹\"满纸荒唐言\"的创作意图。",
				"content": "贾宝玉和林黛玉的爱情如何体现《红楼梦》的深层主题？",
				"document": {
					"id": "59f95774-31fc-4e05-a691-eb89f1b5be22",
					"name": "红楼梦解析"
				},
				"score": 0.65222532
			}
		]
	},
	"message": "知识库检索成功!"
}
```




## GET 查询知识库知识图谱数据（目前不具备，因此暂未兼容）

GET /v1/kb/5ba99c8236b811f08483e2281ab37f32/knowledge_graph

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Username|header|string| 否 |none|

### 返回示例

```json
{
  "code": 0,
  "data": {
    "graph": {},
    "mind_map": {}
  },
  "message": "string"
}
```

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|object|true|none||none|
|»» graph|object|true|none||none|
|»» mind_map|object|true|none||none|
|» message|string|true|none||none|










# 研究院知识库/文件管理

## POST 文件上传（已兼容）

POST /v1/document/upload

### 请求参数

```yaml
kb_id: 5ba99c8236b811f08483e2281ab37f32
file: file://C:\Users\CX\Desktop\内涝演示环境\城市生命线排水清单.xlsx
```

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Username|header|string| 否 |none|
|body|body|object| 否 |none|
|» kb_id|body|string| 否 |ID 编号|
|» file|body|string(binary)| 否 |none|

### 新增参数 ----> **_新增参数_**

- file_name: 命名上传的文档的名称
- mode: 文档处理方式，默认 custom，也可以设置未 automatic，但是建议保持不动，参数已经设置完毕，aotu 模式可能会影响文档处理效果
- separator: 文档分割标识符，如果有很明确的分割符号，可以主动指定，比如："=、\n等符号"，如果不明确，可以不填
- max_tokens：文档分割的最大 tokens
- indexing_technique：文档索引方式
- doc_form：文档处理方式：text_model（默认），qa_model
- doc_language：qa_model时，指定需要的语言，默认为 Chinses


### 返回示例

```json
{
  "code": 0,
  "data": [
    {
      "created_by": "string",
      "id": "string",
      "kb_id": "string",
      "location": "string",
      "name": "string",
      "parser_config": {
        "pages": [
          [
            0
          ]
        ]
      },
      "parser_id": "string",
      "size": 0,
      "thumbnail": "string",
      "type": "string"
    }
  ],
  "message": "string"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|[object]|true|none||none|
|»» created_by|string|false|none||none|
|»» id|string|false|none||none|
|»» kb_id|string|false|none||none|
|»» location|string|false|none||none|
|»» name|string|false|none||none|
|»» parser_config|object|false|none||none|
|»»» pages|[array]|true|none||none|
|»» parser_id|string|false|none||none|
|»» size|integer|false|none||none|
|»» thumbnail|string|false|none||none|
|»» type|string|false|none||none|
|» message|string|true|none||none|





## 文档状态 ----> 新增接口

- post
- api /document/status

### 参数说明

- kb_id	body	string	是		指定的知识库唯一标识符
- batch	body	string	是		本次文档处理的批次标识符

### 返回示例

indexing_status 可以为：splitting/paused/waiting/indexing/error

```json
{
    "data": {
        "data": [
            {
                "cleaning_completed_at": null,
                "completed_at": null,
                "completed_segments": 0,
                "error": null,
                "id": "b2bcf89b-cf94-42f7-9f89-493dd05507e6",
                "indexing_status": "splitting",
                "parsing_completed_at": 1751441760,
                "processing_started_at": 1751441760,
                "splitting_completed_at": null,
                "total_segments": 0
            }
        ]
    },
    "info": "request chat info successful!",
    "status_code": 0
}
```








## GET 文件查询（已兼容）

GET /v1/document/list

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|page_size|query|string| 否 |none|
|page|query|string| 否 |none|
|keywords|query|string| 否 |none|
|kb_id|query|string| 否 |none|
|file_name|query|string| 否 |none|
|Username|header|string| 否 |none|

### 返回示例

```json
{
  "code": 0,
  "data": {
    "docs": [
      {
        "chunk_num": 0,
        "create_date": "string",
        "create_time": 0,
        "created_by": "string",
        "id": "string",
        "kb_id": "string",
        "location": "string",
        "meta_fields": {},
        "name": "string",
        "parser_config": {
          "pages": [
            null
          ]
        },
        "parser_id": "string",
        "process_begin_at": null,
        "process_duation": 0,
        "progress": 0,
        "progress_msg": "string",
        "run": "string",
        "size": 0,
        "source_type": "string",
        "status": "string",
        "thumbnail": "string",
        "token_num": 0,
        "type": "string",
        "update_date": "string",
        "update_time": 0
      }
    ],
    "total": 0
  },
  "message": "string"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|object|true|none||none|
|»» docs|[object]|true|none||none|
|»»» chunk_num|integer|true|none||none|
|»»» create_date|string|true|none||none|
|»»» create_time|integer|true|none||none|
|»»» created_by|string|true|none||none|
|»»» id|string|true|none||none|
|»»» kb_id|string|true|none||none|
|»»» location|string|true|none||none|
|»»» meta_fields|object|true|none||none|
|»»» name|string|true|none||none|
|»»» parser_config|object|true|none||none|
|»»»» pages|[array]|true|none||none|
|»»» parser_id|string|true|none||none|
|»»» process_begin_at|null|true|none||none|
|»»» process_duation|integer|true|none||none|
|»»» progress|integer|true|none||none|
|»»» progress_msg|string|true|none||none|
|»»» run|string|true|none||none|
|»»» size|integer|true|none||none|
|»»» source_type|string|true|none||none|
|»»» status|string|true|none||none|
|»»» thumbnail|string|true|none||none|
|»»» token_num|integer|true|none||none|
|»»» type|string|true|none||none|
|»»» update_date|string|true|none||none|
|»»» update_time|integer|true|none||none|
|»» total|integer|true|none||none|
|» message|string|true|none||none|










## POST 文件解析（此接口dify中无法单独存在）

### 新增说明

**_dify 不具备该接口，在上传文件时，dify必须执行文档的解析、嵌入、索引_**


### 请求参数

POST /v1/document/run

```json
{
  "delete": false,
  "doc_ids": [
    "569fa39836b911f0a5c0e2281ab37f32"
  ],
  "run": 1
}
```

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Username|header|string| 否 |none|
|body|body|object| 否 |none|

### 返回示例

```json
{
  "code": 0,
  "data": true,
  "message": "string"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|boolean|true|none||none|
|» message|string|true|none||none|





## GET 文件下载（新增）

### 研究院接口

GET /v1/document/get/f48d71bc36b811f0b2c88aca13ba27e8

#### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Username|header|string| 否 |none|

#### 返回示例

```
{}
```

#### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

#### 返回数据结构


### 本地下载接口(单文件下载)

GET /document/get

#### 参数要求

- kb_id： 必填
- document_id: 必填
- download_dir： 下载路径，非必填

#### 响应情况

```json
{
	"code": 0,
	"data": {
		"download_url": "http://10.0.15.21/files/debad906-570e-4302-b1a4-0ffd5253d0d1/file-preview?timestamp=1752224762&nonce=336efb8db41fdbd128cc758b81ab68a0&sign=_8O5UD9jpFypZTFrnWbJSIsu25t2_DN2-MVBvJJR1LI=&as_attachment=true",
		"file_info": {
			"created_at": 1752214968.581919,
			"created_by": "c85ba575-0a9f-4c7c-bc1b-95dc6810efaf",
			"download_url": "/files/debad906-570e-4302-b1a4-0ffd5253d0d1/file-preview?timestamp=1752224762&nonce=336efb8db41fdbd128cc758b81ab68a0&sign=_8O5UD9jpFypZTFrnWbJSIsu25t2_DN2-MVBvJJR1LI=&as_attachment=true",
			"extension": "pdf",
			"id": "debad906-570e-4302-b1a4-0ffd5253d0d1",
			"mime_type": "application/pdf",
			"name": "DB21T 3976-2024_《农村集中供水工程水价测算导则》.pdf",
			"size": 810648,
			"url": "/files/debad906-570e-4302-b1a4-0ffd5253d0d1/file-preview?timestamp=1752224762&nonce=336efb8db41fdbd128cc758b81ab68a0&sign=_8O5UD9jpFypZTFrnWbJSIsu25t2_DN2-MVBvJJR1LI="
		},
		"file_path": "./cdify/datas/downloads-from-dify/DB21T 3976-2024_《农村集中供水工程水价测算导则》.pdf"
	},
	"elapsed_s": 0.0647,
	"message": "文档已成功下载到: ./cdify/datas/downloads-from-dify/DB21T 3976-2024_《农村集中供水工程水价测算导则》.pdf"
}
```

### 文件下载接口（批量下载）

GET /documents/batch-download

#### 参数情况

- kb_id： 知识库ID 必填
- download_dir： 文件存储路径，非必填

#### 响应结果

```json
{
	"code": 0,
	"data": {
		"download_dir": "",
		"failed_count": 0,
		"results": [
			{
				"document_id": "39ea732d-f58e-4944-bc68-087ac81e3489",
				"document_name": "[总-产品功能开发指导]应用场景与功能模块.docx",
				"result": {
					"code": 0,
					"data": {
						"download_url": "http://10.0.15.21/files/d8d023cf-dd17-446e-8ea9-5f62e0c92991/file-preview?timestamp=1752225740&nonce=c9b5e647dafa9f0cb4afe545731d0648&sign=2WC4W1__FSKALI8S7jonS-5jAbOPIK9I9x0LNyGH6DI=&as_attachment=true",
						"file_info": {
							"created_at": 1752054566.264399,
							"created_by": "c85ba575-0a9f-4c7c-bc1b-95dc6810efaf",
							"download_url": "/files/d8d023cf-dd17-446e-8ea9-5f62e0c92991/file-preview?timestamp=1752225740&nonce=c9b5e647dafa9f0cb4afe545731d0648&sign=2WC4W1__FSKALI8S7jonS-5jAbOPIK9I9x0LNyGH6DI=&as_attachment=true",
							"extension": "docx",
							"id": "d8d023cf-dd17-446e-8ea9-5f62e0c92991",
							"mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
							"name": "[总-产品功能开发指导]应用场景与功能模块.docx",
							"size": 16301,
							"url": "/files/d8d023cf-dd17-446e-8ea9-5f62e0c92991/file-preview?timestamp=1752225740&nonce=c9b5e647dafa9f0cb4afe545731d0648&sign=2WC4W1__FSKALI8S7jonS-5jAbOPIK9I9x0LNyGH6DI="
						},
						"file_path": "./cdify/datas/downloads-from-dify/[总-产品功能开发指导]应用场景与功能模块.docx"
					},
					"message": "文档已成功下载到: ./cdify/datas/downloads-from-dify/[总-产品功能开发指导]应用场景与功能模块.docx"
				},
				"status": "success"
			},
      ... // 其他文件信息，结构相同，所以省略掉避免繁复
		],
		"success_count": 5,
		"total_documents": 5
	},
	"elapsed_s": 0.5734,
	"message": "批量下载完成，成功: 5，失败: 0"
}
```






## POST 文件删除（已兼容）

POST /v1/document/rm

> Body 请求参数

```json
{
  "doc_id": [
    "569fa39836b911f0a5c0e2281ab37f32"
  ]
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Username|header|string| 否 |none|
|body|body|object| 否 |none|


### 返回示例

```json
{
  "code": 0,
  "data": true,
  "message": "string"
}
```

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|boolean|true|none||none|
|» message|string|true|none||none|











## POST 文档切片查询（已兼容）

POST /v1/chunk/list

### 请求参数

### 新增说明 ---> **_keywords 支持传入单个 str；也支持传入 [str1, str2, ...]_**

```json
{
  "page": 1,
  "size": 10,
  "doc_id": "d087b0ec36be11f0827a82b73f02c197",
  "keywords": "临期"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Username|header|string| 否 |none|
|body|body|object| 否 |none|

### 返回示例

```json
{
  "code": 0,
  "data": {
    "chunks": [
      {
        "available_int": 0,
        "chunk_id": "string",
        "content_with_weight": "string",
        "doc_id": "string",
        "docnm_kwd": "string",
        "image_id": "string",
        "important_kwd": [
          "string"
        ],
        "positions": [
          "string"
        ],
        "question_kwd": [
          "string"
        ]
      }
    ],
    "doc": {
      "chunk_num": 0,
      "create_date": "string",
      "create_time": 0,
      "created_by": "string",
      "id": "string",
      "kb_id": "string",
      "location": "string",
      "meta_fields": {},
      "name": "string",
      "parser_config": {
        "pages": [
          [
            null
          ]
        ]
      },
      "parser_id": "string",
      "process_begin_at": "string",
      "process_duation": 0,
      "progress": 0,
      "progress_msg": "string",
      "run": "string",
      "size": 0,
      "source_type": "string",
      "status": "string",
      "thumbnail": "string",
      "token_num": 0,
      "type": "string",
      "update_date": "string",
      "update_time": 0
    },
    "total": 0
  },
  "message": "string"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|object|true|none||none|
|»» chunks|[object]|true|none||none|
|»»» available_int|integer|true|none||none|
|»»» chunk_id|string|true|none||none|
|»»» content_with_weight|string|true|none||none|
|»»» doc_id|string|true|none||none|
|»»» docnm_kwd|string|true|none||none|
|»»» image_id|string|true|none||none|
|»»» important_kwd|[string]|true|none||none|
|»»» positions|[string]|true|none||none|
|»»» question_kwd|[string]|true|none||none|
|»» doc|object|true|none||none|
|»»» chunk_num|integer|true|none||none|
|»»» create_date|string|true|none||none|
|»»» create_time|integer|true|none||none|
|»»» created_by|string|true|none||none|
|»»» id|string|true|none||none|
|»»» kb_id|string|true|none||none|
|»»» location|string|true|none||none|
|»»» meta_fields|object|true|none||none|
|»»» name|string|true|none||none|
|»»» parser_config|object|true|none||none|
|»»»» pages|[array]|true|none||none|
|»»» parser_id|string|true|none||none|
|»»» process_begin_at|string|true|none||none|
|»»» process_duation|number|true|none||none|
|»»» progress|integer|true|none||none|
|»»» progress_msg|string|true|none||none|
|»»» run|string|true|none||none|
|»»» size|integer|true|none||none|
|»»» source_type|string|true|none||none|
|»»» status|string|true|none||none|
|»»» thumbnail|string|true|none||none|
|»»» token_num|integer|true|none||none|
|»»» type|string|true|none||none|
|»»» update_date|string|true|none||none|
|»»» update_time|integer|true|none||none|
|»» total|integer|true|none||none|
|» message|string|true|none||none|









## 指定文档切片的删除 ---> **_新增接口_**

### base url

- 请求方法：delete
- api /chunk/paragraph/rm

### params 

- kb_id	必填；数据库 ID
- doc_id	必填；文档 ID； 该文档必须存在于指定的数据库中
- para_id	必填；需要被删除的段落 ID


### 响应结构

- code = 0: 删除成功
- code = -1： 删除失败

```json
{
    "data": "delete db 1095fcf4-0108-4f75-b2a9-a73b39138d19 doc 463e3615-a746-488a-ace1-e2e91e875d4c, para_id 9dc0d052-0dec-4126-a2f7-f87ea32481ad true",
    "info": "Delete Paragraph successful!",
    "status_code": 0
}
```



## 向指定文档切片中添加信息 ---> **_新增接口_**

### base url

- post
- /chunk/paragraph/add

### 参数列表

- kb_id	是（常规参数）	知识库 ID
- doc_id	是（常规参数）	文档 ID，要求文档必须在指定的数据库内
- content	是	文本内容
- answer	条件必填（可为空）	仅在数据库为 Q-A 类型时必填；

### 响应情况

#### text_model 知识库

```json
{
    "data": [
        {
            "content": "国家水资源管理法",
            "document_id": "463e3615-a746-488a-ace1-e2e91e875d4c",
            "id": "558b2626-d93c-4a1f-9017-e3efb8ae05bc",
            "keywords": [
                "水资源", ...
            ]
        }
    ],
    "message": "向知识库的文档添加文本段落成功!",
    "code": 0
}
```

#### qa_model 知识库

```json
{
    "data": [
        {
            "answer": "请问国家南水北调工程中线辐射区域",
            "content": "关于南水北调中线工程段，其流域面积涉及 ...",
            "document_id": "09c95eca-877f-476b-a34e-2efe552ed757",
            "id": "8981b514-a4f9-4d27-af84-c3aa13c23ac2",
            "keywords": []
        }
    ],
    "info": "向知识库的文档添加文本段落成功!",
    "status_code": 0
}
```











## POST 文档切片状态切换(目前未开发)

POST /v1/chunk/switch

### 请求参数

```json
{
  "available_int": 0,
  "chunk_ids": [
    "98ada12045ee8263"
  ],
  "doc_id": "d087b0ec36be11f0827a82b73f02c197"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Username|header|string| 否 |none|
|body|body|object| 否 |none|

### 返回示例

```
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|503|[Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)|none|Inline|

### 返回数据结构










# 研究院知识库/模型

## POST 选择模型（dify原生不具备，需要二开，目前不具备）

POST /v1/user/set_tenant_info

### 请求参数

```json
{
  "asr_id": "",
  "embd_id": "BAAI/bge-large-zh-v1.5@BAAI",
  "img2txt_id": "",
  "llm_id": "hanweiGPT4o",
  "name": "H05583‘s Kingdom",
  "parser_ids": "naive:General,qa:Q&A,resume:Resume,manual:Manual,table:Table,paper:Paper,book:Book,laws:Laws,presentation:Presentation,picture:Picture,one:One,audio:Audio,email:Email,tag:Tag",
  "rerank_id": "",
  "tenant_id": "H05583",
  "tts_id": null
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|UserName|header|string| 否 |none|
|body|body|object| 否 |none|

### 返回示例

```json
{
  "code": 0,
  "data": true,
  "message": "string"
}
```

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|boolean|true|none||none|
|» message|string|true|none||none|







## POST 选择知识库（dify不具备，dify也没有单独选择知识库的需求）

POST /v1/dialog/set

### 求参数

```json
{
  "icon": "",
  "kb_ids": [
    "5ba99c8236b811f08483e2281ab37f32"
  ],
  "language": "English",
  "llm_id": "hanweiGPT4o",
  "llm_setting": {
    "frequency_penalty": 0.7,
    "presence_penalty": 0.4,
    "temperature": 0.1,
    "top_p": 0.3
  },
  "name": "test_init",
  "prompt_config": {
    "empty_response": "",
    "keyword": false,
    "parameters": [
      {
        "key": "knowledge",
        "optional": false
      }
    ],
    "prologue": "你好！ 我是你的助理，有什么可以帮到你的吗？",
    "quote": true,
    "reasoning": false,
    "refine_multiturn": false,
    "system": "你是一个智能助手，请总结知识库的内容来回答问题，请列举知识库中的数据详细回答。当所有知识库内容都与问题无关时，你的回答必须包括\"知识库中未找到您要的答案！\"这句话。回答需要考虑聊天历史。\n        以下是知识库：\n        {knowledge}\n        以上是知识库。",
    "tavily_api_key": "",
    "tts": false,
    "use_kg": false
  },
  "similarity_threshold": 0.2,
  "top_n": 8,
  "vector_similarity_weight": 0.30000000000000004
}
```

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|UserName|header|string| 否 |none|
|body|body|object| 否 |none|

### 返回示例

```json
{
  "code": 0,
  "data": {
    "description": "string",
    "icon": "string",
    "id": "string",
    "kb_ids": [
      "string"
    ],
    "llm_id": "string",
    "llm_setting": {
      "frequency_penalty": 0,
      "presence_penalty": 0,
      "temperature": 0,
      "top_p": 0
    },
    "name": "string",
    "prompt_config": {
      "empty_response": "string",
      "keyword": true,
      "parameters": [
        {
          "key": "string",
          "optional": true
        }
      ],
      "prologue": "string",
      "quote": true,
      "reasoning": true,
      "refine_multiturn": true,
      "system": "string",
      "tavily_api_key": "string",
      "tts": true,
      "use_kg": true
    },
    "rerank_id": "string",
    "similarity_threshold": 0,
    "tenant_id": "string",
    "top_k": 0,
    "top_n": 0,
    "vector_similarity_weight": 0
  },
  "message": "string"
}
```

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|object|true|none||none|
|»» description|string|true|none||none|
|»» icon|string|true|none||none|
|»» id|string|true|none||none|
|»» kb_ids|[string]|true|none||none|
|»» llm_id|string|true|none||none|
|»» llm_setting|object|true|none||none|
|»»» frequency_penalty|number|true|none||none|
|»»» presence_penalty|number|true|none||none|
|»»» temperature|number|true|none||none|
|»»» top_p|number|true|none||none|
|»» name|string|true|none||none|
|»» prompt_config|object|true|none||none|
|»»» empty_response|string|true|none||none|
|»»» keyword|boolean|true|none||none|
|»»» parameters|[object]|true|none||none|
|»»»» key|string|false|none||none|
|»»»» optional|boolean|false|none||none|
|»»» prologue|string|true|none||none|
|»»» quote|boolean|true|none||none|
|»»» reasoning|boolean|true|none||none|
|»»» refine_multiturn|boolean|true|none||none|
|»»» system|string|true|none||none|
|»»» tavily_api_key|string|true|none||none|
|»»» tts|boolean|true|none||none|
|»»» use_kg|boolean|true|none||none|
|»» rerank_id|string|true|none||none|
|»» similarity_threshold|number|true|none||none|
|»» tenant_id|string|true|none||none|
|»» top_k|integer|true|none||none|
|»» top_n|integer|true|none||none|
|»» vector_similarity_weight|number|true|none||none|
|» message|string|true|none||none|





## GET 获取模型列表（目前不具备，需要看如何二开）

GET /v1/llm/my_llms

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|UserName|header|string| 否 |none|

### 返回示例

```json
{
  "code": 0,
  "data": {
    "Azure-OpenAI": {
      "llm": [
        {
          "name": "string",
          "type": "string",
          "used_token": 0
        }
      ],
      "tags": "string"
    },
    "BaiduYiyan": {
      "llm": [
        {
          "name": "string",
          "type": "string",
          "used_token": 0
        }
      ],
      "tags": "string"
    },
    "Ollama": {
      "llm": [
        {
          "name": "string",
          "type": "string",
          "used_token": 0
        }
      ],
      "tags": "string"
    },
    "OpenAI-API-Compatible": {
      "llm": [
        {
          "name": "string",
          "type": "string",
          "used_token": 0
        }
      ],
      "tags": "string"
    },
    "Tongyi-Qianwen": {
      "llm": [
        {
          "name": "string",
          "type": "string",
          "used_token": 0
        }
      ],
      "tags": "string"
    },
    "VolcEngine": {
      "llm": [
        {
          "name": "string",
          "type": "string",
          "used_token": 0
        }
      ],
      "tags": "string"
    }
  },
  "message": "string"
}
```

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|object|true|none||none|
|»» Azure-OpenAI|object|true|none||none|
|»»» llm|[object]|true|none||none|
|»»»» name|string|false|none||none|
|»»»» type|string|false|none||none|
|»»»» used_token|integer|false|none||none|
|»»» tags|string|true|none||none|
|»» BaiduYiyan|object|true|none||none|
|»»» llm|[object]|true|none||none|
|»»»» name|string|false|none||none|
|»»»» type|string|false|none||none|
|»»»» used_token|integer|false|none||none|
|»»» tags|string|true|none||none|
|»» Ollama|object|true|none||none|
|»»» llm|[object]|true|none||none|
|»»»» name|string|false|none||none|
|»»»» type|string|false|none||none|
|»»»» used_token|integer|false|none||none|
|»»» tags|string|true|none||none|
|»» OpenAI-API-Compatible|object|true|none||none|
|»»» llm|[object]|true|none||none|
|»»»» name|string|false|none||none|
|»»»» type|string|false|none||none|
|»»»» used_token|integer|false|none||none|
|»»» tags|string|true|none||none|
|»» Tongyi-Qianwen|object|true|none||none|
|»»» llm|[object]|true|none||none|
|»»»» name|string|true|none||none|
|»»»» type|string|true|none||none|
|»»»» used_token|integer|true|none||none|
|»»» tags|string|true|none||none|
|»» VolcEngine|object|true|none||none|
|»»» llm|[object]|true|none||none|
|»»»» name|string|false|none||none|
|»»»» type|string|false|none||none|
|»»»» used_token|integer|false|none||none|
|»»» tags|string|true|none||none|
|» message|string|true|none||none|












# 研究院知识库/调用模型知识库（对话模块需要专门开发）

## POST 调用模型对话

POST /v1/conversation/completion

> Body 请求参数

```json
{
  "conversation_id": "kwbVxZ6L5WkEDWuH9W6vKb",
  "messages": [
    {
      "id": "aujPHmCmNy1aKhzwYaR4Vu",
      "content": "你好，我是AI助手，作为你的智能伙伴，我既能写文案、想点子，又能陪你聊天、答疑解惑。",
      "role": "assistant"
    },
    {
      "id": "2Y5BLL792tN4x2NMD7Hmfs",
      "content": "11",
      "role": "user"
    }
  ]
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|UserName|header|string| 否 |none|
|body|body|object| 否 |none|

### 返回示例

...

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构









# 数据模型

... ...

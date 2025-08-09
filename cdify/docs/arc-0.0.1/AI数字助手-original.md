---
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

---

# AI数字助手

Base URLs:

# Authentication

# 研究院知识库/知识库管理

## GET 获取知识库列表

GET /v1/kb/list

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|page|query|string| 否 |none|
|page_size|query|string| 否 |none|
|keywords|query|string| 否 |none|
|Username|header|string| 否 |none|

> 返回示例

> 200 Response

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
      {
        "avatar": "",
        "chunk_num": 1336,
        "description": "",
        "doc_num": 449,
        "embd_id": "BAAI/bge-large-zh-v1.5@BAAI",
        "id": "8bc05e142edf11f0acb71a5a51635fdb",
        "language": "English",
        "name": "数据支撑平台-公开",
        "parser_id": "naive",
        "permission": "team",
        "token_num": 423320,
        "update_time": 1747733392082
      },
      {
        "avatar": "",
        "chunk_num": 582,
        "description": "",
        "doc_num": 2,
        "embd_id": "BAAI/bge-large-zh-v1.5@BAAI",
        "id": "292ce708230a11f08d8e36259918c849",
        "language": "English",
        "name": "test_api",
        "parser_id": "naive",
        "permission": "team",
        "token_num": 122091,
        "update_time": 1747733392051
      },
      {
        "avatar": "",
        "chunk_num": 115,
        "description": "",
        "doc_num": 1,
        "embd_id": "BAAI/bge-large-zh-v1.5@BAAI",
        "id": "a1e6964621aa11f09c8136259918c849",
        "language": "English",
        "name": "test_only",
        "parser_id": "naive",
        "permission": "team",
        "token_num": 18767,
        "update_time": 1747733392026
      },
      {
        "avatar": "",
        "chunk_num": 226,
        "description": "",
        "doc_num": 1,
        "embd_id": "BAAI/bge-large-zh-v1.5@BAAI",
        "id": "7073f362218511f0816eae8f642b08bb",
        "language": "English",
        "name": "AI技术组",
        "parser_id": "manual",
        "permission": "team",
        "token_num": 39678,
        "update_time": 1747733392018
      },
      {
        "avatar": "",
        "chunk_num": 478,
        "description": "测试团队权限，有查询、管理权限，并且开启知识图谱",
        "doc_num": 1,
        "embd_id": "BAAI/bge-large-zh-v1.5@BAAI",
        "id": "cd40cc36218111f0bf6dae8f642b08bb",
        "language": "English",
        "name": "test_team",
        "parser_id": "naive",
        "permission": "team",
        "token_num": 63531,
        "update_time": 1747733392037
      }
    ],
    "total": 6
  },
  "message": "success"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## POST 新增知识库

POST /v1/kb/create

> Body 请求参数

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

> 返回示例

> 200 Response

```json
{
  "code": 0,
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
|» message|string|true|none||none|

## GET 获取单个知识库详情

GET /v1/kb/detail

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|kb_id|query|string| 否 |none|
|Username|header|string| 否 |none|

> 返回示例

> 200 Response

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

## POST 知识库更新

POST /v1/kb/update

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Username|header|string| 否 |none|
|body|body|object| 否 |none|

> 返回示例

> 200 Response

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

## POST 知识库删除

POST /v1/kb/rm

> Body 请求参数

```json
{
  "kb_id": "998ff43836a911f09aaca68d932eca9a"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## POST 召回测试

POST /v1/chunk/retrieval_test

> Body 请求参数

```json
{
  "similarity_threshold": 0.2,
  "vector_similarity_weight": 0.30000000000000004,
  "use_kg": false,
  "question": "一级",
  "doc_ids": [],
  "kb_id": "226c7cd63ad311f0aa52360cd0cdbb30",
  "page": 1,
  "size": 10
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Username|header|string| 否 |none|
|authentication|header|string| 否 |none|
|timestamp|header|string| 否 |none|
|body|body|object| 否 |none|

> 返回示例

> 502 Response

```
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|502|[Bad Gateway](https://tools.ietf.org/html/rfc7231#section-6.6.3)|none|Inline|

### 返回数据结构

## GET 查询知识库知识图谱数据

GET /v1/kb/5ba99c8236b811f08483e2281ab37f32/knowledge_graph

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Username|header|string| 否 |none|

> 返回示例

> 200 Response

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
|»» graph|object|true|none||none|
|»» mind_map|object|true|none||none|
|» message|string|true|none||none|

# 研究院知识库/文件管理

## POST 文件上传

POST /v1/document/upload

> Body 请求参数

```yaml
kb_id: 5ba99c8236b811f08483e2281ab37f32
file: file://C:\Users\CX\Desktop\内涝演示环境\城市生命线排水清单.xlsx
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Username|header|string| 否 |none|
|body|body|object| 否 |none|
|» kb_id|body|string| 否 |ID 编号|
|» file|body|string(binary)| 否 |none|

> 返回示例

> 200 Response

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

## GET 文件查询

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

> 返回示例

> 200 Response

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

## POST 文件解析

POST /v1/document/run

> Body 请求参数

```json
{
  "delete": false,
  "doc_ids": [
    "569fa39836b911f0a5c0e2281ab37f32"
  ],
  "run": 1
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Username|header|string| 否 |none|
|body|body|object| 否 |none|

> 返回示例

> 200 Response

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

## GET 文件下载

GET /v1/document/get/f48d71bc36b811f0b2c88aca13ba27e8

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Username|header|string| 否 |none|

> 返回示例

> 200 Response

```
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## POST 文件删除

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

> 返回示例

> 200 Response

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

## POST 文档切片查询

POST /v1/chunk/list

> Body 请求参数

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

> 返回示例

> 200 Response

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

## POST 文档切片状态切换

POST /v1/chunk/switch

> Body 请求参数

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

> 返回示例

> 503 Response

```
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|503|[Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)|none|Inline|

### 返回数据结构

# 研究院知识库/模型

## POST 选择模型

POST /v1/user/set_tenant_info

> Body 请求参数

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

> 返回示例

> 200 Response

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

## POST 选择知识库

POST /v1/dialog/set

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|UserName|header|string| 否 |none|
|body|body|object| 否 |none|

> 返回示例

> 200 Response

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

## GET 获取模型列表

GET /v1/llm/my_llms

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|UserName|header|string| 否 |none|

> 返回示例

> 200 Response

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

# 研究院知识库/调用模型知识库

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

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

# 数据模型


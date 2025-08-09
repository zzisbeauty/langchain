知识库操作
---------------------------------------------------------------------------------------------------------

## 获取知识库列表 - √

GET /kb/list

> 此接口参数和 YJY 情况一致；且响应结果也尽可能做了统一

### 请求参数

- page
- page_size
- keywords： 非必填

### 返回示例

```json
{
	"code": 0,
	"data": {
		"kbs": [
			{
				"avatar": "",
				"chunk_num": 0,
				"description": "",
				"doc_num": 4,
				"embd_id": "bge-m3:latest@langgenius/ollama/ollama",
				"id": "e0b33974-287c-42cf-bf85-9aa09fa9ae59",
				"language": "Chinese",
				"name": "测试知识库-1754297802951",
				"parser_id": "naive",
				"permission": "only_me",
				"token_num": 81243,
				"update_time": 1754297803
			},
			{
				"avatar": "",
				"chunk_num": 0,
				"description": "",
				"doc_num": 1,
				"embd_id": "bge-m3:latest@langgenius/ollama/ollama",
				"id": "02e54617-65ef-435f-815a-85ed6579e634",
				"language": "Chinese",
				"name": "测试知识库-1754297645282",
				"parser_id": "naive",
				"permission": "only_me",
				"token_num": 2730,
				"update_time": 1754297646
			}
		],
		"total": 2
	},
	"elapsed_s": 1.7739,
	"message": "success"
}
```


## POST 新增/创建知识库 - √

- POST /kb/create

> 此接口参数和 YJY 情况一致；且响应结果也尽可能做了统一

### 请求参数

```json
{
  "name": "testApi"  // 知识库名称
}
```

> 水务有如下已经设置好默认值的参数，非必要可以不处理这些参数

- description：知识库描述 （已和已有字段合并）
- indexing_technique：索引方案
- search_method：检索方法，默认是语义检索；
- score_threshold_enabled：语义检索阈值开关，建议设置为 false，否则可能会影响召回
- embedding_model：目前写定为本地模型
- reranking_enable：目前默认 False，本地无 rerank model，且非必需为 True；且目前为语义检索，此参数不起作用
- score_threshold: 语义检索召回阈值
- top_k：默认召回的片段数量
- weights：混合检索，语义权重

### 返回示例

```json
{
	"code": 0,
	"data": {
		"description": "鲁迅杂文赏析",
		"id": "edccc869-3275-479c-8e59-a850e412eb6f",
		"name": "鲁迅杂文民族主义文学14:52"
	},
	"params":"存储的是创建知识库时的字段",
	"elapsed_s": 6.8629,
	"message": "按照参数完成DB修正后，完成DB创建！"
}
```


## 获取单个知识库详情 - √

GET /v1/kb/detail

> 此接口参数和 YJY 情况一致；且响应结果也尽可能做了统一

### 请求参数

kb_id 必填

### 返回示例

```json
{
	"code": 0,
	"data": {
		"auth_list": [],
		"avatar": "",
		"chunk_num": 0,
		"description": "",
		"doc_num": 4,
		"embd_id": "bge-m3:latest@langgenius/ollama/ollama",
		"id": "e0b33974-287c-42cf-bf85-9aa09fa9ae59",
		"language": "Chinese",
		"manager_list": [],
		"name": "测试知识库-1754297802951",
		"pagerank": 0,
		"parser_config": {
			"graphrag": {
				"community": true,
				"entity_types": [],
				"method": "",
				"resolution": true,
				"use_graphrag": true
			},
			"layout_recognize": ""
		},
		"parser_id": "naive",
		"permission": "only_me",
		"token_num": 81243
	},
	"elapsed_s": 0.4768,
	"message": "success"
}
```


## POST 知识库更新 - √

POST /v1/kb/update

> 此接口参数和 YJY 情况一致；且响应结果也尽可能做了统一

### 请求参数

- kb_id 必填参数

> _均设置默认值向下兼容,因此如果无需调整，可以不关注这些参数_

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
		"avatar": "",
		"chunk_num": 0,
		"create_date": "",
		"create_time": 1754297803,
		"created_by": "419e054c-66b7-482a-8615-63fa9ad227dd",
		"description": "",
		"doc_num": 4,
		"embd_id": "bge-m3:latest@langgenius/ollama/ollama",
		"id": "e0b33974-287c-42cf-bf85-9aa09fa9ae59",
		"language": "Chinese",
		"name": "测试知识库-1754297802951",
		"pagerank": 0,
		"parser_config": {
			"auto_keywords": 0,
			"auto_questions": 0,
			"graphrag": {
				"entity_types": [],
				"method": "",
				"resolution": true,
				"use_graphrag": true
			},
			"layout_recognize": "",
			"raptor": {
				"use_raptor": true
			}
		},
		"parser_id": "naive",
		"permission": "only_me",
		"similarity_threshold": 0.25,
		"status": "",
		"tenant_id": "",
		"token_num": 81243,
		"update_date": "",
		"update_time": 1754550958,
		"vector_similarity_weight": 0.6
	},
	"elapsed_s": 0.6138,
	"message": "success"
}
```


## 知识库删除 - √

POST /v1/kb/rm

> 此接口参数和 YJY 情况一致；且响应结果也尽可能做了统一

### 请求参数

```json
{
  "kb_id": "998ff43836a911f09aaca68d932eca9a"
}
```

### 返回示例

- code = 0: 表示删除成功
- code = -1：表示删除失败

```json
{
	"code": 0,
	"data": "delete DB f3338b4c-d710-4f10-a651-ad75a7df5511 true",
	"message": "Delete DB successful!"
}
```


## 召回测试 - √

POST /v1/chunk/retrieval_test

### 请求参数

> 相同的参数或水务才有但是具备默认值的参数  >  此接口参数和 YJY 情况一致；且响应结果也尽可能做了统一

- kb_id：知识库ID， 必填
- question： 检索关键词， 必填
- top_k：召回的片段数量，非必填，默认 5
- search_method：默认为 semantic_search；如果没有特殊需求，不要修改参数
- score_threshold_enabled：召回阈值开关，非必填，默认 false,否则很难召回
- similarity_threshold 如果 score_threshold_enabled 设置为开，那么该参数有效，默认为 0.2，建议 0.1 ~ 0.3 之间，过高不容易召回
- vector_similarity_weight 召回时语义占比权重，可不设置，默认 0.6

> 水务没有的参数

- page
- size
- doc_ids

### 响应示例

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





知识库中的文件操作
---------------------------------------------------------------------------------------------------------

## 文件上传 - √

### POST 文件上传（Java）

> 需要直接调用 dify api，否则上传的是 route api 服务器上的文件； 
> 此上传过程是写在 spring boot 方法中的，执行文件上传时，就是前端封装参数即可，Java方法中会自动调用 api，即前端无需执行 api 的调用；
> 但是需要注意返回的结果信息，此响应就是 dify 原始的上传文件的响应，需要前端做适配解析。对接时字段问题可以沟通明确

- kbId: 知识库ID
- filepath：文件路径

api ：POST String uploadUrl = "http://10.30.30.97:8080/v1/datasets/" + kbId + "/document/create_by_file";

#### 返回示例（Java Result）

```json
{
	"document": {
		"id": "60f9f674-2b7b-49b8-bfde-f4ac208c7872",
		"position": 2,
		"data_source_type": "upload_file",
		"data_source_info": {
			"upload_file_id": "f1fc9567-2c87-4070-8cb3-7d8a2b3ff9c3"
		},
		"data_source_detail_dict": {
			"upload_file": {
				"id": "f1fc9567-2c87-4070-8cb3-7d8a2b3ff9c3",
				"name": "222222.txt",
				"size": 656,
				"extension": "txt",
				"mime_type": "text/plain",
				"created_by": "419e054c-66b7-482a-8615-63fa9ad227dd",
				"created_at": 1754452088.593775
			}
		},
		"dataset_process_rule_id": "445f6303-bb1e-48d6-84f2-219b8dbaedde",
		"name": "222222.txt",
		"created_from": "api",
		"created_by": "419e054c-66b7-482a-8615-63fa9ad227dd",
		"created_at": 1754452089,
		"tokens": 0,
		"indexing_status": "parsing",
		"error": null,
		"enabled": true,
		"disabled_at": null,
		"disabled_by": null,
		"archived": false,
		"display_status": "indexing",
		"word_count": 0,
		"hit_count": 0,
		"doc_form": "text_model",
		"doc_metadata": null
	},
	"batch": "20250806034808896242"
}
```

### POST 文件上传（python调用路由，无需关心此接口说明记录）

POST /v1/document/upload

### 请求参数（必填）

```shell
file: 上传的本地文件
kb_id: 5ba99c8236b811f08483e2281ab37f32
```

### 新增参数（非必填）

> 均有默认值，非特殊情况可以不指定

- mode: 文档处理方式，默认 custom，也可以设置未 automatic，但是建议保持不动，参数已经设置完毕，aotu 模式可能会影响文档处理效果
- separator: 文档分割标识符，如果有很明确的分割符号，可以主动指定，比如："=、\n等符号"，如果不明确，有默认值可以不填
- max_tokens：文档分割的最大 tokens
- indexing_technique：文档索引方式
- doc_form：文档处理方式：text_model（默认），qa_model
- doc_language：qa_model时，指定需要的语言，默认为 Chinses

### 返回示例(python api)

```json
{
  "code": 0,
  "data": [
    {
      "created_by": "419e054c-66b7-482a-8615-63fa9ad227dd",
      "id": "8441ad28-acaf-4f75-bf57-8549a4b1404d",
      "kb_id": "d32dbfb4-6cb0-4551-ad30-ec2a3cd78fd2",
      "location": "",
      "name": "Universal Quantum Computational Spectroscopy on a Quantum Chip.pdf",
      "parser_config": {
        "pages": [
          []
        "pages": [
          []
        ]
      },
      "parser_id": "naive",
      "size": 8917312,
      "thumbnail": "",
      "type": "pdf"
    }
  ],
  "elapsed_s": 8.2529,
  "message": "success"
}
```


## 知识库中的文件列表查询

GET /v1/document/list

### 请求参数

> 水务目前此接口只有 kb_id 为必填

kb_id  必填

> 研究院此接口还有如下参数，这三个参数目前水务没有

- page
- page_size
- keywords

### 返回示例

```json
{
	"code": 0,
	"data": {
		"docs": [
			{
				"chunk_num": 0,
				"create_date": "",
				"create_time": 0,
				"created_by": "",
				"id": "4982aa94-d810-48a9-92fe-82a3a7913933",
				"kb_id": "e5176734-ead9-44cf-8bd6-124bc73564e0",
				"location": "",
				"meta_fields": {},
				"name": "从百草园到三味书屋.txt",
				"parser_config": {
					"pages": [
						null
					]
				},
				"parser_id": "naive",
				"process_begin_at": null,
				"process_duation": 0,
				"progress": 0,
				"progress_msg": "",
				"run": "",
				"size": 0,
				"source_type": "",
				"status": "",
				"thumbnail": "",
				"token_num": 0,
				"type": "text_model",
				"update_date": "",
				"update_time": 0
			},
			{
				"chunk_num": 0,
				"create_date": "",
				"create_time": 0,
				"created_by": "",
				"id": "f4d9a9a3-08f6-4199-b9be-715f7638133b",
				"kb_id": "e5176734-ead9-44cf-8bd6-124bc73564e0",
				"location": "",
				"meta_fields": {},
				"name": "鲁迅杂文-“民族主义文学”的任务和运命.txt",
				"parser_config": {
					"pages": [
						null
					]
				},
				"parser_id": "naive",
				"process_begin_at": null,
				"process_duation": 0,
				"progress": 0,
				"progress_msg": "",
				"run": "",
				"size": 0,
				"source_type": "",
				"status": "",
				"thumbnail": "",
				"token_num": 0,
				"type": "text_model",
				"update_date": "",
				"update_time": 0
			}
		],
		"total": 2
	},
	"elapsed_s": 0.0956,
	"message": "success"
}
```


## 文件解析

> 目前dify不会有这个文件解析的接口，上传文档，文档会被直接解析与索引


## GET 文件下载 - √

> 此接口原理同文件上传一致，前端无需关注接口，只需要传入必要参数到 spring boot 此文件下载 Java 方法，方法内部在调用 dify 文件下载服务

### POST 文件下载（Java）

- kb_id： 必填
- document_id: 必填
- download_dir： 下载路径，非必填

### 本地下载接口(单文件下载 - python，无需关注此时说明，和Java无关)

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


## POST 文件删除 - √

DELETE /v1/document/rm

### 请求参数

```json
{
  "kb_id": "知识库id"
  "doc_id": "知识库中的文档id"
}
```

### 返回示例

- 0 就是正常删除
- -1 就是删除出现错误

```json
{
	"code": 0,
	"data": "",
	"elapsed_s": 0.2908,
	"message": "Delete DB successful!"
}
```


## 文件切片查询 - √

GET /v1/chunk/list

### 参数列表

- kb_id 必填
- doc_id 必填
- page 默认是 1
- size 默认是 100， 每页返回的 chunks 数量，可以根据情况自己调整
- keywords： 保留，但是  dify 没用，因此这个值默认为空，可以不用填写

> 参数和响应已经统一

### 返回示例

```json
{
	"code": 0,
	"data": {
		"chunks": [
			{
				"available_int": 1,
				"chunk_id": "ae0c9559-49cf-4500-ba0e-02bbd58ec7ef",
				"content_with_weight": "从百草园到三味书屋",
				"doc_id": "1ead7466-dd54-4caf-a0a4-dd1e3174901f",
				"docnm_kwd": "",
				"image_id": "",
				"important_kwd": null,
				"positions": [],
				"question_kwd": []
			},
			... // 省略其他文档分段
		],
		"doc": {},
		"total": 20
	},
	"elapsed_s": 0.1146,
	"message": "success"
}
```


## 知识库中整篇文档的启停

POST /document/change_status

> 备注：功能已经根据 console api 开发完毕，绕过权限检验

### 请求参数

```json
- kb_id 文档ID 必填
- doc_id 文档ID 必填
- action  enable or disable，必填，且必须是两者中的一个
```

### 响应示例

- 0 成功
- -1 失败

```json
{
	"code": 0,
	"data": "",
	"elapsed_s": 0.0759,
	"message": "Document disable successful!"
}
```


## 设置默认模型 - 设置系统的默认模型 与 选择知识库问题

- POST /user/set_tenant_info
- ~~POST /models/set_default~~

> 1. 此接口和研究院的功能逻辑存在差异，参数无法进行有效统一：研究院的这个方法看起来是用在对话前选择模型，就像对话前选择知识库；因此用 dify 此接口设置系统默认模型，作为用户对模型的选择；
> 2. 关于知识库的选择接口，研究院是为了在对话前选择知识库方便对话。但是dify在对话过程中，基于工作流编排展开。因此目前对于此接口，水务这边是提前将知识库作为参数传入
>    到对话系统中，在对话过程中调用知识库展开知识库的查询。因此这个设置知识库的参数不做接口，而是一个参数；**因此此功能在对话模块处理**。


### 请求参数

- model： 模型名称
- provider： 模型供应商
- model_type： llm、text-embedding、rerank

> 请求参数示例

```json
{
    "model": "qwen3:4b",
    "model_type": "llm",
    "provider": "langgenius/ollama/ollama"
}
```

### 响应结果

```json
{
	"code": 0,
	"data": "",
	"elapsed_s": 0.3235,
	"message": "Set default model successful!"
}
```


## 获取模型列表

GET /llm/my_llms

### 模型参数

- model_type： 三种值可选： llm 、text-embedding 、rerank

### 响应示例

```json
{
	"code": 0,
	"data": [
		{
			"icon_large": {
				"en_US": "/console/api/workspaces/ff9c6ae1-527b-40df-9739-1da76ca40039/model-providers/langgenius/ollama/ollama/icon_large/en_US",
				"zh_Hans": "/console/api/workspaces/ff9c6ae1-527b-40df-9739-1da76ca40039/model-providers/langgenius/ollama/ollama/icon_large/zh_Hans"
			},
			"icon_small": {
				"en_US": "/console/api/workspaces/ff9c6ae1-527b-40df-9739-1da76ca40039/model-providers/langgenius/ollama/ollama/icon_small/en_US",
				"zh_Hans": "/console/api/workspaces/ff9c6ae1-527b-40df-9739-1da76ca40039/model-providers/langgenius/ollama/ollama/icon_small/zh_Hans"
			},
			"label": {
				"en_US": "Ollama",
				"zh_Hans": "Ollama"
			},
			"models": [
				{
					"deprecated": false,
					"features": [
						"structured-output"
					],
					"fetch_from": "customizable-model",
					"label": {
						"en_US": "qwen3:4b",
						"zh_Hans": "qwen3:4b"
					},
					"load_balancing_enabled": false,
					"model": "qwen3:4b",
					"model_properties": {
						"context_size": 4096,
						"mode": "chat"
					},
					"model_type": "llm",
					"status": "active"
				},
				{
					"deprecated": false,
					"features": [
						"structured-output"
					],
					"fetch_from": "customizable-model",
					"label": {
						"en_US": "mistral:latest",
						"zh_Hans": "mistral:latest"
					},
					"load_balancing_enabled": false,
					"model": "mistral:latest",
					"model_properties": {
						"context_size": 4096,
						"mode": "chat"
					},
					"model_type": "llm",
					"status": "active"
				}
			],
			"provider": "langgenius/ollama/ollama",
			"status": "active",
			"tenant_id": "ff9c6ae1-527b-40df-9739-1da76ca40039"
		}
	],
	"elapsed_s": 0.0966,
	"message": "Get models successful!"
}
```



## 文档切片状态控制

PATCH /datasets/{dataset_id}/documents/{document_id}/segment/{action}

### 模型参数

```shell
enable: 启用
disable: 禁用
```


## 文档切片状态启停

- POST /chunk/switch

### 参数信息

> 主要参数都以对齐，但是相较于研究院，此接口多了一个 kb_id 必须指定

```json
{
    "kb_id": "60651635-5a62-42f4-9425-8d07f3cd69e8",
    "doc_id": "550b8df8-e200-4439-b38c-6b982e4256ac",
    "chunk_ids":["62ffb48e-d4c5-4a91-bae0-8ff4b62b5cd8"],
    "available_int": 0 // 1-enable \ 0-disable
}
```

### 返回信息

- 0 表示接口正常执行
- -1 表示接口出现问题

```json
{
	"code": 0,
	"data": "",
	"elapsed_s": 0.1761,
	"message": "Chunks disable successful!"
}
```


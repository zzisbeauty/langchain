DIFY Base URLs and info
--------------------------------------------------------------------------------------------------------------------

http://10.0.15.21:5627/hanwei/v1

### 接口服务健康检查

> GET /hello 以及返回示例

```json
{
	"code": 0,
	"data": "",
	"elapsed_ms": 0.0403,  // 接口耗时记录，方便后续性能优化
	"message": "Healthy check successful!"
}
```


额外的功能 function
--------------------------------------------------------------------------------------------------------------------

### 向指定文档切片中添加信息

#### base url

- post /chunk/paragraph/add

#### 参数列表

- kb_id	是（常规参数）	知识库 ID
- doc_id	是（常规参数）	文档 ID，要求文档必须在指定的数据库内
- content	是	文本内容
- answer	条件必填（可为空）	仅在数据库为 Q-A 类型时必填；

#### 响应示例

- text_model 知识库

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

- qa_model 知识库

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


### 文件下载接口（批量下载）

GET /documents/batch-download

#### 参数情况

- kb_id： 知识库ID 必填
- download_dir： 文件存储路径，非必填

#### 响应示例

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






### 指定文档切片的删除

#### base url

- 请求方法：delete
- api /chunk/paragraph/rm

#### params 

- kb_id	必填；数据库 ID
- doc_id	必填；文档 ID； 该文档必须存在于指定的数据库中
- para_id	必填；需要被删除的段落 ID

#### 响应结构

- code = 0: 删除成功
- code = -1： 删除失败

```json
{
    "data": "delete db 1095fcf4-0108-4f75-b2a9-a73b39138d19 doc 463e3615-a746-488a-ace1-e2e91e875d4c, para_id 9dc0d052-0dec-4126-a2f7-f87ea32481ad true",
    "info": "Delete Paragraph successful!",
    "status_code": 0
}
```

### base url

/hanwei

以下所有API均由 base_url + 路由构成




### 健康检查

- /hello





### 对话模块

#### 聊天会话

- /chat





### databsae and doc 操作模块

#### 获取所有 DBs

- /dbList

#### 获取指定 DB 的具体信息

- /dbInfo

#### 创建知识库

- /createDb

#### 删除知识库

- /deleteDb

#### 编辑知识库属性（关键参数）

- /editDbProperty

#### 向知识库插入文件（以文件作为信息载体）

- /insertTypeFile2DB

#### 向知识库插入文本（直接插入想要输入的文本）

- /insertText2DB

#### 获取指定知识库下的文档列表

- /getDbDocList

#### 获取指定知识库下指定文档的分段情况

- /getDbDocParasList

#### 删除指定知识库下指定文档的指定分段

- /delParagraphs

#### 向指定文档插入文本的形式完善文档内容（增加 doc paragraph）

- /addParagraph








### 检索模块

#### 发起检索

- /dbRetrieval



### 获取文档的一些状态

#### 获取文档 embedding 进度

- /embTqdm
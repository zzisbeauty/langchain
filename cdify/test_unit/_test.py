# ===================================================== other check infos =====================================================

"""
from cdify.api.dbs.db_list import requests_datasets_list
already_dbs = requests_datasets_list() # db list

if dataset_id not in [i['id'] for i in already_dbs]:
    return {'status_code': -1, 'data': "", 'info': f'当前需要被删除的知识库ID {dataset_id} 不存在'}
        
if name in [i['name'] for i in already_dbs]:
    return {'status_code': -1, 'data': "", 'info': '知识库名称重复，请求改名称再进行创建'}
"""

chat_return_all_columns = {
	"event": "message",
	"task_id": "db82aad9-57f6-4197-badc-d2957ba93979",
	"id": "2a32e83f-66fe-4ff0-a91f-d522fdd18540",
	"message_id": "2a32e83f-66fe-4ff0-a91f-d522fdd18540",
	"conversation_id": "7c8645a3-98d1-4555-9888-f76513752671",
	"mode": "advanced-chat",
	"answer": "{\n  \"api\": \"ZHSC-0019\",\n  \"parameter\": []\n}",
	"metadata": {
		"retriever_resources": [
			{
				"position": 1,
				"dataset_id": "8ad0fda9-f1f0-413c-80fc-d776a4de2479",
				"dataset_name": "政务水务系统API-知识库-初版250607",
				"document_id": "c29e277f-76f4-431f-800e-057e5f8dc34c",
				"document_name": "api梳理.txt",
				"data_source_type": "upload_file",
				"segment_id": "37f524f4-3494-48f2-98c9-e472b8d92169",
				"retriever_from": "workflow",
				"score": 0.68382776,
				"hit_count": 3,
				"word_count": 68,
				"segment_position": 50,
				"index_node_hash": "5dd53ccd71637f2b41d1b2ae9f52506b8823794920686a891bc1d183ebf8b118",
				"content": "API：ZHSC-0019\n二水厂加氯间工艺总览\n二水厂加氯间运行态势图\n二水厂加氯间实时运行情况图\nparams:\nno_params",
				# "page": null,
				# "doc_metadata": null
			},
			{
				"position": 2,
				"dataset_id": "8ad0fda9-f1f0-413c-80fc-d776a4de2479",
				"dataset_name": "政务水务系统API-知识库-初版250607",
				"document_id": "c29e277f-76f4-431f-800e-057e5f8dc34c",
				"document_name": "api梳理.txt",
				"data_source_type": "upload_file",
				"segment_id": "c1838717-e4d9-4ee4-8931-796d4feeff03",
				"retriever_from": "workflow",
				"score": 0.62162852,
				"hit_count": 2,
				"word_count": 68,
				"segment_position": 41,
				"index_node_hash": "09af708a39e3ca5339443665811283c4f6591f615df2e54c5bda0b4944c5fd4b",
				"content": "API：ZHSC-0010\n二水厂加药间工艺总览\n二水厂加药间运行态势图\n二水厂加药间实时运行情况图\nparams:\nno_params",
				# "page": null,
				# "doc_metadata": null
			}
		],
		"usage": {
			"prompt_tokens": 1936,
			"prompt_unit_price": "0",
			"prompt_price_unit": "0",
			"prompt_price": "0",
			"completion_tokens": 412,
			"completion_unit_price": "0",
			"completion_price_unit": "0",
			"completion_price": "0",
			"total_tokens": 2348,
			"total_price": "0",
			"currency": "USD",
			"latency": 22.06833207514137
		}
	},
	"created_at": 1749607413
}




from cdify.tools import OS_NAME

text_demo_long = ''
if OS_NAME == "Windows":
	with open(r'E:\其他文件\长文-2.txt','r',encoding='utf-8') as f:
		text_demo_long = f.read()
if OS_NAME == 'Linux':
	with open('./test_unit/docs-data-api-test/鲁迅文章-长.txt','r',encoding='utf-8') as f:
		text_demo_long = f.read()


text_demo = """
鲁迅文集·杂文集·二心集
风马牛①
　　主张“顺而不信”译法的大将赵景深先生，近来却并没有译什么大作，他大抵只在《小说月报》上，将“国外文坛消息”②来介绍给我们。这自然是很可感谢的。那些消息，是译来的呢，还是介绍者自去打听来，研究来的？我们无从捉摸。即使是译来的罢，但大抵没有说明出处，我们也无从考查。自然，在主张“顺而不信”译法的赵先生，这是都不必注意的，如果有些“不信”，倒正是贯彻了宗旨。然而，疑难之处，我却还是遇到的。

　　在二月号的《小说月报》里，赵先生将“新群众作家近讯”告诉我们，其一道：“格罗泼已将马戏的图画故事《A layOop》③脱稿。”这是极“顺”的，但待到看见了这本图画，却不尽是马戏。借得英文字典来，将书名下面注着的两行英文“Life andLove Among the Acrobats Told Entirely in Pictures”④查了一通，才知道原来并不是“马戏”的故事，而是“做马戏的戏子们”的故事。这么一说，自然，有些“不顺”了。但内容既然是这样的，另外也没有法子想。必须是“马戏子”，这才会有“Love”。⑤《小说月报》到了十一月号，赵先生又告诉了我们“塞意斯完成四部曲⑥”，而且“连最后的一册《半人半牛怪》（DerZentaur）也已于今年出版”了。这一下“Der”，就令人眼睛发白，因为这是茄门话⑦，就是想查字典，除了同济学校⑧也几乎无处可借，那里还敢发生什么贰心。然而那下面的一个名词，却不写尚可，一写倒成了疑难杂症。这字大约是源于希腊的，英文字典上也就有，我们还常常看见用它做画材的图画，上半身是人，下半身却是马，不是牛。牛马同是哺乳动物，为了要“顺”，固然混用一回也不关紧要，但究竟马是奇蹄类，牛是偶蹄类，有些不同，还是分别了好，不必“出到最后的一册”的时候，偏来“牛”一下子的。

　　“牛”了一下之后，使我联想起赵先生的有名的“牛奶路”⑨来了。这很像是直译或“硬译”，其实却不然，也是无缘无故的“牛”了进去的。这故事无须查字典，在图画上也能看见。却说希腊神话里的大神宙斯是一位很有些喜欢女人的神，他有一回到人间去，和某女士生了一个男孩子。物必有偶，宙斯太太却偏又是一个很有些嫉妒心的女神。她一知道，拍桌打凳的（？）大怒了一通之后，便将那孩子取到天上，要看机会将他害死。然而孩子是天真的，他满不知道，有一回，碰着了宙太太的乳头，便一吸，太太大吃一惊，将他一推，跌落到人间，不但没有被害，后来还成了英雄。但宙太太的乳汁，却因此一吸，喷了出来，飞散天空，成为银河，也就是“牛奶路”，──不，其实是“神奶路”。但白种人是一切“奶”都叫“Milk”的，我们看惯了罐头牛奶上的文字，有时就不免于误译，是的，这也是无足怪的事。

　　但以对于翻译大有主张的名人，而遇马发昏，爱牛成性，有些“牛头不对马嘴”的翻译，却也可当作一点谈助。──不过当作别人的一点谈助，并且借此知道一点希腊神话而已，于赵先生的“与其信而不顺，不如顺而不信”的格言，却还是毫无损害的。这叫作“乱译万岁！”

　　【注释】

　　①本篇最初发表于一九三一年十二月二十日《北斗》第一卷第四期，署名长庚。

　　风马牛，语出《左传》僖公四年：“君处北海，寡人处南海，唯是风马牛不相及也。”意思是齐楚两国相距很远，即使马牛走失，也不会跑到对方境内。后来用以比喻事物之间毫不相干。

　　②“国外文坛消息”：《小说月报》自一九三一年一月第二十二卷第一期起设立的专栏。赵景深是主要撰稿人。

　　③格罗泼（W．Gropper，1897—1977）：犹太血统的美国画家，“Alay Oop”是吆喝的声音，格罗泼以此作为画册的名字。

　　④英语：“马戏演员的生活和恋爱的图画故事”。

　　⑤“Love”：英语“爱”或“爱情”。

　　⑥塞意斯（F．Thiess）：应译提斯，德国作家。赵景深介绍他的四部曲为：《离开了乐园》《世界之门》、《健身》和《半人半牛怪》。按这四部书总称为“青年四部曲”，其中《健身》应译为《魔鬼》，《半人半牛怪》应译为《半人半马怪》。这些书于一九二四年至一九三一年陆续出版。

　　⑦茄门话：即德语。茄门，German的音译，通译日耳曼。Der是德语阳性名词的冠词。

　　⑧同济学校：一九〇七年德国人在上海设立同济德文医学校，一九一七年由中国政府接办，改为同济德文医工大学，一九二七年改为同济大学。

　　⑨“牛奶路”：这是赵景深在一九二二年翻译契诃夫的小说《樊凯》，（通译《万卡》）时，对英语 MilkyWay（银河）的误译。
"""


demo_json = {
	"data": "{\"id\": \"a7d3df71-9c71-4b65-9cad-4e81df4cf7d9\", \"name\": \"test-db-08:59\", \"description\": \"11111111111\", \"provider\": \"vendor\", \"permission\": \"only_me\", \"data_source_type\": null, \"indexing_technique\": \"high_quality\", \"app_count\": 0, \"document_count\": 0, \"word_count\": 0, \"created_by\": \"c85ba575-0a9f-4c7c-bc1b-95dc6810efaf\", \"created_at\": 1750121960, \"updated_by\": \"c85ba575-0a9f-4c7c-bc1b-95dc6810efaf\", \"updated_at\": 1750213777, \"embedding_model\": \"bge-m3:latest\", \"embedding_model_provider\": \"langgenius/ollama/ollama\", \"embedding_available\": null, \"retrieval_model_dict\": {\"search_method\": \"semantic_search\", \"reranking_enable\": false, \"reranking_mode\": null, \"reranking_model\": {\"reranking_provider_name\": \"\", \"reranking_model_name\": \"\"}, \"weights\": null, \"top_k\": 2, \"score_threshold_enabled\": false, \"score_threshold\": null}, \"tags\": [], \"doc_form\": null, \"external_knowledge_info\": {\"external_knowledge_id\": null, \"external_knowledge_api_id\": null, \"external_knowledge_api_name\": null, \"external_knowledge_api_endpoint\": null}, \"external_retrieval_model\": {\"top_k\": 2, \"score_threshold\": 0.0, \"score_threshold_enabled\": null}, \"doc_metadata\": [], \"built_in_field_enabled\": false, \"partial_member_list\": []}\n",
	"info": "Edit DB successful!",
	"status_code": 0
}

import json

# demo_data = json.loads(demo_json['data'])
demo_json_str = json_str = json.dumps({"dataset_id": "ca2c2d3e-5131-4287-ba0b-a12547dbec1b"})
a = 1



# demo = {
# 	"indexing_technique":"high_quality",
# 	"process_rule":{
# 		"rules":{
#             "pre_processing_rules":  [{"id":"remove_extra_spaces","enabled":true},{"id":"remove_urls_emails","enabled":true}],
# 			"segmentation":  {"separator":"###","max_tokens":500}
#         },
# 		"mode":"custom"
# 	}
# }
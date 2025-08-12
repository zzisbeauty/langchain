"""
Blueprint 是一个“路由集合容器”
→ 定义了一个 Blueprint kbs_kernel
→ 所有数据库的核心操作如下（/kb/update、/kb/create）都添加到这个 kbs_kernel 中
→ 注册这个 kbs_kernel 到 app 上，相当于把所有接口一次性装上
"""

# 注册路由蓝图
from .health import health
from .kbs_kblist import kbs_kblist
from .kbs_kbdetail import kbs_kbdetail
from .kbs_kbcreate_update import kbs_kernel
from .kbs_kbrm import kbs_kbrm
from .kbs_ups import kbs_kbup
from .kbs_kbdoclist import kbs_kbdoclist
from .retrieval import retrieval
from .embeddings import emb_status

from .downfiles import downloadfiles

from .document_del import deldoc
from .document_start_stop import doc_toggle
from .models import model_select


from .conversation_with_kg import chat_kg
from .conversation_with_db_id import chat_db
from .conversation_with_nothing import chat_bp
from .conversation_history_id import chat_bp_history_with_convid

all_blueprints = [
    health,
    kbs_kblist,
    kbs_kbdetail,
    kbs_kernel,
    kbs_kbrm,
    kbs_kbup,
    kbs_kbdoclist,
    retrieval,
    emb_status,

    downloadfiles,
    deldoc,

    doc_toggle, # 文档启停， 对应 yjy change_status 控制文档状态
    model_select,

    chat_bp,
    chat_db,
    chat_kg,
    chat_bp_history_with_convid,
]

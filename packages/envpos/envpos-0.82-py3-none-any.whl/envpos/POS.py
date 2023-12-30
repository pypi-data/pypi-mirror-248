from .models import *
from .visualizers import *
from .files import FileConfig
from typing import *


class POS:
    LABEL_MAPPING = {
            "med":"环境介质",
            "phe":"环境现象",
            "pol":"污染物",
            "microbe":"微生物",
            "plant":"植物",
            "animal":"动物",
            "desease":"疾病",
            "hy":"行业",
            "group":"群体",
            "act":"政策行动",
            "policy":"政策要求",
            "b":"抽象属性",
            "env":"其他专业术语",
            "time":"时间",
            "loc":"地点",
            "per":"人名",
            "com":"公司名",
            "org":"组织名",
            "gov":"政府部门",
            "doc":"文档名",
            "event":"事件名",
            "pro":"设施/项目名",
            "ins":"工具名",
            "means":"方法名",
            "meet":"会议名",
            "code":"编码",
            "n":"名词",
            "v":"动词",
            "a":"形容词",
            "d":"副词",
            "vn":"动名词",
            "f":"方位词",
            "p":"介词",
            "r":"代词",
            "m":"数词",
            "q":"量词",
            "conj":"连词",
            "w":"标点",
            "u":"助词",
            "xc":"虚词",
        }

    ENTITY_LABLES = ['time', 'loc', 'per', 'com', 'org', 'gov','doc','event','pro','ins','means','meet','code']
    TERM_LABELS = ['med','phe','pol','microbe','plant','animal','desease','hy','group','act','policy','b','env']
    POS_LABELS = ['n','v','a','d','vn','f','p','r','m','q','conj','w','u','xc']
    KEYWORDS_LABEL = ["med","phe","pol","microbe","plant","animal","desease","hy","group","act","policy","b","env","per","com","org","gov","doc","event","pro","ins","means","meet"]


    def __init__(self):
        self.file_config = FileConfig()
        self.model = AlbertNER(self.file_config.pos_albert)
        self.ddp_vizer = DependencyVisualizer()

    def change_bert(self,path = None):
        if path is None:
            path = "celtics1863/pos-bert"
        
        self.model = BertNER(path)
        
    def use_cuda(self):
        self.model.set_device("cuda")


    def extract_keywords(self, 
            text:Union[str, List[str]],
            label_class = 'entity',
            auto_group=True, 
            batch_size = 16,
            **kwargs):
        '''
        抽取关键词
            str 或者 List[str]
                对str，返回Tuple(words, pos)
                对List[str]，返回[List[Tuple(words, pos )]
            
            label_class: 'entity','word','

            auto_group: 是否使用自动聚合，在大量文本时可以加速推理，但是会对内存造成一定负担

            batch_size：推理的批大小，在显存和内存支持的情况下，越大越好

        '''
        if label_class == 'entity':
            label_class = self.ENTITY_LABLES
        elif label_class == 'term':
            label_class = self.TERM_LABELS
        elif label_class == 'POS':
            label_class = self.POS_LABELS
        elif label_class == 'keyword':
            label_class = self.KEYWORDS_LABEL
        else:
            assert isinstance(label_class, (tuple,list,set)), "`label_class` 这个参数 要么是一系列标签，要么是`entity`，`POS`，`keyword`中的一个"

        result = self.model(text, 
                            print_result=False,
                            auto_group=auto_group,
                            batch_size=batch_size,
                            **kwargs)

        keywords = []
        for res in result:
            local_keywords = []
            for w,p in zip(*res):
                if p in label_class:
                    local_keywords.append(w)
            keywords.append(local_keywords)

        if isinstance(text, str):
            return keywords[0]
        else:
            return keywords

    def cut(self,
            text:Union[str, List[str]],
            auto_group=True, 
            batch_size = 16,
            **kwargs):
        '''
        str 或者 List[str]
            对str，返回Tuple(words, pos)
            对List[str]，返回[List[Tuple(words, pos )]
        
        auto_group: 是否使用自动聚合，在大量文本时可以加速推理，但是会对内存造成一定负担

        batch_size：推理的批大小，在显存和内存支持的情况下，越大越好
        '''
        result = self.model(text, 
                            print_result=False,
                            auto_group=auto_group,
                            batch_size=batch_size,
                            **kwargs)

        if isinstance(text, str):
            return result[0]
        else:
            return result

    def viz(self,text : str):
        return self.model(text, print_result=True, return_result= False)


    def generate_html(self,s : str):
        '''
        可视化生成html
        '''
        words,poses = self.cut(s)
        return self.model.visualizer.generate_html(words, poses)

    def _init_ddp(self):
        if hasattr(self,"ddp"):
            return True
        else:
            try:
                from ddparser import DDParser
            except:
                assert 0,"请安装ddparser，使用命令：pip install paddlepaddle==2.3.2 LAC ddparser"
            self.ddp = DDParser(use_pos=True)
    
    def dp_viz(self,s:str,save_path = "ddp.html"):
        '''
        可视化depencency visualizer
        '''
        self._init_ddp()
        
        words,poses = self.cut(s)
        
        res = self.ddp.parse_seg([words])[0]
        
        words = [{"word":w,"text":w, "tag":p}  for w,p in zip (words, poses)]

        words = [{"word":"HEAD","text":"HEAD","tag":"HEAD"}] + words

        id2words = {idx:word["word"] for idx,word in enumerate(words)}

        arcs = [
            {
                "start" : min(idx + 1,head),
                "end": max(idx + 1,head),
                "dir" : True if idx < head else False,
                "label": label
            }
            for idx,(head,label) in enumerate(zip(res["head"],res["deprel"]))
        ]
        
        self.ddp_vizer.render(0,words,arcs,save_path=save_path)

    
    def dp_cut(self,s):
        '''
        s: str or List(str)
        '''
        self._init_ddp()
        
        result = self.cut(s)
        if isinstance(s,str):
            result = [result]
            
        words = [w for w,p in result]
        poses = [p for w,p in result]
        
        ddp_result = self.ddp.parse_seg(words)
        
        for i in range(len(ddp_result)):
            ddp_result[i]["pos"] = poses[i]
        
        return ddp_result
    
    @property
    def labels(self):
        return self.LABEL_MAPPING

    @property
    def labels_entities(self):
        return [self.LABEL_MAPPING.get(e,"") for e in self.ENTITY_LABLES]
    
    @property
    def labels_term(self):
        return [self.LABEL_MAPPING.get(e,"") for e in self.TERM_LABELS]

    @property
    def labels_pos(self):
        return [self.LABEL_MAPPING.get(e,"") for e in self.POS_LABELS]

    @property
    def labels_zh(self):
        return list(self.LABEL_MAPPING.values())

    @property
    def labels_en(self):
        return list(self.LABEL_MAPPING.keys())

    

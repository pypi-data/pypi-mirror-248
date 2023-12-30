from .POS import POS
from .wordcloud import WordCloud

import warnings
warnings.filterwarnings("ignore", message=".*FutureWarning:.*")

        
        
pos = POS()
cut = pos.cut
generate_html = pos.generate_html
change_bert = pos.change_bert
extract_keywords = pos.extract_keywords
use_cuda = pos.use_cuda
viz = pos.viz
dp_cut = pos.dp_cut
dp_viz = pos.dp_viz
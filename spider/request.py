import requests
from lxml import etree
import pandas as pd
import pymysql
import urllib.parse
url = "https://api.github.com/repos/arbenson/FGDnPVC?client_id=a26c83afeb1a41304d10&client_secret=ea8586a6b1d16c9f645112fd04b5bf57f5bae88e"
addr = '/root/deepmp/spider/links-between-papers-and-code.json'
auth = "?client_id=a26c83afeb1a41304d10&client_secret=ea8586a6b1d16c9f645112fd04b5bf57f5bae88e"
df = pd.read_json(addr)
#df.drop_duplicates(subset=["paper_title"], keep="first", inplace=True)
urls = []
for i in range(len(df)):
    title = df["paper_title"][i]
    urls.append('https://paperswithcode.com/search?q='+urllib.parse.quote(title))

def null_arxiv(arxiv_id):
    if arxiv_id == None:
        return ""
    else: return arxiv_id

def get_pretrained_model(readme):
    if ".pth" in readme:
        return True
    elif "pre_trained" in readme:
        return True
    elif "pretrained model" in readme:
        return True
    elif "pre-trained model" in readme:
        return True
    else: return False

def get_dataset(readme):
    if "dataset" in readme:
        pos = readme.index("dataset")
        try:
            return readme[pos-20:pos+20]
        except:
            return readme[pos:pos+7]
    else: return ""

db = pymysql.connect(host='localhost', user='root', password='975481DING!', db='deepmp')
cursor = db.cursor()
#cursor.execute('''drop table if exists paperswithcode''')
#cursor.execute('''drop table if exists github''')
#cursor.execute('''drop table if exists semantic''')
sql_create1 = '''create table if not exists paperswithcode
		         (id int,
                 arxiv_id varchar(32),
                 paper_title varchar(256),
   		         paper_abstract text,
                 tags text,
                 primary key(id, arxiv_id))'''
sql_create2 = '''create table if not exists github
		         (id int not null auto_increment,
                 paper_title varchar(256),
                 address varchar(256),
                 frame varchar(16),
		         readme longtext,
  		         description text,
		         clone_url varchar(256),
		         home_page varchar(256),
		         size int,
                 star int,
                 fork int,
  		         watch int,
		         language varchar(32),
		         has_issues int,
		         has_projects int,
		         open_issues int,
		         has_downloads int,
		         has_wiki int,
		         archived int,
		         disabled int,
                 created_at varchar(32),
                 updated_at varchar(32),
                 dataset varchar(256),
                 pretrained_model int,
                 primary key(id, paper_title, address))'''
sql_create3 = '''create table if not exists semantic
                 (id int not null auto_increment,
                 arxiv_id varchar(32),
                 paper_title varchar(256),
                 paper_abstract text,
                 authors text,
                 citationVelocity varchar(32),
                 citations_arxiv_id text,
                 citations int,
                 references_arxiv_id text,
                 venue varchar(256),
                 year int,
                 topic text,
                 influence int,
                 fields varchar(256),
                 primary key(id, arxiv_id, paper_title))'''
cursor.execute(sql_create1)
cursor.execute(sql_create2)
cursor.execute(sql_create3)
db.commit()
print(len(df))
for i in range(23404, len(df)):
    print(i)
    r = requests.get(urls[i])
    paperswithcode = {}
    github = {}
    paperswithcode["paper_title"] = df["paper_title"][i]
    github[df["paper_title"][i]] = []
    text = r.text
    element = etree.HTML(text)
    try:
        detail_addr = "https://paperswithcode.com"+element.xpath('//div[@class="row"]/div/h1/a/@href')[0]
    except:
        continue
    r1 = requests.get(detail_addr)
    text = r1.text
    element = etree.HTML(text)
    abstract = element.xpath('//div[@class="paper-abstract"]/div/div/p/text()')
    _abstract = ""
    if abstract:
        _abstract = abstract[0].strip().replace('\n', ' ')
        hideabstract = element.xpath('//div[@class="paper-abstract"]/div/div/p/span/text()')
        if hideabstract:
            _abstract += hideabstract[0].strip().replace('\n', ' ')
    paperswithcode["paper_abstract"] = _abstract.replace("\"", "\'")
    # {"paper_title":[{"address":a,"frame":f,"star":s,"fork":f,"readme":r,"creat":c,"size":s,""}]
    code_infos = element.xpath('//div[@id="id_paper_implementations_collapsed"]/div')
    for code_info in code_infos:
        tmp_dic = {"address":"", "frame":""}
        repo_addr = code_info.xpath('div[@class="col-md-7"]/div/a/@href')
        if repo_addr:
            tmp_dic["address"] = repo_addr[0]
        frame = code_info.xpath('div[@class="col-md-2"]/div/img/@src')
        if frame:
            tmp_dic["frame"] = frame[0].replace('/static/frameworks/', '').replace('.png', '').replace('py', '')
        github[df["paper_title"][i]].append(tmp_dic)
    paperswithcode["tags"] = []
    tags = element.xpath('//div[@class="paper-tasks"]/div/div/ul/li/a/@href')
    for tag in tags:
        tag = tag.replace('/task/', '').replace('-', ' ')
        paperswithcode["tags"].append(tag)
    papers_data = [i, df["paper_arxiv_id"][i], paperswithcode["paper_title"], paperswithcode["paper_abstract"], ','.join(paperswithcode["tags"])]
    papers_data = list(map(str, papers_data))
    insert_paperswithcode_sql = '''insert into paperswithcode values(%s, %s, %s, %s, %s)'''
    cursor.execute(insert_paperswithcode_sql, papers_data)
    db.commit()
    for git_info in github[df["paper_title"][i]]:
        _git_addr = git_info["address"]
        if _git_addr:
            _git_url1 = _git_addr.replace('github.com', 'api.github.com/repos') + auth
            _git_url2 = _git_addr.replace('github', 'raw.githubusercontent') + '/master/README.md' + auth
            r1 = requests.get(_git_url1)
            r2 = requests.get(_git_url2)
            text1 = r1.text
            text2 = r2.text
            data = r1.json()
            git_info["readme"] = text2
            git_info["description"] = data.get("description", " ")
            git_info["clone_url"] = data.get("clone_url", "")
            git_info["home_page"] = data.get("homepage", "")
            if git_info["home_page"] == None:
                git_info["home_page"] = ""
            git_info["size"] = data.get("size", 0)
            git_info["star"] = data.get("watchers", 0)
            git_info["fork"] = data.get("forks", 0)
            git_info["watch"] = data.get("subscribers_count", 0)
            git_info["language"] = data.get("language", "")
            git_info["has_issues"] = int(data.get("has_issues", 0))
            git_info["has_projects"] = int(data.get("has_projects", 0))
            git_info["open_issues"] = data.get("open_issues", 0)
            git_info["has_downloads"] = int(data.get("has_downloads", 0))
            git_info["has_wiki"] = int(data.get("has_wiki", 0))
            git_info["archived"] = int(data.get("archived", 0))
            git_info["disabled"] = int(data.get("disabled", 0))
            git_info["created_at"] = data.get("created_at", 0)
            git_info["updated_at"] = data.get("updated_at", 0)
            git_info["dataset"] = get_dataset(text2)
            git_info["pretrained_model"] = int(get_pretrained_model(text2))
            for key, value in git_info.items():
                if value == None:
                    git_info[key] = ""
            data = [df["paper_title"][i], git_info["address"], git_info["frame"], git_info["readme"],
                    git_info["description"], git_info["clone_url"], git_info["home_page"], git_info["size"],
               	    git_info["star"], git_info["fork"], git_info["watch"], git_info["language"],
                    git_info["has_issues"], git_info["has_projects"], git_info["open_issues"], git_info["has_downloads"],
                    git_info["has_wiki"], git_info["archived"], git_info["disabled"], git_info["created_at"],
                    git_info["updated_at"], git_info["dataset"], git_info["pretrained_model"], ""]
            data_0 = list(map(str, data))
            insert_git = '''insert into github values(default, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(insert_git, data_0)
    if df["paper_arxiv_id"][i]:
        semantic_url1 = "https://api.semanticscholar.org/v1/paper/arXiv:" + df["paper_arxiv_id"][i]
        r3 = requests.get(semantic_url1)
        try:
            data = r3.json()
            semantic_data = {}
            semantic_data["arxiv_id"] = df["paper_arxiv_id"][i]
            semantic_data["paper_title"] = data.get("title", "")
            semantic_data["paper_abstract"] = data.get("abstract", "")
            semantic_data["authors"] = ",".join([author["name"] for author in data["authors"]])
            semantic_data["citationVelocity"] = data.get("citationVelocity", "")
            semantic_data["citations_arxiv_id"] = ",".join([null_arxiv(citation["arxivId"]) for citation in data["citations"]])
            semantic_data["citations"] = len(data["citations"])
            semantic_data["references_arxiv_id"] = ",".join([null_arxiv(reference["arxivId"]) for reference in data["references"]])
            semantic_data["venue"] = data.get("venue", "")
            semantic_data["year"] = data.get("year", "")
            semantic_data["topic"] = ",".join([topic["topic"] for topic in data["topics"]])
            semantic_data["influence"] = data.get("influentialCitationCount", "")
            semantic_data["fields"] = data.get("fieldsOfStudy", "")
            #semantic_data["paper_img"] = data
            #semantic_url2 = "https://www.semanticscholar.org/search?q=" + urllib.parse.quote(semantic_data["paper_title"])
            #r4 = requests.get(semantic_url2)
            #element = etree.HTML(r4.text)
            #semantic_url3 = element.xpath('//div[@class="result-page"]/arti')
            #semantic_data["paper_img"] = element.xpath('//ul[@class="flex-row paper-detail-figures-list"]/li/a/@href')
            data = [semantic_data["arxiv_id"], semantic_data["paper_title"], semantic_data["paper_abstract"], semantic_data["authors"],
                    semantic_data["citationVelocity"], semantic_data["citations_arxiv_id"], semantic_data["citations"], semantic_data["references_arxiv_id"],
                    semantic_data["venue"], semantic_data["year"], semantic_data["topic"], semantic_data["influence"], semantic_data["fields"]]
            data = list(map(str, data))
            insert_semantic = '''insert into semantic values(default, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(insert_semantic, data)
        except:
            pass
        db.commit()


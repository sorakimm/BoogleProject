#-*- coding:cp949
from django.shortcuts import render
from Searcher import c_searcher
from django.http import HttpResponse
import math
#for template
from django.template import Context, loader

listSize = 10
showLength = 100

# Create your views here.
def main_page(request):
    return render(request, 'search/main_page.html', {})


def SearchPage(req, mode, keyword, page=1): # req : request
    global listSize
    page = int(page)
    #print (page)
    print ("SearchPage - mode : ", mode)
    print ("SearchPage - keyword : ", keyword)
    print ("SearchPage - page : ", page)
    
    resultTup = callSearch(mode, keyword, page)
    print ("resultTup : ", resultTup)
    #pageCnt = int(resultTup[0]/10+1)
    pageCnt = 15
    print ("pageCnt : ", pageCnt)
    
    showItemTup = tuple(resultTup[1])
    #pageSeq = int((page-1)%10+1)
    firstPage = int(math.floor(page*0.1)*10+1)
    #startPage = int(math.floor(page, -1)+1)
    if(pageCnt - firstPage > 10):
        lastPage = firstPage + 9
    else:
        lastPage = pageCnt

    nextPage = lastPage + 1
    prevPage = firstPage -1
    print("firstPage :", firstPage)
    print("lastPage : ", lastPage)
    print("page :", page)
    pageList = range(firstPage, lastPage+1)
    print("pageList : ", pageList)
    if mode != 'allsearch':
        searchList = matchContentData(mode, keyword, showItemTup) # 페이지에 표시할 데이터 생성
        if mode == 'smisearch':
            tpl = loader.get_template('search/sub_search.html')
        elif mode == 'dictsearch':
            tpl = loader.get_template('search/dict_search.html') # 템플릿 로딩
        elif mode == 'websearch':
            tpl = loader.get_template('search/web_search.html') # 템플릿 로딩
        
        ctx = Context({
            'searchList' : searchList, # 변수값 채우기
            'keyword' : keyword,
            'mode' : mode,
            'page' : page,
            'firstPage' : firstPage,
            'lastPage' : lastPage,
            'prevPage' : prevPage,
            'nextPage' : nextPage,
            'pageList' : pageList,
            })

        html = tpl.render(ctx)
        return HttpResponse(html)

    elif mode == 'allsearch':
        web_resultTup = (showItemTup[0], showItemTup[1], showItemTup[2])
        dict_resultTup = (showItemTup[3], showItemTup[4], showItemTup[5])
        smi_resultTup = (showItemTup[6], showItemTup[7], showItemTup[8])
        
        web_searchList = matchContentData('websearch', keyword, web_resultTup)
        dict_searchList = matchContentData('dictsearch', keyword, dict_resultTup)
        smi_searchList = matchContentData('smisearch', keyword, smi_resultTup)
        
        tpl = loader.get_template('search/all_search.html') # 템플릿 로딩
        ctx = Context({
            'web_searchList' : web_searchList, # 변수값 채우기
            'dict_searchList' : dict_searchList, # 변수값 채우기
            'smi_searchList' : smi_searchList, # 변수값 채우기
            'keyword' : keyword,
            'mode' : mode,
            })

        print('web_searchList : ', web_searchList)
        print('dict_searchList : ', dict_searchList)
        print('smi_searchList : ', smi_searchList)
       
        html = tpl.render(ctx)
        return HttpResponse(html)

def callSearch(mode, keyword, page):
    print("callSearch - mode : ", mode)
    print("callSearch - keyword : ", keyword)
    print("callSearch - page : ", page)
    
    searcher = c_searcher(mode, keyword, page)
    if mode == "allsearch":
        print("callSearch - mode:allsearch")
        searchTup = searcher.AllSearcher()
        print(searchTup)
    elif mode == "websearch":
        searchTup = searcher.WebSearcher()
    elif mode == "dictsearch":
        searchTup = searcher.DictSearcher()
    elif mode == "smisearch":
        searchTup = searcher.SubSearcher()

    
    return searchTup

def matchContentData(mode, keyword, listTup):
    #"템플릿에 사용될 데이터 생성 "
    ResultData = []
    
    if(mode == "allsearch"):
        print ("allsearch listTup : ", listTup)
        for i in range(0, 6):
            conTitle = listTup[i][0].replace(listTup[i][0], "<b>" +listTup[i][0] + "</b>")
            conPreview = makeContentPreview(keyword, listTup[i][1])
            conLink = listTup[i][2]
            ResultData.append(({'preview':conPreview, 'link':conLink, 'title':conTitle}))
           
        for i in range(6, len(listTup)):
            conTitle = listTup[i][0].replace(listTup[i][0], "<b>" + listTup[i][0] + "</b>")
            conEng = listTup[i][1]
            conKor = listTup[i][2]
            ResultData.append(({'title':conTitle, 'eng':conEng, 'kor':conKor}))
        


    if(mode == "websearch"):
        for item in listTup:
            conTitle = item[0].replace(keyword, "<b>" + keyword + "</b>")
            conPreview = makeContentPreview(keyword, item[2])
            conLink = item[1]
            ResultData.append(({'preview':conPreview, 'link':conLink, 'title':conTitle}))

   
    elif(mode == "dictsearch"):
        for item in listTup:
            conTitle = item[0].replace(keyword, "<b>" + keyword + "</b>")
            conPreview = makeContentPreview(keyword, item[2])
            conLink = item[1]
            ResultData.append(({'preview':conPreview, 'link':conLink, 'title':conTitle}))


    elif(mode == "smisearch"):
        for item in listTup:
            conTitle = item[0].replace(item[0], "<b>" + item[0] + "</b>")
            conEng = item[1]
            conKor = item[2]
            ResultData.append(({'title':conTitle, 'eng':conEng, 'kor':conKor}))
       
    
    print ("ResultData : ", ResultData) 
    return ResultData

def makeContentPreview(keyword, text):
    global showLength
    contData = text
    #contData = contData.decode('utf-8')
    #strTitle = contData.readline()
    pos = contData.find(keyword)

    PreviewData = ""
    if pos > (showLength/2):
        PreviewData = contData[pos - (showLength / 2) : pos + (showLength / 2)]
    else:
        PreviewData = contData[0:showLength]

    if len(PreviewData) <= 0:
        PreviewData = "empty contents"
    
    # 데이터에서 키워드에 해당하는 곳 불드체로 표시
    #strTitle = strTitle.replace(keyword, "<b>" + keyword + "</b>")
    PreviewData = PreviewData.replace(keyword, "<b>" + keyword + "</b>")

    return PreviewData

def makeTitle(title):
    strTitle = title
    strTitle = strTitle.replace(keyword, "<b>" + keyword + "</b>")
    return strTitle

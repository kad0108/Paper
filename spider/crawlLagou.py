#!/usr/bin/env python
# -*- coding: utf-8 -*-



from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys  
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time  
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base64 import b64encode        
import sys

reload(sys)
sys.setdefaultencoding('utf8')
# print sys.getfilesystemencoding()

# 常量：
encodeName = "gb18030"
CompanyNameSelector = ".company_main > h1 > a"
CompanyBasicInfoSelector = '#basic_container ul > li'
CompanyIntroSelector = ".company_intro_text"
CompanyIntroHasExpandSelector = ".company_intro_text .company_content"
CompanyNavsSelector = '#company_navs li'
ExpandOrFoldSelector = ".text_over"

Page404Selector = ".page404"
PageStillConstructionSelector = ".incomplete_tips"
Page404Name = "page404"
PageStillConstructionName = "still_construction"

MaxWaitTime = 10


class OrEC:
    """ Use with WebDriverWait to combine expected_conditions
        in an OR.
    """
    # callBackIndex 是一个对int的wrapper 对象
    def __init__(self, indexWrapper, *args):
        self.indexWrapper = indexWrapper
        self.ecs = args
    def __call__(self, driver):
        for i in xrange(len(self.ecs)):
            fn = self.ecs[i]
            ans = None
            try:
                ans = fn(driver)
            except:
                pass
            if ans:
                self.indexWrapper.value = i
                return ans
        return None

class AndEC:
    """ Use with WebDriverWait to combine expected_conditions
        in an AND.
    """
    def __init__(self, *args):
        self.ecs = args
    def __call__(self, driver):
        resTuple = ()
        for fn in self.ecs:
            ans = None
            try:
                ans = fn(driver)
            except:
                ans = None
            if bool(ans) == False:                
                return ()
            resTuple += (ans,)
        return resTuple


def getChromeBrowser():
    myProxy= 'proxy.abuyun.com:9020'
    option = webdriver.ChromeOptions()
    option.add_argument('--user-data-dir=C:\Users\LZ\AppData\Local\Google\Chrome\User Data\Default') #设置成用户自己的数据目录
    option.add_argument('--proxy-server=%s' % myProxy)
    browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=option)
    return browser

import localData
def getFirefoxBrowser():
    proxy = {'host': "proxy.abuyun.com", 'port': 9020, 'usr': "HWJB1R49VGL78Q3D", 'pwd': "0C29FFF1CB8308C4"}

    # userProfileFilePath = r"C:\Users\LZ\AppData\Roaming\Mozilla\Firefox\Profiles\vbqy66hj.default"
    # kadUserProfileFilePath = r"C:\Users\zml\AppData\Roaming\Mozilla\Firefox\Profiles\lotur5zd.default"
    fp = webdriver.FirefoxProfile(localData.FirefoxUserProfileFilePath)

    fp.add_extension('resource/closeproxy.xpi')

    fp.set_preference('network.proxy.type', 1)
    fp.set_preference('network.proxy.http', proxy['host'])
    fp.set_preference('network.proxy.http_port', int(proxy['port']))
    fp.set_preference('network.proxy.ssl', proxy['host'])
    fp.set_preference('network.proxy.ssl_port', int(proxy['port']))
    fp.set_preference('network.proxy.ftp', proxy['host'])
    fp.set_preference('network.proxy.ftp_port', int(proxy['port']))       
    fp.set_preference('network.proxy.no_proxies_on', 'localhost, 127.0.0.1')



# 禁止浏览器访问图片信息
    fp.set_preference('permissions.default.image', 2)

    credentials = '{usr}:{pwd}'.format(**proxy)
    credentials = b64encode(credentials.encode('ascii')).decode('utf-8')
    fp.set_preference('extensions.closeproxyauth.authtoken', credentials)
    browser = webdriver.Firefox(executable_path="resource/geckodriver", firefox_profile=fp)
    # browser = webdriver.Firefox(executable_path="geckodriver")

    browser.set_page_load_timeout(1)
    return browser

def getCompanyInfoUrl(cid):
    return "https://www.lagou.com/gongsi/" + str(cid) + ".html"

HtmlParser = "html.parser"

Without_establishing_a_connection = "without establishing a connection"
This_browserForTab_is_undefined = "this.browserForTab is undefined"
Failed_to_decode_response_from_marionette = "Failed to decode response from marionette"

# browser = None # 全局浏览器


class Wrapper:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(value)
    # def value():
    #     return self.value



def restartBrowser(browserWrapper):
    # global browser
    try:
        browserWrapper.value.quit()
    except Exception, e:                    
        print "when browser quit, some exception occurs:", e, "| just pass it"
    browserWrapper.value = getFirefoxBrowser()
    print "restart a new firefox browser"

# 封装函数，等待函数执行确实执行完毕，或者超出了时间上限
# 如果返回true表示执行成功，false表示超出时间上限
# fun是一个函数，参数为空，
def waitFunctionFinish(fun, maxWaitTime = MaxWaitTime, sleepSeconds = 1):
    for i in xrange(maxWaitTime):
        result = None
        try:
            result = fun()
        except Exception, e:
            pass
        if result:
            return result
        else:
            time.sleep(sleepSeconds)
    print "waitFunctionFinish: time excceed"
    return None

def checkNeedRestartBrowserException(exception):
    e = str(exception)
    if e.find(Without_establishing_a_connection) != -1 or\
       e.find(This_browserForTab_is_undefined) != -1 or \
       e.find(Failed_to_decode_response_from_marionette) != -1: # need 重启firefox
        return True
    else:
        return False

#如果click成功，返回True，否则False        
def ensureClickSuccessfully(browserWrapper, locator, checkSuccessfulAfterClick, maxWaitTime = 2, sleepSeconds = 0.4):    
    try:
        browserWrapper.value.find_element_by_css_selector(locator).click()
    except Exception, e:
        print "ensureClickSuccessfully exception occurs: ", e
        return False

    waitResult = waitFunctionFinish(checkSuccessfulAfterClick, maxWaitTime = maxWaitTime, sleepSeconds = sleepSeconds)
    if waitResult:
        return True
    else:
        return False

#如果url load 成功，返回True，否则False
def ensureLoadPageSuccessfully(browserWrapper, url, expectedConditions):
    try:
        browserWrapper.value.get(url)
        print u"browser.get end-----"
    except Exception, e:
        print "ensureLoadPageSuccessfully exception occurs : ", e
        if checkNeedRestartBrowserException(e):
            restartBrowser(browserWrapper)
            return False

    try:
        element = WebDriverWait(browserWrapper.value, 10).until(expectedConditions)
    except Exception, e:   
        print "Error in wait page element load finish: ", e
        return False
    return True

def getEmptyCompanyInfo(url):
    answer = {
        "cid":-1, 
        "name":"", 
        "content":"", 
        "tag":"", 
        "process":"", 
        "total":0, 
        "url": url,
        "salary":[],
    }
    return answer

def _getCompanyInfo(cid, browserWrapper):
    # global browser
    print '\n'*4+'getting company info:'+ str(cid)+ "-"*100
    url = getCompanyInfoUrl(cid)
    answer = getEmptyCompanyInfo(url)
    

    ansIndex = Wrapper(-1)
    hasRealDataEC = AndEC(EC.presence_of_element_located((By.CSS_SELECTOR, CompanyNameSelector)),\
                        EC.presence_of_element_located((By.CSS_SELECTOR, CompanyBasicInfoSelector)),\
                        EC.presence_of_element_located((By.CSS_SELECTOR, CompanyIntroSelector)))
    page404EC = EC.presence_of_element_located((By.CSS_SELECTOR, Page404Selector))
    pageStillConstructionEC = EC.presence_of_element_located((By.CSS_SELECTOR, PageStillConstructionSelector))
    allEC = OrEC(ansIndex, hasRealDataEC, page404EC, pageStillConstructionEC)        

    waitResult = waitFunctionFinish(lambda: ensureLoadPageSuccessfully(browserWrapper, url, allEC))
    if bool(waitResult) == False:
        return answer

    if ansIndex.value == 0:
        pass    
    elif ansIndex.value == 1:
        print Page404Name
        answer['cid'] = cid
        answer['name'] = Page404Name
        return answer        
    elif ansIndex.value == 2:
        print PageStillConstructionName
        answer['cid'] = cid
        answer['name'] = PageStillConstructionName
        return answer
    else:
        print u"Error ansIndex:", ansIndex
        return answer

    

    
    soup = BeautifulSoup(browserWrapper.value.page_source, HtmlParser)
    # 获取 公司简介内容content:
    content = ""
    if len(soup.select(ExpandOrFoldSelector)) == 0:
        content = soup.select(CompanyIntroSelector)[0].text
        print "no expand button"
    elif soup.select(ExpandOrFoldSelector)[0].attrs.has_key("style") and\
         soup.select(ExpandOrFoldSelector)[0].attrs["style"].find("none") != -1:
        content = soup.select(CompanyIntroHasExpandSelector)[0].text
        print "expand button must be hided "
        
    else :
        def checkExpandClickFinish():
            # global browser
            soup = BeautifulSoup(browserWrapper.value.page_source, HtmlParser)
            if soup.select(ExpandOrFoldSelector)[0].text == u'收起':
                return True
            else:
                print u"not found expand button"
                return False

        waitResult = waitFunctionFinish(lambda : ensureClickSuccessfully(browserWrapper, ExpandOrFoldSelector, checkExpandClickFinish), 20, 1)
        soup = BeautifulSoup(browserWrapper.value.page_source, HtmlParser)
        if waitResult:
            content = soup.select(CompanyIntroHasExpandSelector)[0].text
        else:
            print u'expand the company intro info not successful'
            content = soup.select(CompanyIntroSelector)[0].text


    content = content.encode(encodeName, "ignore")
    total = int(filter(unicode.isdigit, soup.select(CompanyNavsSelector)[1].text))
    name = soup.select(CompanyNameSelector)[0].text.strip()
    info = soup.select(CompanyBasicInfoSelector)
    tag = info[0].find('span').text.encode(encodeName, "ignore")
    process = info[1].find('span').text.encode(encodeName, "ignore")   


    print "company cid:", cid
    print "company name:", name
    print "company content:", content
    print "company tag:", tag
    print "company process:", process
    print "company total:", total

    answer['cid'] = cid
    answer['name'] = name
    answer['content'] = content
    answer['tag'] = tag
    answer['process'] = process
    answer['total'] = total
    return answer




globalBrowserWrapper = Wrapper(getFirefoxBrowser())
def getCompanyInfo(cid):

    
    answer = getEmptyCompanyInfo(getCompanyInfoUrl(cid))
    try:        
        answer = _getCompanyInfo(cid, globalBrowserWrapper)
    except Exception, e: # 当有任何Exception时候，直接pass
        print "Exception in getCompanyInfo", e

    time.sleep(2)
    return answer




def getCompanyJobsUrl(cid):
    return "https://www.lagou.com/gongsi/j" + str(cid) + ".html"

JobInfoSelector = ".con_list_item"
JobTotalNumberSelector = "#company_navs .current a"

def getJobTotalNumber(soup):    
    return int(filter(unicode.isdigit, soup.select(JobTotalNumberSelector)[0].text))

class CompanyJobsEC:
    """ 
    """    
    def __init__(self):
        pass
        
    def __call__(self, browser):        
        

        if EC.presence_of_element_located((By.CSS_SELECTOR, JobTotalNumberSelector))(browser):
            soup = BeautifulSoup(browser.page_source, HtmlParser)
            jobTotalNumber = getJobTotalNumber(soup)                        
            firstPageJobNumber = min(10, jobTotalNumber)
            if len(soup.select(JobInfoSelector)) == firstPageJobNumber:
                return True
        return False


DisapperedText = u"亲，你来晚了，该信息已经被删除鸟~"

def buildEmptyJobInfo():
    job = {
        'name': "",
        'salary':"",
    }
    return job

def getCompanyJobListInPage(soup):
    
    jobList = []
    for jobTag in soup.select(JobInfoSelector):
        job = buildEmptyJobInfo()
        job['name'] = jobTag.select("div a")[0].text.replace(" ", "").replace("\n", "").encode(encodeName, "ignore")
        job['salary'] = jobTag.select("p .item_salary")[0].text.replace(" ", "").replace("\n", "")
        print job['name'] , "|" , job['salary']
        jobList.append(job)
    return jobList

def getDefaultBeautifulSoup(browserWrapper):
    return BeautifulSoup(browserWrapper.value.page_source, HtmlParser)

'''
返回当前页面中.pages .current 的页码数，
如果找不到，则返回-1
'''
def getCurrentPageNumberInPage(browserWrapper):
    soup = BeautifulSoup(browserWrapper.value.page_source, HtmlParser)
    currentPageTagList = soup.select(".pages .current")
    if len(currentPageTagList) != 1: return -1

    return int(currentPageTagList[0].text)


def checkCompanyJobsClickFinish(browserWrapper, currentShouldPageNumber):

    return getCurrentPageNumberInPage(browserWrapper) >= currentShouldPageNumber

def _getCompanyJobsInfo(cid, browserWrapper):
    print '\n'*3 + "getCompanyJobsInfo: " + str(cid) + '-'*100
    url = getCompanyJobsUrl(cid)
    answer = []

    indexWrapper = Wrapper(-1)
    disapperTextEC = EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".content"),DisapperedText)
    page404EC = EC.presence_of_element_located((By.CSS_SELECTOR, Page404Selector))
    jobEC = OrEC(indexWrapper, CompanyJobsEC(), disapperTextEC,  page404EC)

    waitResult = waitFunctionFinish(lambda:ensureLoadPageSuccessfully(browserWrapper, url,  jobEC ), 10, 2)

    soup = BeautifulSoup(browserWrapper.value.page_source, HtmlParser)
    
    if waitResult == True:
        if indexWrapper.value == 0:            
            jobTotalNumber = getJobTotalNumber(soup)
            print "jobTotalNumber: " + str(jobTotalNumber)
            soup = BeautifulSoup(browserWrapper.value.page_source, HtmlParser)
            answer = getCompanyJobListInPage(soup)
        elif indexWrapper.value == 1:
            print "DisapperedText"
            return answer
        elif indexWrapper.value == 2:
            print "page404"
            return answer
        else:
            print "unknow"
            return answer
    else:
        print "error in waitFunctionFinish , ensureLoadPageSuccessfully"
        return answer

    totalPageNumber = jobTotalNumber / 10 
    if jobTotalNumber % 10 != 0: totalPageNumber += 1

    for currentPageNumber in xrange(2, totalPageNumber + 1):
        print "get page " + str(currentPageNumber) + '='*50
        currentPageNumberInPage = getCurrentPageNumberInPage(browserWrapper)
        if currentPageNumberInPage > currentPageNumber:
            print 'get page ' + str(currentPageNumber) + ' not successful'
            continue
        if currentPageNumberInPage == currentPageNumber:
            soup = getDefaultBeautifulSoup(browserWrapper)
            answer.extend(getCompanyJobListInPage(soup))
            continue

        waitResult = waitFunctionFinish(lambda:ensureClickSuccessfully(browserWrapper, ".next", \
            lambda : checkCompanyJobsClickFinish(browserWrapper, currentPageNumber), 10, 1), 10, 2)
        if waitResult and getCurrentPageNumberInPage(browserWrapper) == currentPageNumber:
            soup = getDefaultBeautifulSoup(browserWrapper)
            answer.extend(getCompanyJobListInPage(soup))
        else:
            print 'get page ' + str(currentPageNumber) + ' not successful'

    return answer


def getCompanyJobsInfo(cid):
    answer = []
    try:
        answer = _getCompanyJobsInfo(cid, globalBrowserWrapper)
    except Exception, e:
        print '_getCompanyJobsInfo exception occurs: ', e

    return answer

import json 



def getCompanyJobsInfoFromJsonUrl(cid, pageNo):
    return "https://www.lagou.com/gongsi/searchPosition.json?companyId="+str(cid)+"&pageNo="+str(pageNo)

def _getCompanyJobsInfoFromJsonInOnePage(cid, browserWrapper, pageNo):
    url = getCompanyJobsInfoFromJsonUrl(cid, pageNo)
    # try:
    #     browserWrapper.value.get(url)
    # except Exception, e:
    #     pass

    jobDataJsonEC = EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body"), "totalCount")
    waitResult = waitFunctionFinish(lambda:ensureLoadPageSuccessfully(browserWrapper, url,  jobDataJsonEC ), 10, 2)
    answer = []
    if waitResult:
        soup = getDefaultBeautifulSoup(browserWrapper)
        jsonDataString = soup.select("body")[0].text
        # print jsonDataString
        jsonData = json.loads(jsonDataString)
        jobDataList = jsonData['content']['data']['page']['result']

        for jobData in jobDataList:
            job = buildEmptyJobInfo()
            job['name'] = jobData['positionName']
            job['salary'] = jobData['salary']            
            answer.append(job)

        totalCount = int(jsonData['content']['data']['page']['totalCount'])
        print '\n' * 2 + 'getting company cid:' + str(cid) +' , page number:' + str(pageNo) + " has " + str(len(answer)) + " job info" + '='*30
        for job in answer:
            print job["name"], job['salary']
        return (answer, totalCount)
    else:
        print "get company jobs info list failed"
        return (answer, -1);


'''
每页最多countPerPage 个job，一共有totalCount个页
返回总共页数
'''
def calculateTotalPageNumberInJobPage(totalCount, countPerPage = 10):
    ans = totalCount / countPerPage
    if totalCount % countPerPage != 0:
        ans += 1
    return ans


def _getCompanyJobsInfoFromJson(cid):


    answer, totalCount = _getCompanyJobsInfoFromJsonInOnePage(cid, globalBrowserWrapper, 1)

    totalPageNumber = calculateTotalPageNumberInJobPage(totalCount)
    for i in xrange(2, totalPageNumber + 1):
        tmpAnswer, tmpTotalCount = _getCompanyJobsInfoFromJsonInOnePage(cid, globalBrowserWrapper, i)
        answer.extend(tmpAnswer)
        if tmpTotalCount != totalCount:
            print "error in page:" + str(i) + ", tmpTotalCount != totalCount"

    return answer

def getCompanyJobsInfoFromJson(cid):
    answer = []
    try:
        answer = _getCompanyJobsInfoFromJson(cid)
    except Exception, e:
        print "exception occurs in getCompanyJobsInfoFromJson, just pass it"
    return answer
            
    


if __name__ == '__main__':

    # browserWrapper = Wrapper(getFirefoxBrowser())
    for cid in range(34683, 134683 + 1):
        print '*'*150
        
        


        # continue
        companyInfoAnswer = getCompanyInfo(cid)
        # companyJobsAnswer = getCompanyJobsInfo(cid)

        companyJobsAnswer = getCompanyJobsInfoFromJson(cid)

        print "companyInfoAnswer:" + "-"*50
        print "companyInfoAnswer cid:", companyInfoAnswer['cid']
        print "companyInfoAnswer name:", companyInfoAnswer['name']
        print "companyInfoAnswer content:", companyInfoAnswer['content']
        print "companyInfoAnswer tag:", companyInfoAnswer['tag']
        print "companyInfoAnswer process:", companyInfoAnswer['process']
        print "companyInfoAnswer total:", companyInfoAnswer['total']
        print "companyInfoAnswer url:", companyInfoAnswer['url']
        print "companyInfoAnswer salary:", companyInfoAnswer['salary']

        print "companyJobsAnswer total:" , len(companyJobsAnswer)
        for item in companyJobsAnswer:
            print "companyJobsAnswer: " , item['name'], item['salary']





        # answer = getCompanyInfo(cid)
        # print "answer:" + "-"*50
        # print "answer cid:", answer['cid']
        # print "answer name:", answer['name']
        # print "answer content:", answer['content']
        # print "answer tag:", answer['tag']
        # print "answer process:", answer['process']
        # print "answer total:", answer['total']
        # print "answer url:", answer['url']
        # print "answer salary:", answer['salary']


    # try:        
    #     getCompanyInfo(cid, browser)
    # except Exception, e: # 当有任何Exception时候，直接pass
    #     print "Exception in getCompanyInfo", e
    # time.sleep(2)
# getPosition(cid, browser)
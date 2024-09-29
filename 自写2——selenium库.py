from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import 提取首字母 as ex
import parsel
import pandas as pd
import sys
import random as rd
import time
def modify_rel_attribute(driver,original_rel_tag, new_rel_value):
    ''''定义修正driver实例函数以确保连接有效'''
    try:
        try:
            driver.execute_script("arguments[0].setAttribute('rel', arguments[1]);", original_rel_tag, new_rel_value)
        except Exception as e:
            print(f"An error occurred: {e}")
    except Exception as e:
        if "invalid session id" in str(e):
            print("Session invalid, retrying...")
            modify_rel_attribute(original_rel_tag, new_rel_value)
        else:
            print(f"An unexpected error occurred: {e}")
# 启动 WebDriver 服务,以避免服务器无法响应请求的问题
service = Service(ChromeDriverManager().install())
#导入模块，构建驱动对象，可以设置成后台运行（无头浏览器），不设置是为了解决验证码的问题
driver = webdriver.Chrome(service=service)
#导航指定URL，打开该网页,并设置隐式等待
driver.implicitly_wait(10)
intended_city='福州'#input("选择一个城市：")
initials=ex.extract_initials(intended_city)
city_url=f'https://{initials}.zu.anjuke.com/'
driver.get(city_url)
'''with open('自写2DOM树.html','w',encoding='utf-8') as f:
    f.write(driver.page_source)'''
try:#登录安居客网站租房页面，并选择一个城市
    regions=driver.find_elements(By.CSS_SELECTOR,'body > div.w1170 > div.div-border.items-list > div:nth-child(1) > span.muti-row > div')
    region_name=[region.text for region in regions] 
    text_region=region_name[0]
    region_names=text_region.split()
    '''for i in region_names:
        print(i)'''
    #在城市基础上选择一个地区
    region_select='仓山'#input('选择一个地区 '+'，'.join(region_names)+':')
    region_selector=parsel.Selector(driver.page_source)    
    region_link=[i.get() for i in region_selector.css('body > div.w1170 > div.div-border.items-list > div:nth-child(1) > span.muti-row > div>a::attr(href)')]
    '''for item in region_link:
        print(item)'''
    region_url=region_link[region_names.index(region_select)]#css选择器没有根据文本内容直接选择标签的语法，因而将地区名和对应的链接名分别存储在列表中，通过索引实现地区与链接的相互引用
except Exception as e:#在selenium库中，xpath和css都不能提取到标签属性
    print("Error:",e)
    sys.exit()
finally:
    driver.quit()
    print("城市选择驱动器已关闭")
try:#跳转到特定地区页面，并在地区基础上选择一个租金范围
    driver_region=webdriver.Chrome(service=service)
    driver_region.implicitly_wait(10)
    driver_region.get(region_url)
    rentals=driver_region.find_elements(By.CSS_SELECTOR,'body > div.w1170 > div.div-border.items-list > div:nth-child(2) > span.muti-row > a')
    rental_range=[rental.text for rental in rentals]
    '''for money in rental_range:
        print(money)'''
    rental_select='1000-1500元'#input('选择一个租金范围 '+'，'.join(rental_range)+':')
    rental_selector=parsel.Selector(driver_region.page_source)
    rental_link=[i.get() for i in rental_selector.css('body > div.w1170 > div.div-border.items-list > div:nth-child(2) > span.muti-row > a::attr(href)') ]
    '''for i in rental_link:
        print(i)'''
    rental_url=rental_link[rental_range.index(rental_select)]
except Exception as e:
    print("Error:",e)
    sys.exit()
finally:
    driver_region.quit()
    print("地区选择驱动器已关闭")
try:#跳转到特定租金范围页面，并在此基础上选择一个房型
    driver_rental_last=webdriver.Chrome(service=service)
    driver_rental_last.implicitly_wait(10)
    driver_rental_last.get(rental_url)
    housetype=driver_rental_last.find_elements(By.CSS_SELECTOR,'body > div.w1170 > div.div-border.items-list > div:nth-child(3) > span.elems-l > a')
    housetype_choice=[i.text for i in housetype]
    '''for i in housetype_choice:
        print(i)'''
    housetype_select='一室'#input('选择一个房型 '+'，'.join(housetype_choice)+':')
    housetype_selector=parsel.Selector(driver_rental_last.page_source)
    housetype_button=driver_rental_last.find_element(By.XPATH,'/html/body/div[5]/div[2]/div[3]/span[2]/a[text()="一室"]')
    #print(housetype_button.get_attribute('href'))
    housetype_button.click()
    driver_rental_last.implicitly_wait(10)
    '''前两个链接均通过设定新的驱动器进行，此处直接利用selenium库中的元素交互功能'''
except Exception as e:
    print("Error:",e)
    sys.exit()
finally:
    print("已跳转至租赁类型页面")
try:#跳转到房型页面，并在此基础上选择租赁类型
    leasetype=driver_rental_last.find_elements(By.CSS_SELECTOR,'body > div.w1170 > div.div-border.items-list > div:nth-child(4) > span.elems-l > a')
    leasetype_choice=[i.text for i in leasetype]
    '''for i in leasetype_choice:
        print(i)'''
    leasetype_select='整租'#input('选择一种租赁方式'+'，'.join(leasetype_choice)+':')
    '''with open('自写22DOM树.html','w',encoding='utf-8') as f:
        f.write(driver_rental_last.page_source)'''
    leasetype_selector=parsel.Selector(driver_rental_last.page_source)
    original_rel_tags=driver_rental_last.find_elements(By.XPATH, '/html/body/div[5]/div[2]/div[4]/span[2]/a[@rel]')#爬取带有rel属性的标签并更改属性值nofollow
    new_rel_value='noopener noreferrer'
    for i in original_rel_tags:
        modify_rel_attribute(driver=driver_rental_last,original_rel_tag=i,new_rel_value=new_rel_value)
        #print(i.get_attribute('rel'))
    leasetype_button=driver_rental_last.find_element(By.XPATH,'/html/body/div[5]/div[2]/div[4]/span[2]/a[text()="整租"]')
    #print(leasetype_button.get_attribute('href'))
    leasetype_button.click()
    driver_rental_last.implicitly_wait(10)
except Exception as e:
    print("Error:",e)
    sys.exit()
finally:
    print("选择成功，正在跳转获取符合条件的房源数据……")
try:
    '''with open("自写DOM222树.html",'w',encoding='utf-8') as f:
        f.write(driver_rental_last.page_source)'''
    basic_information=[]
    rent_per_month=[]
    housing_resource_selector=parsel.Selector(driver_rental_last.page_source)
    housing_resource_datas={'房屋基本信息':None,
                            '租金（元/月）':None}
    page_number=1
    while True:
        print(f'正在爬取第{page_number}页的内容……')
        Flag_next_page=housing_resource_selector.css('body > div.w1170 > div.maincontent > div.page-content > div > a.aNxt')
        time.sleep(rd.randint(3,6))
        for i in range(3,38):
            basic_information_text=housing_resource_selector.css(f'#list-content > div:nth-child({i}) > div.zu-info > h3 > a > b::text').get()
            basic_information.append(basic_information_text)
            rent_per_month_text=housing_resource_selector.css(f'#list-content > div:nth-child({i}) > div.zu-side > strong::text').get()
            rent_per_month.append(rent_per_month_text)
        if len(Flag_next_page)!=0:
            page_number+=page_number+1
            driver_rental_last.get(f'https://fz.zu.anjuke.com/fangyuan/cangshan/zj204-fx1-x1-p{page_number}/')
            housing_resource_selector=parsel.Selector(driver_rental_last.page_source)
        else:
            break
    '''for i in basic_information:
        print(i,sep='')
    for i in rent_per_month:
        print(i)'''
    housing_resource_datas['房屋基本信息']=basic_information
    housing_resource_datas['租金（元/月）']=rent_per_month
    df = pd.DataFrame(housing_resource_datas)
    name=intended_city+region_select+rental_select+housetype_select+leasetype_select
    df.to_excel(f'{name}——房源收集表.xlsx',index=False, header=True)
    print("爬取完成，已生成Excel表格，文件名：",name)
except Exception as e:
    print("Error:",e)
    sys.exit()
finally:
    input("回车以关闭驱动器：")
    driver_rental_last.quit()
    print('over')



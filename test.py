from CloudflareBypasser import CloudflareBypasser
from DrissionPage import ChromiumPage, ChromiumOptions, SessionPage
import time
import json
import platform

if __name__ == '__main__':

    nh_conf = 'gallery-dl-nh-liwei782339_020501.conf'
    with open(nh_conf, 'r') as f:
        nh_conf_json = json.load(f)

    nh_headers_ua = nh_conf_json.get('extractor').get('nhentai').get('user-agent')
    sessionid = nh_conf_json.get('extractor').get('nhentai').get('cookies').get('sessionid')
    # Chromium Browser Path
    browser_path = "/usr/bin/google-chrome"
    #browser_path = "/root/flaresolverr/chrome/chrome"

    options = ChromiumOptions()
    options.set_paths(browser_path=browser_path)
    if platform.system() == 'Windows':
        print("系统是Windows")
        nh_headers_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/527.35'
        # Windows Example
        browser_path = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
    else:
        print("系统不是Windows")
        nh_headers_ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/527.35'
    options.set_user_agent(user_agent=nh_headers_ua)
    #options.set_proxy('http://127.0.0.1:1083')

    # Some arguments to make the browser better for automation and less detectable.
    arguments = [
        "--lang=en-US",
        "--accept-lang=en-GB", #设置网页英文语言
        "-no-first-run",
        "--no-sandbox",
        "--headless=new", #无头模式
        "-force-color-profile=srgb",
        "-metrics-recording-only",
        "-password-store=basic",
        "-use-mock-keychain",
        "-export-tagged-pdf",
        "-no-default-browser-check",
        "-disable-background-mode",
        "-enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions",
        "-disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage",
        "-deny-permission-prompts",
        "-disable-gpu",
    ]


    for argument in arguments:
        options.set_argument(argument)

    driver = ChromiumPage(addr_driver_opts=options)
    print(driver.user_agent)
    driver.set.cookies([{'name': 'sessionid', 'value': sessionid, 'domain': 'nhentai.net'}])

    driver.get('https://nhentai.net')

    # Where the bypass starts
    cf_bypasser = CloudflareBypasser(driver)
    cf_bypasser.bypass()

    print("Enjoy the content!")

    #print(driver.html) # You can extract the content of the page.
    print("Title of the page: ", driver.title)

    time.sleep(5)

    csrftoken, cf_clearance = False, False
    for i in driver.cookies(as_dict=False, all_domains=True):
        print(i)
        if 'csrftoken' == i.get('name') :
            csrftoken = i.get('value')
        if 'cf_clearance' == i.get('name') :
            cf_clearance = i.get('value')

    driver.user_agent = nh_headers_ua
    print(nh_headers_ua)
    print('----')

    if csrftoken :
        print(csrftoken)
        print(cf_clearance)

        nh_conf_json['extractor']['nhentai']['cookies']['csrftoken'] = csrftoken
        nh_conf_json['extractor']['nhentai']['cookies']['cf_clearance'] = cf_clearance
        nh_conf_json['extractor']['nhentai']['user-agent'] = nh_headers_ua

        print(nh_conf_json)

        with open(nh_conf, 'w', encoding='utf-8') as file:
            file.write(json.dumps(nh_conf_json, ensure_ascii=False, indent=4))

    driver.quit()

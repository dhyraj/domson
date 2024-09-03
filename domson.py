from bs4 import *
import requests
import json

class Domson:

    shredditApp = False

    def __init__(self, logTreeEnabled = False):
        self.logTreeEnabled = logTreeEnabled

    
    def parseElements(self, component: BeautifulSoup, tabs) -> dict:
        if self.logTreeEnabled: 
            with open("domElementsTree.txt","a+") as d:
                d.write(f'{" "*4*tabs} {component.name}\n')
        d = dict()
        try: 
            attributes = component.attrs
            if attributes != None and len(attributes)>0:
                d['attributes'] = attributes
        except Exception as e:
            print("error caught: ", e)

        try:
            for element in component.children:
                if element is not None and element.name is not None:
                    childDict = self.parseElements(element, tabs+1)
                    if childDict is not None:
                        if element.name not in d:
                            d[element.name] = childDict
                        else:
                            if not isinstance(d[element.name], list):
                                d[element.name] = list(d[element.name])
                            d[element.name].append(childDict)
        except Exception as e:
            print("another error caught: ", e)


        return (d if d is not {} else None)
            


    def toDict(self, html: str) -> dict:
        html = BeautifulSoup(html, "html.parser")
        finding = html.find("article")

        pathToArticle = []
        while finding.name!= 'html': 
            pathToArticle.append(finding.name)
            finding = finding.parent
        else:
            pathToArticle.append(finding.name)

        print(".".join(pathToArticle[::-1]))
        thisDict = self.parseElements(html,0)
        return thisDict
    
    def toJson(self, html: str) :
        d = self.toDict(html)
        return json.dumps(d)


if __name__ == "__main__":
    url = "https://www.reddit.com/r/AskReddit/"
    response = requests.get(url, verify= True)
    with open("dom.json","w+") as f:
        d = Domson(True).toJson(response.text)
        f.write(str(d))


    # print("response: ", d)
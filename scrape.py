# project: p3
# submitter: jnovoa
# partner: none
# hours: 12
import pandas as pd
import time
import requests
class Parent:
    def twice(self):
        self.message()
        self.message()
        
    def message(self):
        print("parent says hi")
        
class Child(Parent):
    def message(self):
        print("child says hi")
        
class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def visit_and_get_children(self, node):
        """ Record the node value in self.order, and return its children
        param: node
        return: children of the given node
        """
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        self.visited = set() 
        self.order = []
        self.dfs_visit(node)
        
    def dfs_visit(self, node):
        if node in self.visited:
            return
        self.visited.add(node)
        children = self.visit_and_get_children(node)
        for child in children:
            self.dfs_visit(child)
    
    def bfs_search(self, node):
        # check node
        self.visited = set() # nodes that have been visited
        self.order = []
        
        queueToCheck = [node] # what nodes need to be checked
        # check node
        while len(queueToCheck) > 0:
            c = queueToCheck.pop(0)
            if not c in self.visited:
                self.visited.add(c)
            children = self.visit_and_get_children(c) # this method adds c to order
            for child in children:
                if child not in self.visited and child not in queueToCheck:
                    queueToCheck.append(child)
                                                
class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__() # call constructor method of parent class
        self.df = df

    def visit_and_get_children(self, node):
        if not node in self.order:
            self.order.append(node)
        children = []
        for node, has_edge in self.df.loc[node].items():
            if has_edge == 1:
                children.append(node)
        return children

class FileSearcher(GraphSearcher):
    # the constructor of FileSearcher which does not take additional  parameter besides the instance itself   
    def __init__(self):
        self.order = []
        self.visited = set()
    # visit the file to record its value and get its children
    def visit_and_get_children(self, file):
        path = "file_nodes/" + file
        f = open(path)
        contents = f.read()
        f.close()
        listData = contents.split()
        Data = listData[0]
        children = listData[1].split(",") # list of children
        if Data not in self.order:
            self.order.append(Data)
        return children
    # concatenate the values in self.order to a string
    def concat_order(self):
        return ''.join(self.order)
    
class WebSearcher(GraphSearcher):
    def __init__(self, webDriver):
        self.webDriver = webDriver
        self.df = []
        self.table_fragments = []
        self.order = []
    # The visit_and_get_children method of WebSearcher should treat the node as a URL. It should use the webdriver to visit that page and return the URLs of other pages to which the visited page has hyperlinks. See web_test in the tester for examples of how it should behave.
    def visit_and_get_children(self, node):
        self.webDriver.get(node)
        if node not in self.order:
            self.order.append(node)
        children = []
        read = pd.read_html((self.webDriver.find_element("id", "locations-table")).get_attribute("outerHTML"))
        # self.webDriver.get_element("id","table")
        # if not read in self.table_fragments:
        self.table_fragments.append(read[0])
        for elem in self.webDriver.find_elements("tag name", "a"):
            # print(elem.text)
            child = elem.get_attribute("href")
            children.append(child)
            if child not in self.order:
                self.order.append(child)
        return children
    
    def table(self):
        df = pd.concat(self.table_fragments, ignore_index = True)
        df = df.drop_duplicates(ignore_index = True)
        return df
        
def reveal_secrets(driver, url, travellog):
    strings = [str(x) for x in list(travellog["clue"])]
    password = ''.join(strings)
    driver.get(url)
    textBox = driver.find_element("id", "password")
    Button = driver.find_element("id", "attempt-button")
    textBox.send_keys(password) # types into the box for us
    Button.click()
    time.sleep(.5)
    viewLocation = driver.find_element("id", "securityBtn")
    viewLocation.click()
    time.sleep(1)
    imageLink = driver.find_element("id", "image").get_attribute("src")
    x = requests.get(imageLink)
    with open("Current_Location.jpg", 'wb') as f: #https://www.w3schools.com/python/ref_requests_get.asp
        f.write(x.content)
    secretLocation = driver.find_element("id", "location").text
    return secretLocation
    

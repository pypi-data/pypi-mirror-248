import abc

class Factory(abc.ABC):
    def __init__(self, client, cls):
        self.client = client
        self.cls = cls
    
    @staticmethod
    def create(client, cls):
        k = cls.__name__
        factories = {"Project": ProjectFactory,
                     "ProjectInventory": ProjectInventoryFactory}
        factory = factories.get(k)
        return factory(client, cls)
    
    @abc.abstractmethod
    def all(self):
        pass

class ProjectFactory(Factory):
    #Note API endpoints switch between projects and project...
    def all(self):
        path = "projects"
        resp = self.client.request("GET", url_part=path)
        projects = []
        for project_data in resp.json()['data']:
            projects.append(self.cls.from_dict(project_data))
        return projects
    
    def get(self, id:str):
        path = f"projects/{id}"
        resp = self.client.request("GET", url_part=path)
        project_data = resp.json()
    
    def get_id(self, projectName:str):
        path = f"project/id"
        params = {"projectName": projectName}
        resp = self.client.request("GET", url_part=path, params=params)
        projectId = resp.json()['Content']
        return projectId

class ProjectInventoryFactory(Factory):
    @DeprecationWarning
    def all(self):
        pass
    def get(self, id:str, skip_vulnerabilities: bool = False):
        path = f"project/inventory/{id}"
        params = {"skipVulnerabilities": skip_vulnerabilities}
        resp = self.client.request("GET", url_part=path, params=params)
        project_inventory = resp.json()
        project_cls = self.cls.from_dict(project_inventory)
        return project_cls

import math

class PageNavigation:
    """
    Representa a paginação de uma datagrid (adaptado de Pablo Dall'Oglio)
    """
    def __init__(self):
        self.action = None
        self.pageSize = 10
        self.currentPage = 1
        self.totalRecords = 0

    def setAction(self, action):
        self.action = action

    def setPageSize(self, pageSize):
        self.pageSize = pageSize

    def setCurrentPage(self, currentPage):
        self.currentPage = currentPage

    def setTotalRecords(self, totalRecords):
        self.totalRecords = totalRecords

    def render(self):
        pages = math.ceil(self.totalRecords / self.pageSize) if self.pageSize else 0
        html = ['<ul class="pagination">']
        for n in range(1, pages + 1):
            offset = (n - 1) * self.pageSize
            action = self.action
            if action:
                action.setParameter('offset', offset)
                action.setParameter('page', n)
                url = action.serialize() if hasattr(action, 'serialize') else '#'
            else:
                url = '#'
            class_ = 'active' if self.currentPage == n else ''
            html.append(f"<li class='{class_}'><a href='{url}'>{n}</a>&nbsp;&nbsp;</li>")
        html.append('</ul>')
        return '\n'.join(html)

    def __str__(self):
        return self.render()

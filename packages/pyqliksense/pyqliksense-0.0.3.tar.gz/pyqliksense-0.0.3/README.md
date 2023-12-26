# PyQlikSense


1. [Installation](#installation)
2. [Getting started](#getting-started)
   1. [Authentication](#authentication)
   2. [Retriving data](#getting-calculation-results)


## Installation
```bash
pip install pyqliksense
```

## Getting started
### Authentication


#### NTLM Authenication
```python
from pyqliksense import QlikSense


qlik_sense = QlikSense(host='https://your-qlik-instance.com', auth_type='NTLM',username=r'domain\username', password='password')
```

#### JWT Authenication
```python
from pyqliksense import QlikSense


qlik_sense = QlikSense(host='https://your-qlik-instance.com', auth_type='JWT', jwt_token="your_token", virtual_proxy='your_proxy')
```

### Getting Calculation Results
```python
from pyqliksense import QlikSense

qlik_sense = QlikSense(host='https://your-qlik-instance.com', auth_type='NTLM',username=r'domain\username', password='password')
apps = qlik_sense.get_apps()
sales_app = apps[0]
result = sales_app.evaluate_expression("sum(Sales)")
print (result)
```


### Getting hypercube data
```python
from pyqliksense import QlikSense
from pyqliksense.objects import QlikSenseHyperCube

qlik_sense = QlikSense(host='https://your-qlik-instance.com', auth_type='NTLM',username=r'domain\username', password='password')
hypercube = QlikSenseHyperCube(
    dimensions=['Country'],
    measures=['sum(Sales)'],
    context_set_analysis="{<Product={'Jeans'}>}"
)

app = qlik_sense.get_apps_by_name("Sales Report")[0]
data = app.get_hypercube_data(hypercube, 10, 3)
print (data['qDataPages'][0]['qMatrix'])
```
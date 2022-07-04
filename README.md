![homebudget](https://user-images.githubusercontent.com/82864230/177012266-cb729dcd-e130-4ab4-b447-5789ad4b62f2.png)

## Overview
<table>
<tr>
<td>
Home-budget is an app that allows user to display nicely formatted overview of his monthly expenses.<br>
Track savings increase by planning your budget and adding realized transactions.

</td>
</tr>
</table>


### Demo
Demo version: [https://homebudget-demo.herokuapp.com/](https://homebudget-demo.herokuapp.com/)


### Technologies
- Python
- Flask
- SQLAlchemy
- Jinja2
- HTML
- CSS
- JavaScript

### Installation
```
git clone <url>
```
```
pip install -r requirements.txt
```
>If you want to store your data **locally**, you need to change database URI.<br>
Replace config line to ```app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"``` 


### Running
```
flask run
```
Go to ```http://127.0.0.1:5000```


### Support
Notice: Application doesn't support screen readers.

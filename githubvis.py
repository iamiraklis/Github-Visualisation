import base64
import pygal
import requests
from github import Github
from pprint import pprint


#Make an API call, and store the response

# Github username
username = input("Enter a valid GitHub Username: ")
# pygithub object

# This code is to hide the main tkinter window
try:
    token = input("Enter a valid OAuth Token: ")
    g = Github(token)
    user = g.get_user(username)
    print("Valid token (Not Limited")
except:
    print("Not Valid token. Program works, but is limited.")
    g = Github()
    user = g.get_user(username)

r = user.get_repos()


#Store API response in a variable.

#Explore information about the repositories.
#repo_dicts = response_dict['items']

names, stars, languages= [], [], {}
for repo_dict in r:
    names.append(repo_dict.name)
    language = repo_dict.language
    if language in languages:
        languages[language] = languages[language] + 1
    else:
        languages[language] = 1
    if repo_dict.stargazers_count == 0:
        stars.append(0)
    else: 
        stars.append(repo_dict.stargazers_count)

print(languages)
print(names)
print(stars)

followers = user.followers_url
user_data = requests.get(followers).json()

#Make visualisation.

my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = True
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.major_label_font_size = 18
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width=1300

chart = pygal.Pie(my_config, inner_radius=.4)
chart.title = f"{user.login}'s Top Followers (Total: {user.followers})"
for account in user_data:
    chart.add(account["login"], 1)
chart.render_in_browser()
chart.render_to_file("top_followers.svg")

my_configBar = pygal.Config()
my_configBar.x_label_rotation = 45
my_configBar.show_legend = False
my_configBar.title_font_size = 24
my_configBar.label_font_size = 14
my_configBar.major_label_font_size = 18
my_configBar.truncate_label = 15
my_configBar.show_y_guides = False
my_configBar.width=1300

chart2 = pygal.HorizontalBar(my_configBar, y_title='Repo', x_title='Stars', rounded_bars=5)
chart2.title = f"{user.login}'s  Most Liked Repos"
chart2.x_labels = names
chart2.render
chart2.add('', stars)
chart2.render_in_browser()
chart2.render_to_file("most_liked_repos.svg")


chart3 = pygal.Treemap(my_config)
chart3.title = f"{user.login}'s  Languages used"
for language in languages:
    chart3.add(language, languages[language])
chart3.render
chart3.render_in_browser()
chart3.render_to_file("Languages_used.svg")
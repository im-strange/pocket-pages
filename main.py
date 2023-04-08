from flask import Flask, render_template, redirect, url_for, request
import json
from datetime import date, datetime
import os
import re

app = Flask(__name__)

info = json.load(open("data.json"))

host = info["host_ip"]
port = info["port"]

def get_time():
  time = datetime.now()
  time = time.strftime("%I:%M%p")
  today = date.today()
  today = today.strftime("%B %d, %Y ")
  return today+time

def fetch_each_blog(filename):
  with open(filename) as file:
    data = file.read().splitlines()
  content = ""
  for line in data[2:]:
    whitespace = re.search("\S", line)
    if whitespace != None:
      line = ("\u00A0"*whitespace.start()) + line
      content += line + "\n"
    elif whitespace == None:
      content += line+"\n"
  return [data[0], data[1], content]

def fetch_blog():
  files = os.listdir("pocket_pages")
  blog = []
  files.sort()
  for file in files:
    blog.append(fetch_each_blog("pocket_pages/"+file))
  return blog

def add_blog(file_name, content):
  file = open("pocket_pages/"+file_name, "w")
  file.write(content)
  file.close()

@app.route("/")
def home():
  blog_info = fetch_blog()

  return render_template("blog.html",
		blog_info=blog_info)

@app.route("/create_blog", methods=["GET", "POST"])
def create_blog():
  error = None
  method = request.method

  if method == "POST":
    body = request.form["content"]

    if len(body) == 0:
      error = "Content cannot be empty"
      return render_template("create_blog.html", error=error)

    else:
      blog_file_name = f"pocketpage-{len(os.listdir('pocket_pages'))+1}"

      user_name = info["name"]
      user_name = f"@{user_name}"

      add_blog((f"{blog_file_name}.txt"), (f"{user_name}\n{get_time()}\n{body}"))
      return  redirect(url_for("home"))

  return render_template("create_blog.html",
		error=error)

if __name__ == "__main__":
  app.run(host=host, port=port)

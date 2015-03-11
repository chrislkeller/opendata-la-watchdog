import os
import csv
import re
import envoy
import requests
from jinja2 import Template
from datetime import datetime
from hurry.filesize import size
from BeautifulSoup import BeautifulSoup
from dateutil.parser import parse as dateparse
import logging

logger = logging.getLogger("root")
logging.basicConfig(
    format = "\033[1;36m%(levelname)s: %(filename)s (def %(funcName)s %(lineno)s): \033[1;37m %(message)s",
    level=logging.DEBUG
)

class Watchdog(object):
    """
    Tricks for downloading and archiving Checkbook LA data.
    """
    format_list = ["csv", "json"]

    url_template = "https://data.lacity.org/api/views/%(id)s/rows.%(format)s?accessType=DOWNLOAD"

    headers = {
        "User-agent": "KPCC - Southern California Public Radio (ckeller@scpr.org)"
    }

    catalog_url = "https://data.lacity.org/browse?limitTo=datasets&sortBy=alpha&view_type=table&limit=1000"

    def handle(self, *args, **kwargs):
        """
        make everything happen
        """
        print "Running the checkbook la watchdog"
        self.set_options()
        self.get_file_list()
        [self.download(f) for f in self.file_list]
        self.update_github()

    def set_options(self):
        """
        prep everything.
        """
        self.now = datetime.now()

        # Set template paths
        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        self.template_dir = os.path.join(self.this_dir, "templates")
        self.csv_dir = os.path.join(self.this_dir, "csv")
        self.json_dir = os.path.join(self.this_dir, "json")

        # Make sure template paths exist
        os.path.exists(self.csv_dir) or os.mkdir(self.csv_dir)
        os.path.exists(self.json_dir) or os.mkdir(self.json_dir)

    def get_file_list(self):
        """
        scrape all of the "datasets" published by the controller.
        """
        r = requests.get(self.catalog_url, headers=self.headers)
        soup = BeautifulSoup(r.text)
        row_list = soup.find("table", {"class": lambda L: "gridList" in L.split()}).findAll("tr")
        self.file_list = []
        for row in row_list[1:]:
            cell = row.find("td", {"class": "nameDesc"})
            data = cell.find("a", {"class": "name"})
            name = data.string.replace("&#x27;", "")
            name = re.sub(r"\W+", " ", name)
            description = cell.find("div", {"class": "description"}).text.encode("utf-8")
            url = data["href"]
            id = url.split("/")[-1]
            file_name = name.lower().replace(" ", "-")
            self.file_list.append({
                "name": name,
                "description": description,
                "url": url,
                "id": id,
                "file_name": file_name,
                "csv_name": "%s.csv" % (file_name),
                "json_name": "%s.json" % (file_name),
            })

    def download(self, obj):
        """
        download a file in pieces.
        """
        for format_ in self.format_list:
            url = self.url_template % dict(
                format=format_,
                id=obj["id"],
            )
            file_name = "%s.%s" % (obj["file_name"], format_)
            print "- Downloading %s in %s format" % (obj["file_name"], format_)
            r = requests.get(url, headers=self.headers, stream=True)
            file_path = os.path.join(getattr(self, "%s_dir" % format_), file_name)
            with open(file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()

    def update_log(self):
        """
        log activity to the readme file.
        """
        print "- Updating log"
        template_path = os.path.join(self.template_dir, "README.md")
        template_data = open(template_path, "r").read()
        template = Template(template_data)
        dict_list = []
        for obj in self.file_list:
            logger.debug(obj)
            csv_path = os.path.join(self.csv_dir, obj["csv_name"])
            try:
                csv_reader = csv.reader(open(csv_path, "r"))
                row_count = len(list(csv_reader))
                if row_count < 10000:
                    repo_status = True
                else:
                    repo_status = None
                dict_list.append({
                    "name": obj["name"],
                    "description": obj["description"],
                    "row_count": row_count,
                    "last_updated": str(self.now),
                    "csv_name": obj["csv_name"],
                    "json_name": obj["json_name"],
                    "url": obj["url"],
                    "repo_status": repo_status
                })
            except Exception, exception:
                logger.error(exception)
                break
        diff = envoy.run("git diff --stat").std_out
        out_data = template.render(file_list=dict_list, diff=diff)
        out_file = open(os.path.join(self.this_dir, "README.md"), "w")
        out_file.write(out_data)
        out_file.close()
        return dict_list

    def update_github(self):
        """
        commit changes and push them to github
        """
        print "- Updating GitHub"
        dict_list = self.update_log()
        for item in dict_list:
            if item["repo_status"] == True:
                envoy.run("git add csv/%s" % item["csv_name"])
                envoy.run("git add json/%s" % item["json_name"])
        envoy.run("git add README.md")
        envoy.run("git commit --file=%s" % os.path.join(
            self.template_dir,
            "commit.txt"
        ))
        envoy.run("git push origin master")

if __name__ == "__main__":
    wd = Watchdog()
    wd.handle()

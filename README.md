# Team Fudan 2022 Software Tool - PartHub
**This is the mirror repository of [Software of Fudan - iGEM 2022](https://gitlab.igem.org/2022/software-tools/fudan).**

Improve your part design with 50000+ parts！

Try our public PartHub [here](http://3.238.241.161:5000/)!

## Description

For more information, please visit our wiki page [Software | Fudan - iGEM 2022](https://2022.igem.wiki/fudan/software)
![multi-device.png (3011×2006) (igem.wiki)](https://static.igem.wiki/teams/4162/wiki/software/multi-device.png) 

### Highlight

- A quick, efficient and powerful tool for building and designing new parts
- Provide multiple ways for searching for 50000+ existing parts with Registry of Standard Biological Parts platform
- Visualization of the relationship between parts
- Can be used across various platforms, and intuitive workflow

## Installation
***If you only want to use [the public PartHub](http://3.238.241.161:5000/), you don't need to perform installation. Please click [here](https://gitlab.igem.org/2022/software-tools/fudan#for-common-users) and read the how-to section.***

Since there is no image of Oracle JDK in the docker hub, it is not convenient to install PartHub using docker. We recommend using Amazon Machine Image (AMI) to install it.

### (Recommended) Install with AMI

***Quick installation guide***

1. Open the Amazon EC2 console at https://console.amazonaws.cn/ec2/.

2.  Under **Images > AMI Catalog**, do the following: 

   a. Search ***PartHub*** in **Community AMls**

   b. Select the PartHub AMI (ami-036510704fd194c8f) and choose **Launch Instance with AMI**

3. Select  **Instance type** as **t3.xlarge or higher** and **Launch instance**.

4. Configure the  **Inbound rules** under **Network & Security >  Security Groups**  as follows:

   | **IP version** |  **Type**  | **Protocol** | **Port range** | **Source** | **Description** |
   | :------------: | :--------: | :----------: | :------------: | :--------: | :-------------: |
   |      IPv4      | Custom TCP |     TCP      |      7687      | 0.0.0.0/0  |      neo4j      |
   |      IPv4      | Custom TCP |     TCP      |      7474      | 0.0.0.0/0  |      neo4j      |
   |      IPv4      | Custom TCP |     TCP      |      5000      | 0.0.0.0/0  |       web       |
   |      IPv4      |    SSH     |     TCP      |       22       | 0.0.0.0/0  |        –        |

5. Connect to your server using SSH, and run the following in your Terminal:

   ```bash
   screen -S neo4j
   ```

   then run the following in the `screen`:

   ```bash
   sudo -s
   cd /usr/local/neo4j-community-4.4.11/bin/
   ./neo4j console
   ```

6. Press Crtl + A and then press D to detach the `screen` session and run the following in your Terminal:

   ```
   screen -S web
   ```

   then run the following in the `screen`:

   ```bash
   cd /home/ubuntu/fudan-main/
   source venv/bin/activate
   python /home/ubuntu/fudan-main/DataBase/LoadCSVFile.py
   gunicorn -b 0.0.0.0:5000 app:app
   ```

7. Visit http://serverIP:5000/ (change serverIP to the IP of your server) and start using your PartHub!

### Manual installation (For local deployment)

The system requirements to deploy PartHub are as follows:

| Minimum    |                               | Recommended |                               |
| ---------- | ----------------------------- | ----------- | ----------------------------- |
| CPU        | 2-core, 2.4 GHz               | CPU         | 8-core, 2.9 GHz               |
| Memory     | 8 GB                          | Memory      | 16 GB                         |
| Hard Drive | 20 GB, SSD                    | Hard Drive  | 512 GB, SSD                   |
| Network    | Broadband Internet connection | Network     | Broadband Internet connection |

Environmental requirements: Neo4j & Oracle JDK (We recommend Neo4j 4.4.11 & Oracle JDK 11.0.16). For more information, see https://neo4j.com/docs/operations-manual/current/installation/ & https://docs.oracle.com/en/java/javase/11/install/overview-jdk-installation.html. For Neo4j, please set the Username as *neo4j* & Password as *igem2022*.

1.  Check your JDK version in your Terminal:

   ```bash
   java --version
   ```

   If the JDK version is correct, the return should be:

   ```
   java 11.0.16 2022-07-19 LTS
   Java(TM) SE Runtime Environment 18.9 (build 11.0.16+11-LTS-199)
   Java HotSpot(TM) 64-Bit Server VM 18.9 (build 11.0.16+11-LTS-199, mixed mode)
   ```

2. Download PartHub:

   ```bash
   git@gitlab.igem.org:2022/software-tools/fudan.git
   ```

3. Replace the `neo4j.conf`  in the conf file where you install your Neo4j (e.g. /usr/local/neo4j-community-4.4.11/conf/) with that in this Repository.

4. Change directory to the location of the bin file of Neo4j, and run the following in your Terminal:

   ```bash
   screen -S neo4j
   ```

   then run the following in the `screen`:

   ```bash
   sudo -s
   ./neo4j console
   ```

5. Press Crtl + A and then press D to detach the `screen` session and run the following in your Terminal:

   ```bash
   screen -S web
   ```

   then run the following in the `screen`:

   ```
   cd /home/ubuntu/fudan-main/
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python /home/ubuntu/fudan-main/DataBase/LoadCSVFile.py
   gunicorn -b 0.0.0.0:5000 app:app
   ```

   where `/home/ubuntu/fudan-main/` should be changed to the directory of your `fudan-main` file.

6. Visit http://serverIP:5000/ (change serverIP to the IP of your server) and start using your PartHub!

## How-to

### For common users

Below is an overview of PartHub's workflow.

![parthub-workflow.png (2125×1063) (igem.wiki)](https://static.igem.wiki/teams/4162/wiki/software/parthub-workflow.png) 

The process of using PartHub is shown below: 

1. Visit PartHub, for example, http://3.238.241.161:5000/. The website is supposed to be like this:

   ![homepage.png (2880×1800) (igem.wiki)](https://static.igem.wiki/teams/4162/wiki/software/homepage.gif) 

2. Select the search type and enter search terms (e.g. search type is Content & search term is carotene).  The format of the search terms corresponding to different search types is as follows:

   | **Search type** |                     **Meaning & Format**                     |    **Example**    |                       **Example URL**                        |
   | :-------------: | :----------------------------------------------------------: | :---------------: | :----------------------------------------------------------: |
   |       ID        | The id of the part (e.g. BBa_xxxxxxxx). It is fine to enter a search term with or without BBa_. |     K3790012      |  http://3.238.241.161:5000/sp?s=K3790012&searchtype=number   |
   |      Name       | The name of the part in Registry of Standard Biological Parts. |        GFP        |      http://3.238.241.161:5000/sp?s=GFP&searchtype=name      |
   |    Sequence     | The sequence of the part (if it exists). The search term can only be the combination of [a, t, g, c, A, T, G, C]. | TTAACTTTAAGAAGGAG | http://3.238.241.161:5000/sp?s=TTAACTTTAAGAAGGAG&searchtype=sequence |
   |    Designer     |        The name of the person who designed the part.         |   Guanqiao Chi    | http://3.238.241.161:5000/sp?s=Guanqiao%20Chi&searchtype=designer |
   |      Team       |        The name of the team which designed the part.         |       Fudan       |     http://3.238.241.161:5000/sp?s=Fudan&searchtype=team     |
   |     Content     | The content of the part in Registry of Standard Biological Parts. |     carotene      | http://3.238.241.161:5000/sp?s=carotene&searchtype=contents  |

   Our search engine is case-insensitive and support partial match retrieval. In addition, PartHub supports boolean search with multiple search terms (The format of the boolean search with multiple search terms should be *xxx AND xxx or xxx OR xxx*).

   ***What's more, PartHub supports fuzzy search.*** For example, if you want to search for *beta AND carotene* but you accidentally type in *bata AND carotene*, PartHub will automatically do the fuzzy search for you and the result will be:

   ![fuzzysearch.png (2880×1800) (igem.wiki)](https://static.igem.wiki/teams/4162/wiki/software/fuzzysearch.png) 

3. View sorted searching results (you can choose certain sorting order). PartHub provides several ways to sort the results, like Most cited, Best match, etc. In this way, users can organize the result in order to their needs. Sorting by Recommended is a weighted sort that considers various aspects of suitability and can be used in situations where users are unsure which sort is more appropriate for their needs.

4. Click on a specific part you are interested in and visualize the relationship network of this part. The page is as follows:

   ![graph.png (2880×1800) (igem.wiki)](https://static.igem.wiki/teams/4162/wiki/software/graph.gif) 

   This relationship network is interactive, you can scroll to zoom the canvas and drag to move the nodes. Click to display the part details and double click to go to the part page. You can drag nodes to change the layout of the canvas. On this page, you can also get the sequence of this part directly.

## **For developers**

*The source code is in this Repository.* 

1. The `DataBase` file contains code to import data into the database.  

2. The `WebCrawler` file contains code to get data from the Registry of Standard Biological Parts. If you want to update the data for a new year, replace the year in [line 679](https://gitlab.igem.org/2022/software-tools/fudan/-/blob/main/WebCrawler/software_ver0.4.py#L679) of `software_ver0.4.py` with the year you want to get the data for. Then you can run `MergeCSVFiles.py` to get the new `all_collections.csv`. Then run `Preprocessing.py` to get `all_collections_filted.csv`. After uploading the data via `LoadCSVFile.py`, you are able to use PartHub with updated data. We recommend you to run it on a PC with more than 8 core CPUs for getting data of just one year, and on a higher performance computer for getting multiple years of data. Remember to switch the appropriate number of threads in `software_ver0.4.py` for better performance. Our recommended configuration is as follows:

   | CPUs       | Dual Intel® Xeon E5-2680v2(10core, 20thread, 2.80 GHz to 3.60 GHz) |
   | ---------- | ------------------------------------------------------------ |
   | Memory     | 64 GB, DDR3, 1600 MHz                                          |
   | Hard Drive | 500 GB, NVMe, SSD                                             |
   | GPU        | NVIDIA® GeForce GTX1050 Ti                                   |

3. The back-end code of PartHub is written in Python (`.py` files). The role of each code has been commented in the file.

4. The `static` file contains static files(images and JavaScript files). The `templates` file contains front-end HTML files.

## Contributing

### Pull Requests

We actively welcome your pull requests.

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.

In order to accept your pull request, please send me an [email](mailto:20301050198@fudan.edu.cn). 

### Issues

We use GitLab issues to track bugs. Please describe your isuee clearly and give sufficient instructions to reproduce the issue.

## Authors and acknowledgment

### Authors

- Zhiyue Chen ([@mistyfield](https://gitlab.igem.org/mistyfield))
- Yunjia Liu ([@VeronicaLiu](https://gitlab.igem.org/VeronicaLiu))

### Acknowledgment

- Sunzhe Kang ([@KangSunzhe](https://gitlab.igem.org/KangSunzhe))
- Shitao Gong  ([@Tom_GhoST_Smith](https://gitlab.igem.org/Tom_GhoST_Smith)), and 2021's [Part Camera](https://2021.igem.org/Team:Fudan/Software)

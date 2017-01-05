## About

**waybackeess** was build to be a fast and easy way to fetch and analyze web archive website's snapshots. It is a simple python client API integrated with Elastic Search and Kibana, so you can research semantically and visualize the data.


### Installation

###Requirements
 - Elastic Search
 - Kibana

For a fast and clean envirolment setup you can use Docker.

To start an Elastic Search instance:
```
docker run -p 9200:9200 -p 9300:9300 -d elasticsearch
```

And Kibana:
```
docker run --link elastic_docker_name:elasticsearch -p 5601:5601 -d kibana
```

###Instructions

Clone waybackess repository
```
git clone https://github.com/VulcanoAhab/waybackeess.git
```

Browse waybackeess directory
```
cd waybackeess
```

Install Python dependencies
```
pip install -r requirements.txt
```

Start a single website research
```
python3 research.py -u site_url --date_start YYYMMDD --date_end YYYMMDD
```

run a multiple website research
```
create a json configuration file:

{

   "site_1": {
      "report": "sites",
      "date_range": {
         "full_year": true,
         "end": {
            "year": 0000,
            "month":00,
            "day":00
         },
         "start": {
           "year": 0000,
           "month":00,
           "day":00
         }
      }
   },

   "site_2": {
      "report": "sites",
      "date_range": {
         "full_year": true,
         "end": {
           "year": 0000,
           "month":00,
           "day":00
         },
         "start": {
           "year": 0000,
           "month":00,
           "day":00
         }
      }
   }

}

then run:

python3 research.py -c config_file_name.json

```

Once is running, access the Kibana interface:
http://127.0.0.1:5601

#!/usr/bin/env python
# coding: utf-8

import requests
from requests.adapters import HTTPAdapter
from requests.packages import urllib3
from requests.packages.urllib3.util.retry import Retry
import time
import os
import numpy
import multiprocessing
from multiprocessing import set_start_method
from multiprocessing import get_context
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from urllib.error import HTTPError
from urllib.error import URLError
import tldextract
import pandas as pd
from urllib3.exceptions import NewConnectionError, ConnectTimeoutError, MaxRetryError
from functools import reduce
from multiprocessing import Pool, cpu_count
import certifi
import lxml
import pickle


def parse_website_chunk(urls):
    session = requests.Session()
    retryer = Retry(
        total=5, read=5, connect=5, backoff_factor=0.1, status=1, redirect=1, status_forcelist=None) #levi had put the backoff_factor at 0.2...
    adapter = HTTPAdapter(max_retries=retryer)
    adapter.max_retries.respect_retry_after_header = False
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    all_out = [].
    for i in range(len(urls)):
        url = "http://" + urls[i] if not (urls[i].startswith("http://")) else urls[i]
        print(str((i+1)) + "/" + str(len(urls)) + "|| looking at url{}".format(url))
        try:
            content = session.get(url, verify=False, timeout= (5, 0.5)).content 
            parsed = BeautifulSoup(content, parser="lxml", features='lxml')
            all_out.append((url, True, parsed.get_text()))
            print ("b")
        except requests.ConnectionError:
            all_out.append((url, False, requests.ConnectionError))
            print ("a")
        except requests.Timeout:
            all_out.append((url, False, requests.Timeout))
            print("t")
        except requests.RequestException:
            all_out.append((url, False, requests.RequestException))
            print("r.e.")
        except HTTPError:
            all_out.append((url, False, HTTPError))
            print("HTTPError")
        except Exception as e:
            all_out.append((url, False, e))
            print("f")
        except MaxRetryError:
            all_out.append((url, False, MaxRetryError))
            print("g")
        except requests.exceptions.Timeout:
            print("Timeout occurred")
        time.sleep(0.5)#it was 0.5 when levi did it
    session.close()
    print('Completed scraping for this chunk')
    return pd.DataFrame(all_out, columns=["url", "status", "text"]).reset_index(drop= True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parse_websites(urls):
    n_jobs = os.cpu_count()
    chunks = numpy.array_split(urls, n_jobs)
    with get_context("spawn").Pool(processes=n_jobs) as P:
        result = P.map(parse_website_chunk, chunks)
    P.close()
    print("parsing done. about to concat results and return")
    print(result)
    return pd.concat(result)

if __name__ == "__main__":
    set_start_method("spawn")



    with open('urls_common_crawl.pkl', 'rb') as f:
        list_of_urls = pickle.load(f)

    splitted_array = numpy.array_split(list_of_urls, 4)

    list_of_splitted_arrays = [splitted_array[i] for i in range(4)]

    splitted_chunk = numpy.array_split(splitted_array[1], 3)

    list_of_splitted_chunks = [splitted_chunk[i] for i in range(3)]

    outcome_dataframe = pd.DataFrame()
    for splitted_array in list_of_splitted_arrays:
        print(len(splitted_array))
        outcome = pd.concat([outcome_dataframe, parse_websites(splitted_array)])
        print(outcome.tail())
        print(len(outcome))
        outcome.to_pickle("scraped_websites.pkl")


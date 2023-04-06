import pandas as pd
import numpy as np
import math
import pickle
import yfinance as yf
import scipy.stats as ss
import datetime
import talib as ta
import matplotlib
matplotlib.use('TkAgg')  # Or any other interactive backend
import matplotlib.pyplot as plt
from tqdm import tnrange
import kmapper as km
import umap
import tkinter
import sys
import sklearn
import datetime
import plotly.express as px
import sklearn.manifold as manifold
from sklearn.cluster import AgglomerativeClustering
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mutual_info_score
from scipy.cluster.hierarchy import dendrogram, linkage
import ReadData
import os


NameOfStocks = ReadData.ReadData("C:\\Users\\user\\Desktop\\stumpy2\\Stocks")
Name = NameOfStocks.NameofStocks()

ii=np.array(Name)
print (type(Name))
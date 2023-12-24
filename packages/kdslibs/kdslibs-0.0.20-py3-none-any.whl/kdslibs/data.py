TSF-LIB
##HEADER##from statsmodels.tsa.seasonal     import seasonal_decompose, STL
from statsmodels.tsa.api import Holt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima_process import ArmaProcess
import statsmodels.api as sm

from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import adfuller
import  matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import matplotlib.pyplot                  as      plt
import seaborn                            as      sns
from   IPython.display                    import  display
from   pylab                              import  rcParams 
from   datetime                           import  datetime, timedelta
from statsmodels.tsa.stattools            import  adfuller
from statsmodels.tsa.stattools            import  pacf
from statsmodels.tsa.stattools            import  acf
from statsmodels.graphics.tsaplots        import  plot_pacf
from statsmodels.graphics.tsaplots        import  plot_acf
from statsmodels.graphics.gofplots        import  qqplot
from statsmodels.tsa.seasonal             import  seasonal_decompose
from statsmodels.tsa.arima_model          import  ARIMA
from statsmodels.tsa.statespace.sarimax   import  SARIMAX
from pmdarima import auto_arima
from statsmodels.tsa.stattools import adfuller
from statsmodels.tools.eval_measures import mse,rmse
from statsmodels.tsa.statespace.varmax import VARMAX,VARMAXResults

from statsmodels.tsa.api                  import  ExponentialSmoothing
from statsmodels.tsa.ar_model       import AutoReg
from statsmodels.tsa.arima_model import ARMA
import statsmodels as sm
pip install pmdarima

import warnings
warnings.filterwarnings(""ignore"")
###ENDOFSEGMENT###TSF-DATE
##HEADER##pd.read_csv('file', parse_dates = ['col1'], index_col = 'Year-Month')
pd.date_range(start='', end='', freq='M/D/Q')
df2.set_index('col')
df_comp.date = pd.to_datetime(df_comp.date, dayfirst = True)
df[""Date""]=pd.to_datetime(df[""Date""], format = ""%d-%m-%Y"")
###ENDOFSEGMENT###TSF-PLOT
##HEADER##df1.plot(figsize=(12,8),grid=True)
df.groupby(df.index.month_name(),sort=None).mean().plot(kind=""bar"")
###ENDOFSEGMENT###TSF-IMPUTE
##HEADER##df.fillna(df.rolling(6,min_periods=1).mean())
df_imputed= df.interpolate(method = 'linear')
df_comp=df_comp.fillna(method='ffill')
df_comp=df_comp.asfreq('b')
###ENDOFSEGMENT###TSF-CONVERT
##HEADER##df.resample('Q').sum()
###ENDOFSEGMENT###TSF-DECOMPOSE
##HEADER##decomposition = seasonal_decompose(df,model='additive')
decomposition.plot();

decomposition = STL(df1).fit()
decomposition.plot();

decomposition = STL(np.log10(df1)).fit()
decomposition.plot();

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

fig, ax = plt.subplots(figsize=(12,8))
plt.subplot(411)
plt.plot(coviddata['Hospitalized'], label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal,label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()
plt.show()
###ENDOFSEGMENT###TSF-ROLLING
##HEADER### compute the rolling mean and standard deviation of the closing prices
rolling_mean = df['Hospitalized'].rolling(window=7).mean()
rolling_std =df['Hospitalized'].rolling(window=7).std()

# plot the stock prices, rolling mean, and rolling standard deviation
fig, ax = plt.subplots(figsize=(10, 6))
df['Hospitalized'].plot(ax=ax, label='Original Data')
rolling_mean.plot(ax=ax, label='Rolling Mean (7 days)')
rolling_std.plot(ax=ax, label='Rolling Std (7 days)')
ax.set_xlabel('Date')
ax.set_ylabel('Hospitalized')
ax.legend()
plt.show()
###ENDOFSEGMENT###TSF-MACODE
##HEADER##df5.rolling(5).mean()
plt.plot(df5, label='closing price')
plt.plot(df5.rolling(30).mean(), label='Moving Average')

m=[]
rolling=2
for app in range(1,rolling):
  m.append(""0"")
for eachRow in range(rolling-1,df1.shape[0]):
  #print(df1.iloc[eachRow][""Pax""], df1.iloc[eachRow-1][""Pax""], df1.iloc[eachRow-2][""Pax""])
  mi=0
  for eachRolling in range(0,rolling):
    mi+=df1.iloc[eachRow-eachRolling][""Pax""]
  mi=mi/rolling
  m.append(mi)
df1[""moving""]=m
###ENDOFSEGMENT###TSF-ACF
##HEADER##fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
plot_acf(df['Hospitalized'], lags=50, ax=ax1,zero= False )
plot_pacf(df['Hospitalized'], lags=50, ax=ax2,zero = False)
plt.show()
###ENDOFSEGMENT###TSF-YEARLY
##HEADER##months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October','November', 'December']
yearly_sales_across_years = pd.pivot_table(df1, values = 'Pax', columns = df1.index.year,index = df1.index.month_name())
yearly_sales_across_years = yearly_sales_across_years.reindex(index = months)
yearly_sales_across_years.plot()
plt.grid()
plt.legend(loc='best');
###ENDOFSEGMENT###TSF-TESTTRAIN
##HEADER##size = int(len(df[""Hospitalized""])*0.8)
train, test = df.iloc[:size], coviddata.iloc[size:]
###ENDOFSEGMENT###PLOTLY
##HEADER##import plotly.express as px
###ENDOFSEGMENT###MATPLOTLIB-LINE
##HEADER### Line Plot
df.plot(x = 'Date', y = 'FB', label = 'label', figsize = (15, 10), linewidth = 3)
plt.ylabel('ylabel')
plt.title('title')
plt.legend(loc = 'upper right')
plt.grid()

#Multiple Line
stock_df.plot(x = 'Date', y = ['NFLX', 'FB', 'TWTR'], figsize = (18, 10), linewidth = 3)
plt.ylabel('price [$]')
plt.title('Stock Prices')
plt.grid()
plt.legend(loc = 'upper center')

###ENDOFSEGMENT###MATPLOTLIB-SCATTER
##HEADER##
#Scatter plot
plt.figure(figsize = (15, 10))
plt.scatter(x, y)
plt.grid()

###ENDOFSEGMENT###MATPLOTLIB-PIE
##HEADER##
#Pie Chart
values = [20, 55, 5, 17, 3]
colors = ['g', 'r', 'y', 'b', 'm']
labels = [""Apple"", ""Google"", ""T"", ""TSLA"", ""AMZN""]
explode = [0, 0.2, 0, 0, 0.2]
# Use matplotlib to plot a pie chart 
plt.figure(figsize = (10, 10))
plt.pie(values, colors = colors, labels = labels, explode = explode)
plt.title('Stock Portfolio')

###ENDOFSEGMENT###MATPLOTLIB-HISTOGRAM
##HEADER##
#Historgram
mu = daily_return_df['FB'].mean()
sigma = daily_return_df['FB'].std()

num_bins = 40
plt.figure(figsize = (15, 9))
plt.hist(daily_return_df['FB'], num_bins, facecolor = 'blue'); # ; is to get rid of extra text printing
plt.grid()

plt.title('Historgram: mu = ' + str(mu) + ', sigma: ' + str(sigma))


###ENDOFSEGMENT###MATPLOTLIB-SUBPLOT
##HEADER##

# SUBPLOT
plt.figure(figsize = (20, 10))

plt.subplot(1, 2, 1) # will have 1 row and 2 columns, we are plotting first one
plt.plot(stock_df['NFLX'], 'r--') # r color, -- style
plt.grid()

plt.subplot(1, 2, 2) # will have 1 row and 2 columns, we are plotting second one
plt.plot(stock_df['FB'], 'b.')
plt.grid()
###ENDOFSEGMENT###SNS-SCATTER
##HEADER##plt.figure(figsize = (10,10))
sns.scatterplot(x = 'mean area', y = 'mean smoothness', hue = 'target', data = df_cancer)
###ENDOFSEGMENT###SNS-COUNT
##HEADER##plt.figure(figsize = (10,10))
sns.countplot(df_cancer['target'], label = 'Count')
###ENDOFSEGMENT###SNS-HEATMAP
##HEADER##plt.figure(figsize = (30, 30)) 
sns.heatmap(df_cancer.corr(), annot = True)
###ENDOFSEGMENT###SNS-HISTOGRAM
##HEADER##sns.distplot(df_cancer['mean radius'], bins = 25, color = 'b')

plt.figure(figsize = (10, 7))
sns.distplot(class_0_df['mean radius'], bins = 25, color = 'blue')
sns.distplot(class_1_df['mean radius'], bins = 25, color = 'red')
plt.grid()
###ENDOFSEGMENT###TSF-ADF
##HEADER##result = adfuller(df[""x""])
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
 print('\t%s: %.3f' % (key, value))
###ENDOFSEGMENT###TSF-EXPSMOOTH
##HEADER##X1
F=[]
F.append(X1[0,1])
a=0.1
for eachElement in range(1,len(X1)):
  cal=a * X1[eachElement-1,1] +(1-a) * F[eachElement-1]
  F.append(cal)
df_sales[""F""]=F
df_sales[""Y-F""]=df_sales[""Sales""]-df_sales[""F""]
df_sales[""abs(Y-F/Y)""]=abs((df_sales[""Sales""]-df_sales[""F""])/df_sales[""Sales""])
df_sales[""Y-F_squared""]=df_sales[""Y-F""]*df_sales[""Y-F""]

#Holt
model_holt = Holt(np.asarray(train[""Hospitalized""])).fit(smoothing_level=0.9, smoothing_slope=0.1)
forecast = model_holt.forecast(len(test[""Hospitalized""]))
print(model_holt.summary())


# Fit Triple Exponential Smoothing (Holt-Winter) model
model_hw = ExponentialSmoothing(train[""Hospitalized""], trend='add', seasonal='add', seasonal_periods=len(test))
model_fit_hw = model_hw.fit()
hwforecast=model_fit_hw.forecast(len(test[""Hospitalized""]))
print(model_fit_hw.summary())
test[""HoltWinter-forecast""]=hwforecast
###ENDOFSEGMENT###TSF-MAPE
##HEADER##Results=pd.DataFrame({})
#User defined function to evaluate the given model. 
from sklearn import metrics
def calculateMetrics(info,ytest,ypred ):
    global Results
    # User defined function to calculate MAPE from actual and predicted values. 
    def MAPE (y_test, y_pred):
      y_test, y_pred = np.array(y_test), np.array(y_pred)
      return np.mean(np.abs((y_test - y_pred) / y_test)) * 100

    result = MAPE(ytest, ypred)
   
    new_row = {'Info' :  info,
               'MAE' : metrics.mean_absolute_error(ytest, ypred),
               'RMSE' : round(np.sqrt(metrics.mean_squared_error(ytest, ypred)),3),
               'MAPE' : result,
               'MSE' : metrics.mean_squared_error(ytest, ypred),
               'RMSLE': np.log(np.sqrt(metrics.mean_squared_error(ytest, ypred)))
               }
    Results = Results.append(new_row, ignore_index=True)
###ENDOFSEGMENT###TSF-RESIDUAL
##HEADER##train[""residuals-train-HoltWinter""].plot(figsize = (20,5),label=""HoltWinter-Model"")
train[""residuals-train-Holt""].plot(figsize = (20,5),label=""Holt-Model"")

test[""residuals_HoltWinter""].plot(figsize = (20,5),label=""HoltWinter-Forecast"")
test[""residuals_Holt""].plot(figsize = (20,5),label=""Holt-Forecast"")
plt.legend()
###ENDOFSEGMENT###TSF-LS
##HEADER###For Two unknown a and b
A=[[x.sum(),len(x)],[sum( x ** 2),x.sum()]]
B=[y.sum(),sum(x * y)]

A_inv=np.linalg.inv(A)
first_order=A_inv.dot(B)
ypred_df1=first_order[0]*x + first_order[1]

yerror_df1=sum(((ypred_df1-y)**2))
print(""Error in First order"",yerror_df1)

#For Three unknown a , b and c
A_df2=[
      [sum( x ** 2), x.sum(),      len(x)],
      [sum( x ** 3), sum( x ** 2),  x.sum()],
      [sum( x ** 4), sum( x ** 3),  sum( x ** 2)],
    ]
B_df2 =[y.sum(),sum(x * y),sum(x * x*  y)]

A_df2_inv=np.linalg.inv(A_df2)
second_order=A_df2_inv.dot(B_df2)
ypred_df2=second_order[0]*x*x + second_order[1]*x + second_order[2]

yerror_df2=sum(((ypred_df2-y)**2))
print(""Error in First order"",yerror_df2)



###ENDOFSEGMENT###TSF-AR-CODE
##HEADER##import pandas as pd
import pylab as pl 
import sympy as sy
import numpy as np
sy.init_printing()

def AR_p(p,a,eparam, eps):
  N=len(eps)
  me,ve=eparam
  y=np.zeros(N)
  for i in range(p,N):
    y[i]=eps[i]
    for k in range(p):
      y[i] +=a[k] * y[i-k-1]
  return y
  
def AR_param(p,y):
    N=len(y)
    
    ymat=np.zeros((N-p,p))

    yb=np.zeros((N-p-1,1   ))
    print(ymat)
    print(yb)
    for c in range(p,0,-1):
      ymat[:,p-c]=y[p-c:-c]
    yb=y[p:]
    return np.matmul(np.linalg.pinv(ymat),yb)[::-1]

# White Noise
def w_n(y,acap):
  N=len(y)
  p=len(acap)
  w=np.zeros(N)
  for i in range(N):
    w[i]=y[i]
    for k in range(p):
      if i-k-1>0:
        w[i] +=-acap[k] * y[i-k-1]
  return w
  
def plotting_ar_nodel_fitting(x1,eps, y,ycap):
  pl.figure(figsize=(12,6))
  pl.subplot(221)
  pl.plot(x1,eps,label=""$\epsilon_n$"")
  pl.title(""$\epsilon_n$"",fontsize=25)
  pl.xticks(fontsize=18)
  pl.yticks(fontsize=18)


  pl.subplot(223)
  pl.plot(0,0)
  pl.plot(x1,y,label=""$y_n$"")
  pl.title(""$y_n$"",fontsize=25)
  pl.xticks(fontsize=18)
  pl.yticks(fontsize=18)


  pl.subplot(122)
  pl.plot(y,eps,""."",label=""$\epsilon_n$"")
  pl.plot(y,ycap,""."",label=""$\hat{y}_n$"")
  pl.legend(loc=2,fontsize=16)
  pl.xlabel(""$y_n$"",fontsize=25)
  pl.ylabel(""$\{\epsilon_n,\hat{y}_n\}$"",fontsize=25)
  pl.title(""$y_n$ vs. $\{\epsilon_n,\hat{y}_n\}$"",fontsize=25)
  pl.xticks(fontsize=18)
  pl.yticks(fontsize=18)
  pl.tight_layout()
  
p=1

a=1.0 * np.random.rand(p) -0.5
print(""Original/Initial AR parameters : \n"",a)

N=10;n=np.arange(0,N)
eparam=(0,5.0)
eps=np.sqrt(eparam[1]) * np.random.randn(N) + eparam[0]
print(""eps :\n"",eps)

print(""a(Initial Guess):"",a)
print(""p:"",p)
print(""eparam:"",eparam)
print(""eps:"",eps)


#Generate AR time series
y=AR_p(p,a,eparam,eps)
print(""y:"",y)

# Estimate AR Model parameter 
acap=AR_param(p,df1.sales)
print(""acap(Estimated AR):"",acap)

# Generate estimated parameter
ycap=AR_p(p,acap,eparam,eps)
print(""ycap:"",ycap)

plotting_ar_nodel_fitting(n,eps,y,ycap)
w=w_n(y,acap)

pl.figure(figsize=(3,3))
pl.plot(eps,w,""."")
pl.xlabel(""$\epsilon_n$"",fontsize=16)
pl.ylabel(""$w_n$"",fontsize=16)
pl.title(""$\epsilon_n$ vs. $w_n$"",fontsize=25)
pl.xticks(fontsize=18)
pl.yticks(fontsize=18)
###ENDOFSEGMENT###TSF-DIFF
##HEADER##odds_diff=np.diff(df[""Pax""],n=1)

actual=lag1 + diff1.cumsum 
diff1= (lag1-lag2) + diff2.cumsum()

nobs=20
df_forecast['Spending_Forcast_1D'] = (df_cons['Spending'].iloc[-nobs-1]-df_cons['Spending'].iloc[-nobs-2]) + df_forecast['Spending_Forcast_2D'].cumsum()
df_forecast['Spending_Forcast'] = df_cons['Spending'].iloc[-nobs-1] + df_forecast['Spending_Forcast_1D'].cumsum()

df_cons[""Money""].iloc[-nops-1]+ (df_cons[""Money""].iloc[-nops-1]-df_cons[""Money""].iloc[-nops-2] +test[""Money-2D""].cumsum()).cumsum()
###ENDOFSEGMENT###TSF-ACVF_CODE
##HEADER##data = [27, 28, 29, 30, 32, 32, 33]
##(Create a Matrix $Z$ for the data set)
Z = np.array(data)
print('Z=',Z)
print('=======================================================')
##  (Compute the Mean and substract it from the data) 
meanZ = Z.mean() 
print('mean of Z=',meanZ)
print('=======================================================')
Z1 = Z - meanZ
print('Z1=',Z1)
print('=======================================================')
## (Transpose the Z matrix and perform the mat multiplication Z and Z') 
Ztrans = np.transpose(Z1) 
print('Z Transpose=',Ztrans)
print('=======================================================')
rho = np.dot(Z1[:,None],Ztrans[None,:]) 
print('rho=',rho)
print('=======================================================')

l = len(data)
slist = []
for i in range(0,l):
    s = 0
    for j in range(0,l-i):
        s = s + rho[j+i][j]
    slist.append(s)
    print('s=',s)
    print('=======================================================')
    print('slist=',slist)
    print('=======================================================')

print('slist=',slist)
print('=======================================================')
plt.plot(range(0,l), slist)
plt.show()
###ENDOFSEGMENT###TSF-PACF_CODE
##HEADER##lag = 5
acvf_lags = slist[1:lag+1]
matr = np.zeros((lag, lag))
for i in range(0,lag) :
    for j in range(0,lag-i) :
        matr[j+i][j] = slist[i]
        matr[j][j+i] = slist[i]    
        print('matr=',matr)
        print('=======================================================')
        print('slist=',slist)
        print('=======================================================')
ainv = np.linalg.inv(matr)
result1 = np.matmul(ainv,acvf_lags)

print('a inverse=',ainv)
print('=======================================================')
print('result1=',result1)
print('=======================================================')
plt.plot(range(lag), result1)
plt.show()
###ENDOFSEGMENT###TSF-AR
##HEADER##train = sample['t'][:train_len]
ar_model = AutoReg(train, lags=2).fit()

print(ar_model.summary())
pred = ar_model.predict(start=train_len, end=num_samples, dynamic=False)
###ENDOFSEGMENT###TSF-MA
##HEADER##ma_model = ARMA(train, order=(0,1)).fit()

print(ma_model.summary())
pred = ma_model.predict(start=train_len, end=num_samples, dynamic=False)
###ENDOFSEGMENT###TSF-WN
##HEADER##sample = pd.DataFrame({'timestamp' : pd.date_range('2021-01-01', periods=48, freq='MS'),
                       't' : np.random.randint(1,101,len(time))
                      })
###ENDOFSEGMENT###TSF-RANDOMWALK
##HEADER##np.random.seed(42)

random_walk = [0]

for i in range(1, 48):
    # Movement direction based on a random number
    num = -1 if np.random.random() < 0.5 else 1
    random_walk.append(random_walk[-1] + num)
    
sample = pd.DataFrame({'timestamp' : pd.date_range('2021-01-01', periods=48, freq='MS'),
                       't' : random_walk
                      })

f, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 4))

sns.lineplot(x=sample.timestamp, y=sample['t'], marker='o')
ax.set_xlim([sample.timestamp.iloc[0], sample.timestamp.iloc[-1]])
ax.set_title('Sample Time Series')
plt.tight_layout()
plt.show()
###ENDOFSEGMENT###TSF-SIGNALS
##HEADER##theta_1 = 0.5
theta_2 = 0.5
phi_1 = 0.5
phi_2= -0.5
num_samples =  150

SEED = 42
np.random.seed(SEED)
# Visualizations
lag_acf = 15
lag_pacf = 15
height = 4
width = 12
T = 12
time = np.arange(0, 48)
random_walk = [0]

for i in range(1, 48):
    # Movement direction based on a random number
    num = -1 if np.random.random() < 0.5 else 1
    random_walk.append(random_walk[-1] + num)
    
f, ax = plt.subplots(nrows=10, ncols=3, figsize=(2*width, 10*height))

### AR(1) ###
np.random.seed(SEED)
ar = np.r_[1, -np.array([phi_1])] # add zero-lag and negate
ma = np.r_[1] # add zero-lag

sample = pd.DataFrame({'timestamp' : pd.date_range('2021-01-01', periods=num_samples, freq='MS'),
                       't' : sm.tsa.arima_process.arma_generate_sample(ar, ma, num_samples)
                      })

sns.lineplot(x=sample.timestamp, y=sample['t'], marker='o', ax=ax[0,0])
ax[0,0].set_xlim([sample.timestamp.iloc[0], sample.timestamp.iloc[-1]])
ax[0,0].set_title('Time Series for AR(1)')

plot_acf(sample['t'],lags=lag_acf, ax=ax[0, 1], title='ACF for AR(1)')
plot_pacf(sample['t'],lags=lag_pacf, ax=ax[0, 2], method='ols', title='PACF for AR(1)')
ax[0,2].annotate('Potential correlation at lag = 1', xy=(1, 0.6),  xycoords='data',
            xytext=(0.17, 0.75), textcoords='axes fraction',
            arrowprops=dict(color='red', shrink=0.05, width=1))

### AR(2) ###
np.random.seed(SEED)
ar = np.r_[1, -np.array([phi_1, phi_2])] # add zero-lag and negate
ma = np.r_[1] # add zero-lag

sample = pd.DataFrame({'timestamp' : pd.date_range('2021-01-01', periods=num_samples, freq='MS'),
                       't' : sm.tsa.arima_process.arma_generate_sample(ar, ma, num_samples)
                      })

sns.lineplot(x=sample.timestamp, y=sample['t'], marker='o', ax=ax[1,0])
ax[1,0].set_xlim([sample.timestamp.iloc[0], sample.timestamp.iloc[-1]])
ax[1,0].set_title('Time Series for AR(2)')

plot_acf(sample['t'],lags=lag_acf, ax=ax[1, 1], title='ACF for AR(2)')
plot_pacf(sample['t'],lags=lag_pacf, ax=ax[1, 2], method='ols', title='PACF for AR(2)')

ax[1, 2].annotate('Potential correlation at lag = 1', xy=(1, 0.36),  xycoords='data',
            xytext=(0.15, 0.7), textcoords='axes fraction',
            arrowprops=dict(color='red', shrink=0.05, width=1))

ax[1, 2].annotate('Potential correlation at lag = 2', xy=(2.1, -0.5),  xycoords='data',
            xytext=(0.25, 0.1), textcoords='axes fraction',
            arrowprops=dict(color='red', shrink=0.05, width=1))

### MA(1) ###
np.random.seed(SEED)
ar = np.r_[1] # add zero-lag and negate
ma = np.r_[1, np.array([theta_1])] # add zero-lag

sample = pd.DataFrame({'timestamp' : pd.date_range('2021-01-01', periods=num_samples, freq='MS'),
                       't' : sm.tsa.arima_process.arma_generate_sample(ar, ma, num_samples)
                      })    

sns.lineplot(x=sample.timestamp, y=sample['t'], marker='o', ax=ax[2,0])
ax[2,0].set_xlim([sample.timestamp.iloc[0], sample.timestamp.iloc[-1]])
ax[2,0].set_title('Time Series for MA(1)')

plot_acf(sample['t'],lags=lag_acf, ax=ax[2, 1], title='ACF for MA(1)')
plot_pacf(sample['t'],lags=lag_pacf, ax=ax[2, 2], method='ols', title='PACF for MA(1)')

ax[2,1].annotate('Potential correlation at lag = 1', xy=(1, 0.5),  xycoords='data',
            xytext=(0.15, 0.7), textcoords='axes fraction',
            arrowprops=dict(color='red', shrink=0.05, width=1))

### MA(2) ###
np.random.seed(SEED)
ar = np.r_[1] # add zero-lag and negate
ma = np.r_[1, np.array([theta_1, theta_2])] # add zero-lag

sample = pd.DataFrame({'timestamp' : pd.date_range('2021-01-01', periods=num_samples, freq='MS'),
                       't' : sm.tsa.arima_process.arma_generate_sample(ar, ma, num_samples)
                      })    

sns.lineplot(x=sample.timestamp, y=sample['t'], marker='o', ax=ax[3,0])
ax[3,0].set_xlim([sample.timestamp.iloc[0], sample.timestamp.iloc[-1]])
ax[3,0].set_title('Time Series for MA(2)')

plot_acf(sample['t'],lags=lag_acf, ax=ax[3, 1], title='ACF for MA(2)')
plot_pacf(sample['t'],lags=lag_pacf, ax=ax[3, 2], method='ols', title='PACF for MA(2)')

ax[3, 1].annotate('Potential correlation at lag = 1', xy=(1, 0.65),  xycoords='data',
            xytext=(0.15, 0.8), textcoords='axes fraction',
            arrowprops=dict(color='red', shrink=0.05, width=1))

ax[3, 1].annotate('Potential correlation at lag = 2', xy=(2, 0.5),  xycoords='data',
            xytext=(0.25, 0.7), textcoords='axes fraction',
            arrowprops=dict(color='red', shrink=0.05, width=1))

### Periodical ###
sample = pd.DataFrame({'timestamp' : pd.date_range('2021-01-01', periods=48, freq='MS'),
                       't' : [1, 2, 3, 4, 4.5, 5, 7, 8, 6, 4, 2, 2, 1, 2, 3, 4, 4.5, 5, 7, 8, 6, 4, 2, 2, 1, 2, 3, 4, 4.5, 5, 7, 8, 6, 4, 2, 2, 1, 2, 3, 4, 4.5, 5, 7, 8, 6, 4, 2, 2]
                      })

sns.lineplot(x=sample.timestamp, y=sample['t'], marker='o', ax=ax[4,0])
ax[4,0].set_xlim([sample.timestamp.iloc[0], sample.timestamp.iloc[-1]])
ax[4,0].set_title('Time Series for Periodical')

plot_acf(sample['t'],lags=lag_acf, ax=ax[4, 1], title='ACF for Periodical')
plot_pacf(sample['t'],lags=lag_pacf, ax=ax[4, 2], method='ols', title='PACF for Periodical')

ax[4,2].axvline(x=T, color='r', linestyle='--')

### Trend ###
sample = pd.DataFrame({'timestamp' : pd.date_range('2021-01-01', periods=48, freq='MS'),
                       't' : ((0.05*time)+20)
                      })

sns.lineplot(x=sample.timestamp, y=sample['t'], marker='o', ax=ax[5,0])
ax[5,0].set_xlim([sample.timestamp.iloc[0], sample.timestamp.iloc[-1]])
ax[5,0].set_title('Time Series for Trend (NON-STATIONARY!)')

plot_acf(sample['t'],lags=lag_acf, ax=ax[5, 1], title='ACF for Trend (applied to non-stationary)')
plot_pacf(sample['t'],lags=lag_pacf, ax=ax[5, 2], method='ols', title='PACF for Trend (applied to non-stationary)')

### White Noise ###
sample = pd.DataFrame({'timestamp' : pd.date_range('2021-01-01', periods=48, freq='MS'),
                       't' : np.random.randint(1,101,len(time))
                      })

sns.lineplot(x=sample.timestamp, y=sample['t'], marker='o', ax=ax[6,0])
ax[6,0].set_xlim([sample.timestamp.iloc[0], sample.timestamp.iloc[-1]])
ax[6,0].set_title('Time Series for White Noise')

plot_acf(sample['t'],lags=lag_acf, ax=ax[6, 1], title='ACF for White Noise')
plot_pacf(sample['t'],lags=lag_pacf, ax=ax[6, 2], method='ols', title='PACF for White Noise')

### Random-Walk ###
sample = pd.DataFrame({'timestamp' : pd.date_range('2021-01-01', periods=48, freq='MS'),
                       't' : random_walk
                      })

sns.lineplot(x=sample.timestamp, y=sample['t'], marker='o', ax=ax[7,0])
ax[7,0].set_xlim([sample.timestamp.iloc[0], sample.timestamp.iloc[-1]])
ax[7,0].set_title('Time Series for Random-Walk (NON-STATIONARY!)')

plot_acf(sample['t'],lags=lag_acf, ax=ax[7, 1], title='ACF for Random-Walk (applied to non-stationary)')
plot_pacf(sample['t'],lags=lag_pacf, ax=ax[7, 2], method='ols', title='PACF for Random-Walk (applied to non-stationary)')

sample['t_diff'] = sample['t'].diff().fillna(0)

plot_acf(sample['t_diff'],lags=lag_acf, ax=ax[8, 1], title='ACF for Random-Walk (applied to differenced/stationary)')
plot_pacf(sample['t_diff'],lags=lag_pacf, ax=ax[8, 2], method='ols', title='PACF for Random-Walk (applied to differenced/stationary)')


### Constant ###
sample = pd.DataFrame({'timestamp' : pd.date_range('2021-01-01', periods=48, freq='MS'),
                       't' : 5
                      })

sns.lineplot(x=sample.timestamp, y=sample['t'], marker='o', ax=ax[9,0])
ax[9,0].set_xlim([sample.timestamp.iloc[0], sample.timestamp.iloc[-1]])
ax[9,0].set_title('Time Series for Constant (NON-STATIONARY!)')

plot_acf(sample['t'],lags=lag_acf, ax=ax[9, 1], title='ACF for Constant (applied to non-stationary)')
plot_pacf(sample['t'],lags=lag_pacf, ax=ax[9, 2], method='ols', title='PACF for Constant (applied to non-stationary)')

for i in range(9):
    ax[i, 1].set_ylim([-1.1, 1.1])
    ax[i, 2].set_ylim([-1.1, 1.1])

    
f.delaxes(ax[8, 0])
plt.tight_layout()
plt.show()
###ENDOFSEGMENT###TSF-COMPARE
##HEADER##plt.figure(figsize=(15,5))
plt.plot(train.index, train[""Gasoline Prices""], label='Training Data')
plt.plot(test.index, test['Gasoline Prices'], label='Test Data')
plt.plot(test.index, test[""Pred_MA_11_cumsum""], label='Predictions -MA(11)')
plt.plot(test.index, test[""Pred_AR_20_cumsum""], label='Predictions -AR(20)')
plt.title(""All model comparison"")
plt.legend()
plt.show()
###ENDOFSEGMENT###TSF-VAR
##HEADER##from statsmodels.tsa.vector_ar.var_model import VAR
model=VAR(train)
model_results=model.fit(5)
model_results.summary()
model_results.forecast(train.values,steps=20)

###ENDOFSEGMENT###TSF-VARMA
##HEADER##model = VARMAX(train, order=(1,2), trend='c') # c indicates a constant trend
results = model.fit(maxiter=1000, disp=False)
results.summary()
df_forecast = results.forecast(12) 
df_forecast
df_forecast['Money1d'] = (df['Money'].iloc[-nobs-1]-df['Money'].iloc[-nobs-2]) + df_forecast['Money'].cumsum()
# Now build the forecast values from the first difference set
df_forecast['MoneyForecast'] = df['Money'].iloc[-nobs-1] + df_forecast['Money'].cumsum()


model = VARMAX(train2_diff[[ 'Open', 'High', 'Low', 'Close' ]], order=(0,2)).fit( disp=False)
result = model.forecast(steps = 30)
###ENDOFSEGMENT###TSF-AUTOARIMA
##HEADER##pip install pmdarima
from pmdarima import auto_arima
auto_arima(df_cons[""Money""])


pq = []
for name, column in train2_diff[[ 'Open', 'High', 'Low', 'Close'  ]].iteritems():
    print(f'Searching order of p and q for : {name}')
    stepwise_model = auto_arima(train2_diff[name],start_p=1, start_q=1,max_p=7, max_q=7, seasonal=False,
        trace=True,error_action='ignore',suppress_warnings=True, stepwise=True,maxiter=1000)
    parameter = stepwise_model.get_params().get('order')
    print(f'optimal order for:{name} is: {parameter} \n\n')
    pq.append(stepwise_model.get_params().get('order'))
###ENDOFSEGMENT###TSF-ARIMA
##HEADER##from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima

from matplotlib import pyplot
# load dataset
auto_arima_model=auto_arima(y_train,trace=True,Supress_warnings=True)
arima_model_202 = ARIMA(y_train, order=(3,1,3)).fit()
arima_model_202.summary()

pred_future_10101=arima_model_202.predict(start=len(dataset)+1,end=len(dataset)+(180),dynamic=False)
print(""The length of pred_future values :"",len(pred_future_10101))
pred_future_10101
###ENDOFSEGMENT###TSF-WALK
##HEADER##history = [x for x in y_train]
predictions = list()
from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning
warnings.simplefilter('ignore', ConvergenceWarning)
from math import sqrt
# walk-forward validation
for t in range(len(y_test)):
	model = ARIMA(history, order=(3,1,3))
	model_fit = model.fit()
	output = model_fit.forecast()
	yhat = output[0]
	predictions.append(yhat)
	obs = y_test[t]
	history.append(obs)
	print('predicted=%f, expected=%f' % (yhat, obs))
# evaluate forecasts
rmse = sqrt(mean_squared_error(y_test, predictions))
print('Test RMSE: %.3f' % rmse)
###ENDOFSEGMENT###TSF-LEAST
##HEADER##x=df[""Open""].values
y=np.append([None],x[:-1])
len(x),len(y)
x=x[1:]
y=y[1:]
n=len(x)

A=[[x.sum(),n],
   [(x**2).sum(),x.sum()]]
B=[y.sum(),(x *y).sum()]

A=[
      [( x ** 2).sum(), x.sum(),      len(x)],
      [( x ** 3).sum(), ( x ** 2).sum(),  x.sum()],
      [( x ** 4).sum(), ( x ** 3).sum(),  ( x ** 2).sum()],
    ]
B =[y.sum(),(x * y).sum(),(x * x*  y).sum()]
A_inv=np.linalg.inv(A)
order=A_inv.dot(B)
order

from scipy.optimize import curve_fit
def func(x, a, b,c):
    y = a*x*x + b * x +   c
    return y

alpha = curve_fit(func, xdata = x, ydata = y)[0]
print(alpha)
plt.scatter(x, y,color=""red"")
plt.plot(x, pred1,color=""blue"")
###ENDOFSEGMENT###TSP-MOVING
##HEADER##roll=50
df_a=df[""Open""].copy()
mov_avg=[]
for i in range(0,roll-1):
    mov_avg.append(np.NaN)

for i in range(roll-1,df_a.shape[0]):
    sum=0
    for j in range(i,i-roll,-1):
        sum+=df.iloc[j][""Open""]
    mov_avg.append(sum/roll)
    
pd.concat([df_a,pd.DataFrame(mov_avg,columns=[""MA""],index=df_a.index)],axis=1)
###ENDOFSEGMENT###


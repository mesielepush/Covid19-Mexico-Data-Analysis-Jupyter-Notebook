import pandas as pd
import numpy as numpy
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import OrderedDict
from constants import *
plt.style.use('seaborn-whitegrid')

class Covid:
    
    database = {'confirmed'   : '',
                'suspicious'  : '',
                'negatives'   : '',
                'deaths'      : '',
                'patients'    : ''}

    
    def __init__(self,state):
        if state.lower() in ['national','nacional','all','country']:
            self.state = 'Nacional'
        elif state.lower() in ['cdmx', 'distritofederal', 'df', 'ciudad de mexico']:
            self.state = 'DISTRITO FEDERAL'
        elif state.upper() not in cdns_states:
            print_state_names()
            return
        else:
            self.state = state.upper()
        self.state_code = inverse_dict_for_name_states[self.state]

    def discrete(self,data_type):
        data =  pd.read_csv(Covid.database[data_type], encoding='ANSI')
        
        return data.loc[data['nombre'] == self.state].values[0][3:]
    
    def cummulative(self,data_type):
        data =  pd.read_csv(Covid.database[data_type], encoding='ANSI')

        cummulative = []
        raw = data.loc[data['nombre'] == self.state]
        
        for i in raw.values[0][3:]:
            if len(cummulative) == 0:
                cummulative.append(i)
            else:
                cummulative.append(i+cummulative[-1])
        return cummulative 
    
    def actives(self,window=14):
               
        if self.state == 'Nacional':
            data = pd.read_csv(Covid.database['patients'], encoding='ANSI')
            data = change_df_names(data)
        else:
            data = pd.read_csv(Covid.database['patients'], encoding='ANSI')
            data = change_df_names(data)
            data = data[data['lives_at'] == self.state_code]
        
        data = data[data['result']==1]
        data['onset_symptoms'] = pd.to_datetime(data['onset_symptoms'])
        
        set_dates = set(data['onset_symptoms'])
        timeline= pd.date_range(start=min(set_dates), end = data['Updated_at'].iloc[0])
        result = {key:0 for key in timeline}
        
        for ind, day_active in enumerate(data['onset_symptoms']):
            for _ in range(window):
                if day_active not in timeline:
                    break
                elif data['day_of_death'].iloc[ind] != '9999-99-99' and day_active > pd.to_datetime(data['day_of_death'].iloc[ind]):
                    break
                else:
                    result[day_active] +=1
                    day_active = day_active + timedelta(days=1)
        
        new_data = pd.DataFrame()
        new_data['actives'] = result.values()
        new_data['dates']   = result.keys()
        new_data = new_data.set_index('dates',drop=True)
        
        return new_data

    class patients(self,state):
        raw_data = change_df_names(pd.read_csv(Covid.database['patients'], encoding='ANSI'))

        def __init__(self):
            if self.state == 'Nacional':
                self.data = patients.raw_data
            else:
                self.data = patients.raw_data[patients.raw_data['lives_at']==self.state_code]

    def population(self):
        data = pd.read_csv(Covid.database['confirmed'])
        return data[data['nombre']==self.state].poblacion.values[0]

    @staticmethod
    def cohens_d(data1,data2):
        from numpy import mean, var, sqrt
        mean1 = mean(data1)
        mean2 = mean(data2)
        var1  = var(data1)
        var2  = var(data2)
            
        numerator = mean1 - mean2
        
        len1 = len(data1)-1
        len2 = len(data2)-1
        
        total_var = (len1*var1) + (len2*var2)
        total_len = len1 + len2
        
        denominator = sqrt(total_var / total_len)
            
        return numerator / denominator

    @staticmethod
    def plot_actives(data,names,trim=0):
        plt.close('all')
        plt.rcParams["figure.figsize"] = (15,7)
        
        if type(data) == pd.core.frame.DataFrame:
            new_index = pd.date_range(start=data.index[0], end=data.index[-1])
            
            plt.plot([str(x)[5:11] for x in new_index],data['actives'],label=names)
            plt.scatter(list(range(0,len(data.index)))[-1],data['actives'].iloc[-1])
            plt.text(list(range(0,len(data.index)))[-1],data['actives'].iloc[-1],str(data['actives'].iloc[-1]))
            
        else:
            
            first_day = min([min(x.index) for x in data])
            last_day = max([max(x.index) for x in data])

            new_index = pd.date_range(start=first_day, end=last_day)

            for ind, dataframe in enumerate(data):
                if len(dataframe) != len(new_index):
                    plt.plot([str(x)[5:11] for x in new_index],[0]*(len(new_index)-len(dataframe))+list(dataframe['actives']),label=names[ind])
                    
                else:
                    plt.plot([str(x)[5:11] for x in new_index],dataframe['actives'],label=names[ind])
                plt.scatter(list(range(0,len(new_index)))[-1],dataframe['actives'].iloc[-1])
                plt.text(list(range(0,len(new_index)))[-1],dataframe['actives'].iloc[-1],str(dataframe['actives'].iloc[-1]))

        plt.xticks(rotation=90, fontsize=12)
        plt.xlim(trim,)
        plt.legend(fontsize=14,loc=2)
        plt.show()
    
    @staticmethod
    def plot_cummulative(data, names = None, title = None, trim=None):
        plt.close('all')
        plt.rcParams["figure.figsize"] = (15,7)
        
        if type(data[0]) == int:
            index = pd.date_range(start=pd.to_datetime(pd.read_csv(Covid.database['confirmed']).columns[-1]) - timedelta(days=len(data)),periods = len(data),freq='D')
            plt.plot(index, data, label = names, alpha = 0.6)
            plt.scatter(index[-1],data[-1])
            plt.text(index[-1], data[-1],str(int(data[-1])) , fontsize=14)
        else:
            
            max_len = max([len(x) for x in data])
            index = pd.date_range(start=pd.to_datetime(pd.read_csv(Covid.database['confirmed']).columns[-1]) - timedelta(days=max_len),
                                periods=max_len, freq='D')
            
            for ind,i in enumerate(data):
                if len(i) != max_len:
                    i = [0]*(max_len-len(i))+i

                plt.plot(index,i,label=names[ind])
                plt.scatter(index[-1],i[-1])
                plt.text(index[-1], i[-1],str(int(i[-1])) , fontsize=14)
                

        plt.xticks(rotation=90,fontsize=13)
        plt.title(title, fontsize=14)
        
        if trim:
            plt.xlim(index[0] + timedelta(days=trim),)
            
        plt.legend(loc='upper left',fontsize=14)
        plt.show()

    @staticmethod
    def plot_discrete(data, names = None, title=None, trim=None):
        plt.close('all')
        plt.rcParams["figure.figsize"] = (15,6)
        
        if type(data) == np.ndarray:
            index = pd.date_range(start=pd.to_datetime(pd.read_csv(Covid.database['confirmed']).columns[-1]) - timedelta(days=len(data)),periods = len(data),freq='D')
                    
            plt.bar(index,data, label = names, alpha = 0.6)
            
        else:
            
            max_len = max([len(x) for x in data])
            index = pd.date_range(start=pd.to_datetime(pd.read_csv(Covid.database['confirmed']).columns[-1]) - timedelta(days=len(data)), periods=max_len, freq='D')

            for ind, i in enumerate(data):
                if len(i) < max_len:
                    i = [0]*(max_len-len(i))+list(i)

                plt.bar(index,i, label = names[ind],alpha = 0.5)
        
        plt.title(title, fontsize=14)
        plt.legend(loc='upper left',fontsize=12)
        plt.xticks(rotation=90)
        if trim:
            plt.xlim(index[0] + timedelta(days=trim),)
        plt.show()

    @classmethod
    def update_data(cls,databases_dir):
        cls.database  = databases_dir

    @classmethod
    def get_max_to_min(cls,dtype, include_national = False, max_to_min = True,window=14):
                
        if dtype not in ['confirmed','negatives','deaths','suspicious','actives']:
            dtype_error(dtype)
            return
        if include_national:
            names = cdns_states
        else:
            names = [x for x in cdns_states if x != 'Nacional']
        
        if dtype in ['confirmed','negatives','deaths','suspicious']:
            dictionary = {x:sum(cls(x).discrete(dtype)) for x in names}
            return OrderedDict(sorted(dictionary.items(), key=lambda t: t[1],reverse=max_to_min))
        else:
            dictionary = {x:sum(cls(x).actives(window=window).iloc[-1]) for x in names}
            return OrderedDict(sorted(dictionary.items(), key=lambda t: t[1],reverse=max_to_min))

    @classmethod
    def plot_max_to_min(cls,dtype,n=None,title=None, trim=None, include_national = False, max_to_min = True):
        if dtype not in ['confirmed','negatives','deaths','suspicious','actives']:
            dtype_error(dtype)
            return
        if include_national:
            names = cdns_states
        else:
            names = [x for x in cdns_states if x != 'Nacional']
        
        if dtype == 'actives':
            data = {key:Covid(key).actives() for key in names}
            data = OrderedDict(sorted(data.items(), key=lambda t: t[1].actives.iloc[-1],reverse=max_to_min))
            names = list(data.keys())[:n]

            plt_actives([data[name] for name in names],names,trim=trim)


        else:
            data = {key:Covid(key).cummulative(dtype) for key in names}
            data = OrderedDict(sorted(data.items(), key=lambda t: t[1][-1],reverse=True))
            names = list(data.keys())[:n]

            plot_cummulative([data[name] for name in names],names,trim=trim)



def get_age_bins(data,bin_size):
    
    current = 0
    bin_size = bin_size
    iterations = int(max(data['age'])/bin_size)
    result = {}

    while iterations >= 0:
        result[f'{current}-{current+(bin_size-1)}'] = 0

        for i in range(current,current+bin_size):
            result[f'{current}-{current+(bin_size-1)}'] += list(data['age']).count(i)
        current += bin_size
        iterations -= 1
    return result

def get_proportions(death_histogram,patients_histogram):
    result = {}
    for i in patients_histogram.keys():
        try:
            result[i]= (death_histogram[i]/patients_histogram[i])*100
        except:
            result[i]=0
    return result



def get_illness_proportions(data):
    from collections import OrderedDict
    result = {}
    for i in data.keys():
        result[i] = list(data[i].values).count(1)/len(data[i])*100
    result = OrderedDict(sorted(result.items(), key=lambda t: t[1],reverse=False))   
    return result

def get_active_database(raw_data,state,window):
    import pandas as pd
    from datetime import datetime, timedelta
    try:
        state_code = inverse_dict_for_name_states[state]
    except:
        print('ERROR, the state name is not in the database please check again')
        print('List of state names available: ')
        print('###########')
        print(inverse_dict_for_name_states.keys())
        return
    if state == 'ESTADOS UNIDOS MEXICANOS':
        data = raw_data
    else:
        data = raw_data[raw_data['lives_at'] == state_code]
    
    data = data[data['result']!=2]
    dates = data['onset_symptoms']
    dates = pd.to_datetime(dates)
    data = data.drop('onset_symptoms',axis = 1)
    data['onset_symptoms'] = dates
    infection_window = pd.to_datetime(datetime.today() - timedelta(days=window))
    data = data[data['onset_symptoms']>infection_window]
    return data

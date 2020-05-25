import pandas as pd
import numpy as numpy
from datetime import datetime, timedelta
from constants import *

class Covid:
    
    database = {'confirmed'   : '',
                'suspicious'  : '',
                'negatives'   : '',
                'deaths'      : '',
                'patients'    : ''}

    @classmethod
    def update_confirmed(cls,databases_dir):
        cls.database  = databases_dir

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
    
    def active(self,window=14):
               
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







def plt_actives(data,names,trim=0):
    import matplotlib.pyplot as plt
    plt.close('all')
    plt.style.use('seaborn-whitegrid')
    plt.rcParams["figure.figsize"] = (15,7)
    
    if type(data) == pd.core.frame.DataFrame:
        plt.plot([str(x)[5:11] for x in data.index],data['actives'],label=names,color ='b')
        plt.scatter([str(x)[5:11] for x in data.index][-1],data.actives[-1],color='b')
        plt.text([str(x)[5:11] for x in data.index][-1],data.actives[-1],str(data.actives[-1]) , fontsize=14 ,color='black')
    else:
        
        first_day = min([min(x.index) for x in data])
        last_day = max([max(x.index) for x in data])

        new_index = pd.date_range(start=first_day, end=last_day)

        for ind, dataframe in enumerate(data):
            if len(dataframe) != len(new_index):
                plt.plot([str(x)[5:11] for x in new_index],[0]*(len(new_index)-len(dataframe))+list(dataframe['actives']),label=names[ind])
                
            else:
                plt.plot([str(x)[5:11] for x in new_index],dataframe['actives'],label=names[ind])
            plt.scatter([str(x)[5:11] for x in new_index][-1],dataframe.actives[-1])
            plt.text([str(x)[5:11] for x in new_index][-1],dataframe.actives[-1],str(dataframe.actives[-1]) , fontsize=14,color='black')
    
    plt.xticks(rotation=90, fontsize=12)
    plt.xlim(trim,)
    plt.legend(fontsize=14)
    plt.show()



def get_max_to_min(raw_data, include_national = False, reverse = False, patient_data = False):

    dic = {}
    
    if patient_data == False:

        if include_national:
            names = raw_data.nombre
        else:
            names = [x for x in raw_data.nombre if x != 'Nacional']
    else:
        names = [patients_codes['states'][x] for x in set(raw_data.treated_at)]

    for name in names:
        
        if patient_data:
            result = list(raw_data['treated_at']).count(inverse_dict_for_name_states[name])
        else:
            result = raw_data.loc[raw_data['nombre'] == name].values[0][3:].sum()
                
        if result in dic.keys():
            dic[result+0.01] = name
        else:
            dic[result] = name
    if reverse:
        dic_sort = sorted(dic.keys(),reverse=False)
    else:
        dic_sort = sorted(dic.keys(),reverse=True)

    true_dic = {dic[key]:key for key in dic.keys()}

    return [dic[x] for x in dic_sort],true_dic

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

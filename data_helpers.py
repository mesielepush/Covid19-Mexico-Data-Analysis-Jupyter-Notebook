patients_codes = {
        'origin': {
            1: 'viral respiratory disease monitor unit - USMER',
            2: 'outside USMER',
            99: 'no specified'
        },
        'sector':{
            1 : 'red cross',
            2 : 'Integral Family Development System (DIF)',
            3 : 'state',
            4 : 'Mexican Institute for Social Security (IMSS)',
            5 : 'IMSS-BIENESTAR',
            6 : 'Institute for Social Security and Services for State Workers (ISSSTE)',
            7 : 'county',
            8 : 'Mexican Oil (PEMEX)',
            9 : 'Private',
            10 : 'National Secretary of Defense (SEDENA)',
            11 : 'Secretary of Sea (SEMAR)',
            12 : 'Secretary of Health (SSA)',
            13 : 'University',
            99 : 'no specified'
        },
        'sex': {
            1: 'women',
            2: 'man',
            99: 'no specified'
        },
        'patient_type': {
            1: 'outpatient',
            2: 'hospitalized',
            99: 'no specified'
        },
        'is_mexican': {
            1: 'mexican',
            2: 'alien',
            99: 'no specified'
        },
        'result': {
            1: 'Positive for SARS-CoV-2',
            2: 'Negative for SARS-CoV-2',
            3: 'Result Pending'
        },
        'states':{
            1:  'AGUASCALIENTES',
            2:  'BAJA CALIFORNIA',
            3:  'BAJA CALIFORNIA SUR',
            4:  'CAMPECHE',
            5:  'COAHUILA DE ZARAGOZA',
            6:  'COLIMA',
            7:  'CHIAPAS',
            8:  'CHIHUAHUA',
            9:  'CIUDAD DE MÉXICO',
            10: 'DURANGO',
            11: 'GUANAJUATO',
            12: 'GUERRERO',
            13: 'HIDALGO',
            14: 'JALISCO',
            15: 'MÉXICO',
            16: 'MICHOACÁN DE OCAMPO',
            17: 'MORELOS',
            18: 'NAYARIT',
            19: 'NUEVO LEÓN',
            20: 'OAXACA',
            21: 'PUEBLA',
            22: 'QUERÉTARO',
            23: 'QUINTANA ROO',
            24: 'SAN LUIS POTOSÍ',
            25: 'SINALOA',
            26: 'SONORA',
            27: 'TABASCO',
            28: 'TAMAULIPAS',
            29: 'TLAXCALA',
            30: 'VERACRUZ DE IGNACIO DE LA LLAVE',
            31: 'YUCATÁN',
            32: 'ZACATECAS',
            36: 'ESTADOS UNIDOS MEXICANOS',
            97: 'not apply',
            98: 'unknown',
            99: 'not specified',

        },
        'boolean':{
            1: 'yes',
            2: 'no',
            97: 'not apply',
            98: 'unknown',
            99: 'no specified'
        }
    }

inverse_dict_for_name_states = {patients_codes['states'][i]: i for i in patients_codes['states'].keys()}

def patient_data_keys(column_name,key = None):
    """ Takes the name of a column and decodes the keys from the database: 
    '200XXXCOVID19MEXICO.csv' """
    
    if column_name in ['treated_at','borne_at','lives_at']:
        
        if key:
            return patients_codes['states'][key]
        else:
            print('KEYS for ', column_name.upper(),':')
            for i in patients_codes['states'].keys():
                print('Key: ', i, ' : ', patients_codes['states'][i])
                
    elif column_name in ['intubated', 'pneumonia','pregnancy',
                        'speaks_dialect', 'diabetes', 'copd',
                        'asthma','immunosuppression', 'hypertension',
                        'another_illness','cardiovascular', 'obesity',
                        'kidney_disease', 'smoker','close_to_infected',
                        'migrant','icu']:
        if key:
            return patients_codes['boolean'][key]
            
        else:
            print('KEYS for ', column_name.upper(),':')
            for i in patients_codes['boolean'].keys():
                print('Key: ', i, ' : ', patients_codes['boolean'][i])
                
    else:
        if column_name not in patients_codes.keys():
            print('ERROR: Column name not in the data base, please check')
            return
        
        if key:
            return patients_codes[column_name][key]
         
        else:
            print('KEYS for ', column_name.upper(),':')
            for i in patients_codes[column_name].keys():
                print('Key: ', i, ' : ', patients_codes[column_name][i])

def get_discrete(name,raw_data):
    if name == 'National':
        name = 'Nacional'
    return raw_data.loc[raw_data['nombre'] == name].values[0][3:]

def get_cummulative(name,raw_data):
    if name == 'National':
        name = 'Nacional'
    cummulative = []
    raw = raw_data.loc[raw_data['nombre'] == name]
    
    for i in raw.values[0][3:]:
        if len(cummulative) == 0:
            cummulative.append(i)
        else:
            cummulative.append(i+cummulative[-1])
    return cummulative

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

def get_cummulative_actives(raw_data,state,window):
    import pandas as pd
    from datetime import datetime, timedelta
    
    if state in ['ESTADOS UNIDOS MEXICANOS', 'NATIONAL', 'National',' Nacional']:
        data = raw_data
    else:
        
        try:
            state_code = inverse_dict_for_name_states[state]
        except:
            print('###########')
            print('ERROR, the state name is not in the database please check again')
            print('List of state names available: ')
            print('###########')
            print(inverse_dict_for_name_states.keys())
            return
        data = raw_data[raw_data['lives_at'] == state_code]
    
    
    data = data[data['result']!=2]
    dates = data['onset_symptoms']
    dates = pd.to_datetime(dates)
    data = data.drop('onset_symptoms',axis = 1)
    data['onset_symptoms'] = dates
    
    set_dates = set(dates)
    timeline= pd.date_range(start=min(set_dates), end =data['Updated_at'].iloc[0])
    result = {key:0 for key in timeline}
    
    for ind, day_active in enumerate(data['onset_symptoms']):
        for _ in range(14):
            if day_active not in timeline:
                continue
            elif day_active == data['day_of_death'].iloc[ind]:
                continue
            else:
                result[day_active] +=1
                day_active = day_active + timedelta(days=1)
    
    new_data = pd.DataFrame()
    new_data['actives']=result.values()
    new_data['dates'] = result.keys()
    new_data = new_data.set_index('dates',drop=True)
    
    return new_data
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

def get_max_to_min(raw_data,n=None,discrete=True,include_national=False):
    dic = {}
    
    if include_national:
        names = raw_data.nombre
    else:
        names = [x for x in raw_data.nombre if x != 'Nacional']

    for i in names:
        
        if discrete:
            result = get_discrete(i,raw_data).sum()
        else:
            result = get_cummulative(i,raw_data)[-1]
        
        if result in dic.keys():
            dic[result+0.01] = i
        else:
            dic[result] = i

    dic_sort = sorted(dic.keys(),reverse=True)
    sorted_names = [dic[x] for x in dic_sort][:n]
    
    if discrete:
        return [get_discrete(x,raw_data) for x in sorted_names], sorted_names
    else:
        return [get_cummulative(x,raw_data) for x in sorted_names], sorted_names

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
    mean1 = np.mean(data1)
    mean2 = np.mean(data2)
    var1  = np.var(data1)
    var2  = np.var(data2)
        
    numerator = mean1 - mean2
    
    len1 = len(data1)-1
    len2 = len(data2)-1
    
    total_var = (len1*var1) + (len2*var2)
    total_len = len1 + len2
    
    denominator = np.sqrt(total_var / total_len)
        
    return numerator / denominator

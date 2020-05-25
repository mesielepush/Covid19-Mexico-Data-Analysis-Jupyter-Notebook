patients_codes = {
        'origin': {
            1: 'viral respiratory disease monitor unit - USMER',
            2: 'outside USMER',
            99: 'no specified'
        },
        'sector':{
            1 : 'red cross',
            2 : 'DIF',
            3 : 'state',
            4 : 'IMSS',
            5 : 'IMSS-BIENESTAR',
            6 : 'ISSSTE',
            7 : 'county',
            8 : 'PEMEX',
            9 : 'Private',
            10 : 'SEDENA',
            11 : 'SEMAR',
            12 : 'SSA',
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
            5:  'COAHUILA',
            6:  'COLIMA',
            7:  'CHIAPAS',
            8:  'CHIHUAHUA',
            9:  'DISTRITO FEDERAL',
            10: 'DURANGO',
            11: 'GUANAJUATO',
            12: 'GUERRERO',
            13: 'HIDALGO',
            14: 'JALISCO',
            15: 'MEXICO',
            16: 'MICHOACAN',
            17: 'MORELOS',
            18: 'NAYARIT',
            19: 'NUEVO LEON',
            20: 'OAXACA',
            21: 'PUEBLA',
            22: 'QUERETARO',
            23: 'QUINTANA ROO',
            24: 'SAN LUIS POTOSI',
            25: 'SINALOA',
            26: 'SONORA',
            27: 'TABASCO',
            28: 'TAMAULIPAS',
            29: 'TLAXCALA',
            30: 'VERACRUZ',
            31: 'YUCATAN',
            32: 'ZACATECAS',
            36: 'Nacional',
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

cdns_states = ['AGUASCALIENTES',
                'BAJA CALIFORNIA',
                'BAJA CALIFORNIA SUR',
                'CAMPECHE',
                'CHIAPAS',
                'CHIHUAHUA',
                'DISTRITO FEDERAL',
                'COAHUILA',
                'COLIMA',
                'DURANGO',
                'GUANAJUATO',
                'GUERRERO',
                'HIDALGO',
                'JALISCO',
                'MEXICO',
                'MICHOACAN',
                'MORELOS',
                'NAYARIT',
                'NUEVO LEON',
                'OAXACA',
                'PUEBLA',
                'QUERETARO',
                'QUINTANA ROO',
                'SAN LUIS POTOSI',
                'SINALOA',
                'SONORA',
                'TABASCO',
                'TAMAULIPAS',
                'TLAXCALA',
                'VERACRUZ',
                'YUCATAN',
                'ZACATECAS',
                'Nacional']

inverse_dict_for_name_states = {patients_codes['states'][i]: i for i in patients_codes['states'].keys()}

def print_state_names():
    print('####')
    print('ERROR: State Name not in database')
    print('Available state names: ')
    print('####')
    for name in cdns_states:
        print('..............')
        print(f':: {name} ::')

def change_df_names(patient_data):

    patient_data = patient_data.rename(columns={"FECHA_ACTUALIZACION":"Updated_at",
                                             "ID_REGISTRO": "id",
                                             "ORIGEN":"origin",
                                             "SECTOR":"sector",
                                             "ENTIDAD_UM": "treated_at",
                                             "SEXO": "sex",
                                             "ENTIDAD_NAC":"borne_at",
                                             "ENTIDAD_RES": "lives_at",
                                             "TIPO_PACIENTE": "pacient_type",
                                             "FECHA_INGRESO":"admission_date",
                                             "FECHA_SINTOMAS":"onset_symptoms",
                                             "FECHA_DEF": "day_of_death",
                                             "INTUBADO": "intubated",
                                             "NEUMONIA":"pneumonia",
                                             "EDAD":"age",
                                             "NACIONALIDAD":"is_mexican",
                                             "EMBARAZO":"pregnancy",
                                             "HABLA_LENGUA_INDIG":"speaks_dialect",
                                             "DIABETES":"diabetes",
                                             "EPOC": "copd",
                                             "ASMA":"asthma",
                                             "INMUSUPR":"immunosuppression",
                                             "HIPERTENSION":"hypertension",
                                             "OTRA_COM":"another_illness",
                                             "CARDIOVASCULAR":"cardiovascular",
                                             "OBESIDAD":"obesity",
                                             "RENAL_CRONICA":"kidney_disease",
                                             "TABAQUISMO":"smoker",
                                             "OTRO_CASO":"close_to_infected",
                                             "RESULTADO":"result",
                                             "MIGRANTE":"migrant",
                                             "PAIS_NACIONALIDAD":"nationality",
                                             "PAIS_ORIGEN": "country_of_origin",
                                             "UCI":"icu"})
    return patient_data

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
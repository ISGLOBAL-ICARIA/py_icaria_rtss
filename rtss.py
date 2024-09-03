
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import redcap
import params
import tokens
import gspread
from gspread_dataframe import set_with_dataframe

def all_participants_grater_than(months=6,when=['15-04-2024','15-04-2024','16-04-2024']):
    """
    Used to predict the number of childs affected by the RTSS vaccination
    started in Tonkolili and Port Loko on 15-04-2024, and Bombali on 16-04-2024.

    :param months: MoA threshold
    :param when: started_points per district
    :return:
    """
    list_records_vaccine,bombali_number, tonkolili_number, portloko_number = [],[],[],[]
    tonkolili_start_date = datetime.strptime(when[0],'%d-%m-%Y') - relativedelta(months=months)
    portloko_start_date = datetime.strptime(when[1],'%d-%m-%Y') - relativedelta(months=months)
    bombali_start_date = datetime.strptime(when[2],'%d-%m-%Y') - relativedelta(months=months)

    dict_ages = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    for project_name in tokens.REDCAP_PROJECTS_ICARIA:
        print(project_name)
        project = redcap.Project(tokens.URL, tokens.REDCAP_PROJECTS_ICARIA[project_name])
        df = project.export_records(format_type='df', fields=['child_dob'],events=['epipenta1_v0_recru_arm_1'])
        if project_name in params.district_HF['Bombali']:
            start_date = when[2]
            from_date = bombali_start_date
            bombali_number += list(df[df['child_dob']>datetime.strftime(from_date,'%Y-%m-%d')].reset_index()['record_id'])
        elif project_name in params.district_HF['Tonkolili']:
            start_date = when[2]
            from_date = tonkolili_start_date
            tonkolili_number += list(df[df['child_dob']>datetime.strftime(from_date,'%Y-%m-%d')].reset_index()['record_id'])
        else:
            start_date = when[0]
            from_date = portloko_start_date
            portloko_number += list(df[df['child_dob']>datetime.strftime(from_date,'%Y-%m-%d')].reset_index()['record_id'])
        list_records_vaccine+= list(df[df['child_dob']>datetime.strftime(from_date,'%Y-%m-%d')].reset_index()['record_id'])
        df_lower_months = df[df['child_dob'] > datetime.strftime(from_date,'%Y-%m-%d')].reset_index()['child_dob']
        for el in df_lower_months:
            rd=relativedelta(datetime.strptime(start_date,'%d-%m-%Y'),datetime.strptime(el,'%Y-%m-%d'))
            dict_ages[rd.months]+=1

    print(len(list_records_vaccine))
    print("Bombali: "+ str(len(bombali_number)))
    print("Tonkolili: "+ str(len(tonkolili_number)))
    print("Port Loko: "+ str(len(portloko_number)))
    print(dict_ages)

def rtss_counts():
    """
    This script analysis the number of doses and the number of ICARIA participants vaccinated with RTSS
    :return:
    """
    all_vacc = pd.DataFrame(columns=['HF','record_id','redcap_event_name','vacc_date','num_vaccine'])
    summary = pd.DataFrame(columns=['HFs','1st dose','2nd dose','3rd dose','4th dose','total'])
    errors_df = pd.DataFrame(columns=['HFs','record_id','duplicate_dose_data'])
    for project_name in tokens.REDCAP_PROJECTS_ICARIA:
        print(project_name)
        project = redcap.Project(tokens.URL, tokens.REDCAP_PROJECTS_ICARIA[project_name])
        df = project.export_records(format_type='df',fields=['int_vacc_rtss1_date','int_vacc_rtss2_date','int_vacc_rtss3_date','int_vacc_rtss4_date'], events=params.rtss_events)
        if not df.empty:
            df = df.fillna(0).reset_index()
            for k,el in df[df['int_vacc_rtss1_date']!=0].T.items():
                if not all_vacc[(all_vacc['record_id'] == el['record_id']) & (all_vacc['num_vaccine'] == '1')].empty:
                    print("ERROR CASE 1: " + str(el['record_id']))
                    errors_df.loc[(len(errors_df))] = project_name.split(".")[0], el['record_id'], '1'
                else:
                    all_vacc.loc[len(all_vacc)] = str(project_name).split(".")[0], el['record_id'],el['redcap_event_name'], el['int_vacc_rtss1_date'],'1'
            for k,el in df[df['int_vacc_rtss2_date']!=0].T.items():
                if not all_vacc[(all_vacc['record_id']==el['record_id']) & (all_vacc['num_vaccine']=='2')].empty:
                    print("ERROR CASE 2: "+str(el['record_id']))
                    errors_df.loc[(len(errors_df))] = project_name.split(".")[0], el['record_id'], '2'
                else:
                    all_vacc.loc[len(all_vacc)] = str(project_name).split(".")[0],el['record_id'],el['redcap_event_name'], el['int_vacc_rtss2_date'],'2'
            for k,el in df[df['int_vacc_rtss3_date']!=0].T.items():
                if not all_vacc[(all_vacc['record_id'] == el['record_id']) & (all_vacc['num_vaccine'] == '3')].empty:
                    print("ERROR CASE 3: " + str(el['record_id']))
                    errors_df.loc[(len(errors_df))] = project_name.split(".")[0], el['record_id'], '3'
                else:
                    all_vacc.loc[len(all_vacc)] = str(project_name).split(".")[0],el['record_id'],el['redcap_event_name'], el['int_vacc_rtss3_date'],'3'
            for k,el in df[df['int_vacc_rtss4_date']!=0].T.items():
                if not all_vacc[(all_vacc['record_id'] == el['record_id']) & (all_vacc['num_vaccine'] == '4')].empty:
                    print("ERROR CASE 4: " + str(el['record_id']))
                    errors_df.loc[(len(errors_df))] = project_name.split(".")[0], el['record_id'], '4'
                else:
                    all_vacc.loc[len(all_vacc)] = str(project_name).split(".")[0],el['record_id'],el['redcap_event_name'], el['int_vacc_rtss4_date'],'4'


    all_vacc_ind = all_vacc.set_index('record_id')
    first_doses_records = all_vacc_ind[all_vacc_ind['num_vaccine']=='1'].index
    second_doses_records = all_vacc_ind[all_vacc_ind['num_vaccine']=='2'].index
    print(second_doses_records.difference(first_doses_records))
    print(errors_df)

#    with pd.ExcelWriter(tokens.hf_sheet,mode='a',if_sheet_exists='replace') as writer:
    total_first = 0
    total_second = 0
    total_third = 0
    total_four = 0
    total_all = 0
    for hf, el in all_vacc.groupby(['HF']):
        first,second,third,four = 0,0,0,0
        for k, l in el.groupby(['num_vaccine']):
            if k == '1':
                first = l['record_id'].nunique()
            elif k == '2':
                second = l['record_id'].nunique()
            elif k == '3':
                third = l['record_id'].nunique()
            elif k == '4':
                four = l['record_id'].nunique()
        total = first + second + third + four
        total_all += total
        total_first += first
        total_second += second
        total_third += third
        total_four += four
        summary.loc[len(summary)] = hf, first, second, third, four, total
#        el.to_excel(writer, sheet_name=str(hf), index=False)

    summary.loc[len(summary)] = 'total', total_first, total_second, total_third, total_four, total_all
    summary.loc[len(summary)] = 'Different ICARIA participants vaccinated with RTSS', '','','','',all_vacc['record_id'].nunique()

    print(summary)

#    summary.to_excel(tokens.summary_sheet,sheet_name='ICARIA_rtss',index=False)

    file_to_drive(summary,params.summary_drive_filename,
                  params.summary_drive_worksheet_name,tokens.rtss_drive_folder,
                  index_included=False, deleting=True)

    print("\n\nScript Completed on "+ str(datetime.today()))


def file_to_drive(df,drive_file_name,worksheet,folder_id,index_included=True,deleting=False):
    gc = gspread.oauth(tokens.path_credentials)
    sh = gc.open(title=drive_file_name,folder_id=folder_id)

    if deleting:
        actual_worksheet = sh.worksheet(worksheet)
        actual_worksheet.clear()
    set_with_dataframe(sh.worksheet(worksheet), df,include_index=index_included)


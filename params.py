summary_drive_filename = 'ICARIA_rtss_administrations_summary_tool'

summary_drive_worksheet_name = 'ICARIA_rtss'

district_HF = {
    'Port Loko': ['HF01.01','HF01.02','HF01.03','HF02.01','HF02.02','HF03',
                  'HF04.01','HF04.02','HF05.01','HF05.02','HF06'],
    'Tonkolili': ['HF08.01','HF08.02','HF08.03','HF08.04','HF10'],
    'Bombali': ['HF11.01','HF11.02','HF12.01','HF12.02','HF13.01','HF13.02',
                'HF15','HF16.01','HF16.02','HF16.03','HF16.04','HF16.05',
                'HF17.01','HF17.02']
}

RTSS_FIELDS = ['int_vacc_rtss1','int_vacc_rtss1_date','int_vacc_rtss2_date',
               'int_vacc_rtss2','int_vacc_rtss3','int_vacc_rtss3_date',
               'int_vacc_rtss4','int_vacc_rtss4_date','int_interviewer_id',
               'int_date','int_comments','int_time','int_duration']

rtss_fields_to_import = [
    'record_id','redcap_event_name','redcap_repeat_instrument',
    'redcap_repeat_instance','ver_sop_rtss','ver_dci_rtss','rtss_vacc_rtss1',
    'rtss_vacc_rtss1_date','rtss_vacc_rtss2','rtss_vacc_rtss2_date',
    'rtss_vacc_rtss3','rtss_vacc_rtss3_date','rtss_vacc_rtss4',
    'rtss_vacc_rtss4_date','rtss_why_warnings','rtss_interviewer_id','rtss_date',
    'rtss_comments','rtss_time','rtss_complete']

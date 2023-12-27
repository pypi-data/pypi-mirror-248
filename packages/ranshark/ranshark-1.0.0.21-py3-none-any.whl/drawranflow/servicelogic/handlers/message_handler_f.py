import pandas as pd
import logging

from django.db import IntegrityError

from drawranflow.models import Identifiers, UploadedFile
from drawranflow.servicelogic.handlers.utils import get_gnb_id
import numpy as np


def split_values(row):
    row = str(row)
    row = row.strip()
    if pd.notna(row) or not str(row).lower() != 'nan':
        values = str(row).split(',')
        return values[1] if len(values) > 1 else values[0]
    else:
        return pd.Series([np.nan])

def message_handler(df, item_id):
    # Filter rows with required protocol
    upload_table = UploadedFile.objects.get(id=item_id)
    logging.error(f"MessageHandler: Preparing initial analysis for the file : {upload_table.filename}")

    f1ap_df = df[df['frame.protocols'].apply(lambda x: 'f1ap' in x.lower() if isinstance(x, str) else False)]
    ngap_df = df[df['frame.protocols'].apply(lambda x: 'ngap' in x.lower() if isinstance(x, str) else False)]
    e1ap_df = df[df['frame.protocols'].apply(lambda x: 'e1ap' in x.lower() if isinstance(x, str) else False)]
    xnap_df = df[df['frame.protocols'].apply(lambda x: 'xnap' in x.lower() if isinstance(x, str) else False)]

    f1ap_df[['f1ap.GNB_DU_UE_F1AP_ID']] = f1ap_df['f1ap.GNB_DU_UE_F1AP_ID'].apply(lambda x: pd.Series(split_values(x)))
    # f1ap_df['f1ap.cause_desc'] = f1ap_df.apply(lambda row: map_cause_description(row), axis=1)
    # missing_cause_desc_rows = f1ap_df[~f1ap_df['f1ap.cause_desc'].isna()]
    # print("Rows with missing cause descriptions:")
    # print(missing_cause_desc_rows)
    # print(f1ap_df['f1ap.GNB_DU_UE_F1AP_ID'])

    # Find RRC Setup, Reestablishment, and Setup Request messages
    rrc_setup_df = f1ap_df[f1ap_df['_ws.col.info'] == 'RRC Setup']
    rrc_reestablish_res_df = f1ap_df[f1ap_df['_ws.col.info'] == 'RRC Reestablishment']
    rrc_setup_request_df = f1ap_df[(f1ap_df['_ws.col.info'] == 'RRC Setup Request') & ~f1ap_df['f1ap.C_RNTI'].isnull()]
    rrc_reestablish_df = f1ap_df[
        (f1ap_df['_ws.col.info'] == 'RRC Reestablishment Request') & ~f1ap_df['f1ap.C_RNTI'].isnull()]

    combined_df = pd.concat([rrc_setup_request_df, rrc_reestablish_df])
    combined_df.loc[:,'f1ap.nRCellIdentity'] = combined_df['f1ap.nRCellIdentity'].map(get_gnb_id)

    service_request_df = ngap_df[
        ((ngap_df['_ws.col.info'] == 'Service request')
         | (ngap_df['_ws.col.info'] == 'Registration request')
         | (ngap_df['_ws.col.info'] == 'Tracking area update request')) & ~ngap_df['ngap.RAN_UE_NGAP_ID'].isnull()
        ]

    ngap_initial_messages_df = ngap_df[
        ((ngap_df['_ws.col.info'] == 'InitialContextSetupRequest') |
         (ngap_df['_ws.col.info'] == 'Registration Reject') |
         (ngap_df['_ws.col.info'].str.contains('Registration reject')) |
         (ngap_df['_ws.col.info'] == 'PDU Session Setup Request')) &
        ~ngap_df['ngap.RAN_UE_NGAP_ID'].isnull() &
        ~ngap_df['ngap.AMF_UE_NGAP_ID'].isnull()
        ]


    e1ap_bctxt_mesg_df = e1ap_df[(e1ap_df['_ws.col.info'] == 'BearerContextSetupRequest')
                                 & ~e1ap_df['e1ap.GNB_CU_CP_UE_E1AP_ID'].isnull()]

    e1ap_bctxt_resp_messages_df = e1ap_df[
        (e1ap_df['_ws.col.info'] == 'BearerContextSetupResponse') |
        (e1ap_df['_ws.col.info'] == 'BearerContextSetupFailure') &
        ~e1ap_df['e1ap.GNB_CU_CP_UE_E1AP_ID'].isnull() &
        ~e1ap_df['e1ap.GNB_CU_UP_UE_E1AP_ID'].isnull()
        ]


    xnap_handover_df = xnap_df[
        (xnap_df['_ws.col.info'] == 'HandoverRequest') &
        ~xnap_df['xnap.NG_RANnodeUEXnAPID_src'].isnull() &
        xnap_df['xnap.NG_RANnodeUEXnAPID_dst'].isnull()
        ]
    xnap_handover_ack_df = xnap_df[
        (xnap_df['_ws.col.info'] == 'HandoverRequestAcknowledge') &
        ~xnap_df['xnap.NG_RANnodeUEXnAPID_src'].isnull() &
        ~xnap_df['xnap.NG_RANnodeUEXnAPID_dst'].isnull()
        ]

    logging.debug("xnap_handover_ack_df:\n%s", xnap_handover_df)
    logging.debug("xnap_handover_ack_df:\n%s", xnap_handover_ack_df)

    identifiers_df = combined_df[
        ['f1ap.C_RNTI',
         'f1ap.GNB_DU_UE_F1AP_ID',
         'f1ap.GNB_CU_UE_F1AP_ID',
         'nr-rrc.pdcch_DMRS_ScramblingID',
         'ip.src', 'ip.dst',
         'frame.time',
         'ngap.RAN_UE_NGAP_ID',
         'ngap.AMF_UE_NGAP_ID',
         'xnap.NG_RANnodeUEXnAPID_src',
         'xnap.NG_RANnodeUEXnAPID_dst',
         'e1ap.GNB_CU_CP_UE_E1AP_ID',
         'e1ap.GNB_CU_UP_UE_E1AP_ID',
         'f1ap.nRCellIdentity'
         ]].copy()
    identifiers_df.rename(columns={
        'f1ap.C_RNTI': 'c_rnti',
        'f1ap.GNB_DU_UE_F1AP_ID': 'gnb_du_ue_f1ap_id',
        'f1ap.GNB_CU_UE_F1AP_ID': 'gnb_cu_ue_f1ap_id',
        'nr-rrc.pdcch_DMRS_ScramblingID': 'pci',
        'frame.time': 'frame_time',
        'ngap.RAN_UE_NGAP_ID': 'ran_ue_ngap_id',
        'ngap.AMF_UE_NGAP_ID': 'amf_ue_ngap_id',
        'ip.src': 'du_f1c_ip',
        'ip.dst': 'cucp_f1c_ip',
        'xnap.NG_RANnodeUEXnAPID_src': 'xnap_src_ran_id',
        'xnap.NG_RANnodeUEXnAPID_dst': 'xnap_trgt_ran_id',
        'e1ap.GNB_CU_CP_UE_E1AP_ID': 'gnb_cu_cp_ue_e1ap_id',
        'e1ap.GNB_CU_UP_UE_E1AP_ID': 'gnb_cu_up_ue_e1ap_id',
        'f1ap.nRCellIdentity': 'gnb_id',
    }, inplace=True)

    # Save to Identifiers table
    identifiers_df['uploadedFiles_id'] = item_id

    # identifiers_df = identifiers_df.astype(str)
    for _, identifier_row in identifiers_df.iterrows():
        # Extract relevant information from the Identifier DataFrame
        identifier_time = identifier_row['frame_time']
        identifier_du_ip = identifier_row['du_f1c_ip']
        identifier_cucp_ip = identifier_row['cucp_f1c_ip']
        # print(rrc_reestablish_res_df)
        # print(identifier_time)
        matching_rrc_restablish_res = rrc_reestablish_res_df[
            (rrc_reestablish_res_df['frame.time'] >= identifier_time) &
            (rrc_reestablish_res_df['frame.time'] <= identifier_time + pd.Timedelta('1s')) &
            (rrc_reestablish_res_df['ip.src'] == identifier_cucp_ip) &
            (rrc_reestablish_res_df['ip.dst'] == identifier_du_ip) &
            (rrc_reestablish_res_df['f1ap.GNB_DU_UE_F1AP_ID'] == identifier_row['gnb_du_ue_f1ap_id'])
            ]
        # If there's a match, update GNB_CU_UE_F1AP in the Identifier DataFrame
        if not matching_rrc_restablish_res.empty:
            identifiers_df.at[_, 'gnb_cu_ue_f1ap_id'] = matching_rrc_restablish_res.iloc[0]['f1ap.GNB_CU_UE_F1AP_ID']

        # Filter RRC Setup within 1 second and matching IPs
        matching_rrc_setup = rrc_setup_df[
            (rrc_setup_df['frame.time'] >= identifier_time) &
            (rrc_setup_df['frame.time'] <= identifier_time + pd.Timedelta('1s')) &
            (rrc_setup_df['ip.src'] == identifier_cucp_ip) &
            (rrc_setup_df['ip.dst'] == identifier_du_ip) &
            (rrc_setup_df['f1ap.GNB_DU_UE_F1AP_ID'] == identifier_row['gnb_du_ue_f1ap_id'])
            ]
        # If there's a match, update GNB_CU_UE_F1AP in the Identifier DataFrame
        if not matching_rrc_setup.empty:
            identifiers_df.at[_, 'gnb_cu_ue_f1ap_id'] = matching_rrc_setup.iloc[0]['f1ap.GNB_CU_UE_F1AP_ID']


        # Access the updated value after the update
        updated_value = identifiers_df.at[_, 'gnb_cu_ue_f1ap_id']

        logging.debug(f"F1AP: RRC Setup within 1 second and matching src & dst IPs: "
                      f"c_rnti : {identifier_row['c_rnti']}, gnb_cu_ue_f1ap_id:{updated_value}")

        matching_ngap_setup = service_request_df[
            (service_request_df['frame.time'] >= identifier_row['frame_time']) &
            (service_request_df['frame.time'] <= identifier_row['frame_time'] + pd.Timedelta('3s')) &
            (service_request_df['ngap.RAN_UE_NGAP_ID'] == updated_value)
            ]

        if not matching_ngap_setup.empty:
            identifiers_df.at[_, 'ran_ue_ngap_id'] = matching_ngap_setup.iloc[0]['ngap.RAN_UE_NGAP_ID']

        updated_ran_value = identifiers_df.at[_, 'ran_ue_ngap_id']

        logging.debug(f"NGAP: Setup within 3 second & RAN_UE_NGAP_ID==GNB_CU_UE_F1AP_ID: ran_ue_ngap_id: {updated_ran_value}")

        matching_ngap_ictxt_setup = ngap_initial_messages_df[
            (ngap_initial_messages_df['frame.time'] >= identifier_row['frame_time']) &
            (ngap_initial_messages_df['frame.time'] <= identifier_row['frame_time'] + pd.Timedelta('2s')) &
            (ngap_initial_messages_df['ngap.RAN_UE_NGAP_ID'] == updated_ran_value)
            ]

        if not matching_ngap_ictxt_setup.empty:
            identifiers_df.at[_, 'amf_ue_ngap_id'] = matching_ngap_ictxt_setup.iloc[0]['ngap.AMF_UE_NGAP_ID']

        logging.debug(
            f"NGAP: Initial Context/Reg Rej/PDU setup within 3 second & RAN_UE_NGAP_ID==GNB_CU_UE_F1AP_ID:"
            f"ran_ue_ngap_id: {updated_ran_value}")

        matching_e1ap_setup = e1ap_bctxt_mesg_df[
            (e1ap_bctxt_mesg_df['frame.time'] >= identifier_row['frame_time']) &
            (e1ap_bctxt_mesg_df['frame.time'] <= identifier_row['frame_time'] + pd.Timedelta('2s')) &
            (e1ap_bctxt_mesg_df['e1ap.GNB_CU_CP_UE_E1AP_ID'] == updated_value)
            ]

        if not matching_e1ap_setup.empty:
            identifiers_df.at[_, 'gnb_cu_cp_ue_e1ap_id'] = matching_e1ap_setup.iloc[0]['e1ap.GNB_CU_CP_UE_E1AP_ID']

        updated_e1ap_value = identifiers_df.at[_, 'gnb_cu_cp_ue_e1ap_id']

        logging.debug(
            f"E1AP: Bearer Ctxt setup within 3 second & GNB_CU_CP_UE_E1AP_ID==GNB_CU_UE_F1AP_ID: "
            f"gnb_cu_cp_ue_e1ap_id: {updated_e1ap_value}" )

        matching_e1ap_resp_setup = e1ap_bctxt_resp_messages_df[
            (e1ap_bctxt_resp_messages_df['frame.time'] >= identifier_row['frame_time']) &
            (e1ap_bctxt_resp_messages_df['frame.time'] <= identifier_row['frame_time'] + pd.Timedelta('10s')) &
            (e1ap_bctxt_resp_messages_df['e1ap.GNB_CU_CP_UE_E1AP_ID'] == updated_e1ap_value)
            ]

        if not matching_e1ap_resp_setup.empty:
            identifiers_df.at[_, 'gnb_cu_up_ue_e1ap_id'] = matching_e1ap_resp_setup.iloc[0]['e1ap.GNB_CU_UP_UE_E1AP_ID']

            logging.debug(
                f"E1AP: Bearer Ctxt setup Response/Failure within 10 second & GNB_CU_CP_UE_E1AP_ID==GNB_CU_UE_F1AP_ID: "
                f"gnb_cu_up_ue_e1ap_id: {matching_e1ap_setup}")

        matching_xnap_req_setup = xnap_handover_df[
            (xnap_handover_df['frame.time'] >= identifier_row['frame_time']) &
            (xnap_handover_df['frame.time'] <= identifier_row['frame_time'] + pd.Timedelta(minutes=5)) &
            (xnap_handover_df['xnap.NG_RANnodeUEXnAPID_src'] == updated_value)
            ]

        if not matching_xnap_req_setup.empty and not matching_e1ap_setup.empty and not matching_e1ap_setup.empty :
            identifiers_df.at[_, 'xnap_src_ran_id'] = matching_xnap_req_setup.iloc[0]['xnap.NG_RANnodeUEXnAPID_src']

        updated_xnap_value = identifiers_df.at[_, 'xnap_src_ran_id']

        logging.debug(
            f"XNAP: Ho Request  & NG_RANnodeUEXnAPID_src==GNB_CU_UE_F1AP_ID:xnap_src_ran_id:"
            f" {updated_xnap_value:}\n")

        matching_xnap_resp_setup = xnap_handover_ack_df[
            (xnap_handover_ack_df['frame.time'] >= identifier_row['frame_time']) &
            (xnap_handover_ack_df['xnap.NG_RANnodeUEXnAPID_src'] == updated_xnap_value)
            ]

        if not matching_xnap_resp_setup.empty:
            identifiers_df.at[_, 'xnap_trgt_ran_id'] = matching_xnap_resp_setup.iloc[0]['xnap.NG_RANnodeUEXnAPID_dst']

        logging.debug(
           f"XNAP: Ho Ack  & NG_RANnodeUEXnAPID_src==GNB_CU_UE_F1AP_ID: {matching_xnap_req_setup}")

    # Section 4: Bulk update Identifiers objects
    identifiers_to_update = []
    for _, row in identifiers_df.iterrows():
        try:
            identifier_object = Identifiers(
                c_rnti=row.get('c_rnti', None),
                gnb_du_ue_f1ap_id=row.get('gnb_du_ue_f1ap_id', None),
                gnb_cu_ue_f1ap_id=row.get('gnb_cu_ue_f1ap_id', None),
                gnb_cu_cp_ue_e1ap_id=row.get('gnb_cu_cp_ue_e1ap_id', None),
                gnb_cu_up_ue_e1ap_id=row.get('gnb_cu_up_ue_e1ap_id', None),
                ran_ue_ngap_id=row.get('ran_ue_ngap_id', None),
                amf_ue_ngap_id=row.get('amf_ue_ngap_id', None),
                xnap_src_ran_id=row.get('xnap_src_ran_id', None),
                xnap_trgt_ran_id=row.get('xnap_trgt_ran_id', None),
                pci=row.get('pci', None),
                cucp_f1c_ip=row.get('cucp_f1c_ip', None),
                du_f1c_ip=row.get('du_f1c_ip', None),
                gnb_id=row.get('gnb_id', None),
                uploaded_file_id=row['uploadedFiles_id'],
                frame_time=row.get('frame_time', None)
            )

            identifier_object.save()
            identifiers_to_update.append(identifier_object)

        except IntegrityError as e:
            logging.error(f"Message handling IntegrityError: {e}")
        except Exception as e:
            logging.error(f"Message handling -1Error: {e}")

    # Bulk update Identifiers objects
    Identifiers.objects.bulk_update(
        identifiers_to_update,
        fields=['c_rnti', 'gnb_du_ue_f1ap_id', 'gnb_cu_ue_f1ap_id', 'amf_ue_ngap_id', 'ran_ue_ngap_id', 'frame_time',
                'cucp_f1c_ip', 'du_f1c_ip', 'gnb_id']
    )
    logging.error(f"MessageHandler: Completed Initial Analysis for the file : {upload_table.filename}")

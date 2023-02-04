VALID_RECALL_ID_PATTERN = '\d{2}[A-Z]{1}\d{2}(\d{1}|[A-Z])\d{3}'

REQUIRED_DATASET_COLUMNS = ['CAMPNO', 'MAKETXT', 'MODELTXT', 'YEARTXT',
                            'COMPNAME_GROUP', 'COMPNAME', 'MFGNAME', 'MFGTXT', 'POTAFF', 'RCDATE']

# https://static.nhtsa.gov/odi/ffdd/rcl/RCL.txt
RECALLS_DATASET_COLUMNS = ['CAMPNO',
                           'MAKETXT',
                           'MODELTXT',
                           'YEARTXT',
                           'MFGCAMPNO',
                           'COMPNAME',
                           'MFGNAME',
                           'BGMAN',
                           'ENDMAN',
                           'RCLTYPECD',
                           'POTAFF',
                           'ODATE',
                           'INFLUENCED_BY',
                           'MFGTXT',
                           'RCDATE',
                           'DATEA',
                           'RPNO',
                           'FMVSS',
                           'DESC_DEFECT',
                           'CONEQUENCE_DEFECT',
                           'CORRECTIVE_ACTION',
                           'NOTES',
                           'RCL_CMPT_ID',
                           'MFR_COMP_NAME',
                           'MFR_COMP_DESC',
                           'MFR_COMP_PTNO']

DUPLICATED_COMPONENTS_TYPE = {'OTHER': 'UNKNOWN OR OTHER', 'TBD': 'UNKNOWN OR OTHER',
                              'Tether, Lower Anchor (on car seat or vehicle)': 'SEAT BELTS'}

REPORT_RECEIVED_DATE_FORMAT = '%Y%m%d'

UNKNOWN_MODEL_YEAR = 9999

def get_component_category(component):
    if component in ['SEAT BELTS', 'AIR BAGS', 'FORWARD COLLISION AVOIDANCE', 'VEHICLE SPEED CONTROL', 'ELECTRONIC STABILITY CONTROL', 'LANE DEPARTURE']:
        return 'SECURITY'
    elif component in ['ENGINE', 'ENGINE AND ENGINE COOLING', 'POWER TRAIN', 'TRACTION CONTROL SYSTEM', 'HYBRID PROPULSION SYSTEM']:
        return 'ENGINE'
    elif component in ['SERVICE BRAKES', 'SERVICE BRAKES, ELECTRIC', 'SERVICE BRAKES, AIR', 'SERVICE BRAKES, HYDRAULIC', 'PARKING BRAKE']:
        return 'BRAKE'
    elif component in ['FUEL SYSTEM, DIESEL', 'FUEL SYSTEM, GASOLINE', 'FUEL SYSTEM, OTHER']:
        return 'FUEL'
    elif component in ['ELECTRICAL SYSTEM', 'INTERIOR LIGHTING']:
        return 'ELECTRICAL'
    elif component in ['STRUCTURE', 'SEATS', 'SUSPENSION', 'LATCHES/LOCKS/LINKAGES', 'STEERING', 'WHEELS', 'TIRES']:
        return 'STRUCTURAL'
    elif component in ['TRAILER HITCHES', 'CHILD SEAT', 'EQUIPMENT',  'COMMUNICATION', 'BACK OVER PREVENTION', 'EQUIPMENT ADAPTIVE/MOBILITY']:
        return 'ACCESSORIES'
    elif component in ['VISIBILITY', 'VISIBILITY/WIPER', 'EXTERIOR LIGHTING']:
        return 'VISIBILITY'
    elif component in ['UNKNOWN OR OTHER']:
        return 'OTHER'
    else:
        print('Component without category:', component)
        return component

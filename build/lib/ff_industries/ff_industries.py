import logging
import re
from io import BytesIO, StringIO
from zipfile import ZipFile

import requests
import pandas as pd


def get_sic_map(num_ports: int) -> dict:
    """
    Create a dictionary mapping SIC codes to Fama-French industry classifications.

    Parameters
    ----------
    num_ports : int
        Number of industries to return. Must be one of [5, 10, 12, 17, 30, 38, 48, 49]

    Returns
    -------
    dict
        Dictionary mapping SIC codes to a tuple of (industry id, industry name, sub-industry name)
    """

    if num_ports not in [5, 10, 12, 17, 30, 38, 48, 49]:
        logging.warning('Invalid number of industries requested.')
        return None

    url = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Siccodes{}.zip'

    resp = requests.get(url.format(num_ports))
    if resp.status_code != 200:
        logging.warning("Failed to download file from Ken French's data library.")
        return None

    with ZipFile(BytesIO(resp.content)) as z:
        for file_name in z.namelist():
            with z.open(file_name) as file:
                file_content = file.read()

    defns = StringIO(file_content.decode()).read()
    defns = re.sub(r'\r\n', '\n', defns)

    inds = re.findall(r'(\d+ [A-z]+[\s\S]*?)(?=\n\s*\d+ |$)', defns)
    assert(len(inds) == num_ports)

    all_inds = []
    for ind in inds:
        if '\n' in ind:
            header, subinds = ind.split('\n', maxsplit=1)
        else:
            header, subinds = ind, None
        indid, indname = re.search(r'(\d+)\s+([A-z]+)', header).groups()
        if subinds:
            siccds = pd.DataFrame(re.findall(r'(\d+)-(\d+) ?(.*)', subinds), columns=['sic1', 'sic2', 'sub'])
            siccds['id'] = int(indid)
            siccds.set_index('id', inplace=True)
            siccds.insert(0, 'ind', indname)
            siccds[['sic1', 'sic2']] = siccds[['sic1', 'sic2']].apply(pd.to_numeric)
            siccds['sub'] = siccds['sub'].str.strip()
            all_inds.append(siccds)
        else:
            logging.warning(
                f'No SIC code ranges provided for industry "{indname}". '
                'The returned dictionary will not contain this industry.'
            )

    inds = pd.concat(all_inds)

    inds_dict = {}
    for id,row in inds.iterrows():
        for sic in range(row['sic1'], row['sic2']+1):
            inds_dict[sic] = (id, row['ind'], row['sub'])

    return inds_dict

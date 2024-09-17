# download the LGA correspondences file
FILE_NAME = "CG_LGA_2021_LGA_2022.csv"
local_correspondence_output_path = f"{output_dir}/{FILE_NAME}"
CORRESPONDENCE_LINK = f'https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/correspondences/{FILE_NAME}'

# retrieve the ABS data
urllib.request.urlretrieve(CORRESPONDENCE_LINK, local_correspondence_output_path)
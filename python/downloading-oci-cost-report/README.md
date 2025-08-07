# OCI Cost and Usage Report Downloader

This Python script downloads all cost and usage reports for an Oracle Cloud Infrastructure (OCI) tenancy. It uses the OCI Python SDK to fetch reports from the Object Storage bucket associated with your tenancy.

## Features
- Downloads all cost and usage reports (or only cost, or FOCUS reports if you adjust the prefix)
- Saves reports to a local directory (`downloaded_reports` by default)

## Prerequisites
- Python 3.x
- OCI Python SDK (`oci`)
- OCI configuration file (`~/.oci/config`) with appropriate credentials
- IAM policy allowing your user/group to read cost reports from the tenancy

### Example IAM Policy
```
define tenancy reporting as ocid1.tenancy.oc1..aaaaaaaaned4fkpkisbwjlr56u7cj63lf3wffbilvqknstgtvzub7vhqkggq
endorse group <group_name> to read objects in tenancy reporting
```
Replace `<group_name>` with your actual OCI group name.

## Installation
1. Clone this repository:
   ```sh
   git clone <repo-url>
   cd downloading-oci-cost-report
   ```
2. Install dependencies:
   ```sh
   pip install oci
   ```

## Usage
1. Ensure your `~/.oci/config` file is set up and you have the required permissions.
2. (Optional) Edit `downloading-oci-cost-report.py` to adjust the `prefix_file` variable if you want only cost or FOCUS reports.
3. Run the script:
   ```sh
   python downloading-oci-cost-report.py
   ```
4. Downloaded reports will be saved in the `downloaded_reports` directory.

## Customization
- To download only cost or FOCUS reports, uncomment and set the appropriate `prefix_file` in the script.
- Change the `destintation_path` variable to save reports to a different directory.

## License
MIT License 